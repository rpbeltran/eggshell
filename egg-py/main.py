#!/usr/bin/env python3
import argparse
import pathlib
import readline
import sys

import lark.exceptions

import parsing
from parsing.lexer import EggLexer
from parsing.lexer_util import LexerError

from backend.py_generator import PythonGenerator

from runtime import egg_lib


def get_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser('egg-py')

    arg_parser.add_argument(
        '-l',
        '--lex',
        help='Run just the lexer instead of executing.',
        action='store_true',
    )

    arg_parser.add_argument(
        '-a',
        '--ast',
        help='Construct an ast from input instead of executing.',
        action='store_true',
    )

    arg_parser.add_argument(
        '--pygen',
        help='Get the output from pygen instead of executing it.',
        action='store_true',
    )

    arg_parser.add_argument(
        '-r',
        '--run',
        help='Path of script to be executed.'
        'If omitted, interactive mode will be enabled.',
        required=False,
    )

    return arg_parser.parse_args()


def show_python(egg_code: str):
    pygen = PythonGenerator()   # todo: don't reinitialize this every time
    ast = parsing.EggParser.parse(egg_code)
    py = pygen.transform(ast)
    print(py)


def execute(egg_code: str):
    pygen = PythonGenerator()   # todo: don't reinitialize this every time
    ast = parsing.EggParser.parse(egg_code)
    py = pygen.transform(ast)
    try:
        print(eval(py))
    except:
        out = exec(py)
        if out != None:
            print(out)


def show_ast(egg_code: str):
    ast = parsing.EggParser.parse(egg_code)
    print(ast.pretty(), end='')


def show_lex(egg_code: str):
    lexer = EggLexer()
    tokens = lexer.lex(egg_code)
    tokens_str = ', '.join([str(token) for token in tokens])
    print(f'[{tokens_str}]')


def main():
    args = get_args()

    if args.run:
        script = pathlib.Path(args.run).read_text('utf-8')
        if args.lex:
            show_lex(script)
        else:
            show_ast(script)
    else:
        while True:
            expression = input('egg(py)> ').strip()
            if not expression:
                continue
            if expression == 'exit':
                break
            try:
                if args.ast:
                    show_ast(expression)
                elif args.lex:
                    show_lex(expression)
                elif args.pygen:
                    show_python(expression)
                else:
                    execute(expression)
            except LexerError as e:
                print(e, file=sys.stderr)
            except lark.exceptions.LarkError as e:
                print(e, file=sys.stderr)


if __name__ == '__main__':
    main()
