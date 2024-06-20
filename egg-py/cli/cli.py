from enum import Enum
import pathlib
import readline
import sys

import lark

from frontend.lexer import EggLexer
from frontend.lexer_util import LexerError
from frontend.parser import Parser
from frontend.source import SourceManager
from backend.py_generator import PythonGenerator
from .profilers import maybe_profile, ProfilerConfig


from runtime import egg_lib as _e


class CLIMode(Enum):
    lex = 1
    ast = 2
    pygen = 3
    execute = 4


class EggCLI:
    def __init__(self, mode: CLIMode, use_profiler: bool = False):
        self.mode = mode
        self.profiler_config = ProfilerConfig(use_profiler)
        self.interactive_counter = 0
        self.initialize_transformers()

    @maybe_profile(lambda self: 'initialization')
    def initialize_transformers(self):
        if self.mode == CLIMode.lex:
            self.lexer = EggLexer()
        elif self.mode == CLIMode.ast:
            self.parser = Parser(lowering=False)
        elif self.mode in [CLIMode.pygen, CLIMode.execute]:
            self.parser = Parser()
            self.pygen = PythonGenerator()

    def interactive_mode(self):
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
    def consume_script(self, path):
        script = pathlib.Path(path).read_text('utf-8')
        SourceManager.add_source(path, script)
        self.consume_source(path)

    @maybe_profile(lambda self, src: f'interactive_{self.interactive_counter}')
    def consume_interactive(self, src):
        if src:
            SourceManager.add_source('', src)
            self.consume_source('')
        self.interactive_counter += 1

    def consume_source(self, path: str):
        if self.mode == CLIMode.lex:
            self.show_lex(path)
        elif self.mode == CLIMode.ast:
            self.show_ast(path)
        elif self.mode == CLIMode.pygen:
            self.show_pygen(path)
        elif self.mode == CLIMode.execute:
            self.execute(path)

    def show_lex(self, path: str):
        src = SourceManager.sources[path].source
        tokens = self.lexer.lex(src)
        tokens_str = ', '.join([str(token) for token in tokens])
        print(f'[{tokens_str}]')

    def show_ast(self, path: str):
        ast = self.parser.parse(path)
        print(ast.pretty(), end='')

    def show_pygen(self, path: str):
        ast = self.parser.parse(path)
        py = self.pygen.transform(ast)
        print(py)

    def execute(self, path: str):
        ast_or_value = self.parser.parse(path)
        if type(ast_or_value) == lark.tree.Tree:
            py_code = self.pygen.transform(ast_or_value)
            try:
                if (output := eval(py_code)) is not None:
                    print(output)
            except SyntaxError:
                exec(py_code)
        else:
            print(ast_or_value)
