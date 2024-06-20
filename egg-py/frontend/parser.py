import pathlib

import lark

from .lexer import EggLexer
from .lowering import LoweringTransformer
from .source import SourceManager


class Parser:
    def __init__(
        self,
        lowering=True,
    ):
        self.current_path = ''
        self.grammar = self.get_grammar()
        self.transformer = LoweringTransformer if lowering else None
        self.parser = lark.Lark(
            self.grammar,
            parser='lalr',
            lexer=self.getLexer(),
            transformer=self.transformer,
        )

    def getLexer(self):
        class WrappedLexer(lark.lexer.Lexer):
            def __init__(lexer_self, _):
                lexer_self.lexer = EggLexer()
                lexer_self.lexer.get_current_path = lambda: self.current_path

            def lex(lexer_self, src: str):
                for token in lexer_self.lexer.lex(src):
                    yield token.to_lark()

        return WrappedLexer

    @staticmethod
    def get_grammar() -> str:
        """Read the Grammar of Egg from egg.lark."""
        here = pathlib.Path(__file__).parent.resolve()
        grammar_file = here / 'egg.lark'
        return grammar_file.read_text('utf-8')

    def parse(self, path: str, show_token_src=False) -> lark.Tree[lark.Token]:
        self.current_path = path
        return self.parser.parse(SourceManager.sources[path].source)
