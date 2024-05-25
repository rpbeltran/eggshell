import lark.lexer

from typing import Callable, Iterable


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
    def __init__(self, data, StartNodeType: Callable):
        self.data = data
        self.token_start = 0
        self.head = 0
        self.state_node = StartNodeType()
        self.prev_token_types = []
        self.curly_depth = 0
        self.paren_depth = 0
        self.square_depth = 0

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
        self.prev_token_types.append(token_type)
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

    def clear_prev(self):
        self.prev_token_types = []

    def get_prev(self) -> str:
        if self.prev_token_types:
            return self.prev_token_types[-1]
        return ''

    def in_block(self) -> bool:
        return (
            self.curly_depth > 0
            or self.paren_depth > 0
            or self.square_depth > 0
        )


class DFANode:
    def __str__(self):
        return f'<{self.__class__.__name__}:  {self.__dict__}>'
