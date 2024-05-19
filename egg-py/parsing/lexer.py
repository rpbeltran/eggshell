import lark.lexer
from typing import Iterator


# Keep operators sorted by length plz.
OPERATORS = {
    # 2-Char Operators
    ':=': 'DECLARE',
    '>>': 'APPEND_FILE',
    '//': 'INT_DIV',
    # 1-Char Operators
    ':': 'COLON',
    '=': 'ASSIGN',
    '|': 'PIPE',
    '(': 'PAREN_OPEN',
    ')': 'PAREN_CLOSE',
    '{': 'CURLY_OPEN',
    '}': 'CURLY_CLOSE',
    '<': 'ANGLE_OPEN',
    '>': 'ANGLE_CLOSE',
    '[': 'SQUARE_OPEN',
    ']': 'SQUARE_CLOSE',
    ';': 'SEMICOLON',
    '$': 'CURRY',
    '+': 'PLUS',
    '-': 'MINUS',
    '/': 'DIVIDE',
    '%': 'MOD',
}

OPERATOR_STARTS = {op[0] for op in OPERATORS}

KEYWORDS = {
    'fn': 'FN',
    'for': 'FOR',
    'while': 'WHILE',
    'continue': 'CONTINUE',
    'break': 'BREAK',
    'true': 'TRUE',
    'false': 'FALSE',
    'and': 'AND',
    'or': 'OR',
    'xor': 'XOR',
    'not': 'NOT',
    'ret': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'use': 'USE',
    'try': 'TRY',
    'catch': 'CATCH',
}


class Token:
    def __init__(self, token_type: str, source: str):
        self.token_type = token_type
        self.source = source

    def to_lark(self):
        return lark.lexer.Token(self.token_type, self.source)

    def __str__(self):
        return f"<{self.token_type}: '{self.source}'>"


class LexerError(Exception):
    def __init__(self, problem, lexer_state: 'LexerState'):
        self.problem = problem
        self.position = lexer_state.head
        self.head = lexer_state.read() if lexer_state.has_data() else 'EOF'
        self.dfa_state = lexer_state.state_node

    def __str__(self):
        return (
            f"{self.problem} '{self.head}' in position {self.position}.\n"
            f'\tDFA State: {self.dfa_state}.\n'
        )


class LexerState:
    def __init__(self, data):
        self.data = data
        self.token_start = 0
        self.head = 0
        self.state_node = StartNode()
        self.prev_token_type = None

    def has_data(self):
        return self.head < len(self.data)

    def read(self):
        return self.data[self.head]

    def get_token_source(self, end=None, inclusive=True):
        if end is None:
            end = self.head
        if inclusive:
            end += 1
        return self.data[self.token_start : end]

    def get_token(self, token_type, end=None, inclusive=True, source=None):
        if source is None:
            source = self.get_token_source(end, inclusive)
        self.prev_token_type = token_type
        return Token(token_type, source)

    def goto_node(self, state, step_back=False):
        self.state_node = state
        if step_back:
            self.step_back()

    def step_back(self, steps=1):
        self.head -= steps

    def step_forward(self, steps=1):
        self.head += steps

    def peek(self, strip=False) -> str:
        tail = self.data[self.head + 1 :]
        if strip:
            return tail.lstrip()
        return tail

    def peek_one(self, strip=False) -> str:
        if peek := self.peek(strip):
            return peek[0]
        return ''


class DFANode:
    def __str__(self):
        return f'<{self.__class__.__name__}:  {self.__dict__}>'


class StartNode(DFANode):
    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if c == '\n':
            state.prev_token_type = None
        elif c.isspace():
            pass
        elif c.isalpha() or c in '_./':
            state.token_start = state.head
            state.goto_node(UnquotedLiteral(), step_back=True)
        elif c.isdigit() or (c == '-' and state.peek_one().isdigit()):
            state.token_start = state.head
            state.goto_node(NumberNode(), step_back=True)
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
        elif c in OPERATOR_STARTS:
            state.token_start = state.head
            state.goto_node(OperatorsNode(), step_back=True)
        else:
            raise LexerError('Read unimplemented char', state)
        yield from ()


class OperatorsNode(DFANode):
    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        print(c, state.head)
        found = False
        data = c + state.peek()
        for pattern, token_type in OPERATORS.items():
            if data.startswith(pattern):
                found = True
                state.step_forward(len(pattern) - 1)
                yield state.get_token(token_type, inclusive=True)
                state.goto_node(StartNode(), step_back=False)
                break
        if not found:
            raise LexerError('Read unimplemented char', state)


class CommentNode(DFANode):
    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if c == '\n':
            state.goto_node(StartNode())
        yield from ()


class IdentifierNode(DFANode):
    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if c.isspace() or c in r':=+-/[]{}()':
            if state.token_start == state.head:
                raise LexerError('Empty identifier not permitted', state)
            yield state.get_token('IDENTIFIER', inclusive=False)
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
            yield state.get_token('QUOTED_STRING', inclusive=False)
            state.goto_node(StartNode(), step_back=False)


class QuotedArgListNode(DFANode):
    def __init__(self):
        self.escaped = False

    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if self.escaped or c == '\\':
            self.escaped = not self.escaped
        elif c.isspace():
            if state.head != state.token_start:
                yield state.get_token('EXEC_ARG', inclusive=False)
            state.token_start = state.head + 1
        elif c == '`':
            if state.head != state.token_start:
                yield state.get_token('EXEC_ARG', inclusive=False)
            state.goto_node(StartNode(), step_back=False)


class UnquotedLiteral(DFANode):
    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        space = False
        if c.isspace():
            c = state.peek_one(strip=True)
            space=True
        elif c in '@':
            raise LexerError('Read unexpected char', state)

        if c in '(:=':
            yield state.get_token('IDENTIFIER', inclusive=False)
            state.goto_node(StartNode(), step_back=True)
        elif space or c in ')|':
            source = state.get_token_source(inclusive=False)
            token_type = self.get_token_type(source, state)
            yield state.get_token(token_type, source=source)
            state.goto_node(StartNode(), step_back=True)

    def get_token_type(self, source: str, state: LexerState):
        if source in KEYWORDS:
            return KEYWORDS[source]
        if state.prev_token_type in ['CATCH', 'COLON', 'FOR', 'FN', 'USE']:
            return 'IDENTIFIER'
        return 'EXEC_ARG'


class NumberNode(DFANode):
    def __init__(self):
        self.has_decimal = False

    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        if c == '.':
            if self.has_decimal:
                raise LexerError('Read unexpected char', state)
            self.has_decimal = True
        elif not (c.isdigit() or c == '-'):
            token_type = self.get_token_type(state)
            yield state.get_token(token_type, inclusive=False)
            state.goto_node(StartNode(), step_back=True)

    def get_token_type(self, state: LexerState) -> str:
        if state.prev_token_type == 'EXEC_ARG':
            return 'EXEC_ARG'
        return 'FLOAT' if self.has_decimal else 'INTEGER'


class EggLexer:
    def __init__(self):
        self.lexer_state = None

    def lex(self, data) -> Iterator[Token]:
        self.lexer_state = LexerState(data + ' #')
        while self.lexer_state.has_data():

            for token in self.step():
                yield token
        if self.lexer_state.state_node.__class__ != CommentNode:
            raise LexerError('Read unexpected char', self.lexer_state)

    def step(self) -> Iterator[Token]:
        atom = self.lexer_state.read()
        #print( "-", atom, self.lexer_state.state_node.__class__)
        for token in self.lexer_state.state_node.step(atom, self.lexer_state):
            yield token
        self.lexer_state.head += 1


class EggLexerLark(lark.lexer.Lexer):
    def __init__(self, _):
        self.lexer = EggLexer()

    def lex(self, egg_code):
        for token in self.lexer.lex(egg_code):
            yield token.to_lark()
