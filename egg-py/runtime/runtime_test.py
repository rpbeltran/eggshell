from contextlib import redirect_stdout
from io import StringIO
from typing import Dict

import lark

from frontend.parser import get_parser
from backend.py_generator import PythonGenerator
from . import egg_lib as _e

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


def execute_src(src: str) -> str:
    ast_or_value = parser.parse(src)
    if type(ast_or_value) != lark.tree.Tree:
        return str(ast_or_value)
    py_code = pygen.transform(ast_or_value)
    try:
        return str(eval(py_code))
    except SyntaxError:
        string_io = StringIO()
        with redirect_stdout(string_io):
            exec(py_code)
        return string_io.getvalue()


def test_add():
    src = '1 + 2'
    expected_output = '3'
    assert execute_src(src) == expected_output
