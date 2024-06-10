from typing import Dict

from parsing.parser import get_parser
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
    expected_gen_code = 'egg_lib.add(1,2)'
    assert get_gen_code(src) == expected_gen_code


def test_subtract():
    src = '1 - 2'
    expected_gen_code = 'egg_lib.subtract(1,2)'
    assert get_gen_code(src) == expected_gen_code


def test_multiply():
    src = '1 * 2'
    expected_gen_code = 'egg_lib.multiply(1,2)'
    assert get_gen_code(src) == expected_gen_code


def test_divide():
    src = '1 / 2'
    expected_gen_code = 'egg_lib.divide(1,2)'
    assert get_gen_code(src) == expected_gen_code


def test_int_divide():
    src = '1 // 2'
    expected_gen_code = 'egg_lib.int_divide(1,2)'
    assert get_gen_code(src) == expected_gen_code


def test_modulus():
    src = '1 % 2'
    expected_gen_code = 'egg_lib.modulus(1,2)'
    assert get_gen_code(src) == expected_gen_code


def test_raise_power():
    src = '1 ** 2'
    expected_gen_code = 'egg_lib.raise_power(1,2)'
    assert get_gen_code(src) == expected_gen_code
