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
        '--sema',
        help='Construct an ast from input and apply lowering and sema instead of executing.',
        action='store_true',
    )
    mode_group.add_argument(
        '--codegen',
        '-c',
        help='Get the output from code generation instead of executing it.',
        action='store_true',
    )
    arg_parser.add_argument(
        '--python',
        '-p',
        help='Use the python backend instead of yolk.',
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
        mode = cli.ExecutionMode.lex
    elif args.ast:
        mode = cli.ExecutionMode.ast
    elif args.sema:
        mode = cli.ExecutionMode.sema
    elif args.codegen:
        mode = cli.ExecutionMode.codegen
    else:
        mode = cli.ExecutionMode.execute

    if args.python:
        backend = cli.BackendMode.python
    else:
        backend = cli.BackendMode.yolk

    cli_mode = cli.CLIMode(mode, backend)

    egg_cli = cli.EggCLI(cli_mode, use_profiler=args.profiler)

    if args.script:
        egg_cli.consume_script(args.script)
    else:
        egg_cli.interactive_mode()


if __name__ == '__main__':
    main()
