from typing import Dict

from ..cli import cli

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


egg_cli = cli.EggCLI(cli.CLIMode(cli.ExecutionMode.codegen, cli.BackendMode.yolk), use_profiler=False)


def get_gen_code(src: str) -> str:
    return egg_cli.get_codegen(src)


def test_integer() -> None:
    src = '1'
    expected_gen_code = 'PUSH_NUM 1'
    assert get_gen_code(src) == expected_gen_code


def test_add2() -> None:
    src = '1 + 2'
    expected_gen_code = (
        'PUSH_NUM 1'
        '\nPUSH_NUM 2'
        '\nBINOP add'
    )
    assert get_gen_code(src) == expected_gen_code


def test_add3() -> None:
    src = '1 + 2 + 3'
    expected_gen_code = (
        'PUSH_NUM 1'
        '\nPUSH_NUM 2'
        '\nBINOP add'
        '\nPUSH_NUM 3'
        '\nBINOP add'
    )
    assert get_gen_code(src) == expected_gen_code


def test_add5() -> None:
    src = '1 + 2 + 3+4+5'
    expected_gen_code = (
        'PUSH_NUM 1'
        '\nPUSH_NUM 2'
        '\nBINOP add'
        '\nPUSH_NUM 3'
        '\nBINOP add'
        '\nPUSH_NUM 4'
        '\nBINOP add'
        '\nPUSH_NUM 5'
        '\nBINOP add'
    )
    assert get_gen_code(src) == expected_gen_code
