#!/usr/bin/env python3
import argparse
import src.cli.cli as cli


def get_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser('egg')

    mode_group = arg_parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--lex',
        '-l',
        help='Run just the lexer instead of executing.',
        action='store_true',
    )
    mode_group.add_argument(
        '--ast',
        '-a',
        help='Construct an ast from input instead of executing.',
        action='store_true',
    )
    mode_group.add_argument(
        '--pygen',
        '-p',
        help='Get the output from pygen instead of executing it.',
        action='store_true',
    )

    arg_parser.add_argument(
        '--profiler',
        help='Run a profiler to analyze performance bottlenecks.',
        action='store_true',
    )

    arg_parser.add_argument(
        '-s',
        '--script',
        help='Path of script to be executed.'
        'If omitted, interactive mode will be enabled.',
        required=False,
    )

    return arg_parser.parse_args()


def main() -> None:
    args = get_args()

    if args.lex:
        mode = cli.CLIMode.lex
    elif args.ast:
        mode = cli.CLIMode.ast
    elif args.pygen:
        mode = cli.CLIMode.pygen
    else:
        mode = cli.CLIMode.execute

    egg_cli = cli.EggCLI(mode, use_profiler=args.profiler)

    if args.script:
        egg_cli.consume_script(args.script)
    else:
        egg_cli.interactive_mode()


if __name__ == '__main__':
    main()
