from typing import Iterator, Optional, Tuple

import lark.lexer

from .lexer_constants import (
    KEYWORDS,
    UNITS,
    all_operators_trie,
    non_arithmetic_ps_trie,
)
from .lexer_util import DFANode, LexerError, LexerState, Token


class StartNode(DFANode):
    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if c == '\n':
            if state.paren_depth == 0:
                yield Token('SEMICOLON', '')
            state.clear_prev()
        elif c.isspace():
            pass
        elif (
            c in all_operators_trie.first_chars
            and (match := match_operator(state)) is not None
        ):
            state.token_start = state.head
            state.goto_node(OperatorsNode(match[0], match[1]), step_back=True)
        elif c.isdigit() or (c == '-' and state.next_char().isdigit()):
            state.token_start = state.head
            state.goto_node(NumberNode(), step_back=True)
        elif c.isalpha() or c in './*+-%_':
            state.token_start = state.head
            state.goto_node(UnquotedLiteral(), step_back=True)
        elif c == '#':
            state.token_start = state.head
            state.goto_node(CommentNode(), step_back=False)
        elif c == '@':
            state.token_start = state.head + 1
            state.goto_node(IdentifierNode(), step_back=False)
        elif c in ('"', "'"):
            state.token_start = state.head + 1
            state.goto_node(QuotedLiteralNode(c), step_back=False)
        elif c == '`':
            state.token_start = state.head + 1
            state.goto_node(QuotedArgListNode(), step_back=False)
        else:
            raise LexerError('Read unimplemented char', state)
        yield from ()


def match_operator(state: LexerState) -> Optional[Tuple[str, str]]:
    allow_arithmetic = state.in_block() or state.get_prev() != 'EXEC_ARG'
    trie = all_operators_trie if allow_arithmetic else non_arithmetic_ps_trie
    if (match := trie.largest_prefix(state.data, state.head)) is not None:
        return state.data[state.head : state.head + match.length], match.token
    return None


class OperatorsNode(DFANode):
    def __init__(self, pattern: str, operator: str):
        self.pattern = pattern
        self.operator = operator

    def step(self, _: str, state: LexerState) -> Iterator[Token]:
        state.step_forward(len(self.pattern) - 1)
        if self.operator == 'CURLY_OPEN':
            state.curly_depth += 1
        elif self.operator == 'CURLY_CLOSE':
            state.curly_depth -= 1
        elif self.operator == 'PAREN_OPEN':
            state.paren_depth += 1
        elif self.operator == 'PAREN_CLOSE':
            state.paren_depth -= 1
        elif self.operator == 'SQUARE_OPEN':
            state.square_depth += 1
        elif self.operator == 'SQUARE_CLOSE':
            state.square_depth -= 1
        yield state.get_token(self.operator, inclusive=True)
        state.goto_node(StartNode(), step_back=False)


class CommentNode(DFANode):
    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if c == '\n':
            if state.paren_depth == 0:
                yield Token('SEMICOLON', '')
            state.goto_node(StartNode())


class IdentifierNode(DFANode):
    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if c == '.' and state.next_char() != '.':
            if state.token_start == state.head:
                raise LexerError('Identifier is empty', state)
            yield state.get_token('NAME', inclusive=False)
            state.token_start = state.head
            yield state.get_token('DOT', inclusive=True)
            state.token_start = state.head + 1
        elif c.isspace() or c in r':=+-/[]{}()<>.':
            if state.token_start == state.head:
                raise LexerError('Identifier is empty', state)
            yield state.get_token('NAME', inclusive=False)
            state.goto_node(StartNode(), step_back=True)
        elif c in '@':
            raise LexerError('Read unexpected char', state)


class QuotedLiteralNode(DFANode):
    def __init__(self, quote_type: str):
        self.quote_type = quote_type
        self.escaped = False

    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if self.escaped or c == '\\':
            self.escaped = not self.escaped
        elif c == self.quote_type:
            if state.get_prev() == 'EXEC_ARG':
                yield state.get_token('EXEC_ARG', inclusive=False)
            else:
                yield state.get_token('QUOTED_STRING', inclusive=False)
            state.goto_node(StartNode(), step_back=False)


class QuotedArgListNode(DFANode):
    def __init__(self) -> None:
        self.escaped = False
        self.quoted = False
        self.quote_type: Optional[str] = None

    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if self.escaped or c == '\\':
            self.escaped = not self.escaped
        elif c in ["'", '"']:
            if not self.quoted:
                self.quoted = True
                self.quote_type = c
                state.token_start = state.head + 1
            elif c == self.quote_type:
                self.quoted = False
                self.quote_type = None
                yield state.get_token('EXEC_ARG', inclusive=False)
                state.token_start = state.head + 1
        elif self.quoted:
            pass
        elif c == '|':
            if state.head != state.token_start:
                yield state.get_token('EXEC_ARG', inclusive=False)
            yield Token('PIPE', '|')
            state.token_start = state.head + 1
        elif c.isspace():
            if state.head != state.token_start:
                yield state.get_token('EXEC_ARG', inclusive=False)
            state.token_start = state.head + 1
        elif c == '`':
            if state.head != state.token_start:
                yield state.get_token('EXEC_ARG', inclusive=False)
            state.goto_node(StartNode(), step_back=False)


tokens_before_names = {
    'AS',
    'BREAK',
    'CATCH',
    'CLASS',
    'COLON',
    'CONTINUE',
    'DOT',
    'ELLIPSIS',
    'FOR',
    'FN',
    'USE',
    'LAMBDA',
    'NAMESPACE',
    # Closing braces
    'PAREN_CLOSE',
    'SQUARE_CLOSE',
    # Arithmetic
    'POWER',
    'INT_DIV',
    'TIMES',
    'DIVIDE',
    'PLUS',
    'MINUS',
    'MOD',
}


class UnquotedLiteral(DFANode):
    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        space = False
        if c.isspace() and c != '\n':
            c = state.next_nonwhitespace()
            space = True

        source = state.get_token_source(inclusive=False)
        predicted_token_type = self.get_token_type(source, state)

        if (
            c == '.'
            and state.next_char() != '.'
            and predicted_token_type in ['NAME', 'IMPLICIT_LAMBDA_PARAM']
        ):
            if len(source) != 0:
                yield state.get_token(predicted_token_type, source=source)
            yield state.get_token('DOT', source='.')
            state.goto_node(StartNode(), step_back=False)
        elif c in '(:=':
            if source in KEYWORDS:
                yield state.get_token(predicted_token_type, source=source)
            else:
                for i, name_part in enumerate(name_parts := source.split('.')):
                    if len(name_part) != 0:
                        if name_part == '_':
                            yield state.get_token(
                                'IMPLICIT_LAMBDA_PARAM', source=name_part
                            )
                        else:
                            yield state.get_token('NAME', source=name_part)
                    if i + 1 < len(name_parts):
                        yield state.get_token('DOT', source='.')
            state.goto_node(StartNode(), step_back=True)
        elif (
            space
            or c in '<>{}[])|;,\n'
            or c == '.'
            and state.next_char() == '.'
        ):
            yield state.get_token(predicted_token_type, source=source)
            if c == '\n' and state.paren_depth == 0:

                yield Token('SEMICOLON', '')
            state.goto_node(StartNode(), step_back=True)
        elif c in '@':
            raise LexerError(
                'Read unexpected char from unquoted esxpression', state
            )

    def get_token_type(self, source: str, state: LexerState) -> str:
        if state.get_prev() == 'EXEC_ARG':
            return 'EXEC_ARG'
        if source in KEYWORDS:
            return KEYWORDS[source]
        if source == '_' or source.startswith('_.'):
            return 'IMPLICIT_LAMBDA_PARAM'
        if state.in_block() or state.get_prev() in tokens_before_names:
            return 'NAME'
        return 'EXEC_ARG'


class NumberNode(DFANode):
    def __init__(self) -> None:
        self.has_decimal = False
        self.first_char = True

    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if c == '.':
            if state.next_char() == '.':
                token_type = self.get_token_type(state)
                yield state.get_token(token_type, inclusive=False)
                state.goto_node(StartNode(), step_back=True)
            elif self.has_decimal:
                raise LexerError('Read unexpected char', state)
            else:
                self.has_decimal = True
        elif not (c.isdigit() or self.first_char and c == '-'):
            token_type = self.get_token_type(state)
            if (
                token_type != 'EXEC_ARG'
                and (unit := self.get_units(c, state)) is not None
            ):
                token_type = f'UNIT_{token_type}'
                source = state.get_token_source(inclusive=False)
                yield Token(token_type, f'{source}:{unit}')
                state.head += len(unit)
            else:
                yield state.get_token(token_type, inclusive=False)
            state.goto_node(StartNode(), step_back=True)
        self.first_char = False

    def get_units(self, c: str, state: LexerState) -> Optional[str]:
        if not c.isalpha():
            return None
        unit = c.lower()
        for i in range(state.data_length - state.head - 1):
            c_next = state.data[state.head + 1 + i]
            if not c_next.isalpha():
                break
            unit += c_next.lower()
        if unit not in UNITS:
            raise LexerError(f'Number literal has unknown unit: {unit}', state)
        return unit

    def get_token_type(self, state: LexerState) -> str:
        if state.get_prev() == 'EXEC_ARG':
            return 'EXEC_ARG'
        return 'FLOAT' if self.has_decimal else 'INTEGER'


class EggLexer:
    def __init__(self) -> None:
        self.lexer_state: Optional[LexerState] = None

    def lex(self, data: str) -> Iterator[Token]:
        self.lexer_state = LexerState(data + ' #', StartNode)
        while self.lexer_state.has_data():
            for token in self.step():
                yield token
        if self.lexer_state.state_node.__class__ != CommentNode:
            raise LexerError('Read unexpected char', self.lexer_state)

    def step(self) -> Iterator[Token]:
        assert self.lexer_state is not None
        atom = self.lexer_state.read()
        for token in self.lexer_state.state_node.step(atom, self.lexer_state):
            yield token
        self.lexer_state.head += 1

    def reset(self) -> None:
        self.lexer_state = None


class EggLexerLark(lark.lexer.Lexer):
    def __init__(self, _) -> None:   # type: ignore[no-untyped-def]
        self.lexer = EggLexer()

    def lex(  # type: ignore[override]
        self, egg_code: str
    ) -> Iterator[lark.lexer.Token]:
        for token in self.lexer.lex(egg_code):
            yield token.to_lark()
