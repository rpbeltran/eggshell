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

parser = get_parser()


def get_ast(src) -> str:
    return parser.parse(src).pretty().strip()


def test_always_loop_to_while():
    src = 'loop {}'
    expected_ast = (
        'while'
        '\n  True'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_integer_literal_to_int():
    src = '1 + 2'
    expected_ast = (
        'addition'
        '\n  1'
        '\n  2'
    )
    assert get_ast(src) == expected_ast


def test_float_literal_to_float():
    src = 'a := 3.14159'
    expected_ast = (
        'declare_untyped_variable'
        '\n  a'
        '\n  3.14159'
    )
    assert get_ast(src) == expected_ast


def test_boolean_literal_to():
    src = 'true == false'
    expected_ast = (
        'comparison_chain'
        '\n  True'
        '\n  equal_to'
        '\n  False'
    )
    assert get_ast(src) == expected_ast
