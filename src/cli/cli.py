import pathlib
import readline
import sys
from contextlib import redirect_stdout
from enum import Enum
from io import StringIO
from subprocess import PIPE, Popen
from typing import Any, Optional

import lark

from ..backend_py import py_generator
from ..backend_py.runtime import egg_lib as _e
from ..backend_py.runtime import external_commands, memory
from ..frontend.lexer import EggLexer
from ..frontend.lexer_util import LexerError
from ..frontend.parser import get_parser
from ..yolk import yolk
from .profilers import ProfilerConfig, maybe_profile

assert readline   # silence pyflakes
assert _e   # silence pyflakes
_m = None


class BackendMode(Enum):
    yolk = 1
    python = 2


class ExecutionMode(Enum):
    lex = 1
    ast = 2
    sema = 3
    codegen = 4
    execute = 5


class CLIMode:
    def __init__(self, mode: ExecutionMode, backend: BackendMode):
        self.mode: ExecutionMode = mode
        self.backend = backend


class EggCLI:
    def __init__(self, mode: CLIMode, use_profiler: bool = False):
        self.mode = mode
        self.profiler_config = ProfilerConfig(use_profiler)
        self.interactive_profiler_counter = 0
        self.initialize_transformers()

    @maybe_profile(lambda _: 'initialization')
    def initialize_transformers(self) -> None:
        if self.mode.mode == ExecutionMode.lex:
            self.lexer = EggLexer()
        elif self.mode.mode == ExecutionMode.ast:
            self.parser = get_parser(lowering=False)
        elif self.mode.mode == ExecutionMode.sema:
            self.parser = get_parser()
        elif self.mode.mode in [ExecutionMode.codegen, ExecutionMode.execute]:
            self.parser = get_parser()
            if self.mode.backend == BackendMode.python:
                self.codegen: lark.Transformer[
                    lark.Token | int | float | str, Any
                ] = py_generator.PythonGenerator()
            else:
                self.codegen = yolk.YolkGenerator()

        if (
            self.mode.mode == ExecutionMode.execute
            and self.mode.backend == BackendMode.python
        ):
            global _m
            _m = memory.Memory()

    def interactive_mode(self) -> None:
        if self.mode.backend == BackendMode.yolk:
            self.yolk_process = Popen(
                ['../yolk/yolk', '-interactive'], stdin=PIPE, stdout=PIPE
            )
        while True:
            expression = input('egg> ').strip()
            if not expression:
                continue
            if expression == 'exit':
                self.yolk_process.stdin.close()   # type: ignore
                break
            try:
                self.consume_interactive(expression)
            except LexerError as e:
                print(e, file=sys.stderr)
            except lark.exceptions.LarkError as e:
                print(e, file=sys.stderr)

    @maybe_profile(lambda self, path: 'script_' + pathlib.Path(path).name)
    def consume_script(self, file_path: str) -> None:
        script = pathlib.Path(file_path).read_text('utf-8')
        self.consume_source(script)

    @maybe_profile(
        lambda self, _: f'interactive_{self.interactive_profiler_counter}'
    )
    def consume_interactive(self, src: str) -> None:
        self.consume_source(src)
        self.interactive_profiler_counter += 1

    def consume_source(self, src: str) -> None:
        if not src:
            return
        if self.mode.mode == ExecutionMode.lex:
            self.show_lex(src)
        elif self.mode.mode in (ExecutionMode.ast, ExecutionMode.sema):
            self.show_ast(src)
        elif self.mode.mode == ExecutionMode.codegen:
            self.show_codegen(src)
        elif self.mode.mode == ExecutionMode.execute:
            self.show_execute(src)

    def show_lex(self, src: str) -> None:
        tokens = self.lexer.lex(src)
        tokens_str = ', '.join([str(token) for token in tokens])
        print(f'[{tokens_str}]')

    def show_ast(self, src: str) -> None:
        ast = self.parser.parse(src)
        print(ast.pretty(), end='')

    def get_codegen(self, src: str) -> str:
        ast = self.parser.parse(src)
        if self.mode.backend == BackendMode.python:
            codegen = py_generator.transform_pygen_result(
                self.codegen.transform(ast)  # type: ignore[arg-type]
            )
            lines = [
                py_generator.transform_pygen_result(func)
                for func in py_generator.get_required_functions()
            ]
            lines.append(codegen)
            return '\n'.join(lines)
        else:
            return '\n'.join(self.codegen.transform(ast))  # type: ignore[arg-type]

    def show_codegen(self, src: str) -> None:
        print(self.get_codegen(src))

    def show_execute(self, src: str) -> None:
        if (output := self.execute(src)) is not None:
            print(output, end='')

    def execute(self, src: str) -> Optional[str]:
        if self.mode.backend == BackendMode.python:
            ast_or_value = self.parser.parse(src)
            py_code = py_generator.transform_pygen_result(
                self.codegen.transform(ast_or_value)  # type: ignore[arg-type]
            )
            for func in py_generator.get_required_functions():
                exec(py_generator.transform_pygen_result(func))
            try:
                if (output := eval(py_code)) is not None:
                    if isinstance(
                        output,
                        external_commands.ExternalCommand
                        | external_commands.Pipeline,
                    ):
                        return str(output.evaluate())
                    return repr(output)
                return None
            except SyntaxError:
                string_io = StringIO()
                with redirect_stdout(string_io):
                    exec(py_code)
                return string_io.getvalue()
        else:
            output = self.get_codegen(src)
            yolk_input = bytes(f'{output}\nPRINT\n', encoding='utf-8')
            self.yolk_process.stdin.write(yolk_input)   # type: ignore
            self.yolk_process.stdin.flush()   # type: ignore
            output = self.yolk_process.stdout.readline()   # type: ignore
            return output.decode('utf-8')   # type: ignore
