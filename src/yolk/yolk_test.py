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
    expected_gen_code = 'PUSH_INT 1'
    assert get_gen_code(src) == expected_gen_code


def test_add2() -> None:
    src = '1 + 2'
    expected_gen_code = (
        'PUSH_INT 1'
        '\nPUSH_INT 2'
        '\nBINOP add'
    )
    assert get_gen_code(src) == expected_gen_code


def test_add3() -> None:
    src = '1 + 2 + 3'
    expected_gen_code = (
        'PUSH_INT 1'
        '\nPUSH_INT 2'
        '\nBINOP add'
        '\nPUSH_INT 3'
        '\nBINOP add'
    )
    assert get_gen_code(src) == expected_gen_code


def test_add5() -> None:
    src = '1 + 2 + 3+4+5'
    expected_gen_code = (
        'PUSH_INT 1'
        '\nPUSH_INT 2'
        '\nBINOP add'
        '\nPUSH_INT 3'
        '\nBINOP add'
        '\nPUSH_INT 4'
        '\nBINOP add'
        '\nPUSH_INT 5'
        '\nBINOP add'
    )
    assert get_gen_code(src) == expected_gen_code


def test_float() -> None:
    src = '1.5'
    expected_gen_code = 'PUSH_NUM 1.5'
    assert get_gen_code(src) == expected_gen_code


def test_float0() -> None:
    src = '1.0'
    expected_gen_code = 'PUSH_NUM 1.0'
    assert get_gen_code(src) == expected_gen_code


def test_add_float() -> None:
    src = '1 + 3.2'
    expected_gen_code = (
        'PUSH_INT 1'
        '\nPUSH_NUM 3.2'
        '\nBINOP add'
    )
    assert get_gen_code(src) == expected_gen_code


def test_sub2() -> None:
    src = '1 - 2'
    expected_gen_code = (
        'PUSH_INT 1'
        '\nPUSH_INT 2'
        '\nBINOP subtract'
    )
    assert get_gen_code(src) == expected_gen_code


def test_mul2() -> None:
    src = '3 * 7'
    expected_gen_code = (
        'PUSH_INT 3'
        '\nPUSH_INT 7'
        '\nBINOP multiply'
    )
    assert get_gen_code(src) == expected_gen_code


def test_div2() -> None:
    src = '14 / 7'
    expected_gen_code = (
        'PUSH_INT 14'
        '\nPUSH_INT 7'
        '\nBINOP divide'
    )
    assert get_gen_code(src) == expected_gen_code


def test_idiv2() -> None:
    src = '3//2'
    expected_gen_code = (
        'PUSH_INT 3'
        '\nPUSH_INT 2'
        '\nBINOP int_divide'
    )
    assert get_gen_code(src) == expected_gen_code


def test_pow2() -> None:
    src = '7 ** 8'
    expected_gen_code = (
        'PUSH_INT 7'
        '\nPUSH_INT 8'
        '\nBINOP power'
    )
    assert get_gen_code(src) == expected_gen_code


def test_mod2() -> None:
    src = '3 % 2'
    expected_gen_code = (
        'PUSH_INT 3'
        '\nPUSH_INT 2'
        '\nBINOP modulus'
    )
    assert get_gen_code(src) == expected_gen_code


def test_mul_add() -> None:
    src = '1 + 2 * 3 + 4'
    expected_gen_code = (
        'PUSH_INT 1'
        '\nPUSH_INT 2'
        '\nPUSH_INT 3'
        '\nBINOP multiply'
        '\nBINOP add'
        '\nPUSH_INT 4'
        '\nBINOP add'
    )
    assert get_gen_code(src) == expected_gen_code


def test_str() -> None:
    src = '"hello world"'
    expected_gen_code = "PUSH_STR 'hello world'"
    assert get_gen_code(src) == expected_gen_code


def test_concat2() -> None:
    src = '"a" ++ "b"'
    expected_gen_code = (
        "PUSH_STR 'a'"
        "\nPUSH_STR 'b'"
        '\nBINOP concat'
    )
    assert get_gen_code(src) == expected_gen_code


def test_bool_true() -> None:
    src = 'true'
    expected_gen_code = 'PUSH_BOOL true'
    assert get_gen_code(src) == expected_gen_code


def test_bool_false() -> None:
    src = 'false'
    expected_gen_code = 'PUSH_BOOL false'
    assert get_gen_code(src) == expected_gen_code


def test_and() -> None:
    src = 'false and true'
    expected_gen_code = (
        'PUSH_BOOL false'
        '\nPUSH_BOOL true'
        '\nBINOP and'
    )
    assert get_gen_code(src) == expected_gen_code


def test_or() -> None:
    src = 'false or true'
    expected_gen_code = (
        'PUSH_BOOL false'
        '\nPUSH_BOOL true'
        '\nBINOP or'
    )
    assert get_gen_code(src) == expected_gen_code


def test_and_or() -> None:
    src = 'false or true and true or false'
    expected_gen_code = (
        'PUSH_BOOL false'
        '\nPUSH_BOOL true'
        '\nPUSH_BOOL true'
        '\nBINOP and'
        '\nBINOP or'
        '\nPUSH_BOOL false'
        '\nBINOP or'
    )
    assert get_gen_code(src) == expected_gen_code


def test_not() -> None:
    src = '!true'
    expected_gen_code = (
        'PUSH_BOOL true'
        '\nNOT'
    )
    assert get_gen_code(src) == expected_gen_code


def test_negate() -> None:
    src = '-5'
    expected_gen_code = (
        'PUSH_INT 5'
        '\nNEGATE'
    )
    assert get_gen_code(src) == expected_gen_code
