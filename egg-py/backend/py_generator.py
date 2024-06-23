import lark
from lark import Transformer, Tree
from .temporary_objects import Block, Name


class FeatureUnimplemented(Exception):
    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return f'This feature has not yet been implemented:\n\t{self.feature}'


class PythonGenerator(Transformer):

    backend_library = '_e'
    memory_instance = '_m'

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
            items = [
                PythonGenerator.__resolve_placeholders(item) for item in items
            ]
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
            items = [
                PythonGenerator.__resolve_placeholders(item) for item in items
            ]
            if quote_args:
                arg_list = ','.join(repr(item) for item in items[1:])
            else:
                arg_list = ','.join(str(item) for item in items[1:])
            return f'{items[0]}.{func_name}({arg_list})'

        return action

    # Blocks
    @staticmethod
    def start(items):
        return Block(
            [PythonGenerator.__resolve_placeholders(item) for item in items]
        )

    # Collections
    string_literal = combine_with_function(
        'make_string', map_items=lambda item: repr(item.value)
    )
    list = combine_with_function('make_list')
    range = combine_with_function('make_range')
    concatenate = combine_with_method_left('concatenate')
    select_element = combine_with_method_left('select_element')

    @staticmethod
    def select_slice(items):
        start = None
        end = None
        jump = None
        for item in items[1:]:
            if not item.children:
                continue
            if item.data == 'slice_start':
                start = item.children[0]
            elif item.data == 'slice_end':
                end = item.children[0]
            elif item.data == 'slice_jump':
                jump = item.children[0]
            else:
                raise ValueError(f'select_slize has unexpected child {item}')
        return f'{items[0]}.select_slice({start},{end},{jump})'

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
    unary_negate = combine_with_method_left('negate')

    # Boolean Arithmetic
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
    unary_not = combine_with_method_left('logical_not')
    boolean_literal = combine_with_function(
        'make_boolean', map_items=lambda item: item == 'true'
    )

    # Memory
    @staticmethod
    def declare_untyped_variable(items):
        (name, value) = items
        name = name.value
        return f'{PythonGenerator.memory_instance}.new({value}, name={repr(name)})'

    @staticmethod
    def declare_untyped_constant(items):
        (name, value) = items
        name = name.value
        return (
            f'{PythonGenerator.memory_instance}'
            f'.new({value}, name={repr(name)}, const=True)'
        )

    @staticmethod
    def reassign(items):
        (lhs, rhs) = items
        assert isinstance(lhs, Name)
        if lhs.namespace:
            raise FeatureUnimplemented('Namespaces are not yet supported')
        return (
            f'{PythonGenerator.memory_instance}'
            f'.update_var({repr(lhs.name)}, {rhs})'
        )

    @staticmethod
    def identifier(items):
        items = [item.value for item in items]
        if len(items) > 1:
            return Name(items[0], namespace=items[1:])
        return Name(items[0])

    # External Commands
    exec = combine_with_function('make_external_command', quote_args=True)
    pipeline = combine_with_function('make_pipeline')

    say = combine_with_function('say')
    assertion = combine_with_function('assertion')

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
    pass_through = {
        'unit_type',
        'unit',
        'slice_start',
        'slice_end',
        'slice_jump',
    }

    @staticmethod
    def __default__(data, children, meta):
        as_tree = Tree(data, children, meta)
        if data in PythonGenerator.pass_through:
            return as_tree
        raise FeatureUnimplemented(as_tree)

    # Utilities

    @staticmethod
    def __resolve_placeholders(result):
        return transform_pygen_result(result)


def transform_pygen_result(result) -> str:
    if isinstance(result, Name):
        return (
            f'{PythonGenerator.memory_instance}'
            f'.get_object_by_name({repr(result.name)})'
        )
    if isinstance(result, Block):
        return result.join()
    return result
