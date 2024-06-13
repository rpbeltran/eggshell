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
    return pygen.transform(ast)


def test_add():
    src = '1 + 2'
    expected_gen_code = 'egg_lib.make_integer(1).add(egg_lib.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_subtract():
    src = '1 - 2'
    expected_gen_code = 'egg_lib.make_integer(1).subtract(egg_lib.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_multiply():
    src = '1 * 2'
    expected_gen_code = 'egg_lib.make_integer(1).multiply(egg_lib.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_divide():
    src = '1 / 2'
    expected_gen_code = 'egg_lib.make_integer(1).divide(egg_lib.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_int_divide():
    src = '1 // 2'
    expected_gen_code = 'egg_lib.make_integer(1).int_divide(egg_lib.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_modulus():
    src = '1 % 2'
    expected_gen_code = 'egg_lib.make_integer(1).modulus(egg_lib.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_raise_power():
    src = '1 ** 2'
    expected_gen_code = 'egg_lib.make_integer(1).raise_power(egg_lib.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_external_command():
    src = 'foo -o bar'
    expected_gen_code = "egg_lib.make_external_command('foo','-o','bar')"
    assert get_gen_code(src) == expected_gen_code


def test_explicit_exec():
    src = '`"foo bar" -o hello`'
    expected_gen_code = "egg_lib.make_external_command('foo bar','-o','hello')"
    assert get_gen_code(src) == expected_gen_code


def test_pipeline():
    src = 'a b | c d'
    expected_gen_code = "egg_lib.make_pipeline(egg_lib.make_external_command('a','b'),egg_lib.make_external_command('c','d'))"
    assert get_gen_code(src) == expected_gen_code


def test_pipeline_data():
    src = '1 | a'
    expected_gen_code = "egg_lib.make_pipeline(egg_lib.make_integer(1),egg_lib.make_external_command('a'))"
    assert get_gen_code(src) == expected_gen_code


def test_comparison_chain():
    src = '1 < 2 <= 3 == 3 != 20 >= 18 > 1'
    expected_gen_code = (
        'egg_lib.do_comparisons(egg_lib.make_integer(1),egg_lib.ComparisonType.LESS,'
        'egg_lib.make_integer(2),egg_lib.ComparisonType.LTE,'
        'egg_lib.make_integer(3),egg_lib.ComparisonType.EQUAL,'
        'egg_lib.make_integer(3),egg_lib.ComparisonType.UNEQUAL,'
        'egg_lib.make_integer(20),egg_lib.ComparisonType.GTE,'
        'egg_lib.make_integer(18),egg_lib.ComparisonType.GREATER,egg_lib.make_integer(1))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_unit_values():
    src = '10gb'
    expected_gen_code = "egg_lib.UnitValue('size', 'gb', 10)"
    assert get_gen_code(src) == expected_gen_code


def test_floats_and_ints():
    src = '1 + 1.0 - 2 * 3.0'
    expected_gen_code = 'egg_lib.make_integer(1).add(egg_lib.make_float(1.0)).subtract(egg_lib.make_integer(2).multiply(egg_lib.make_float(3.0)))'
    assert get_gen_code(src) == expected_gen_code
