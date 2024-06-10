#!/usr/bin/env python3
import argparse

import cli.cli as cli


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


def main():
    args = get_args()

    if args.lex:
        mode = cli.CLIMode.lex
    elif args.ast:
        mode = cli.CLIMode.ast
    elif args.pygen:
        mode = cli.CLIMode.pygen
    else:
        mode = cli.CLIMode.execute

    egg_cli = cli.EggCLI(mode)

    if args.run:
        egg_cli.consume_script(args.run)
    else:
        egg_cli.interactive_mode()


if __name__ == '__main__':
    main()
