from typing import Dict

from .parser import *


"""
INSTRUCTIONS: To add new test cases:
  1) Add them to the new_test_cases variable
      example: `new_test_cases: Dict[str,str] = {"piping": "a | b | c"}`
  2) Run `./add_testcases.py` which will add tests at the bottom of this file
  3) Manually verify the generated code and AST for correctness
  4) Restore `new_test_cases: Dict[str,str] = {}`
  5) Push to github!
"""


# Maps new test cases from test-name to test-code
new_test_cases: Dict[str, str] = {}


# Prevents accidentally committing data in new_test_cases
def test_no_new_test_cases():
    assert len(new_test_cases) == 0


parser = get_parser(lowering=False)


def get_ast(src) -> str:
    return parser.parse(src).pretty().strip()


def test_pipe2():
    src = 'a | b'
    expected_ast = 'pipeline' '\n  exec\ta' '\n  exec\tb'
    assert get_ast(src) == expected_ast


def test_pipe3():
    src = 'a | b | c'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  exec\tb'
        '\n  exec\tc'
    )
    assert get_ast(src) == expected_ast


def test_implicit_execution():
    src = 'foo -ef "bf c" | wow'
    expected_ast = (
        'pipeline'
        '\n  exec'
        '\n    foo'
        '\n    -ef'
        '\n    bf c'
        '\n  exec\twow'
    )
    assert get_ast(src) == expected_ast


def test_explicit_execution():
    src = '`foo -ef bf c "d e"` | `wow`'
    expected_ast = (
        'pipeline'
        '\n  exec'
        '\n    foo'
        '\n    -ef'
        '\n    bf'
        '\n    c'
        '\n    d e'
        '\n  exec\twow'
    )
    assert get_ast(src) == expected_ast


def test_do_block():
    src = 'do {}'
    expected_ast = (
        'do_block'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_comparison():
    src = '1 < 2 <= 3 == 3 != 4 >= 4 > 0'
    expected_ast = (
        'comparison_chain'
        '\n  integer_literal\t1'
        '\n  less_than'
        '\n  integer_literal\t2'
        '\n  less_than_or_equal_to'
        '\n  integer_literal\t3'
        '\n  equal_to'
        '\n  integer_literal\t3'
        '\n  not_equal_to'
        '\n  integer_literal\t4'
        '\n  greater_than_or_equal_to'
        '\n  integer_literal\t4'
        '\n  greater_than'
        '\n  integer_literal\t0'
    )
    assert get_ast(src) == expected_ast


def test_boolean_algebra():
    src = 'not true or false and true or false xor true'
    expected_ast = (
        'xor_expr'
        '\n  or_expr'
        '\n    or_expr'
        '\n      unary_not'
        '\n        boolean_literal\ttrue'
        '\n      and_expr'
        '\n        boolean_literal\tfalse'
        '\n        boolean_literal\ttrue'
        '\n    boolean_literal\tfalse'
        '\n  boolean_literal\ttrue'
    )
    assert get_ast(src) == expected_ast


def test_math_in_block():
    src = 'do { 1 ** -3 + 4 * 5 - 6 // 7 / 8 % 9 }'
    expected_ast = (
        'do_block'
        '\n  block'
        '\n    subtraction'
        '\n      addition'
        '\n        raise_power'
        '\n          integer_literal\t1'
        '\n          unary_negate'
        '\n            integer_literal\t3'
        '\n        multiply'
        '\n          integer_literal\t4'
        '\n          integer_literal\t5'
        '\n      modulus'
        '\n        divide'
        '\n          int_divide'
        '\n            integer_literal\t6'
        '\n            integer_literal\t7'
        '\n          integer_literal\t8'
        '\n        integer_literal\t9'
    )
    assert get_ast(src) == expected_ast


def test_math_top_level():
    src = '1 ** 3 + 4 * 5 - 6 // 7 / 8 % 9 + -1'
    expected_ast = (
        'addition'
        '\n  subtraction'
        '\n    addition'
        '\n      raise_power'
        '\n        integer_literal\t1'
        '\n        integer_literal\t3'
        '\n      multiply'
        '\n        integer_literal\t4'
        '\n        integer_literal\t5'
        '\n    modulus'
        '\n      divide'
        '\n        int_divide'
        '\n          integer_literal\t6'
        '\n          integer_literal\t7'
        '\n        integer_literal\t8'
        '\n      integer_literal\t9'
        '\n  unary_negate'
        '\n    integer_literal\t1'
    )
    assert get_ast(src) == expected_ast


def test_identifier_explicit_1():
    src = '@foo'
    expected_ast = (
        'identifier\tfoo'
    )
    assert get_ast(src) == expected_ast


def test_identifier_explicit_2():
    src = '@foo::bar::a'
    expected_ast = (
        'identifier'
        '\n  foo'
        '\n  bar'
        '\n  a'
    )
    assert get_ast(src) == expected_ast


def test_identifier_explicit_3():
    src = '@foo::bar::a.b.c.d'
    expected_ast = (
        'select_field'
        '\n  select_field'
        '\n    select_field'
        '\n      identifier'
        '\n        foo'
        '\n        bar'
        '\n        a'
        '\n      b'
        '\n    c'
        '\n  d'
    )
    assert get_ast(src) == expected_ast


def test_identifier_in_block_1():
    src = 'do { foo }'
    expected_ast = (
        'do_block'
        '\n  block'
        '\n    identifier\tfoo'
    )
    assert get_ast(src) == expected_ast


def test_identifier_in_block_2():
    src = 'do { foo::bar::a }'
    expected_ast = (
        'do_block'
        '\n  block'
        '\n    identifier'
        '\n      foo'
        '\n      bar'
        '\n      a'
    )
    assert get_ast(src) == expected_ast


def test_identifier_in_block_3():
    src = 'do { foo::bar::a.b.c.d }'
    expected_ast = (
        'do_block'
        '\n  block'
        '\n    select_field'
        '\n      select_field'
        '\n        select_field'
        '\n          identifier'
        '\n            foo'
        '\n            bar'
        '\n            a'
        '\n          b'
        '\n        c'
        '\n      d'
    )
    assert get_ast(src) == expected_ast


def test_curry():
    src = 'a $ @b + 1 $ c'
    expected_ast = (
        'curried_func'
        '\n  curried_func'
        '\n    exec\ta'
        '\n    addition'
        '\n      identifier\tb'
        '\n      integer_literal\t1'
        '\n  exec\tc'
    )
    assert get_ast(src) == expected_ast


def test_function():
    src = 'fn foo(){\n\ta := b\n\tret 1\n}'
    expected_ast = (
        'define_function'
        '\n  foo'
        '\n  param_list'
        '\n  block'
        '\n    declare_untyped_variable'
        '\n      a'
        '\n      identifier\tb'
        '\n    return_expr'
        '\n      integer_literal\t1'
    )
    assert get_ast(src) == expected_ast


def test_function_params():
    src = 'fn foo(a, b: int, c:int=4){\n\tr := a+b+c\n\tret r\n}'
    expected_ast = (
        'define_function'
        '\n  foo'
        '\n  param_list'
        '\n    a'
        '\n    param'
        '\n      b'
        '\n      param_type'
        '\n        identifier\tint'
        '\n    param'
        '\n      c'
        '\n      param_type'
        '\n        identifier\tint'
        '\n      param_default'
        '\n        integer_literal\t4'
        '\n  block'
        '\n    declare_untyped_variable'
        '\n      r'
        '\n      identifier\ta+b+c'
        '\n    return_expr'
        '\n      identifier\tr'
    )
    assert get_ast(src) == expected_ast


def test_function_empty():
    src = 'fn foo(){}'
    expected_ast = (
        'define_function'
        '\n  foo'
        '\n  param_list'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_declare():
    src = 'a := 1'
    expected_ast = (
        'declare_untyped_variable'
        '\n  a'
        '\n  integer_literal\t1'
    )
    assert get_ast(src) == expected_ast


def test_declare_typed():
    src = 'a : int = 1'
    expected_ast = (
        'declare_typed_variable'
        '\n  a'
        '\n  identifier\tint'
        '\n  integer_literal\t1'
    )
    assert get_ast(src) == expected_ast


def test_declare_generic_typed():
    src = 'a : t[g] = [1]'
    expected_ast = (
        'declare_typed_variable'
        '\n  a'
        '\n  type'
        '\n    identifier\tt'
        '\n    type_generic'
        '\n      identifier\tg'
        '\n  list'
        '\n    integer_literal\t1'
    )
    assert get_ast(src) == expected_ast


def test_assignment():
    src = 'a = @b'
    expected_ast = (
        'reassign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_list():
    src = '[1,2,3+3,4,5]'
    expected_ast = (
        'list'
        '\n  integer_literal\t1'
        '\n  integer_literal\t2'
        '\n  addition'
        '\n    integer_literal\t3'
        '\n    integer_literal\t3'
        '\n  integer_literal\t4'
        '\n  integer_literal\t5'
    )
    assert get_ast(src) == expected_ast


def test_range_square():
    src = '[i..j]'
    expected_ast = (
        'range'
        '\n  identifier\ti'
        '\n  identifier\tj'
    )
    assert get_ast(src) == expected_ast


def test_range_paren():
    src = '(i..j)'
    expected_ast = (
        'range'
        '\n  identifier\ti'
        '\n  identifier\tj'
    )
    assert get_ast(src) == expected_ast


def test_lambda():
    src = 'a | \\x -> y'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  lambda_func'
        '\n    x'
        '\n    exec\ty'
    )
    assert get_ast(src) == expected_ast


def test_lambda_block():
    src = 'a | \\x {a;b}'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  lambda_func'
        '\n    x'
        '\n    block'
        '\n      identifier\ta'
        '\n      identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_lambda_no_param():
    src = 'a | \\() -> x'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  lambda_func'
        '\n    param_list'
        '\n    exec\tx'
    )
    assert get_ast(src) == expected_ast


def test_lambda_3_params():
    src = 'a | \\(a, b:int, c:int=1) -> x'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  lambda_func'
        '\n    param_list'
        '\n      a'
        '\n      param'
        '\n        b'
        '\n        param_type'
        '\n          identifier\tint'
        '\n      param'
        '\n        c'
        '\n        param_type'
        '\n          identifier\tint'
        '\n        param_default'
        '\n          integer_literal\t1'
        '\n    exec\tx'
    )
    assert get_ast(src) == expected_ast


def test_ellipsis():
    src = 'a | \\x -> @x.b... | c'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  lambda_func'
        '\n    x'
        '\n    function_pointer'
        '\n      select_field'
        '\n        identifier\tx'
        '\n        b'
        '\n  exec\tc'
    )
    assert get_ast(src) == expected_ast


def test_loop():
    src = 'loop {x(); y()}'
    expected_ast = (
        'always_loop'
        '\n  block'
        '\n    function_call'
        '\n      identifier\tx'
        '\n      arg_list'
        '\n    function_call'
        '\n      identifier\ty'
        '\n      arg_list'
    )
    assert get_ast(src) == expected_ast


def test_loop_empty():
    src = 'loop {}'
    expected_ast = (
        'always_loop'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_loop_labeled():
    src = 'loop as x {y}'
    expected_ast = (
        'always_loop'
        '\n  label\tx'
        '\n  block'
        '\n    identifier\ty'
    )
    assert get_ast(src) == expected_ast


def test_while():
    src = 'while(a == b) {x(); y()}'
    expected_ast = (
        'while'
        '\n  comparison_chain'
        '\n    identifier\ta'
        '\n    equal_to'
        '\n    identifier\tb'
        '\n  block'
        '\n    function_call'
        '\n      identifier\tx'
        '\n      arg_list'
        '\n    function_call'
        '\n      identifier\ty'
        '\n      arg_list'
    )
    assert get_ast(src) == expected_ast


def test_while_empty():
    src = 'while(a == b) {}'
    expected_ast = (
        'while'
        '\n  comparison_chain'
        '\n    identifier\ta'
        '\n    equal_to'
        '\n    identifier\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_while_labeled():
    src = 'while(a == b) as x {y}'
    expected_ast = (
        'while'
        '\n  comparison_chain'
        '\n    identifier\ta'
        '\n    equal_to'
        '\n    identifier\tb'
        '\n  label\tx'
        '\n  block'
        '\n    identifier\ty'
    )
    assert get_ast(src) == expected_ast


def test_for():
    src = 'for i in l {x(); y()}'
    expected_ast = (
        'for'
        '\n  i'
        '\n  exec\tl'
        '\n  block'
        '\n    function_call'
        '\n      identifier\tx'
        '\n      arg_list'
        '\n    function_call'
        '\n      identifier\ty'
        '\n      arg_list'
    )
    assert get_ast(src) == expected_ast


def test_for_empty():
    src = 'for i in [1,2,3] {}'
    expected_ast = (
        'for'
        '\n  i'
        '\n  list'
        '\n    integer_literal\t1'
        '\n    integer_literal\t2'
        '\n    integer_literal\t3'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_for_labeled():
    src = 'for i in [0..1] as x {y}'
    expected_ast = (
        'for'
        '\n  i'
        '\n  range'
        '\n    integer_literal\t0'
        '\n    integer_literal\t1'
        '\n  label\tx'
        '\n  block'
        '\n    identifier\ty'
    )
    assert get_ast(src) == expected_ast


def test_parenthesis():
    src = '(((1 + 2)+((3))+4))'
    expected_ast = (
        'addition'
        '\n  addition'
        '\n    addition'
        '\n      integer_literal\t1'
        '\n      integer_literal\t2'
        '\n    integer_literal\t3'
        '\n  integer_literal\t4'
    )
    assert get_ast(src) == expected_ast


def test_methods():
    src = 'module_name::a.b(1)'
    expected_ast = (
        'function_call'
        '\n  select_field'
        '\n    identifier'
        '\n      module_name'
        '\n      a'
        '\n    b'
        '\n  arg_list'
        '\n    integer_literal\t1'
    )
    assert get_ast(src) == expected_ast


def test_import():
    src = 'import "a.egg"'
    expected_ast = (
        'import\ta.egg'
    )
    assert get_ast(src) == expected_ast


def test_class():
    src = 'class thing {a: b\n c; d\nfn my_method(){}}'
    expected_ast = (
        'define_class'
        '\n  thing'
        '\n  class_fields'
        '\n    class_field_typed'
        '\n      a'
        '\n      identifier\tb'
        '\n    class_field_untyped\tc'
        '\n    class_field_untyped\td'
        '\n  class_methods'
        '\n    define_function'
        '\n      my_method'
        '\n      param_list'
        '\n      block'
    )
    assert get_ast(src) == expected_ast


def test_class_extending():
    src = 'class Cow : Animal {}'
    expected_ast = (
        'define_derived_class'
        '\n  Cow'
        '\n  identifier\tAnimal'
        '\n  class_fields'
        '\n  class_methods'
    )
    assert get_ast(src) == expected_ast


def test_map():
    src = '{1: 10, "b": "b0", l: [1], m:{} }'
    expected_ast = (
        'map'
        '\n  map_entry'
        '\n    integer_literal\t1'
        '\n    integer_literal\t10'
        '\n  map_entry'
        '\n    string_literal\tb'
        '\n    string_literal\tb0'
        '\n  map_entry'
        '\n    identifier\tl'
        '\n    list'
        '\n      integer_literal\t1'
        '\n  map_entry'
        '\n    identifier\tm'
        '\n    map'
    )
    assert get_ast(src) == expected_ast


def test_map_empty():
    src = '{}'
    expected_ast = (
        'map'
    )
    assert get_ast(src) == expected_ast


def test_error_sequence():
    src = 'a && b && c || do {a; b; c}'
    expected_ast = (
        'logical_sequence'
        '\n  and_sequence'
        '\n    exec\ta'
        '\n    logical_sequence'
        '\n      and_sequence'
        '\n        exec\tb'
        '\n        logical_sequence'
        '\n          or_sequence'
        '\n            exec\tc'
        '\n            do_block'
        '\n              block'
        '\n                identifier\ta'
        '\n                identifier\tb'
        '\n                identifier\tc'
    )
    assert get_ast(src) == expected_ast


def test_try():
    src = 'try{`x`}'
    expected_ast = (
        'try_catch'
        '\n  try_catch_unbound'
        '\n    block'
        '\n      exec\tx'
    )
    assert get_ast(src) == expected_ast


def test_try_catch():
    src = 'try{`x`} catch {`y`}'
    expected_ast = (
        'try_catch'
        '\n  try_catch_unbound'
        '\n    block'
        '\n      exec\tx'
        '\n    block'
        '\n      exec\ty'
    )
    assert get_ast(src) == expected_ast


def test_try_catch_param():
    src = 'try{`x`} catch e {`y`}'
    expected_ast = (
        'try_catch'
        '\n  try_catch_bound'
        '\n    block'
        '\n      exec\tx'
        '\n    e'
        '\n    block'
        '\n      exec\ty'
    )
    assert get_ast(src) == expected_ast


def test_try_catch_param_typed():
    src = 'try{`x`} catch e: t {`y`}'
    expected_ast = (
        'try_catch'
        '\n  try_catch_bound'
        '\n    block'
        '\n      exec\tx'
        '\n    e'
        '\n    identifier\tt'
        '\n    block'
        '\n      exec\ty'
    )
    assert get_ast(src) == expected_ast


def test_asynch():
    src = '~(`foo`)'
    expected_ast = (
        'async_expr'
        '\n  exec\tfoo'
    )
    assert get_ast(src) == expected_ast


def test_asynch_block():
    src = '~ { `foo`; `bar` }'
    expected_ast = (
        'async_expr'
        '\n  block'
        '\n    exec\tfoo'
        '\n    exec\tbar'
    )
    assert get_ast(src) == expected_ast


def test_asynch_methods():
    src = '~(`foo`).x'
    expected_ast = (
        'select_field'
        '\n  async_expr'
        '\n    exec\tfoo'
        '\n  x'
    )
    assert get_ast(src) == expected_ast


def test_returned_obj_methods():
    src = '@a().x'
    expected_ast = (
        'select_field'
        '\n  function_call'
        '\n    identifier\ta'
        '\n    arg_list'
        '\n  x'
    )
    assert get_ast(src) == expected_ast


def test_concatenation():
    src = '@a ++ @b'
    expected_ast = (
        'concatenate'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_concatenation_executions():
    src = 'a ++ b'
    expected_ast = (
        'concatenate'
        '\n  exec\ta'
        '\n  exec\tb'
    )
    assert get_ast(src) == expected_ast


def test_select_element():
    src = '@a[i]'
    expected_ast = (
        'select_element'
        '\n  identifier\ta'
        '\n  identifier\ti'
    )
    assert get_ast(src) == expected_ast


def test_select_slice():
    src = '@a[1:2 by 3]'
    expected_ast = (
        'select_slice'
        '\n  identifier\ta'
        '\n  slice_start'
        '\n    integer_literal\t1'
        '\n  slice_end'
        '\n    integer_literal\t2'
        '\n  slice_jump'
        '\n    integer_literal\t3'
    )
    assert get_ast(src) == expected_ast


def test_select_slice2():
    src = '@a[1:2]'
    expected_ast = (
        'select_slice'
        '\n  identifier\ta'
        '\n  slice_start'
        '\n    integer_literal\t1'
        '\n  slice_end'
        '\n    integer_literal\t2'
        '\n  slice_jump'
    )
    assert get_ast(src) == expected_ast


def test_select_slice_rev():
    src = '@a[: by -1]'
    expected_ast = (
        'select_slice'
        '\n  identifier\ta'
        '\n  slice_start'
        '\n  slice_end'
        '\n  slice_jump'
        '\n    unary_negate'
        '\n      integer_literal\t1'
    )
    assert get_ast(src) == expected_ast


def test_select_slice_end_only():
    src = '@a[:1]'
    expected_ast = (
        'select_slice'
        '\n  identifier\ta'
        '\n  slice_start'
        '\n  slice_end'
        '\n    integer_literal\t1'
        '\n  slice_jump'
    )
    assert get_ast(src) == expected_ast


def test_select_slice_end_and_jump():
    src = '@a[:1 by 2]'
    expected_ast = (
        'select_slice'
        '\n  identifier\ta'
        '\n  slice_start'
        '\n  slice_end'
        '\n    integer_literal\t1'
        '\n  slice_jump'
        '\n    integer_literal\t2'
    )
    assert get_ast(src) == expected_ast


def test_with():
    src = 'with a.y() {}'
    expected_ast = (
        'with_block'
        '\n  function_call'
        '\n    select_field'
        '\n      identifier\ta'
        '\n      y'
        '\n    arg_list'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_with_as():
    src = 'with a.y() as x {}'
    expected_ast = (
        'with_block'
        '\n  function_call'
        '\n    select_field'
        '\n      identifier\ta'
        '\n      y'
        '\n    arg_list'
        '\n  x'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_explicit_pipeline():
    src = '`a | b | c`'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  exec\tb'
        '\n  exec\tc'
    )
    assert get_ast(src) == expected_ast


def test_list_comprehension():
    src = '[10**x for x in (0..10)]'
    expected_ast = (
        'list_comprehension'
        '\n  raise_power'
        '\n    integer_literal\t10'
        '\n    identifier\tx'
        '\n  x'
        '\n  range'
        '\n    integer_literal\t0'
        '\n    integer_literal\t10'
    )
    assert get_ast(src) == expected_ast


def test_map_comprehension():
    src = '{-x: 10**-x for x in (0..10)}'
    expected_ast = (
        'map_comprehension'
        '\n  unary_negate'
        '\n    identifier\tx'
        '\n  raise_power'
        '\n    integer_literal\t10'
        '\n    unary_negate'
        '\n      identifier\tx'
        '\n  x'
        '\n  range'
        '\n    integer_literal\t0'
        '\n    integer_literal\t10'
    )
    assert get_ast(src) == expected_ast


def test_fn_normal_multi_and_kw_param():
    src = 'fn foo (a, b, *c, **d){}'
    expected_ast = (
        'define_function'
        '\n  foo'
        '\n  param_list'
        '\n    a'
        '\n    b'
        '\n    star_param\tc'
        '\n    kw_param\td'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_fn_multi_and_kw_param():
    src = 'fn foo (*a, **b){}'
    expected_ast = (
        'define_function'
        '\n  foo'
        '\n  param_list'
        '\n    star_param\ta'
        '\n    kw_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_fn_multi_param():
    src = 'fn foo (a, *b){}'
    expected_ast = (
        'define_function'
        '\n  foo'
        '\n  param_list'
        '\n    a'
        '\n    star_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_fn_multi_param_only():
    src = 'fn foo (*b){}'
    expected_ast = (
        'define_function'
        '\n  foo'
        '\n  param_list'
        '\n    star_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_fn_kw_param():
    src = 'fn foo (a, **b){}'
    expected_ast = (
        'define_function'
        '\n  foo'
        '\n  param_list'
        '\n    a'
        '\n    kw_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_fn_kw_param_only():
    src = 'fn foo (**b){}'
    expected_ast = (
        'define_function'
        '\n  foo'
        '\n  param_list'
        '\n    kw_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_lambda_normal_multi_and_kw_param():
    src = '\\(a, b, *c, **d){}'
    expected_ast = (
        'lambda_func'
        '\n  param_list'
        '\n    a'
        '\n    b'
        '\n    star_param\tc'
        '\n    kw_param\td'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_lambda_multi_and_kw_param():
    src = '\\(*a, **b){}'
    expected_ast = (
        'lambda_func'
        '\n  param_list'
        '\n    star_param\ta'
        '\n    kw_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_lambda_multi_param():
    src = '\\(a, *b){}'
    expected_ast = (
        'lambda_func'
        '\n  param_list'
        '\n    a'
        '\n    star_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_lambda_multi_param_only():
    src = '\\(*b){}'
    expected_ast = (
        'lambda_func'
        '\n  param_list'
        '\n    star_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_lambda_multi_param_only_no_paren():
    src = '\\*b{}'
    expected_ast = (
        'lambda_func'
        '\n  star_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_lambda_kw_param():
    src = '\\(a, **b){}'
    expected_ast = (
        'lambda_func'
        '\n  param_list'
        '\n    a'
        '\n    kw_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_lambda_kw_param_only():
    src = '\\(**b){}'
    expected_ast = (
        'lambda_func'
        '\n  param_list'
        '\n    kw_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_lambda_kw_param_only_no_paren():
    src = '\\**b{}'
    expected_ast = (
        'lambda_func'
        '\n  kw_param\tb'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_kw_args():
    src = 'foo(a, b=c, d=e)'
    expected_ast = (
        'function_call'
        '\n  identifier\tfoo'
        '\n  arg_list'
        '\n    identifier\ta'
        '\n    kwarg'
        '\n      b'
        '\n      identifier\tc'
        '\n    kwarg'
        '\n      d'
        '\n      identifier\te'
    )
    assert get_ast(src) == expected_ast


def test_implicit_lambda():
    src = '_'
    expected_ast = (
        'implicit_lambda_param'
    )
    assert get_ast(src) == expected_ast


def test_implicit_lambda_method():
    src = '_.hello() + _.world()'
    expected_ast = (
        'addition'
        '\n  function_call'
        '\n    select_field'
        '\n      implicit_lambda_param'
        '\n      hello'
        '\n    arg_list'
        '\n  function_call'
        '\n    select_field'
        '\n      implicit_lambda_param'
        '\n      world'
        '\n    arg_list'
    )
    assert get_ast(src) == expected_ast


def test_implicit_lambda_piped():
    src = 'a | _.sort() | b'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  function_call'
        '\n    select_field'
        '\n      implicit_lambda_param'
        '\n      sort'
        '\n    arg_list'
        '\n  exec\tb'
    )
    assert get_ast(src) == expected_ast


def test_selection_lambda_shorthand():
    src = 'get_files | ...date'
    expected_ast = (
        'pipeline'
        '\n  exec\tget_files'
        '\n  selection_lambda_shorthand\tdate'
    )
    assert get_ast(src) == expected_ast


def test_pipeline_to_implicit_lambda():
    src = 'a | _ | c'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  implicit_lambda_param'
        '\n  exec\tc'
    )
    assert get_ast(src) == expected_ast


def test_pipeline_to_implicit_lambda2():
    src = 'a | _ | _ + _ | c'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  implicit_lambda_param'
        '\n  addition'
        '\n    implicit_lambda_param'
        '\n    implicit_lambda_param'
        '\n  exec\tc'
    )
    assert get_ast(src) == expected_ast


def test_if_no_paren():
    src = 'if 1 == 2 {}'
    expected_ast = (
        'if'
        '\n  comparison_chain'
        '\n    integer_literal\t1'
        '\n    equal_to'
        '\n    integer_literal\t2'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_unit_b():
    src = '45b + 4.5b'
    expected_ast = (
        'addition'
        '\n  unit_integer_literal\t45:b'
        '\n  unit_float_literal\t4.5:b'
    )
    assert get_ast(src) == expected_ast


def test_unit_kb():
    src = '45kb + 4.5kb'
    expected_ast = (
        'addition'
        '\n  unit_integer_literal\t45:kb'
        '\n  unit_float_literal\t4.5:kb'
    )
    assert get_ast(src) == expected_ast


def test_unit_mb():
    src = '45mb + 4.5mb'
    expected_ast = (
        'addition'
        '\n  unit_integer_literal\t45:mb'
        '\n  unit_float_literal\t4.5:mb'
    )
    assert get_ast(src) == expected_ast


def test_unit_gb():
    src = '45gb + 4.5gb'
    expected_ast = (
        'addition'
        '\n  unit_integer_literal\t45:gb'
        '\n  unit_float_literal\t4.5:gb'
    )
    assert get_ast(src) == expected_ast


def test_unit_tb():
    src = '45tb + 4.5tb'
    expected_ast = (
        'addition'
        '\n  unit_integer_literal\t45:tb'
        '\n  unit_float_literal\t4.5:tb'
    )
    assert get_ast(src) == expected_ast


def test_unit_pb():
    src = '45pb + 4.5pb'
    expected_ast = (
        'addition'
        '\n  unit_integer_literal\t45:pb'
        '\n  unit_float_literal\t4.5:pb'
    )
    assert get_ast(src) == expected_ast


def test_unit_kib():
    src = '45kib + 4.5kib'
    expected_ast = (
        'addition'
        '\n  unit_integer_literal\t45:kib'
        '\n  unit_float_literal\t4.5:kib'
    )
    assert get_ast(src) == expected_ast


def test_unit_mib():
    src = '45mib + 4.5mib'
    expected_ast = (
        'addition'
        '\n  unit_integer_literal\t45:mib'
        '\n  unit_float_literal\t4.5:mib'
    )
    assert get_ast(src) == expected_ast


def test_unit_gib():
    src = '45gib + 4.5gib'
    expected_ast = (
        'addition'
        '\n  unit_integer_literal\t45:gib'
        '\n  unit_float_literal\t4.5:gib'
    )
    assert get_ast(src) == expected_ast


def test_unit_tib():
    src = '45tib + 4.5tib'
    expected_ast = (
        'addition'
        '\n  unit_integer_literal\t45:tib'
        '\n  unit_float_literal\t4.5:tib'
    )
    assert get_ast(src) == expected_ast


def test_unit_pib():
    src = '45pib + 4.5pib'
    expected_ast = (
        'addition'
        '\n  unit_integer_literal\t45:pib'
        '\n  unit_float_literal\t4.5:pib'
    )
    assert get_ast(src) == expected_ast


def test_plus_assignment():
    src = '@a += @b'
    expected_ast = (
        'plus_assign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_minus_assignment():
    src = '@a -= @b'
    expected_ast = (
        'minus_assign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_times_assignment():
    src = '@a *= @b'
    expected_ast = (
        'times_assign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_divide_assignment():
    src = '@a /= @b'
    expected_ast = (
        'divide_assign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_mod_assignment():
    src = '@a %= @b'
    expected_ast = (
        'mod_assign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_power_assignment():
    src = '@a **= @b'
    expected_ast = (
        'power_assign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_int_div_assignment():
    src = '@a //= @b'
    expected_ast = (
        'int_div_assign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_concat_assignment():
    src = '@a ++= @b'
    expected_ast = (
        'concat_assign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_seq_and_assignment():
    src = '@a &&= @b'
    expected_ast = (
        'seq_and_assign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_seq_or_assignment():
    src = '@a ||= @b'
    expected_ast = (
        'seq_or_assign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_pipe_assignment():
    src = '@a |= @b'
    expected_ast = (
        'pipe_assign'
        '\n  identifier\ta'
        '\n  identifier\tb'
    )
    assert get_ast(src) == expected_ast


def test_assertion():
    src = 'assert 1 == one()'
    expected_ast = (
        'assertion'
        '\n  comparison_chain'
        '\n    integer_literal\t1'
        '\n    equal_to'
        '\n    function_call'
        '\n      identifier\tone'
        '\n      arg_list'
    )
    assert get_ast(src) == expected_ast


def test_const_declare():
    src = 'const a := 1'
    expected_ast = (
        'declare_untyped_constant'
        '\n  a'
        '\n  integer_literal\t1'
    )
    assert get_ast(src) == expected_ast
