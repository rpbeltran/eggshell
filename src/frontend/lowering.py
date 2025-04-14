import typing

from lark import Transformer, Tree
from lark.lexer import Token
from lark.tree import Meta

from .lexer_constants import UNITS


class LoweringTransformer(
    Transformer[Token, Tree[Token | int | float | str] | int | float | str]
):
    @staticmethod
    def exec(items: typing.Iterable[Token]) -> Tree[Token | int | float | str]:
        return Tree('exec', [str(item) for item in items])

    @staticmethod
    def unit_integer_literal(
        items: typing.Iterable[Token],
    ) -> Tree[Token | int | float | str]:
        (literal,) = items
        (value, unit) = literal.split(':')
        unit_type = UNITS[unit]
        return Tree(
            'unit_literal',
            [
                Tree('unit_type', [unit_type]),
                Tree('unit', [unit]),
                int(value),
            ],
        )

    @staticmethod
    def unit_float_literal(
        items: typing.Iterable[Token],
    ) -> Tree[Token | int | float | str]:
        (literal,) = items
        (value, unit) = literal.split(':')
        unit_type = UNITS[unit]
        return Tree(
            'unit_literal',
            [
                Tree('unit_type', [unit_type]),
                Tree('unit', [unit]),
                float(value),
            ],
        )

    @staticmethod
    def plus_assign(
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        return LoweringTransformer.lower_assignment_operator('addition', items)

    @staticmethod
    def minus_assign(
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        return LoweringTransformer.lower_assignment_operator(
            'subtraction', items
        )

    @staticmethod
    def times_assign(
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        return LoweringTransformer.lower_assignment_operator('multiply', items)

    @staticmethod
    def divide_assign(
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        return LoweringTransformer.lower_assignment_operator('divide', items)

    @staticmethod
    def int_div_assign(
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        return LoweringTransformer.lower_assignment_operator(
            'int_divide', items
        )

    @staticmethod
    def mod_assign(
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        return LoweringTransformer.lower_assignment_operator('modulus', items)

    @staticmethod
    def power_assign(
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        return LoweringTransformer.lower_assignment_operator(
            'raise_power', items
        )

    @staticmethod
    def pipe_assign(
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        return LoweringTransformer.lower_assignment_operator('pipeline', items)

    @staticmethod
    def concat_assign(
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        return LoweringTransformer.lower_assignment_operator(
            'concatenate', items
        )

    @staticmethod
    def seq_and_assign(
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        (a, b) = items
        return Tree(
            'reassign',
            [a, Tree('logical_sequence', [Tree('and_sequence', [a, b])])],
        )

    @staticmethod
    def seq_or_assign(
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        (a, b) = items
        return Tree(
            'reassign',
            [a, Tree('logical_sequence', [Tree('or_sequence', [a, b])])],
        )

    @staticmethod
    def lower_assignment_operator(
        operator: str,
        items: typing.Iterable[Token | Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        (a, b) = items
        return Tree('reassign', [a, Tree(operator, [a, b])])

    @staticmethod
    def always_loop(
        items: typing.Iterable[Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        return Tree('while', [True, *items])

    @staticmethod
    def selection_lambda_shorthand(
        items: typing.Iterable[Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        (field,) = items
        identifier: Tree[int | float | str] = Tree(
            'identifier', ['@@shorthand_select@@']
        )
        selection: Tree[int | float | str] = Tree(
            'select_field', [identifier, field]
        )
        return Tree('lambda_func', ['@@shorthand_select@@', selection])

    @staticmethod
    def implicit_lambda_param(
        _items: typing.Iterable[Tree[Token | int | float | str]],
    ) -> Tree[Token | int | float | str]:
        arg = Token('NAME', '@@implicit_lambda@@')
        identifier: Tree[int | float | str] = Tree('identifier', [arg])
        return Tree('poisonous_lambda_func', [arg, identifier])

    @staticmethod
    def __default__(
        data: str,
        children: typing.List[
            Tree[Token | int | float | str] | int | float | str
        ],
        meta: Meta,
    ) -> Tree[Token | int | float | str]:
        tree: Tree[int | float | str] = Tree(data, children, meta)
        if LoweringTransformer._allows_lambda_poisoning(tree):
            return LoweringTransformer._propagate_implicit_lambda(tree)
        return tree

    @staticmethod
    def _propagate_implicit_lambda(
        tree: Tree[Token | int | float | str],
    ) -> Tree[Token | int | float | str]:
        # poison[f] + b => poison[f(_) + b]
        poisoned = False
        for i in range(len(tree.children)):
            c = tree.children[i]
            if isinstance(c, Tree) and LoweringTransformer._is_poisoned_lambda(
                c
            ):
                tree.children[i] = c.children[1]
                poisoned = True
        if poisoned:
            return Tree(
                'poisonous_lambda_func',
                [
                    Token('NAME', '@@implicit_lambda@@'),
                    Tree(tree.data, tree.children),
                ],
            )
        return Tree(tree.data, tree.children, tree.meta)

    @staticmethod
    def _is_poisoned_lambda(tree: Tree[typing.Any]) -> bool:
        return tree.data == 'poisonous_lambda_func'

    @staticmethod
    def _allows_lambda_poisoning(
        tree: Tree[Token | int | float | str],
    ) -> bool:
        cannot_be_poisoned = {'start', 'pipeline', 'curry'}
        data = tree.data
        if data.startswith('__'):
            data = data.split('_')[2]
        return data not in cannot_be_poisoned
