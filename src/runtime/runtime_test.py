from contextlib import redirect_stdout
from io import StringIO
from typing import Dict, Optional

import lark

from ..backend.py_generator import PythonGenerator, transform_pygen_result
from ..cli.cli import CLIMode, EggCLI
from ..frontend.parser import get_parser
from . import egg_lib as _e
from . import memory

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
def test_no_new_test_cases() -> None:
    assert len(new_test_cases) == 0


egg_cli = EggCLI(CLIMode.execute, use_profiler=False)


def execute_src(src: str) -> Optional[str]:
    return egg_cli.execute(src)


def test_arithmetic() -> None:
    src = '10 // 3 + 17 - 7 * 4 / -5**2 + 1.12 + 10*(9863200 + 48) % 100'
    expected_output = '100.0'
    assert execute_src(src) == expected_output


def test_concat_strings() -> None:
    src = '"hello " ++ "world" ++ "!!!"'
    expected_output = "'hello world!!!'"
    assert execute_src(src) == expected_output


def test_concat_lists() -> None:
    src = '[1,2,3] ++ [] ++ [10,20,30]'
    expected_output = '[1,2,3,10,20,30]'
    assert execute_src(src) == expected_output


def test_concat_ranges() -> None:
    src = '(0..5) ++ (100..105) ++ [9,8]'
    expected_output = '[0,1,2,3,4,100,101,102,103,104,9,8]'
    assert execute_src(src) == expected_output


def test_select_element() -> None:
    src = '[ [0,1,2,3][2], (0..4)[1], "0123"[0], [0..4][3] ]'
    expected_output = "[2,1,'0',3]"
    assert execute_src(src) == expected_output


def test_select_slice() -> None:
    src = (
        '([0,1,2,3][2:] ++ (0..4)[1:3] ++ (0..4)[:2])'
        '++ ([0..4][4:0 by -1] ++ [0,1,2,3][:1 by -1])'
    )
    expected_output = '[2,3,1,2,0,1,3,2,1,3,2]'
    assert execute_src(src) == expected_output


def test_select_slice_range() -> None:
    src = '(0..100)[70:30 by -1]'
    expected_output = '(70..30 by -1)'
    assert execute_src(src) == expected_output


def test_logic_and() -> None:
    src = '[false and false, false and true, true and false, true and true]'
    expected_output = '[false,false,false,true]'
    assert execute_src(src) == expected_output


def test_logic_or() -> None:
    src = '[false or false, false or true, true or false, true or true]'
    expected_output = '[false,true,true,true]'
    assert execute_src(src) == expected_output


def test_logic_xor() -> None:
    src = '[false xor false, false xor true, true xor false, true xor true]'
    expected_output = '[false,true,true,false]'
    assert execute_src(src) == expected_output


def test_logic_not() -> None:
    src = '[not false, not true, !false, !true]'
    expected_output = '[true,false,true,false]'
    assert execute_src(src) == expected_output


def test_comparisons() -> None:
    src = '[1 < 3, 3 > 5, 4 <= 5]'
    expected_output = '[True,False,True]'
    assert execute_src(src) == expected_output


def test_declare_untyped_variable() -> None:
    src = 'a := 1'
    expected_output = None
    assert execute_src(src) == expected_output


def test_const_declare() -> None:
    src = 'const a := 1'
    expected_output = None
    assert execute_src(src) == expected_output


def test_say() -> None:
    src = 'say 1 + 10'
    expected_output = None
    string_io = StringIO()
    with redirect_stdout(string_io):
        output = execute_src(src)
    assert output == expected_output
    assert string_io.getvalue() == "11\n"


def test_multiple_lines() -> None:
    src = 'a := 5; a = 7; say @a ** 2'
    expected_output = '49\n'
    assert execute_src(src) == expected_output


def test_if_true() -> None:
    src = 'if true {say "hello world"}'
    expected_output = "hello world\n"
    assert execute_src(src) == expected_output


def test_if_false() -> None:
    src = 'if false {say "hello world"}'
    expected_output = ''
    assert execute_src(src) == expected_output


def test_if_elif_else1() -> None:
    src = 'if true {say 1} elif false {say 2} else if false {say 3} else {say 4}'
    expected_output = '1\n'
    assert execute_src(src) == expected_output


def test_if_elif_else2() -> None:
    src = 'if false {say 1} elif true {say 2} else if false {say 3} else {say 4}'
    expected_output = '2\n'
    assert execute_src(src) == expected_output


def test_if_elif_else3() -> None:
    src = 'if false {say 1} elif false {say 2} else if true {say 3} else {say 4}'
    expected_output = '3\n'
    assert execute_src(src) == expected_output


def test_if_elif_else4() -> None:
    src = 'if false {say 1} elif false {say 2} else if false {say 3} else {say 4}'
    expected_output = '4\n'
    assert execute_src(src) == expected_output


def test_empty_if() -> None:
    src = 'if true {}'
    expected_output = ''
    assert execute_src(src) == expected_output


def test_while() -> None:
    src = 'x := 5\nwhile @x > 0 {\n\tsay x\n\tx -= 1}'
    expected_output = (
        '5'
        '\n4'
        '\n3'
        '\n2'
        '\n1'
        '\n'
    )
    assert execute_src(src) == expected_output


def test_temporary__exec_pipeline() -> None:
    src = 'a | b | c'
    expected_output = 'Exec[a] -> Exec[b] -> Exec[c]'
    assert execute_src(src) == expected_output


def test_temporary__exec_pipeline_number() -> None:
    src = '12| a | b | c'
    expected_output = '12 -> Exec[a] -> Exec[b] -> Exec[c]'
    assert execute_src(src) == expected_output
