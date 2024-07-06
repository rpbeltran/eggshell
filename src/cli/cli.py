import pathlib
import readline
import sys
from contextlib import redirect_stdout
from enum import Enum
from io import StringIO
from typing import Optional

import lark

from ..backend.py_generator import PythonGenerator, transform_pygen_result
from ..frontend.lexer import EggLexer
from ..frontend.lexer_util import LexerError
from ..frontend.parser import get_parser
from ..runtime import egg_lib as _e
from ..runtime import external_commands, memory
from .profilers import ProfilerConfig, maybe_profile

_m = memory.Memory()


class CLIMode(Enum):
    lex = 1
    ast = 2
    sema = 3
    pygen = 4
    execute = 5


class EggCLI:
    def __init__(self, mode: CLIMode, use_profiler: bool = False):
        self.mode = mode
        self.profiler_config = ProfilerConfig(use_profiler)
        self.interactive_counter = 0
        self.initialize_transformers()

    @maybe_profile(lambda self: 'initialization')
    def initialize_transformers(self) -> None:
        if self.mode == CLIMode.lex:
            self.lexer = EggLexer()
        elif self.mode == CLIMode.ast:
            self.parser = get_parser(lowering=False)
        elif self.mode == CLIMode.sema:
            self.parser = get_parser()
        elif self.mode in [CLIMode.pygen, CLIMode.execute]:
            self.parser = get_parser()
            self.pygen = PythonGenerator()

    def interactive_mode(self) -> None:
        while True:
            expression = input('egg> ').strip()
            if not expression:
                continue
            if expression == 'exit':
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

    @maybe_profile(lambda self, src: f'interactive_{self.interactive_counter}')
    def consume_interactive(self, src: str) -> None:
        self.consume_source(src)
        self.interactive_counter += 1

    def consume_source(self, src: str) -> None:
        if not src:
            return
        if self.mode == CLIMode.lex:
            self.show_lex(src)
        elif self.mode in (CLIMode.ast, CLIMode.sema):
            self.show_ast(src)
        elif self.mode == CLIMode.pygen:
            self.show_pygen(src)
        elif self.mode == CLIMode.execute:
            self.show_execute(src)

    def show_lex(self, src: str) -> None:
        tokens = self.lexer.lex(src)
        tokens_str = ', '.join([str(token) for token in tokens])
        print(f'[{tokens_str}]')

    def show_ast(self, src: str) -> None:
        ast = self.parser.parse(src)
        print(ast.pretty(), end='')

    def show_pygen(self, src: str) -> None:
        ast = self.parser.parse(src)
        py = transform_pygen_result(self.pygen.transform(ast))
        print(py)

    def show_execute(self, src: str) -> None:
        if (output := self.execute(src)) is not None:
            print(output)

    def execute(self, src: str) -> Optional[str]:
        ast_or_value = self.parser.parse(src)
        py_code = transform_pygen_result(self.pygen.transform(ast_or_value))
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
