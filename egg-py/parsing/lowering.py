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
        identifier = Tree('identifier', ['_'])
        selection = Tree('select_field', [identifier, field])
        return Tree('lambda_func', ['_', selection])

    def __default__(data, children, meta):
        return Tree(data, children, meta)
