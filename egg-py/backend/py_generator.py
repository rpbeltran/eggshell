from lark import Transformer, Tree


class FeatureUnimplemented(Exception):
    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return f'This feature has not yet been implemented:\n\t{self.feature}'


class PythonGenerator(Transformer):

    backend_library = '_e'

    @staticmethod
    def map_to_constant(value):
        @staticmethod
        def action(_):
            return f'{PythonGenerator.backend_library}.{value}'

        return action

    @staticmethod
    def combine_with_function(func_name, map_items=None, quote_args=False):
        @staticmethod
        def action(items):
            if map_items:
                items = [map_items(item) for item in items]
            if quote_args:
                arg_list = ','.join(repr(item) for item in items)
            else:
                arg_list = ','.join(str(item) for item in items)
            return f'{PythonGenerator.backend_library}.{func_name}({arg_list})'

        return action

    @staticmethod
    def combine_with_method_left(func_name, quote_args=False):
        @staticmethod
        def action(items):
            if quote_args:
                arg_list = ','.join(repr(item) for item in items[1:])
            else:
                arg_list = ','.join(str(item) for item in items[1:])
            return f'{items[0]}.{func_name}({arg_list})'

        return action

    # Arithmetic
    integer_literal = combine_with_function('make_integer')
    float_literal = combine_with_function('make_float')

    addition = combine_with_method_left('add')
    subtraction = combine_with_method_left('subtract')
    multiply = combine_with_method_left('multiply')
    divide = combine_with_method_left('divide')
    int_divide = combine_with_method_left('int_divide')
    modulus = combine_with_method_left('modulus')
    raise_power = combine_with_method_left('raise_power')

    # Boolean Arithmetic
    boolean_literal = combine_with_function(
        'make_boolean', map_items=lambda item: item == 'true'
    )

    comparison_chain = combine_with_function('do_comparisons')

    equal_to = map_to_constant('ComparisonType.EQUAL')
    not_equal_to = map_to_constant('ComparisonType.UNEQUAL')
    less_than_or_equal_to = map_to_constant('ComparisonType.LTE')
    less_than = map_to_constant('ComparisonType.LESS')
    greater_than = map_to_constant('ComparisonType.GREATER')
    greater_than_or_equal_to = map_to_constant('ComparisonType.GTE')

    or_expr = combine_with_method_left('logical_or')
    xor_expr = combine_with_method_left('logical_xor')
    and_expr = combine_with_method_left('logical_and')

    # External Commands
    exec = combine_with_function('make_external_command', quote_args=True)
    pipeline = combine_with_function('make_pipeline')

    @staticmethod
    def unit_literal(items):
        (unit_type_tree, unit_tree, quantity) = items
        unit_type = unit_type_tree.children[0]
        unit = unit_tree.children[0]
        return (
            f'{PythonGenerator.backend_library}.make_unit_value'
            f'({repr(unit_type)}, {repr(unit)}, {quantity})'
        )

    # Nodes not to modify
    pass_through = {'unit_type', 'unit'}

    @staticmethod
    def __default__(data, children, meta):
        as_tree = Tree(data, children, meta)
        if data in PythonGenerator.pass_through:
            return as_tree
        raise FeatureUnimplemented(as_tree)
