from lark import Transformer, Tree


class FeatureUnimplemented(Exception):
    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return f'This feature has not yet been implemented:\n\t{self.feature}'


class PythonGenerator(Transformer):

    backend_library = 'egg_lib'

    @staticmethod
    def combine_with_function(func_name):
        @staticmethod
        def action(items):
            (a, b) = items
            return f'{PythonGenerator.backend_library}.{func_name}({a},{b})'

        return action

    addition = combine_with_function('add')
    subtraction = combine_with_function('subtract')
    multiply = combine_with_function('multiply')
    divide = combine_with_function('divide')
    int_divide = combine_with_function('int_divide')
    modulus = combine_with_function('modulus')
    raise_power = combine_with_function('raise_power')

    @staticmethod
    def __default__(data, children, meta):
        raise FeatureUnimplemented(Tree(data, children, meta))
