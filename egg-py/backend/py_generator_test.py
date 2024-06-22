from typing import Dict

from frontend.parser import get_parser
from .py_generator import *

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


parser = get_parser()
pygen = PythonGenerator()


def get_gen_code(src):
    ast = parser.parse(src)
    return transform_pygen_result(pygen.transform(ast))


def test_add():
    src = '1 + 2'
    expected_gen_code = '_e.make_integer(1).add(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_subtract():
    src = '1 - 2'
    expected_gen_code = '_e.make_integer(1).subtract(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_multiply():
    src = '1 * 2'
    expected_gen_code = '_e.make_integer(1).multiply(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_divide():
    src = '1 / 2'
    expected_gen_code = '_e.make_integer(1).divide(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_int_divide():
    src = '1 // 2'
    expected_gen_code = '_e.make_integer(1).int_divide(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_modulus():
    src = '1 % 2'
    expected_gen_code = '_e.make_integer(1).modulus(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_raise_power():
    src = '1 ** 2'
    expected_gen_code = '_e.make_integer(1).raise_power(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_external_command():
    src = 'foo -o bar'
    expected_gen_code = "_e.make_external_command('foo','-o','bar')"
    assert get_gen_code(src) == expected_gen_code


def test_explicit_exec():
    src = '`"foo bar" -o hello`'
    expected_gen_code = "_e.make_external_command('foo bar','-o','hello')"
    assert get_gen_code(src) == expected_gen_code


def test_pipeline():
    src = 'a b | c d'
    expected_gen_code = (
        "_e.make_pipeline(_e.make_external_command('a','b')"
        ",_e.make_external_command('c','d'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_pipeline_data():
    src = '1 | a'
    expected_gen_code = (
        "_e.make_pipeline(_e.make_integer(1),_e.make_external_command('a'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_comparison_chain():
    src = '1 < 2 <= 3 == 3 != 20 >= 18 > 1'
    expected_gen_code = (
        '_e.do_comparisons(_e.make_integer(1),_e.ComparisonType.LESS,'
        '_e.make_integer(2),_e.ComparisonType.LTE,'
        '_e.make_integer(3),_e.ComparisonType.EQUAL,'
        '_e.make_integer(3),_e.ComparisonType.UNEQUAL,'
        '_e.make_integer(20),_e.ComparisonType.GTE,'
        '_e.make_integer(18),_e.ComparisonType.GREATER,_e.make_integer(1))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_unit_values():
    src = '10gb'
    expected_gen_code = "_e.make_unit_value('size', 'gb', 10)"
    assert get_gen_code(src) == expected_gen_code


def test_floats_and_ints():
    src = '1 + 1.0 - 2 * 3.0'
    expected_gen_code = (
        '_e.make_integer(1).add(_e.make_float(1.0))'
        '.subtract(_e.make_integer(2).multiply(_e.make_float(3.0)))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_and():
    src = 'true and false and true'
    expected_gen_code = (
        '_e.make_boolean(True).logical_and(_e.make_boolean(False))'
        '.logical_and(_e.make_boolean(True))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_or():
    src = 'true or false or true'
    expected_gen_code = (
        '_e.make_boolean(True).logical_or(_e.make_boolean(False))'
        '.logical_or(_e.make_boolean(True))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_xor():
    src = 'true xor false xor true'
    expected_gen_code = (
        '_e.make_boolean(True).logical_xor(_e.make_boolean(False))'
        '.logical_xor(_e.make_boolean(True))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_assertions():
    src = 'assert true'
    expected_gen_code = '_e.assertion(_e.make_boolean(True))'
    assert get_gen_code(src) == expected_gen_code


def test_string():
    src = '"hello world"'
    expected_gen_code = "_e.make_string('hello world')"
    assert get_gen_code(src) == expected_gen_code


def test_concatenate():
    src = '"hello " ++ "world" ++ "!!!"'
    expected_gen_code = (
        "_e.make_string('hello ').concatenate(_e.make_string('world'))"
        ".concatenate(_e.make_string('!!!'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_unary_not():
    src = '! true'
    expected_gen_code = '_e.make_boolean(True).logical_not()'
    assert get_gen_code(src) == expected_gen_code


def test_unary_not2():
    src = 'not true'
    expected_gen_code = '_e.make_boolean(True).logical_not()'
    assert get_gen_code(src) == expected_gen_code


def test_unary_negate():
    src = '-(10)'
    expected_gen_code = '_e.make_integer(10).negate()'
    assert get_gen_code(src) == expected_gen_code


def test_make_list():
    src = '[1,`a`]'
    expected_gen_code = (
        "_e.make_list(_e.make_integer(1),_e.make_external_command('a'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_make_empty_list():
    src = '[]'
    expected_gen_code = '_e.make_list()'
    assert get_gen_code(src) == expected_gen_code


def test_make_list_one_elem():
    src = '[1]'
    expected_gen_code = '_e.make_list(_e.make_integer(1))'
    assert get_gen_code(src) == expected_gen_code


def test_select_element():
    src = '[1,2,3][1]'
    expected_gen_code = (
        '_e.make_list(_e.make_integer(1),_e.make_integer(2),_e.make_integer(3))'
        '.select_element(_e.make_integer(1))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_select_element_str():
    src = '"hello world"[1]'
    expected_gen_code = (
        "_e.make_string('hello world')"
        ".select_element(_e.make_integer(1))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_select_slice():
    src = '[1,2,3][1:3]'
    expected_gen_code = (
        '_e.make_list(_e.make_integer(1),_e.make_integer(2),_e.make_integer(3))'
        '.select_slice(_e.make_integer(1),_e.make_integer(3),None)'
    )
    assert get_gen_code(src) == expected_gen_code


def test_select_slice_str():
    src = '"hello world"[1:3]'
    expected_gen_code = (
        "_e.make_string('hello world')"
        ".select_slice(_e.make_integer(1),_e.make_integer(3),None)"
    )
    assert get_gen_code(src) == expected_gen_code


def test_select_slice_jump():
    src = '[1,2,3][1:2 by 3]'
    expected_gen_code =(
        '_e.make_list(_e.make_integer(1),_e.make_integer(2),_e.make_integer(3))'
        '.select_slice(_e.make_integer(1),_e.make_integer(2),_e.make_integer(3))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_select_slice_str_jump():
    src = '"hello world"[:3 by -1]'
    expected_gen_code = (
        "_e.make_string('hello world')"
        ".select_slice(None,_e.make_integer(3),_e.make_integer(1).negate())"
    )
    assert get_gen_code(src) == expected_gen_code


def test_ranges():
    src = '(5..15)'
    src_square = '[5..15]'
    expected_gen_code = '_e.make_range(_e.make_integer(5),_e.make_integer(15))'
    assert get_gen_code(src) == get_gen_code(src_square) == expected_gen_code


def test_declare_untyped_variable():
    src = 'a := 1'
    expected_gen_code = "_m.new(_e.make_integer(1), name='a')"
    assert get_gen_code(src) == expected_gen_code


def test_const_declare():
    src = 'const a := 1'
    expected_gen_code = "_m.new(_e.make_integer(1), name='a', const=True)"
    assert get_gen_code(src) == expected_gen_code


def test_identifier():
    src = '@foo'
    expected_gen_code = "_m.get_object_by_name('foo')"
    assert get_gen_code(src) == expected_gen_code
