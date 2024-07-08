from typing import Any, Callable, Iterable, List, Optional, Set

import lark.tree
from lark import Transformer, Tree
from lark.lexer import Token

from .temporary_objects import Block, Name, PygenIntermediary


class FeatureUnimplemented(Exception):
    def __init__(self, feature: str):
        self.feature = feature

    def __str__(self) -> str:
        return f'This feature has not yet been implemented:\n\t{self.feature}'


class PythonGenerator(Transformer):

    backend_library = '_e'
    memory_instance = '_m'

    @staticmethod
    def map_to_constant(value: str) -> Callable[[Iterable], PygenIntermediary]:
        @staticmethod   # type: ignore[misc]
        def action(_: Iterable) -> PygenIntermediary:
            return PygenIntermediary(
                f'{PythonGenerator.backend_library}.{value}'
            )

        return action

    @staticmethod
    def combine_with_function(
        func_name: str,
        map_items: Optional[Callable[[Any], Any]] = None,
        quote_args: bool = False,
    ) -> Callable[[Iterable], PygenIntermediary]:
        @staticmethod   # type: ignore[misc]
        def action(items: Iterable) -> PygenIntermediary:
            items = [
                PythonGenerator.__resolve_placeholders(item) for item in items
            ]
            if map_items:
                items = [map_items(item) for item in items]
            if quote_args:
                arg_list = ','.join(repr(item) for item in items)
            else:
                arg_list = ','.join(str(item) for item in items)
            return PygenIntermediary(
                f'{PythonGenerator.backend_library}.{func_name}({arg_list})'
            )

        return action

    @staticmethod
    def combine_with_method_left(
        func_name: str, quote_args: bool = False
    ) -> Callable[[Iterable], PygenIntermediary]:
        @staticmethod   # type: ignore[misc]
        def action(items: Iterable) -> PygenIntermediary:
            items = [
                PythonGenerator.__resolve_placeholders(item) for item in items
            ]
            if quote_args:
                arg_list = ','.join(repr(item) for item in items[1:])
            else:
                arg_list = ','.join(str(item) for item in items[1:])
            return PygenIntermediary(f'{items[0]}.{func_name}({arg_list})')

        return action

    # Blocks
    @staticmethod
    def block(items: Iterable[str | Name | Block]) -> PygenIntermediary:
        return PygenIntermediary(
            Block(
                [
                    PythonGenerator.__resolve_placeholders(item)
                    for item in items
                ]
            )
        )

    function_block = block
    start = block

    @staticmethod
    def if_statement(
        items: List[PygenIntermediary | Tree],
    ) -> PygenIntermediary:
        assert isinstance(items[0], PygenIntermediary)
        condition = items[0].finalize()
        assert isinstance(items[1], PygenIntermediary)
        block = items[1].inline
        assert isinstance(block, Block)
        if_block = block.make_if(condition)
        for item in items[2:]:
            assert isinstance(item, Tree)
            if item.data == 'elif_statement':
                assert isinstance(item.children[0], PygenIntermediary)
                assert isinstance(item.children[1], PygenIntermediary)
                assert isinstance(item.children[1].inline, Block)
                if_block.add_elif(
                    PythonGenerator.__resolve_placeholders(item.children[0]),
                    item.children[1].inline,
                )
            else:
                assert item.data == 'else_statement'
                assert isinstance(item.children[0], PygenIntermediary)
                assert isinstance(item.children[0].inline, Block)
                if_block.add_else(item.children[0].inline)
        return PygenIntermediary(if_block)

    @staticmethod
    def while_statement(
        items: List[Tree | PygenIntermediary],
    ) -> PygenIntermediary:
        assert isinstance(items[0], PygenIntermediary)
        condition = items[0].finalize()
        assert isinstance(items[1], PygenIntermediary)
        block = items[1].inline
        assert isinstance(block, Block)
        return PygenIntermediary(block.make_while(condition))

    # Collections
    string_literal = combine_with_function(
        'make_string', map_items=lambda item: repr(item.value)
    )
    list = combine_with_function('make_list')
    range = combine_with_function('make_range')
    concatenate = combine_with_method_left('concatenate')
    select_element = combine_with_method_left('select_element')

    @staticmethod
    def select_slice(
        items: List[Tree | PygenIntermediary],
    ) -> PygenIntermediary:
        start = None
        end = None
        jump = None
        for item in items[1:]:
            assert isinstance(item, Tree)
            if not item.children:
                continue
            assert isinstance(item.children[0], PygenIntermediary)
            if item.data == 'slice_start':
                start = item.children[0].finalize()
            elif item.data == 'slice_end':
                end = item.children[0].finalize()
            elif item.data == 'slice_jump':
                jump = item.children[0].finalize()
            else:
                raise ValueError(f'select_slize has unexpected child {item}')
        assert isinstance(items[0], PygenIntermediary)
        lhs = items[0].finalize()
        return PygenIntermediary(f'{lhs}.select_slice({start},{end},{jump})')

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

    # Functions

    @staticmethod
    def define_function(
        items: List[Token | Tree | PygenIntermediary],
    ) -> PygenIntermediary:
        (name, param_list, block) = items
        assert isinstance(name, Token)
        assert isinstance(param_list, Tree)
        params = []
        for param in param_list.children:
            assert isinstance(param, Token)
            params.append(param.value)
        assert isinstance(block, PygenIntermediary)
        assert isinstance(block.inline, Block)
        PygenIntermediary.add_header(
            block.inline.make_function(name.value, params)
        )
        arg_list = ','.join(
            f'_m.get_object_by_name({repr(param)})' for param in params
        )
        backing_func = f'___{name}_backing_function'
        lambda_expr = (
            f'{PythonGenerator.backend_library}'
            f'.make_lambda({PythonGenerator.memory_instance},{repr(params)},'
            f'lambda: _m.get_object_by_name({repr(backing_func)})({arg_list}))'
        )
        return PygenIntermediary(
            f'{PythonGenerator.memory_instance}'
            f'.new({lambda_expr}, name={repr(name.value)}, const=True)'
        )

    @staticmethod
    def lambda_func(
        items: List[Tree | Token | PygenIntermediary],
    ) -> PygenIntermediary:
        (lhs, rhs) = items
        if isinstance(lhs, Tree):
            assert lhs.data == 'param_list'
            params = []
            for param in lhs.children:
                assert isinstance(param, Token)
                params.append(param.value)
        else:
            assert isinstance(lhs, Token) and lhs.type == 'NAME'
            params = [lhs.value]

        if isinstance(rhs, Block):
            # lambdas returning blocks need to be handled with temporary
            # function definitions, or we could do something weird perhaps like
            # put each into a list and discard the output of that list.
            raise FeatureUnimplemented('Block lambdas are not yet implemented')

        assert not isinstance(rhs, Tree)
        rhs_pygen = PythonGenerator.__resolve_placeholders(rhs)

        return PygenIntermediary(
            f'{PythonGenerator.backend_library}'
            f'.make_lambda({PythonGenerator.memory_instance},{repr(params)},'
            f'lambda: {rhs_pygen})'
        )

    poisonous_lambda_func = lambda_func

    @staticmethod
    def function_call(
        items: List[PygenIntermediary | Tree],
    ) -> PygenIntermediary:
        (func, arg_list) = items
        assert isinstance(func, PygenIntermediary)
        assert isinstance(arg_list, Tree)
        arg_list_finalized: List[str] = []
        for arg in arg_list.children:
            assert isinstance(arg, PygenIntermediary)
            arg_list_finalized.append(arg.finalize())
        arg_list_inner = ','.join(arg_list_finalized)
        return PygenIntermediary(f'{func.finalize()}.call([{arg_list_inner}])')

    @staticmethod
    def return_statement(items: List[PygenIntermediary]) -> PygenIntermediary:
        assert len(items) == 1
        return PygenIntermediary(
            Block(
                [
                    f'_m.push_stack_register({items[0].finalize()})',
                    '_m.pop_scope()',
                    'return _m.pop_stack_register()',
                ]
            )
        )

    # Memory
    @staticmethod
    def declare_untyped_variable(
        items: List[Token | PygenIntermediary],
    ) -> PygenIntermediary:
        (name, value) = items
        assert isinstance(name, Token)
        name = name.value
        assert isinstance(value, PygenIntermediary)
        return PygenIntermediary(
            f'{PythonGenerator.memory_instance}'
            f'.new({value.finalize()}, name={repr(name)})'
        )

    @staticmethod
    def declare_untyped_constant(
        items: List[Token | PygenIntermediary],
    ) -> PygenIntermediary:
        (name, value) = items
        assert isinstance(name, Token)
        assert isinstance(value, PygenIntermediary)
        return PygenIntermediary(
            f'{PythonGenerator.memory_instance}'
            f'.new({value.finalize()}, name={repr(name.value)}, const=True)'
        )

    @staticmethod
    def reassign(items: List[Token | PygenIntermediary]) -> PygenIntermediary:
        (lhs, rhs) = items
        assert isinstance(lhs, PygenIntermediary)
        assert isinstance(lhs.inline, Name)
        if lhs.inline.namespace:
            raise FeatureUnimplemented('Namespaces are not yet supported')
        assert isinstance(rhs, PygenIntermediary)
        return PygenIntermediary(
            f'{PythonGenerator.memory_instance}'
            f'.update_var({repr(lhs.inline.name)}, {rhs.finalize()})'
        )

    @staticmethod
    def identifier(items: List[Token]) -> PygenIntermediary:
        item_strings = [item.value for item in items]
        if len(items) > 1:
            return PygenIntermediary(
                Name(item_strings[0], namespace=item_strings[1:])
            )
        return PygenIntermediary(Name(item_strings[0]))

    # External Commands
    exec = combine_with_function('make_external_command', quote_args=True)
    pipeline = combine_with_function('make_pipeline')

    say = combine_with_function('say')
    assertion = combine_with_function('assertion')

    @staticmethod
    def unit_literal(
        items: List[Tree | PygenIntermediary | int | float],
    ) -> PygenIntermediary:
        (unit_type_tree, unit_tree, quantity) = items
        assert isinstance(unit_type_tree, Tree)
        unit_type = unit_type_tree.children[0]
        assert isinstance(unit_tree, Tree)
        unit = unit_tree.children[0]
        assert isinstance(quantity, int | float)
        return PygenIntermediary(
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
        'arg_list',
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
    def __resolve_placeholders(
        result: PygenIntermediary | str | Name | Block,
    ) -> str:
        return transform_pygen_result(result)


def transform_pygen_result(
    intermediate: PygenIntermediary | str | Name | Block,
) -> str:
    if isinstance(intermediate, PygenIntermediary):
        return intermediate.finalize()
    if isinstance(intermediate, Name):
        return (
            f'{PythonGenerator.memory_instance}'
            f'.get_object_by_name({repr(intermediate.name)})'
        )
    if isinstance(intermediate, Block):
        return intermediate.join()
    return intermediate


def get_required_functions() -> List[Block]:
    return PygenIntermediary.pop_headers()
