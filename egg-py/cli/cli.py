from enum import Enum
import pathlib
import readline
import sys

import lark

from frontend.lexer import EggLexer
from frontend.lexer_util import LexerError
from frontend.parser import get_parser
from backend.py_generator import PythonGenerator
from runtime import egg_lib


class CLIMode(Enum):
    lex = 1
    ast = 2
    pygen = 3
    execute = 4


class EggCLI:
    def __init__(self, mode: CLIMode):
        self.mode = mode

        if mode == CLIMode.lex:
            self.lexer = EggLexer()
        elif mode == CLIMode.ast:
            self.parser = get_parser(lowering=False)
        elif mode in [CLIMode.pygen, CLIMode.execute]:
            self.parser = get_parser()
            self.pygen = PythonGenerator()

    def interactive_mode(self):
        while True:
            expression = input('egg(py)> ').strip()
            if not expression:
                continue
            if expression == 'exit':
                break
            try:
                self.consume_source(expression)
            except LexerError as e:
                print(e, file=sys.stderr)
            except lark.exceptions.LarkError as e:
                print(e, file=sys.stderr)

    def consume_script(self, file_path):
        script = pathlib.Path(file_path).read_text('utf-8')
        self.consume_source(script)

    def consume_source(self, src: str):
        if not src:
            return
        if self.mode == CLIMode.lex:
            self.show_lex(src)
        elif self.mode == CLIMode.ast:
            self.show_ast(src)
        elif self.mode == CLIMode.pygen:
            self.show_pygen(src)
        elif self.mode == CLIMode.execute:
            self.execute(src)

    def show_lex(self, src: str):
        tokens = self.lexer.lex(src)
        tokens_str = ', '.join([str(token) for token in tokens])
        print(f'[{tokens_str}]')

    def show_ast(self, src: str):
        ast = self.parser.parse(src)
        print(ast.pretty(), end='')

    def show_pygen(self, src: str):
        ast = self.parser.parse(src)
        py = self.pygen.transform(ast)
        print(py)

    def execute(self, src: str):
        ast = self.parser.parse(src)
        py_code = self.pygen.transform(ast)
        try:
            if (output := eval(py_code)) is not None:
                print(output)
        except SyntaxError:
            exec(py_code)