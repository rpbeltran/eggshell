import pathlib

import lark


def get_grammar() -> str:
    """Read the Grammar of Egg from egg.lark."""
    here = pathlib.Path(__file__).parent.resolve()
    grammar_file = here / 'egg.lark'
    return grammar_file.read_text('utf-8')


def get_parser() -> lark.Lark:
    return lark.Lark(get_grammar(), parser='lalr')
