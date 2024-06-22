from contextlib import redirect_stdout
from io import StringIO
from typing import Dict, Optional

import lark

from frontend.parser import get_parser
from backend.py_generator import PythonGenerator

from . import egg_lib as _e
from runtime import memory

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


def execute_src(src: str) -> Optional[str]:
    _m = memory.Memory()
    ast_or_value = parser.parse(src)
    if type(ast_or_value) != lark.tree.Tree:
        if ast_or_value is None:
            return ast_or_value
        return str(ast_or_value)
    py_code = pygen.transform(ast_or_value)
    try:
        value = eval(py_code)
        if value is None:
            return value
        return str(eval(py_code))
    except SyntaxError:
        string_io = StringIO()
        with redirect_stdout(string_io):
            exec(py_code)
        return string_io.getvalue()


def test_arithmetic():
    src = '10 // 3 + 17 - 7 * 4 / -5**2 + 1.12 + 10*(9863200 + 48) % 100'
    expected_output = '100.0'
    assert execute_src(src) == expected_output


def test_concat_strings():
    src = '"hello " ++ "world" ++ "!!!"'
    expected_output = "'hello world!!!'"
    assert execute_src(src) == expected_output


def test_concat_lists():
    src = '[1,2,3] ++ [] ++ [10,20,30]'
    expected_output = '[1,2,3,10,20,30]'
    assert execute_src(src) == expected_output


def test_concat_ranges():
    src = '(0..5) ++ (100..105) ++ [9,8]'
    expected_output = '[0,1,2,3,4,100,101,102,103,104,9,8]'
    assert execute_src(src) == expected_output


def test_select_element():
    src = '[ [0,1,2,3][2], (0..4)[1], "0123"[0], [0..4][3] ]'
    expected_output = '[2,1,0,3]'
    assert execute_src(src) == expected_output


def test_select_slice():
    src = (
        '([0,1,2,3][2:] ++ (0..4)[1:3] ++ (0..4)[:2])'
        '++ ([0..4][4:0 by -1] ++ [0,1,2,3][:1 by -1])'
    )
    expected_output = '[2,3,1,2,0,1,3,2,1,3,2]'
    assert execute_src(src) == expected_output


def test_select_slice_range():
    src = '(0..100)[70:30 by -1]'
    expected_output = '(70..30 by -1)'
    assert execute_src(src) == expected_output


def test_logic_and():
    src = '[false and false, false and true, true and false, true and true]'
    expected_output = '[false,false,false,true]'
    assert execute_src(src) == expected_output


def test_logic_or():
    src = '[false or false, false or true, true or false, true or true]'
    expected_output = '[false,true,true,true]'
    assert execute_src(src) == expected_output


def test_logic_xor():
    src = '[false xor false, false xor true, true xor false, true xor true]'
    expected_output = '[false,true,true,false]'
    assert execute_src(src) == expected_output


def test_logic_not():
    src = '[not false, not true, !false, !true]'
    expected_output = '[true,false,true,false]'
    assert execute_src(src) == expected_output


def test_comparisons():
    src = '[1 < 3, 3 > 5, 4 <= 5]'
    expected_output = '[True,False,True]'
    assert execute_src(src) == expected_output


def test_declare_untyped_variable():
    src = 'a := 1'
    expected_output = None
    assert execute_src(src) == expected_output


def test_const_declare():
    src = 'const a := 1'
    expected_output = None
    assert execute_src(src) == expected_output


def test_say():
    src = 'say 1 + 10'
    expected_output = None
    string_io = StringIO()
    with redirect_stdout(string_io):
        output = execute_src(src)
    assert output == expected_output
    assert string_io.getvalue() == "11\n"
