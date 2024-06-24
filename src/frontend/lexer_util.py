import lark.lexer

import abc
from typing import Callable, Iterator, NamedTuple, Optional


class Token(NamedTuple):
    token_type: str
    source: str

    def to_lark(self) -> lark.lexer.Token:
        return lark.lexer.Token(self.token_type, self.source)

    def __str__(self) -> str:
        return f"<{self.token_type}: '{self.source}'>"


class LexerError(Exception):
    def __init__(self, problem: str, lexer_state: 'LexerState'):
        self.problem = problem
        self.position = lexer_state.head
        self.head = lexer_state.read() if lexer_state.has_data() else 'EOF'
        self.dfa_state = lexer_state.state_node

    def __str__(self) -> str:
        return (
            f"On character '{self.head}' in position {self.position}:\n"
            f'\t{self.problem}\n'
            f'\tCurrent DFA State: {self.dfa_state}.\n'
        )


class LexerState:
    def __init__(self, data: str, start_node_type: Callable):
        self.data = data
        self.data_length = len(data)
        self.token_start = 0
        self.head = 0
        self.state_node: DFANode = start_node_type()
        self.prev_token_type: Optional[str] = None
        self.curly_depth = 0
        self.paren_depth = 0
        self.square_depth = 0

    def has_data(self) -> bool:
        return self.head < self.data_length

    def read(self) -> str:
        return self.data[self.head]

    def get_token_source(
        self, end: Optional[int] = None, inclusive: bool = True
    ) -> str:
        end_unwrapped = self.head if end is None else end
        if inclusive:
            end_unwrapped += 1
        return self.data[self.token_start : end_unwrapped]

    def get_token(
        self,
        token_type: str,
        end: Optional[int] = None,
        inclusive: bool = True,
        source: Optional[str] = None,
    ) -> Token:
        if source is None:
            source = self.get_token_source(end, inclusive)
        self.prev_token_type = token_type
        return Token(token_type, source)

    def goto_node(self, state: 'DFANode', step_back: bool = False) -> None:
        self.state_node = state
        if step_back:
            self.step_back()

    def step_back(self, steps: int = 1) -> None:
        self.head -= steps

    def step_forward(self, steps: int = 1) -> None:
        self.head += steps

    def next_char(self) -> str:
        return self.data[self.head + 1]

    def next_nonwhitespace(self) -> str:
        for i in range(self.data_length - self.head - 1):
            c = self.data[self.head + 1 + i]
            if not c.isspace():
                return c
        return ''

    def clear_prev(self) -> None:
        self.prev_token_type = None

    def get_prev(self) -> Optional[str]:
        return self.prev_token_type

    def in_block(self) -> bool:
        return (
            self.curly_depth > 0
            or self.paren_depth > 0
            or self.square_depth > 0
        )


class DFANode(abc.ABC):
    def __str__(self) -> str:
        return f'<{self.__class__.__name__}:  {self.__dict__}>'

    @abc.abstractmethod
    def step(self, c: str, state: LexerState) -> Iterator[Token]:
        ...
