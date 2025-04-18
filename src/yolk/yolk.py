from typing import Any, Callable, Iterable, List

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
    def append_instruction(
        instruction: str,
    ) -> Callable[[Iterable[Any]], List[str]]:
        @staticmethod   # type: ignore[misc]
        def _inner(children: Iterable[Iterable[str]]) -> List[str]:
            program = [
                instruction for child in children for instruction in child
            ]
            program.append(instruction)
            return program

        return _inner

    # Literals
    @staticmethod
    def integer_literal(items: List[Any]) -> List[str]:
        return [f'PUSH_INT {items[0]}']

    @staticmethod
    def float_literal(items: List[Any]) -> List[str]:
        return [f'PUSH_NUM {items[0]}']

    @staticmethod
    def string_literal(items: List[lark.Token]) -> List[str]:
        return [f'PUSH_STR {repr(items[0].value)}']

    @staticmethod
    def boolean_literal(items: List[lark.Token]) -> List[str]:
        return [f'PUSH_BOOL {items[0]}']

    # Unary Opertors
    unary_negate = append_instruction('NEGATE')
    unary_not = append_instruction('NOT')

    # Binary Operators
    addition = append_instruction('BINOP add')
    subtraction = append_instruction('BINOP subtract')
    multiply = append_instruction('BINOP multiply')
    divide = append_instruction('BINOP divide')
    int_divide = append_instruction('BINOP int_divide')
    modulus = append_instruction('BINOP modulus')
    raise_power = append_instruction('BINOP power')
    concatenate = append_instruction('BINOP concat')
    and_expr = append_instruction('BINOP and')
    or_expr = append_instruction('BINOP or')

    # Comparisons
    equal_to = append_instruction('equal')
    greater_than = append_instruction('greater')
    greater_than_or_equal_to = append_instruction('gte')
    less_than = append_instruction('less')
    less_than_or_equal_to = append_instruction('lte')
    not_equal_to = append_instruction('unequal')

    @staticmethod
    def comparison_chain(items: List[Any]) -> List[str]:
        instrutions = []
        for i in range(len(items)):
            if i == 0:
                instrutions.extend(items[i])
            elif (i - 1) % 2 == 0:
                instrutions.extend(items[i + 1])
            elif (i - 1) % 2 == 1:
                if i == len(items) - 1:
                    instrutions.append(f'COMPARE {items[i-1][0]}')
                else:
                    instrutions.append(f'COMPARE_CHAIN {items[i-1][0]}')
        if len(items) > 3:
            for i in range((len(items) - 3) // 2):
                instrutions.append('BINOP and')
        return instrutions

    @staticmethod
    def __default__(
        data: str,
        children: List[
            Tree[Token | int | float | str] | Token | int | float | str
        ],
        meta: lark.tree.Meta,
    ) -> Tree[Token | int | float | str]:
        raise FeatureUnimplemented(data)
