from lark import Transformer, Tree

from .lexer_constants import UNITS


class LoweringTransformer(Transformer):
    @staticmethod
    def exec(items):
        return Tree('exec', [str(item) for item in items])

    @staticmethod
    def boolean_literal(items):
        (literal,) = items
        return literal == 'true'

    @staticmethod
    def unit_integer_literal(items):
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
    def unit_float_literal(items):
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
    def plus_assign(items):
        return LoweringTransformer.lower_assignment_operator('addition', items)

    @staticmethod
    def minus_assign(items):
        return LoweringTransformer.lower_assignment_operator(
            'subtraction', items
        )

    @staticmethod
    def times_assign(items):
        return LoweringTransformer.lower_assignment_operator('multiply', items)

    @staticmethod
    def divide_assign(items):
        return LoweringTransformer.lower_assignment_operator('divide', items)

    @staticmethod
    def int_div_assign(items):
        return LoweringTransformer.lower_assignment_operator(
            'int_divide', items
        )

    @staticmethod
    def mod_assign(items):
        return LoweringTransformer.lower_assignment_operator('modulus', items)

    @staticmethod
    def power_assign(items):
        return LoweringTransformer.lower_assignment_operator(
            'raise_power', items
        )

    @staticmethod
    def pipe_assign(items):
        return LoweringTransformer.lower_assignment_operator('pipeline', items)

    @staticmethod
    def concat_assign(items):
        return LoweringTransformer.lower_assignment_operator(
            'concatenate', items
        )

    @staticmethod
    def seq_and_assign(items):
        (a, b) = items
        return Tree(
            'reassign',
            [a, Tree('logical_sequence', [Tree('and_sequence', [a, b])])],
        )

    @staticmethod
    def seq_or_assign(items):
        (a, b) = items
        return Tree(
            'reassign',
            [a, Tree('logical_sequence', [Tree('or_sequence', [a, b])])],
        )

    @staticmethod
    def lower_assignment_operator(operator, items):
        (a, b) = items
        return Tree('reassign', [a, Tree(operator, [a, b])])

    @staticmethod
    def always_loop(items):
        return Tree('while', [True, *items])

    @staticmethod
    def selection_lambda_shorthand(items):
        (field,) = items
        identifier = Tree('identifier', ['@@shorthand_select@@'])
        selection = Tree('select_field', [identifier, field])
        return Tree('lambda_func', ['@@shorthand_select@@', selection])

    @staticmethod
    def implicit_lambda_param(items):
        arg = '@@implicit_lambda@@'
        identifier = Tree('identifier', [arg])
        return Tree('poisonous_lambda_func', [arg, identifier])

    @staticmethod
    def __default__(data, children, meta):
        tree = Tree(data, children, meta)
        if LoweringTransformer._allows_poisoning(tree):
            return LoweringTransformer._propagate_poison(tree)
        return tree

    @staticmethod
    def _propagate_poison(tree):
        # poison[f] + b => poison[f(_) + b]
        poisoned = False
        for i in range(len(tree.children)):
            c = tree.children[i]
            if LoweringTransformer._is_poisoned_lambda(c):
                tree.children[i] = c.children[1]
                poisoned = True
        if poisoned:
            return Tree(
                'poisonous_lambda_func',
                ['@@implicit_lambda_arg@@', Tree(tree.data, tree.children)],
            )
        return Tree(tree.data, tree.children, tree.meta)

    @staticmethod
    def _is_poisoned_lambda(tree):
        return isinstance(tree, Tree) and tree.data == 'poisonous_lambda_func'

    @staticmethod
    def _allows_poisoning(tree):
        cannot_be_poisoned = {'start', 'pipeline', 'curry'}
        data = tree.data
        if data.startswith('__'):
            data = data.split('_')[2]
        return data not in cannot_be_poisoned
