import pathlib
import readline
import sys
from enum import Enum
from subprocess import PIPE, Popen
from typing import Tuple

import lark

from ..frontend.lexer import EggLexer
from ..frontend.lexer_util import LexerError
from ..frontend.parser import get_parser
from ..yolk import yolk
from .profilers import ProfilerConfig, maybe_profile

assert readline   # silence pyflakes

class ExecutionMode(Enum):
    lex = 1
    ast = 2
    sema = 3
    codegen = 4
    execute = 5


class CLIMode:
    def __init__(self, mode: ExecutionMode):
        self.mode: ExecutionMode = mode


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
            self.codegen = yolk.YolkGenerator()

    def interactive_mode(self) -> None:
        self.yolk_process = Popen(
            ['../yolk/yolk', '-interactive'], stdin=PIPE, stdout=PIPE
        )
        while True:
            expression = input('egg> ').strip()
            if not expression:
                continue
            if expression == 'exit':
                self.yolk_process.stdin.close()
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
        return '\n'.join(self.codegen.transform(ast))

    def show_codegen(self, src: str) -> None:
        print(self.get_codegen(src))

    def show_execute(self, src: str) -> None:
        if (output := self.execute(src)) is not None:
            print(output, end='')

    def execute(self, src: str) -> Tuple[str, str]:
        output = self.get_codegen(src)
        yolk_input = bytes(f'{output}\nPRINT\n', encoding='utf-8')
        self.yolk_process.stdin.write(yolk_input)
        self.yolk_process.stdin.flush()
        out = self.yolk_process.stdout.readlines()
        return out.decode('utf-8')
