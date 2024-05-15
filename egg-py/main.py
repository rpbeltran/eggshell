import argparse
import pathlib

import parsing
from parsing.lexer import EggLexer


def get_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser('egg-py')

    """
    arg_parser.add_argument(
        "-a", "--ast",
        help="Construct an ast from input instead of executing.",
        action="store_true")
    """  # todo: enable once something else is even supported

    arg_parser.add_argument(
        "-l", "--lex",
        help="Run just the lexer instead of executing.",
        action="store_true")

    arg_parser.add_argument(
        '-r',
        '--run',
        help='Path of script to be executed.'
        'If ommitted, interactive mode will be enabled.',
        required=False,
    )

    return arg_parser.parse_args()


def show_ast(egg_code: str):
    ast = parsing.EggParser.parse(egg_code)
    print(ast.pretty(), end='')


def show_lex(egg_code: str):
    lexer = EggLexer()
    tokens = lexer.lex(egg_code)
    tokens_str = ', '.join([str(token) for token in tokens])
    print(f"[{tokens_str}]")


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
            if args.lex:
                show_lex(expression)
            else:
                show_ast(expression)


if __name__ == '__main__':
    main()
