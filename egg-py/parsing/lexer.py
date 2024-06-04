import lark.lexer
from typing import Iterator, Optional, Tuple

from .lexer_constants import (
    KEYWORDS,
    OPERATORS,
    OPERATOR_STARTS,
    BLOCK_OPERATORS,
    BLOCK_OPERATOR_STARTS,
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
        elif (match := match_operator(c, state)) != None:
            state.token_start = state.head
            state.goto_node(OperatorsNode(match[0], match[1]), step_back=True)
        elif c.isdigit() or (c == '-' and state.peek_one().isdigit()):
            state.token_start = state.head
            state.goto_node(NumberNode(), step_back=True)
        elif state.get_prev() in ['NAME', 'FLOAT', 'INTEGER'] and c == '-':
            state.token_start = state.head
            state.goto_node(NumberNode(), step_back=True)
        elif c.isalpha() or c in './*+-%':
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


def match_operator(c: str, state: LexerState) -> Optional[Tuple[str, str]]:
    starts = BLOCK_OPERATOR_STARTS if state.in_block() else OPERATOR_STARTS
    operators = BLOCK_OPERATORS if state.in_block() else OPERATORS
    if c in starts:
        data = c + state.peek()
        for pattern, token_type in operators.items():
            if token_type == "NAMESPACE" and state.get_prev() == "SQUARE_OPEN":
                continue
            if data.startswith(pattern):
                return pattern, token_type
    return None


class OperatorsNode(DFANode):
    def __init__(self, pattern, operator):
        self.pattern = pattern
        self.operator = operator

    def step(self, c: str, state: LexerState) -> Iterator[Token]:
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
        if c == '.' and state.peek_one() != '.':
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
    def __init__(self):
        self.escaped = False
        self.quoted = False
        self.quote_type = None

    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if self.escaped or c == '\\':
            self.escaped = not self.escaped
        elif c in ['\'','"']:
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
            yield Token(f'PIPE', '|')
            state.token_start = state.head + 1
        elif c.isspace():
            if state.head != state.token_start:
                yield state.get_token('EXEC_ARG', inclusive=False)
            state.token_start = state.head + 1
        elif c == '`':
            if state.head != state.token_start:
                yield state.get_token('EXEC_ARG', inclusive=False)
            state.goto_node(StartNode(), step_back=False)


tokens_before_names = [
    'AS',
    'BREAK',
    'CATCH',
    'CLASS',
    'COLON',
    'CONTINUE',
    'DOT',
    'FOR',
    'FN',
    'USE',
    'LAMBDA',
    'NAMESPACE',
    # Closing braces
    'PAREN_CLOSE',
    'SQUARE_CLOSE',
    # Artithmetic
    'POWER',
    'INT_DIV',
    'TIMES',
    'DIVIDE',
    'PLUS',
    'MINUS',
    'MOD',
]


class UnquotedLiteral(DFANode):
    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        space = False
        if c.isspace() and c != '\n':
            c = state.peek_one(strip=True)
            space = True

        source = state.get_token_source(inclusive=False)
        predicted_token_type = self.get_token_type(source, state)

        if (
            c == '.'
            and state.peek_one() != '.'
            and predicted_token_type == 'NAME'
        ):
            if len(source) != 0:
                yield state.get_token('NAME', source=source)
            yield state.get_token('DOT', source='.')
            state.goto_node(StartNode(), step_back=False)
        elif c in '(:=':
            if source in KEYWORDS:
                yield state.get_token(predicted_token_type, source=source)
            else:
                for i, name_part in enumerate(name_parts := source.split('.')):
                    if len(name_part) != 0:
                        yield state.get_token('NAME', source=name_part)
                    if i + 1 < len(name_parts):
                        yield state.get_token('DOT', source='.')
            state.goto_node(StartNode(), step_back=True)
        elif (
            space or c in '<>{}[])|;,\n' or c == '.' and state.peek_one() == '.'
        ):
            yield state.get_token(predicted_token_type, source=source)
            if c == '\n' and state.paren_depth == 0:

                yield Token(f'SEMICOLON', '')
            state.goto_node(StartNode(), step_back=True)
        elif c in '@':
            raise LexerError(
                'Read unexpected char from unquoted esxpression', state
            )

    def get_token_type(self, source: str, state: LexerState):
        if state.get_prev() == 'EXEC_ARG':
            return 'EXEC_ARG'
        if source in KEYWORDS:
            return KEYWORDS[source]
        if state.in_block() or state.get_prev() in tokens_before_names:
            return 'NAME'
        return 'EXEC_ARG'


class NumberNode(DFANode):
    def __init__(self):
        self.has_decimal = False

    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if c == '.':
            if state.peek_one() == ".":
                token_type = self.get_token_type(state)
                yield state.get_token(token_type, inclusive=False)
                state.goto_node(StartNode(), step_back=True)
            elif self.has_decimal:
                raise LexerError('Read unexpected char', state)
            else:
                self.has_decimal = True
        elif not (c.isdigit() or c == '-'):
            token_type = self.get_token_type(state)
            yield state.get_token(token_type, inclusive=False)
            state.goto_node(StartNode(), step_back=True)

    def get_token_type(self, state: LexerState) -> str:
        if state.get_prev() == 'EXEC_ARG':
            return 'EXEC_ARG'
        return 'FLOAT' if self.has_decimal else 'INTEGER'


class EggLexer:
    def __init__(self):
        self.lexer_state = None

    def lex(self, data) -> Iterator[Token]:
        self.lexer_state = LexerState(data + ' #', StartNode)
        while self.lexer_state.has_data():
            for token in self.step():
                yield token
        if self.lexer_state.state_node.__class__ != CommentNode:
            raise LexerError('Read unexpected char', self.lexer_state)

    def step(self) -> Iterator[Token]:
        atom = self.lexer_state.read()
        for token in self.lexer_state.state_node.step(atom, self.lexer_state):
            yield token
        self.lexer_state.head += 1

    def reset(self):
        self.lexer_state = None


class EggLexerLark(lark.lexer.Lexer):
    def __init__(self, _):
        self.lexer = EggLexer()

    def lex(self, egg_code):
        for token in self.lexer.lex(egg_code):
            yield token.to_lark()
