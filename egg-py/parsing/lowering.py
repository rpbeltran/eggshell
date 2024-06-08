from lark import Transformer, Tree


class LoweringTransformer(Transformer):
    def boolean_literal(items):
        (literal,) = items
        return literal == 'true'

    def integer_literal(items):
        (literal,) = items
        return int(literal)

    def float_literal(items):
        (literal,) = items
        return float(literal)

    def always_loop(items):
        return Tree('while', [True, *items])

    def selection_lambda_shorthand(items):
        (field,) = items
        identifier = Tree('identifier', ['@@shorthand_select@@'])
        selection = Tree('select_field', [identifier, field])
        return Tree('lambda_func', ['@@shorthand_select@@', selection])

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
