from typing import Any, Iterable, List

import lark.tree
from lark import Transformer, Tree
from lark.lexer import Token


class FeatureUnimplemented(Exception):
    def __init__(self, feature: str):
        self.feature = feature

    def __str__(self) -> str:
        return f'This feature has not yet been implemented:\n\t{self.feature}'


class YolkGenerator(Transformer[Token | int | float | str, List[str]]):
    @staticmethod
    def append_instructions(instructions: List[str]):
        @staticmethod   # type: ignore[misc]
        def _inner(children: Iterable[Any]):
            program = [
                instruction for child in children for instruction in child
            ]
            program.extend(instructions)
            return program

        return _inner

    @staticmethod
    def append_instruction(instruction: str):
        @staticmethod   # type: ignore[misc]
        def _inner(children: Iterable[Any]):
            program = [
                instruction for child in children for instruction in child
            ]
            program.append(instruction)
            return program

        return _inner

    # Arithmetic
    @staticmethod
    def integer_literal(items: List[Any]):
        return [f'PUSH_INT {items[0]}']

    @staticmethod
    def float_literal(items: List[Any]):
        return [f'PUSH_NUM {items[0]}']

    addition = append_instruction('BINOP add')
    subtraction = append_instruction('BINOP subtract')
    multiply = append_instruction('BINOP multiply')
    divide = append_instruction('BINOP divide')
    int_divide = append_instruction('BINOP int_divide')
    modulus = append_instruction('BINOP modulus')
    raise_power = append_instruction('BINOP power')

    @staticmethod
    def __default__(
        data: str,
        children: List[
            Tree[Token | int | float | str] | Token | int | float | str
        ],
        meta: lark.tree.Meta,
    ) -> Tree[Token | int | float | str]:
        raise FeatureUnimplemented(data)
