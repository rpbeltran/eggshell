from lark import Transformer, Tree


class LoweringTransformer(Transformer):

    def always_loop(items):
        return Tree("while", [True, *items])


    def __default__(data, children, meta):
        return Tree(data, children, meta)
