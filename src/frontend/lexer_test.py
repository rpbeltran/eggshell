from typing import Dict, List, Tuple

from .lexer import *


"""
INSTRUCTIONS: To add new test cases:
  1) Add them to the new_test_cases variable
      example: `new_test_cases: Dict[str,str] = {"piping": "a | b | c"}`
  2) Run `./add_testcases.py` which will add tests at the bottom of this file
  3) Manually verify the generated code and tokens for correctness
  4) Restore `new_test_cases: Dict[str,str] = {}`
  5) Push to github!
"""


# Maps new test cases from test-name to test-code
new_test_cases: Dict[str, str] = {}


# Prevents accidentally committing data in new_test_cases
def test_no_new_test_cases() -> None:
    assert len(new_test_cases) == 0


lexer = EggLexer()


def get_tokens(egg: str) -> List[Tuple[str,str]]:
    lexer.reset()
    return [(token.token_type, token.source) for token in lexer.lex(egg)]


def test_basic_pipe() -> None:
    egg_code = 'a | b'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('PIPE', '|'),
        ('EXEC_ARG', 'b'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_basic_pipe3() -> None:
    egg_code = 'a b | b | c'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('EXEC_ARG', 'b'),
        ('PIPE', '|'),
        ('EXEC_ARG', 'b'),
        ('PIPE', '|'),
        ('EXEC_ARG', 'c'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_semicolons() -> None:
    egg_code = 'a ; b ; c'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('SEMICOLON', ';'),
        ('EXEC_ARG', 'b'),
        ('SEMICOLON', ';'),
        ('EXEC_ARG', 'c'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_function_basic() -> None:
    egg_code = 'fn foo() {`b`}'
    expected_tokens = [
        ('FN', 'fn'),
        ('NAME', 'foo'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('EXEC_ARG', 'b'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_function_return() -> None:
    egg_code = 'fn foo(): int {\n  ret 2\n}'
    expected_tokens = [
        ('FN', 'fn'),
        ('NAME', 'foo'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
        ('COLON', ':'),
        ('NAME', 'int'),
        ('CURLY_OPEN', '{'),
        ('SEMICOLON', ''),
        ('RETURN', 'ret'),
        ('INTEGER', '2'),
        ('SEMICOLON', ''),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_function_param() -> None:
    egg_code = 'fn foo(a, b := 1, c: int = 2) {}'
    expected_tokens = [
        ('FN', 'fn'),
        ('NAME', 'foo'),
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('NAME', 'b'),
        ('DECLARE', ':='),
        ('INTEGER', '1'),
        ('COMMA', ','),
        ('NAME', 'c'),
        ('COLON', ':'),
        ('NAME', 'int'),
        ('ASSIGN', '='),
        ('INTEGER', '2'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_lambda() -> None:
    egg_code = '\\a -> b'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('NAME', 'a'),
        ('ARROW', '->'),
        ('EXEC_ARG', 'b'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_lambda2() -> None:
    egg_code = '\\(a,b) -> c'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('ARROW', '->'),
        ('EXEC_ARG', 'c'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_lambda3() -> None:
    egg_code = '\\(a,b,c) -> d'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('NAME', 'b'),
        ('COMMA', ','),
        ('NAME', 'c'),
        ('PAREN_CLOSE', ')'),
        ('ARROW', '->'),
        ('EXEC_ARG', 'd'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_lambda_multi() -> None:
    egg_code = '\\a {ret 1}'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('NAME', 'a'),
        ('CURLY_OPEN', '{'),
        ('RETURN', 'ret'),
        ('INTEGER', '1'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_identifiers() -> None:
    egg_code = '@a b @c'
    expected_tokens = [
        ('NAME', 'a'),
        ('EXEC_ARG', 'b'),
        ('NAME', 'c'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_declaration() -> None:
    egg_code = 'a := 1'
    expected_tokens = [
        ('NAME', 'a'),
        ('DECLARE', ':='),
        ('INTEGER', '1'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_typed_declaration() -> None:
    egg_code = 'a : int = 1'
    expected_tokens = [
        ('NAME', 'a'),
        ('COLON', ':'),
        ('NAME', 'int'),
        ('ASSIGN', '='),
        ('INTEGER', '1'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_quoted_executions() -> None:
    egg_code = '`a` {`b`}'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('CURLY_OPEN', '{'),
        ('EXEC_ARG', 'b'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_list() -> None:
    egg_code = 'a := [1,2,3]'
    expected_tokens = [
        ('NAME', 'a'),
        ('DECLARE', ':='),
        ('SQUARE_OPEN', '['),
        ('INTEGER', '1'),
        ('COMMA', ','),
        ('INTEGER', '2'),
        ('COMMA', ','),
        ('INTEGER', '3'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_list_types() -> None:
    egg_code = 'a: [int] = '
    expected_tokens = [
        ('NAME', 'a'),
        ('COLON', ':'),
        ('SQUARE_OPEN', '['),
        ('NAME', 'int'),
        ('SQUARE_CLOSE', ']'),
        ('ASSIGN', '='),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_list_access() -> None:
    egg_code = 'a[1]'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('SQUARE_OPEN', '['),
        ('INTEGER', '1'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_list_access2() -> None:
    egg_code = 'a[1:2]'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('SQUARE_OPEN', '['),
        ('INTEGER', '1'),
        ('COLON', ':'),
        ('INTEGER', '2'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_list_access3() -> None:
    egg_code = 'a[1:2:3]'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('SQUARE_OPEN', '['),
        ('INTEGER', '1'),
        ('COLON', ':'),
        ('INTEGER', '2'),
        ('COLON', ':'),
        ('INTEGER', '3'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_list_access_var() -> None:
    egg_code = 'a[b:c:d]'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('SQUARE_OPEN', '['),
        ('NAME', 'b'),
        ('COLON', ':'),
        ('NAME', 'c'),
        ('COLON', ':'),
        ('NAME', 'd'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_currying() -> None:
    egg_code = 'a $ b $ c'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('CURRY', '$'),
        ('EXEC_ARG', 'b'),
        ('CURRY', '$'),
        ('EXEC_ARG', 'c'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_field_access() -> None:
    egg_code = '@a.b.c'
    expected_tokens = [
        ('NAME', 'a'),
        ('DOT', '.'),
        ('NAME', 'b'),
        ('DOT', '.'),
        ('NAME', 'c'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_comment() -> None:
    egg_code = 'a # hello \n #world \n b'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('SEMICOLON', ''),
        ('SEMICOLON', ''),
        ('EXEC_ARG', 'b'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_pass_by_function() -> None:
    egg_code = '@a...'
    expected_tokens = [
        ('NAME', 'a'),
        ('ELLIPSIS', '...'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_error_handling() -> None:
    egg_code = '(a && b) || c'
    expected_tokens = [
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('SEQ_AND', '&&'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('SEQ_OR', '||'),
        ('EXEC_ARG', 'c'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_try() -> None:
    egg_code = 'try{\n\t`a` }'
    expected_tokens = [
        ('TRY', 'try'),
        ('CURLY_OPEN', '{'),
        ('SEMICOLON', ''),
        ('EXEC_ARG', 'a'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_try_catch() -> None:
    egg_code = 'try { `a` } catch { `b` }'
    expected_tokens = [
        ('TRY', 'try'),
        ('CURLY_OPEN', '{'),
        ('EXEC_ARG', 'a'),
        ('CURLY_CLOSE', '}'),
        ('CATCH', 'catch'),
        ('CURLY_OPEN', '{'),
        ('EXEC_ARG', 'b'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_try_catch_param() -> None:
    egg_code = 'try { `a` } catch e { `b` }'
    expected_tokens = [
        ('TRY', 'try'),
        ('CURLY_OPEN', '{'),
        ('EXEC_ARG', 'a'),
        ('CURLY_CLOSE', '}'),
        ('CATCH', 'catch'),
        ('NAME', 'e'),
        ('CURLY_OPEN', '{'),
        ('EXEC_ARG', 'b'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_range() -> None:
    egg_code = '(a..b)'
    expected_tokens = [
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('RANGE', '..'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_loop() -> None:
    egg_code = 'loop { }'
    expected_tokens = [
        ('ALWAYS_LOOP', 'loop'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_while() -> None:
    egg_code = 'while true { }'
    expected_tokens = [
        ('WHILE', 'while'),
        ('TRUE', 'true'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_for() -> None:
    egg_code = 'for a in @b { }'
    expected_tokens = [
        ('FOR', 'for'),
        ('NAME', 'a'),
        ('IN', 'in'),
        ('NAME', 'b'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_async() -> None:
    egg_code = '~(`b`)'
    expected_tokens = [
        ('ASYNC', '~'),
        ('PAREN_OPEN', '('),
        ('EXEC_ARG', 'b'),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_import() -> None:
    egg_code = 'import "a"'
    expected_tokens = [
        ('IMPORT', 'import'),
        ('QUOTED_STRING', 'a'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_class() -> None:
    egg_code = 'class Thing {a: Int = 1\n b: Int = 2; fn c(){}}'
    expected_tokens = [
        ('CLASS', 'class'),
        ('NAME', 'Thing'),
        ('CURLY_OPEN', '{'),
        ('NAME', 'a'),
        ('COLON', ':'),
        ('NAME', 'Int'),
        ('ASSIGN', '='),
        ('INTEGER', '1'),
        ('SEMICOLON', ''),
        ('NAME', 'b'),
        ('COLON', ':'),
        ('NAME', 'Int'),
        ('ASSIGN', '='),
        ('INTEGER', '2'),
        ('SEMICOLON', ';'),
        ('FN', 'fn'),
        ('NAME', 'c'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_derived_class() -> None:
    egg_code = 'class Cow: Animal {}'
    expected_tokens = [
        ('CLASS', 'class'),
        ('NAME', 'Cow'),
        ('COLON', ':'),
        ('NAME', 'Animal'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_map() -> None:
    egg_code = '{ 1: 10, 2: 20}'
    expected_tokens = [
        ('CURLY_OPEN', '{'),
        ('INTEGER', '1'),
        ('COLON', ':'),
        ('INTEGER', '10'),
        ('COMMA', ','),
        ('INTEGER', '2'),
        ('COLON', ':'),
        ('INTEGER', '20'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_math() -> None:
    egg_code = '(1 + 2 - 3 * 4 / 5 // 6 ** 7 ** 8 % -9)'
    expected_tokens = [
        ('PAREN_OPEN', '('),
        ('INTEGER', '1'),
        ('PLUS', '+'),
        ('INTEGER', '2'),
        ('MINUS', '-'),
        ('INTEGER', '3'),
        ('TIMES', '*'),
        ('INTEGER', '4'),
        ('DIVIDE', '/'),
        ('INTEGER', '5'),
        ('INT_DIV', '//'),
        ('INTEGER', '6'),
        ('POWER', '**'),
        ('INTEGER', '7'),
        ('POWER', '**'),
        ('INTEGER', '8'),
        ('MOD', '%'),
        ('MINUS', '-'),
        ('INTEGER', '9'),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_math_root_level() -> None:
    egg_code = '1 ** 2 // 3 * 4 / 5'
    expected_tokens = [
        ('INTEGER', '1'),
        ('POWER', '**'),
        ('INTEGER', '2'),
        ('INT_DIV', '//'),
        ('INTEGER', '3'),
        ('TIMES', '*'),
        ('INTEGER', '4'),
        ('DIVIDE', '/'),
        ('INTEGER', '5'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_comparison() -> None:
    egg_code = '1 < 2 <= 3 == 4 != 5 >= 6 > 7'
    expected_tokens = [
        ('INTEGER', '1'),
        ('ANGLE_OPEN', '<'),
        ('INTEGER', '2'),
        ('LTE', '<='),
        ('INTEGER', '3'),
        ('EQUALS', '=='),
        ('INTEGER', '4'),
        ('NOT_EQUALS', '!='),
        ('INTEGER', '5'),
        ('GTE', '>='),
        ('INTEGER', '6'),
        ('ANGLE_CLOSE', '>'),
        ('INTEGER', '7'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_logic() -> None:
    egg_code = '(a and b or c cor not !d)'
    expected_tokens = [
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('AND', 'and'),
        ('NAME', 'b'),
        ('OR', 'or'),
        ('NAME', 'c'),
        ('NAME', 'cor'),
        ('NOT', 'not'),
        ('NOT', '!'),
        ('NAME', 'd'),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_function_call() -> None:
    egg_code = 'a()'
    expected_tokens = [
        ('NAME', 'a'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_function_call_params() -> None:
    egg_code = 'a(b,c)'
    expected_tokens = [
        ('NAME', 'a'),
        ('PAREN_OPEN', '('),
        ('NAME', 'b'),
        ('COMMA', ','),
        ('NAME', 'c'),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_function_call_in_block() -> None:
    egg_code = '{a(b)}'
    expected_tokens = [
        ('CURLY_OPEN', '{'),
        ('NAME', 'a'),
        ('PAREN_OPEN', '('),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_env_access() -> None:
    egg_code = 'env["foo"]'
    expected_tokens = [
        ('EXEC_ARG', 'env'),
        ('SQUARE_OPEN', '['),
        ('QUOTED_STRING', 'foo'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_env_get() -> None:
    egg_code = 'env.get()'
    expected_tokens = [
        ('NAME', 'env'),
        ('DOT', '.'),
        ('NAME', 'get'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_method_call() -> None:
    egg_code = '@thing.method()'
    expected_tokens = [
        ('NAME', 'thing'),
        ('DOT', '.'),
        ('NAME', 'method'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_do_block() -> None:
    egg_code = 'do {}'
    expected_tokens = [
        ('DO', 'do'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_multiline_parenthetical() -> None:
    src = '(a\n+\n\n\n\t2)'
    expected_tokens = [
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('PLUS', '+'),
        ('INTEGER', '2'),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(src) == expected_tokens


def test_slice() -> None:
    src = '@a[1:2:3]'
    expected_tokens = [
        ('NAME', 'a'),
        ('SQUARE_OPEN', '['),
        ('INTEGER', '1'),
        ('COLON', ':'),
        ('INTEGER', '2'),
        ('COLON', ':'),
        ('INTEGER', '3'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(src) == expected_tokens


def test_slice_rev() -> None:
    src = '@a[: by 2]'
    expected_tokens = [
        ('NAME', 'a'),
        ('SQUARE_OPEN', '['),
        ('COLON', ':'),
        ('BY', 'by'),
        ('INTEGER', '2'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(src) == expected_tokens


def test_with() -> None:
    src = 'with a.y() {}'
    expected_tokens = [
        ('WITH', 'with'),
        ('NAME', 'a'),
        ('DOT', '.'),
        ('NAME', 'y'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_with_as() -> None:
    src = 'with a.y() as x {}'
    expected_tokens = [
        ('WITH', 'with'),
        ('NAME', 'a'),
        ('DOT', '.'),
        ('NAME', 'y'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
        ('AS', 'as'),
        ('NAME', 'x'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_explicit_pipeline() -> None:
    src = '`a | b | c`'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('PIPE', '|'),
        ('EXEC_ARG', 'b'),
        ('PIPE', '|'),
        ('EXEC_ARG', 'c'),
    ]
    assert get_tokens(src) == expected_tokens


def test_explicit_pipeline_minified() -> None:
    src = '`a|b|c`'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('PIPE', '|'),
        ('EXEC_ARG', 'b'),
        ('PIPE', '|'),
        ('EXEC_ARG', 'c'),
    ]
    assert get_tokens(src) == expected_tokens


def test_quoted_explicit_param() -> None:
    src = '`a "b \' c" d`'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('EXEC_ARG', "b ' c"),
        ('EXEC_ARG', 'd'),
    ]
    assert get_tokens(src) == expected_tokens


def test_quoted_explicit_param2() -> None:
    src = '`"a b c" d e `'
    expected_tokens = [
        ('EXEC_ARG', 'a b c'),
        ('EXEC_ARG', 'd'),
        ('EXEC_ARG', 'e'),
    ]
    assert get_tokens(src) == expected_tokens


def test_list_comprehension() -> None:
    src = '[10**x for x in (0..10)]'
    expected_tokens = [
        ('SQUARE_OPEN', '['),
        ('INTEGER', '10'),
        ('POWER', '**'),
        ('NAME', 'x'),
        ('FOR', 'for'),
        ('NAME', 'x'),
        ('IN', 'in'),
        ('PAREN_OPEN', '('),
        ('INTEGER', '0'),
        ('RANGE', '..'),
        ('INTEGER', '10'),
        ('PAREN_CLOSE', ')'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(src) == expected_tokens


def test_map_comprehension() -> None:
    src = '{-x: 100**-x for x in (0..10)]'
    expected_tokens = [
        ('CURLY_OPEN', '{'),
        ('MINUS', '-'),
        ('NAME', 'x'),
        ('COLON', ':'),
        ('INTEGER', '100'),
        ('POWER', '**'),
        ('MINUS', '-'),
        ('NAME', 'x'),
        ('FOR', 'for'),
        ('NAME', 'x'),
        ('IN', 'in'),
        ('PAREN_OPEN', '('),
        ('INTEGER', '0'),
        ('RANGE', '..'),
        ('INTEGER', '10'),
        ('PAREN_CLOSE', ')'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(src) == expected_tokens


def test_fn_normal_multi_and_kw_param() -> None:
    src = 'fn foo (a, b, *c, **d){}'
    expected_tokens = [
        ('FN', 'fn'),
        ('NAME', 'foo'),
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('NAME', 'b'),
        ('COMMA', ','),
        ('TIMES', '*'),
        ('NAME', 'c'),
        ('COMMA', ','),
        ('POWER', '**'),
        ('NAME', 'd'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_fn_multi_and_kw_param() -> None:
    src = 'fn foo (*a, **b){}'
    expected_tokens = [
        ('FN', 'fn'),
        ('NAME', 'foo'),
        ('PAREN_OPEN', '('),
        ('TIMES', '*'),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('POWER', '**'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_fn_multi_param() -> None:
    src = 'fn foo (a, *b){}'
    expected_tokens = [
        ('FN', 'fn'),
        ('NAME', 'foo'),
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('TIMES', '*'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_fn_multi_param_only() -> None:
    src = 'fn foo (*b){}'
    expected_tokens = [
        ('FN', 'fn'),
        ('NAME', 'foo'),
        ('PAREN_OPEN', '('),
        ('TIMES', '*'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_fn_kw_param() -> None:
    src = 'fn foo (a, **b){}'
    expected_tokens = [
        ('FN', 'fn'),
        ('NAME', 'foo'),
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('POWER', '**'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_fn_kw_param_only() -> None:
    src = 'fn foo (**b){}'
    expected_tokens = [
        ('FN', 'fn'),
        ('NAME', 'foo'),
        ('PAREN_OPEN', '('),
        ('POWER', '**'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_lambda_normal_multi_and_kw_param() -> None:
    src = '\\(a, b, *c, **d){}'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('NAME', 'b'),
        ('COMMA', ','),
        ('TIMES', '*'),
        ('NAME', 'c'),
        ('COMMA', ','),
        ('POWER', '**'),
        ('NAME', 'd'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_lambda_multi_and_kw_param() -> None:
    src = '\\(*a, **b){}'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('PAREN_OPEN', '('),
        ('TIMES', '*'),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('POWER', '**'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_lambda_multi_param() -> None:
    src = '\\(a, *b){}'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('TIMES', '*'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_lambda_multi_param_only() -> None:
    src = '\\(*b){}'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('PAREN_OPEN', '('),
        ('TIMES', '*'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_lambda_multi_param_only_no_paren() -> None:
    src = '\\*b{}'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('TIMES', '*'),
        ('NAME', 'b'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_lambda_kw_param() -> None:
    src = '\\(a, **b){}'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('POWER', '**'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_lambda_kw_param_only() -> None:
    src = '\\(**b){}'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('PAREN_OPEN', '('),
        ('POWER', '**'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_lambda_kw_param_only_no_paren() -> None:
    src = '\\**b{}'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('POWER', '**'),
        ('NAME', 'b'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens


def test_kw_args() -> None:
    src = 'foo(a, b=c, d=e)'
    expected_tokens = [
        ('NAME', 'foo'),
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('COMMA', ','),
        ('NAME', 'b'),
        ('ASSIGN', '='),
        ('NAME', 'c'),
        ('COMMA', ','),
        ('NAME', 'd'),
        ('ASSIGN', '='),
        ('NAME', 'e'),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(src) == expected_tokens


def test_declare_generic_typed() -> None:
    src = 'a : t[g] = [1]'
    expected_tokens = [
        ('NAME', 'a'),
        ('COLON', ':'),
        ('NAME', 't'),
        ('SQUARE_OPEN', '['),
        ('NAME', 'g'),
        ('SQUARE_CLOSE', ']'),
        ('ASSIGN', '='),
        ('SQUARE_OPEN', '['),
        ('INTEGER', '1'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(src) == expected_tokens


def test_implicit_lambda() -> None:
    src = '_'
    expected_tokens = [
        ('IMPLICIT_LAMBDA_PARAM', '_'),
    ]
    assert get_tokens(src) == expected_tokens


def test_implicit_lambda_method() -> None:
    src = '_.hello() + _.world()'
    expected_tokens = [
        ('IMPLICIT_LAMBDA_PARAM', '_'),
        ('DOT', '.'),
        ('NAME', 'hello'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
        ('PLUS', '+'),
        ('IMPLICIT_LAMBDA_PARAM', '_'),
        ('DOT', '.'),
        ('NAME', 'world'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(src) == expected_tokens


def test_implicit_lambda_piped() -> None:
    src = 'a | _.sort | b'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('PIPE', '|'),
        ('IMPLICIT_LAMBDA_PARAM', '_'),
        ('DOT', '.'),
        ('NAME', 'sort'),
        ('PIPE', '|'),
        ('EXEC_ARG', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_selection_lambda_shorthand() -> None:
    src = 'utils::list_files | ...date'
    expected_tokens = [
        ('NAME', 'utils'),
        ('NAMESPACE', '::'),
        ('NAME', 'list_files'),
        ('PIPE', '|'),
        ('ELLIPSIS', '...'),
        ('NAME', 'date'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_b() -> None:
    src = '45b + 4.5b'
    expected_tokens = [
        ('UNIT_INTEGER', '45:b'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_B() -> None:
    src = '45B + 4.5B'
    expected_tokens = [
        ('UNIT_INTEGER', '45:b'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_kb() -> None:
    src = '45kb + 4.5kb'
    expected_tokens = [
        ('UNIT_INTEGER', '45:kb'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:kb'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_Kb() -> None:
    src = '45Kb + 4.5Kb'
    expected_tokens = [
        ('UNIT_INTEGER', '45:kb'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:kb'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_KB() -> None:
    src = '45Kb + 4.5Kb'
    expected_tokens = [
        ('UNIT_INTEGER', '45:kb'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:kb'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_kB() -> None:
    src = '45Kb + 4.5Kb'
    expected_tokens = [
        ('UNIT_INTEGER', '45:kb'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:kb'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_mb() -> None:
    src = '45mb + 4.5mb'
    expected_tokens = [
        ('UNIT_INTEGER', '45:mb'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:mb'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_gb() -> None:
    src = '45gb + 4.5gb'
    expected_tokens = [
        ('UNIT_INTEGER', '45:gb'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:gb'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_tb() -> None:
    src = '45tb + 4.5tb'
    expected_tokens = [
        ('UNIT_INTEGER', '45:tb'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:tb'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_pb() -> None:
    src = '45pb + 4.5pb'
    expected_tokens = [
        ('UNIT_INTEGER', '45:pb'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:pb'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_kib() -> None:
    src = '45kib + 4.5kib'
    expected_tokens = [
        ('UNIT_INTEGER', '45:kib'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:kib'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_mib() -> None:
    src = '45mib + 4.5mib'
    expected_tokens = [
        ('UNIT_INTEGER', '45:mib'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:mib'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_gib() -> None:
    src = '45gib + 4.5gib'
    expected_tokens = [
        ('UNIT_INTEGER', '45:gib'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:gib'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_tib() -> None:
    src = '45tib + 4.5tib'
    expected_tokens = [
        ('UNIT_INTEGER', '45:tib'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:tib'),
    ]
    assert get_tokens(src) == expected_tokens


def test_unit_pib() -> None:
    src = '45pib + 4.5pib'
    expected_tokens = [
        ('UNIT_INTEGER', '45:pib'),
        ('PLUS', '+'),
        ('UNIT_FLOAT', '4.5:pib'),
    ]
    assert get_tokens(src) == expected_tokens


def test_plus_assignment() -> None:
    src = '@a += @b'
    expected_tokens = [
        ('NAME', 'a'),
        ('PLUS_ASSIGN', '+='),
        ('NAME', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_minus_assignment() -> None:
    src = '@a -= @b'
    expected_tokens = [
        ('NAME', 'a'),
        ('MINUS_ASSIGN', '-='),
        ('NAME', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_times_assignment() -> None:
    src = '@a *= @b'
    expected_tokens = [
        ('NAME', 'a'),
        ('TIMES_ASSIGN', '*='),
        ('NAME', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_divide_assignment() -> None:
    src = '@a /= @b'
    expected_tokens = [
        ('NAME', 'a'),
        ('DIVIDE_ASSIGN', '/='),
        ('NAME', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_mod_assignment() -> None:
    src = '@a %= @b'
    expected_tokens = [
        ('NAME', 'a'),
        ('MOD_ASSIGN', '%='),
        ('NAME', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_power_assignment() -> None:
    src = '@a **= @b'
    expected_tokens = [
        ('NAME', 'a'),
        ('POWER_ASSIGN', '**='),
        ('NAME', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_int_div_assignment() -> None:
    src = '@a //= @b'
    expected_tokens = [
        ('NAME', 'a'),
        ('INT_DIV_ASSIGN', '//='),
        ('NAME', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_concat_assignment() -> None:
    src = '@a ++= @b'
    expected_tokens = [
        ('NAME', 'a'),
        ('CONCAT_ASSIGN', '++='),
        ('NAME', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_seq_and_assignment() -> None:
    src = '@a &&= @b'
    expected_tokens = [
        ('NAME', 'a'),
        ('SEQ_AND_ASSIGN', '&&='),
        ('NAME', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_seq_or_assignment() -> None:
    src = '@a ||= @b'
    expected_tokens = [
        ('NAME', 'a'),
        ('SEQ_OR_ASSIGN', '||='),
        ('NAME', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_pipe_assignment() -> None:
    src = '@a |= @b'
    expected_tokens = [
        ('NAME', 'a'),
        ('PIPE_ASSIGN', '|='),
        ('NAME', 'b'),
    ]
    assert get_tokens(src) == expected_tokens


def test_assertion() -> None:
    src = 'assert 1 == one()'
    expected_tokens = [
        ('ASSERT', 'assert'),
        ('INTEGER', '1'),
        ('EQUALS', '=='),
        ('NAME', 'one'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(src) == expected_tokens


def test_const_declare() -> None:
    src = 'const a := 1'
    expected_tokens = [
        ('CONST', 'const'),
        ('NAME', 'a'),
        ('DECLARE', ':='),
        ('INTEGER', '1'),
    ]
    assert get_tokens(src) == expected_tokens


def test_say() -> None:
    src = 'say a b c'
    expected_tokens = [
        ('SAY', 'say'),
        ('EXEC_ARG', 'a'),
        ('EXEC_ARG', 'b'),
        ('EXEC_ARG', 'c'),
    ]
    assert get_tokens(src) == expected_tokens


def test_if_elif_else() -> None:
    src = 'if true {} elif false {} else if true {} else {}'
    expected_tokens = [
        ('IF', 'if'),
        ('TRUE', 'true'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
        ('ELIF', 'elif'),
        ('FALSE', 'false'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
        ('ELSE', 'else'),
        ('IF', 'if'),
        ('TRUE', 'true'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
        ('ELSE', 'else'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(src) == expected_tokens
