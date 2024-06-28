from typing import Any, Callable, Iterable, List, Optional, Set

import lark
import lark.tree
from lark import Transformer, Tree
from lark.lexer import Token

from .temporary_objects import Block, Name


class FeatureUnimplemented(Exception):
    def __init__(self, feature: str):
        self.feature = feature

    def __str__(self) -> str:
        return f'This feature has not yet been implemented:\n\t{self.feature}'


class PythonGenerator(Transformer):

    backend_library = '_e'
    memory_instance = '_m'

    @staticmethod
    def map_to_constant(value: str) -> Callable[[Iterable], str]:
        @staticmethod   # type: ignore[misc]
        def action(_: Iterable) -> str:
            return f'{PythonGenerator.backend_library}.{value}'

        return action

    @staticmethod
    def combine_with_function(
        func_name: str,
        map_items: Optional[Callable[[Any], Any]] = None,
        quote_args: bool = False,
    ) -> Callable[[Iterable], str]:
        @staticmethod   # type: ignore[misc]
        def action(items: Iterable) -> str:
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
    def combine_with_method_left(
        func_name: str, quote_args: bool = False
    ) -> Callable[[Iterable], str]:
        @staticmethod   # type: ignore[misc]
        def action(items: Iterable) -> str:
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
    def block(items: Iterable[str | Name | Block]) -> Block:
        return Block(
            [PythonGenerator.__resolve_placeholders(item) for item in items]
        )

    @staticmethod
    def if_statement(items: List[str | Name | Block | Tree]) -> Block:
        assert not isinstance(items[0], Tree)
        condition = PythonGenerator.__resolve_placeholders(items[0])
        block = items[1]
        assert isinstance(block, Block)
        if_block = block.make_if(condition)
        for item in items[2:]:
            assert isinstance(item, Tree)
            if item.data == 'elif_statement':
                assert not isinstance(item.children[0], Tree)
                assert isinstance(item.children[1], Block)
                if_block.add_elif(
                    PythonGenerator.__resolve_placeholders(item.children[0]),
                    item.children[1],
                )
            else:
                assert item.data == 'else_statement'
                assert isinstance(item.children[0], Block)
                if_block.add_else(item.children[0])
        return if_block

    start = block

    # Collections
    string_literal = combine_with_function(
        'make_string', map_items=lambda item: repr(item.value)
    )
    list = combine_with_function('make_list')
    range = combine_with_function('make_range')
    concatenate = combine_with_method_left('concatenate')
    select_element = combine_with_method_left('select_element')

    @staticmethod
    def select_slice(items: List[Tree]) -> str:
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
    def lambda_func(items: List[Token | str | Name | Block]) -> str:
        (lhs, rhs) = items
        if isinstance(lhs, Tree):
            assert lhs.data == 'param_list'
            params = [param.value for param in lhs.children]
        else:
            assert isinstance(lhs, Token) and lhs.type == 'NAME'
            params = [lhs.value]

        if isinstance(rhs, Block):
            # lambdas returning blocks need to be handled with temporary
            # function definitions, or we could do something weird perhaps like
            # put each into a list and discard the output of that list.
            raise FeatureUnimplemented('Block lambdas are not yet implemented')

        rhs_pygen = PythonGenerator.__resolve_placeholders(rhs)

        return (
            f'{PythonGenerator.backend_library}'
            f'.make_lambda({repr(params)},lambda: {rhs_pygen})'
        )

    poisonous_lambda_func = lambda_func

    # Memory
    @staticmethod
    def declare_untyped_variable(
        items: List[Token | str | Name | Block],
    ) -> str:
        (name, value) = items
        assert isinstance(name, Token)
        name = name.value
        assert not isinstance(value, Token)
        value = PythonGenerator.__resolve_placeholders(value)
        return f'{PythonGenerator.memory_instance}.new({value}, name={repr(name)})'

    @staticmethod
    def declare_untyped_constant(
        items: List[Token | str | Name | Block],
    ) -> str:
        (name, value) = items
        assert isinstance(name, Token)
        name = name.value
        assert not isinstance(value, Token)
        value = PythonGenerator.__resolve_placeholders(value)
        return (
            f'{PythonGenerator.memory_instance}'
            f'.new({value}, name={repr(name)}, const=True)'
        )

    @staticmethod
    def reassign(items: List[Token | str | Name | Block]) -> str:
        (lhs, rhs) = items
        assert isinstance(lhs, Name)
        if lhs.namespace:
            raise FeatureUnimplemented('Namespaces are not yet supported')
        rhs = PythonGenerator.__resolve_placeholders(rhs)
        return (
            f'{PythonGenerator.memory_instance}'
            f'.update_var({repr(lhs.name)}, {rhs})'
        )

    @staticmethod
    def identifier(items: List[Token]) -> Name:
        item_strings = [item.value for item in items]
        if len(items) > 1:
            return Name(item_strings[0], namespace=item_strings[1:])
        return Name(item_strings[0])

    # External Commands
    exec = combine_with_function('make_external_command', quote_args=True)
    pipeline = combine_with_function('make_pipeline')

    say = combine_with_function('say')
    assertion = combine_with_function('assertion')

    @staticmethod
    def unit_literal(items: List[Tree | str | Name | Block]) -> str:
        (unit_type_tree, unit_tree, quantity) = items
        assert isinstance(unit_type_tree, Tree)
        unit_type = unit_type_tree.children[0]
        assert isinstance(unit_tree, Tree)
        unit = unit_tree.children[0]
        assert not isinstance(quantity, Tree)
        quantity = PythonGenerator.__resolve_placeholders(quantity)
        return (
            f'{PythonGenerator.backend_library}.make_unit_value'
            f'({repr(unit_type)}, {repr(unit)}, {quantity})'
        )

    # Nodes not to modify
    pass_through: Set[str] = {
        'elif_statement',
        'else_statement',
        'unit_type',
        'unit',
        'slice_start',
        'slice_end',
        'slice_jump',
        'param_list',
    }

    @staticmethod
    def __default__(
        data: str, children: List[Tree | Token], meta: lark.tree.Meta
    ) -> Tree:
        as_tree = Tree(data, children, meta)
        if data in PythonGenerator.pass_through:
            return as_tree
        raise FeatureUnimplemented(data)

    # Utilities

    @staticmethod
    def __resolve_placeholders(result: str | Name | Block) -> str:
        return transform_pygen_result(result)


def transform_pygen_result(result: str | Name | Block) -> str:
    if isinstance(result, Name):
        return (
            f'{PythonGenerator.memory_instance}'
            f'.get_object_by_name({repr(result.name)})'
        )
    if isinstance(result, Block):
        return result.join()
    return result
