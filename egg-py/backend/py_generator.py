from lark import Transformer, Tree


class FeatureUnimplemented(Exception):
    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return f'This feature has not yet been implemented:\n\t{self.feature}'


class PythonGenerator(Transformer):

    backend_library = 'egg_lib'

    @staticmethod
    def combine_with_function(func_name, quote_args=False):
        @staticmethod
        def action(items):
            if quote_args:
                arg_list = ','.join(repr(item) for item in items)
            else:
                arg_list = ','.join(str(item) for item in items)
            return f'{PythonGenerator.backend_library}.{func_name}({arg_list})'

        return action

    # Arithmetic
    addition = combine_with_function('add')
    subtraction = combine_with_function('subtract')
    multiply = combine_with_function('multiply')
    divide = combine_with_function('divide')
    int_divide = combine_with_function('int_divide')
    modulus = combine_with_function('modulus')
    raise_power = combine_with_function('raise_power')

    # External Commands
    exec = combine_with_function('make_external_command', quote_args=True)
    pipeline = combine_with_function('make_pipeline')

    @staticmethod
    def __default__(data, children, meta):
        raise FeatureUnimplemented(Tree(data, children, meta))
