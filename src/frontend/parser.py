import pathlib

import lark

from .lexer import EggLexerLark
from .lowering import LoweringTransformer


def get_grammar() -> str:
    """Read the Grammar of Egg from egg.lark."""
    here = pathlib.Path(__file__).parent.resolve()
    grammar_file = here / 'egg.lark'
    return grammar_file.read_text('utf-8')


def get_parser(lowering=True) -> lark.Lark:
    grammar = get_grammar()
    transformer = LoweringTransformer if lowering else None
    return lark.Lark(
        grammar,
        parser='lalr',
        lexer=EggLexerLark,
        transformer=transformer,
        cache=True,
    )
