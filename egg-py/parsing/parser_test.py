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


def get_ast(src) -> str:
    return get_parser().parse(src).pretty().strip()


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
    src = 'foo -ef bf c | wow'
    expected_ast = (
        'pipeline'
        '\n  exec'
        '\n    foo'
        '\n    -ef'
        '\n    bf'
        '\n    c'
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
        '\n    "d'
        '\n    e"'
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
        '\n  literal\t1'
        '\n  less_than'
        '\n  literal\t2'
        '\n  less_than_or_equal_to'
        '\n  literal\t3'
        '\n  equal_to'
        '\n  literal\t3'
        '\n  not_equal_to'
        '\n  literal\t4'
        '\n  greater_than_or_equal_to'
        '\n  literal\t4'
        '\n  greater_than'
        '\n  literal\t0'
    )
    assert get_ast(src) == expected_ast


def test_boolean_algebra():
    src = 'not true or false and true or false xor true'
    expected_ast = (
        'xor_expr'
        '\n  or_expr'
        '\n    or_expr'
        '\n      unary_not'
        '\n        literal\ttrue'
        '\n      and_expr'
        '\n        literal\tfalse'
        '\n        literal\ttrue'
        '\n    literal\tfalse'
        '\n  literal\ttrue'
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
        '\n          literal\t1'
        '\n          unary_negate'
        '\n            literal\t3'
        '\n        multiply'
        '\n          literal\t4'
        '\n          literal\t5'
        '\n      modulus'
        '\n        divide'
        '\n          int_divide'
        '\n            literal\t6'
        '\n            literal\t7'
        '\n          literal\t8'
        '\n        literal\t9'
    )
    assert get_ast(src) == expected_ast


def test_math_top_level():
    src = '1 (**) 3 (+) 4 (*) 5 (-) 6 (//) 7 (/) 8 (%) 9 (+) -1'
    expected_ast = (
        'addition'
        '\n  subtraction'
        '\n    addition'
        '\n      raise_power'
        '\n        literal\t1'
        '\n        literal\t3'
        '\n      multiply'
        '\n        literal\t4'
        '\n        literal\t5'
        '\n    modulus'
        '\n      divide'
        '\n        int_divide'
        '\n          literal\t6'
        '\n          literal\t7'
        '\n        literal\t8'
        '\n      literal\t9'
        '\n  literal\t-1'
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
    src = 'a $ @b (+) 1 $ c'
    expected_ast = (
        'curried_func'
        '\n  curried_func'
        '\n    exec\ta'
        '\n    addition'
        '\n      identifier\tb'
        '\n      literal\t1'
        '\n  exec\tc'
    )
    assert get_ast(src) == expected_ast


def test_function():
    src = 'fn foo(){\n\ta := b\n\tret 1\n}'
    expected_ast = (
        'define_function'
        '\n  foo'
        '\n  func_arglist'
        '\n  block'
        '\n    declare_untyped_variable'
        '\n      a'
        '\n      identifier\tb'
        '\n    return_expr'
        '\n      literal\t1'
    )
    assert get_ast(src) == expected_ast


def test_function_args():
    src = 'fn foo(a, b: int, c:int=4){\n\tr := a+b+c\n\tret r\n}'
    expected_ast = (
        'define_function'
        '\n  foo'
        '\n  func_arglist'
        '\n    a'
        '\n    func_arg'
        '\n      b'
        '\n      arg_type'
        '\n        identifier\tint'
        '\n    func_arg'
        '\n      c'
        '\n      arg_type'
        '\n        identifier\tint'
        '\n      arg_default'
        '\n        literal\t4'
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
        '\n  func_arglist'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_declare():
    src = 'a := 1'
    expected_ast = (
        'declare_untyped_variable'
        '\n  a'
        '\n  literal\t1'
    )
    assert get_ast(src) == expected_ast


def test_declare_typed():
    src = 'a : int = 1'
    expected_ast = (
        'declare_typed_variable'
        '\n  a'
        '\n  identifier\tint'
        '\n  literal\t1'
    )
    assert get_ast(src) == expected_ast


def test_declare_generic_typed():
    src = 'a : t<@g> = [1]'
    expected_ast = (
        'declare_typed_variable'
        '\n  a'
        '\n  type'
        '\n    identifier\tt'
        '\n    type_generic'
        '\n      identifier\tg'
        '\n  list'
        '\n    literal\t1'
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
        '\n  literal\t1'
        '\n  literal\t2'
        '\n  addition'
        '\n    literal\t3'
        '\n    literal\t3'
        '\n  literal\t4'
        '\n  literal\t5'
    )
    assert get_ast(src) == expected_ast


def test_list_access():
    src = '@a[i] (+) @b[j]'
    expected_ast = (
        'addition'
        '\n  select'
        '\n    identifier\ta'
        '\n    identifier\ti'
        '\n  select'
        '\n    identifier\tb'
        '\n    identifier\tj'
    )
    assert get_ast(src) == expected_ast


def test_list_slice():
    src = '@a[i:j]'
    expected_ast = (
        'select'
        '\n  identifier\ta'
        '\n  identifier\ti'
        '\n  identifier\tj'
    )
    assert get_ast(src) == expected_ast


def test_list_slice3():
    src = '@a[i:j:k]'
    expected_ast = (
        'select'
        '\n  identifier\ta'
        '\n  identifier\ti'
        '\n  identifier\tj'
        '\n  identifier\tk'
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


def test_lambda_no_arg():
    src = 'a | \\() -> x'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  lambda_func'
        '\n    func_arglist'
        '\n    exec\tx'
    )
    assert get_ast(src) == expected_ast


def test_lambda_3_args():
    src = 'a | \\(a, b:int, c:int=1) -> x'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  lambda_func'
        '\n    func_arglist'
        '\n      a'
        '\n      func_arg'
        '\n        b'
        '\n        arg_type'
        '\n          identifier\tint'
        '\n      func_arg'
        '\n        c'
        '\n        arg_type'
        '\n          identifier\tint'
        '\n        arg_default'
        '\n          literal\t1'
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
        '\n      function_call_args'
        '\n    function_call'
        '\n      identifier\ty'
        '\n      function_call_args'
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
        '\n      function_call_args'
        '\n    function_call'
        '\n      identifier\ty'
        '\n      function_call_args'
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
        '\n      function_call_args'
        '\n    function_call'
        '\n      identifier\ty'
        '\n      function_call_args'
    )
    assert get_ast(src) == expected_ast


def test_for_empty():
    src = 'for i in [1,2,3] {}'
    expected_ast = (
        'for'
        '\n  i'
        '\n  list'
        '\n    literal\t1'
        '\n    literal\t2'
        '\n    literal\t3'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_for_labeled():
    src = 'for i in [0..1] as x {y}'
    expected_ast = (
        'for'
        '\n  i'
        '\n  range'
        '\n    literal\t0'
        '\n    literal\t1'
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
        '\n      literal\t1'
        '\n      literal\t2'
        '\n    literal\t3'
        '\n  literal\t4'
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
        '\n  function_call_args'
        '\n    literal\t1'
    )
    assert get_ast(src) == expected_ast


def test_import():
    src = 'import "a.egg"'
    expected_ast = (
        'import\ta.egg'
    )
    assert get_ast(src) == expected_ast


def test_class():
    src = 'class thing {a: b, c, d\nfn my_method(){}}'
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
        '\n      func_arglist'
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
        '\n    literal\t1'
        '\n    literal\t10'
        '\n  map_entry'
        '\n    literal\tb'
        '\n    literal\tb0'
        '\n  map_entry'
        '\n    identifier\tl'
        '\n    list'
        '\n      literal\t1'
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


def test_try_catch_arg():
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


def test_try_catch_arg_typed():
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
        '\n    function_call_args'
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
