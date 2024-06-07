from lark import Transformer, Tree


class LoweringTransformer(Transformer):

    def boolean_literal(items):
        (literal,) = items
        return literal == "true"


    def integer_literal(items):
        (literal,) = items
        return int(literal)


    def float_literal(items):
        (literal,) = items
        return float(literal)


    def always_loop(items):
        return Tree("while", [True, *items])


    def __default__(data, children, meta):
        return Tree(data, children, meta)
