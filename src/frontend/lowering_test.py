from typing import Dict

from .parser import get_parser

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


parser = get_parser()


def get_ast(src: str) -> str:
    return parser.parse(src).pretty().strip()


def test_always_loop_to_while() -> None:
    src = 'loop {}'
    expected_ast = (
        'while'
        '\n  True'
        '\n  block'
    )
    assert get_ast(src) == expected_ast


def test_selection_lambda_shorthand() -> None:
    src = 'a | ...b'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  lambda_func'
        '\n    @@shorthand_select@@'
        '\n    select_field'
        '\n      identifier\t@@shorthand_select@@'
        '\n      b'
    )
    assert get_ast(src) == expected_ast


def test_pipeline_to_implicit_lambda() -> None:
    src = 'a | _ | c'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  poisonous_lambda_func'
        '\n    @@implicit_lambda@@'
        '\n    identifier\t@@implicit_lambda@@'
        '\n  exec\tc'
    )
    assert get_ast(src) == expected_ast


def test_pipeline_to_implicit_lambda2() -> None:
    src = 'a | _ | _ + _ | c'
    expected_ast = (
        'pipeline'
        '\n  exec\ta'
        '\n  poisonous_lambda_func'
        '\n    @@implicit_lambda@@'
        '\n    identifier\t@@implicit_lambda@@'
        '\n  poisonous_lambda_func'
        '\n    @@implicit_lambda@@'
        '\n    addition'
        '\n      identifier\t@@implicit_lambda@@'
        '\n      identifier\t@@implicit_lambda@@'
        '\n  exec\tc'
    )
    assert get_ast(src) == expected_ast


def test_unit_literals() -> None:
    src = '10gb + 1.5mb'
    expected_ast = (
        'addition'
        '\n  unit_literal'
        '\n    unit_type\tsize'
        '\n    unit\tgb'
        '\n    10'
        '\n  unit_literal'
        '\n    unit_type\tsize'
        '\n    unit\tmb'
        '\n    1.5'
    )
    assert get_ast(src) == expected_ast


def test_plus_assignment() -> None:
    src = '@a += @b'
    equivalent_src = '@a = @a + @b'
    assert get_ast(src) == get_ast(equivalent_src)


def test_minus_assignment() -> None:
    src = '@a -= @b'
    equivalent_src = '@a = @a - @b'
    assert get_ast(src) == get_ast(equivalent_src)


def test_times_assignment() -> None:
    src = '@a *= @b'
    equivalent_src = '@a = @a * @b'
    assert get_ast(src) == get_ast(equivalent_src)


def test_divide_assignment() -> None:
    src = '@a /= @b'
    equivalent_src = '@a = @a / @b'
    assert get_ast(src) == get_ast(equivalent_src)


def test_mod_assignment() -> None:
    src = '@a %= @b'
    equivalent_src = '@a = @a % @b'
    assert get_ast(src) == get_ast(equivalent_src)


def test_power_assignment() -> None:
    src = '@a **= @b'
    equivalent_src ='@a = @a ** @b'
    assert get_ast(src) == get_ast(equivalent_src)


def test_int_div_assignment() -> None:
    src = '@a //= @b'
    equivalent_src ='@a = @a // @b'
    assert get_ast(src) == get_ast(equivalent_src)


def test_concat_assignment() -> None:
    src = '@a ++= @b'
    equivalent_src ='@a = @a ++ @b'
    assert get_ast(src) == get_ast(equivalent_src)


def test_seq_and_assignment() -> None:
    src = '@a &&= @b'
    equivalent_src ='@a = @a && @b'
    assert get_ast(src) == get_ast(equivalent_src)


def test_seq_or_assignment() -> None:
    src = '@a ||= @b'
    equivalent_src ='@a = @a || @b'
    assert get_ast(src) == get_ast(equivalent_src)


def test_pipe_assignment() -> None:
    src = '@a |= @b'
    equivalent_src = '@a = (@a | @b)'
    assert get_ast(src) == get_ast(equivalent_src)


def test_exec() -> None:
    src = 'foo'
    expected_ast = (
        'exec\tfoo'
    )
    assert get_ast(src) == expected_ast


def test_exec_multiple_args() -> None:
    src = 'foo -o bar'
    expected_ast = (
        'exec'
        '\n  foo'
        '\n  -o'
        '\n  bar'
    )
    assert get_ast(src) == expected_ast


def test_explicit_exec() -> None:
    src = '`"foo bar" -o hello`'
    expected_ast = (
        'exec'
        '\n  foo bar'
        '\n  -o'
        '\n  hello'
    )
    assert get_ast(src) == expected_ast
