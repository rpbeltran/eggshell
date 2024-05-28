from typing import Dict

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
new_test_cases: Dict[str,str] = {}


def get_tokens(egg: str):
    return [
        (token.token_type, token.source)
        for token in EggLexer().lex(egg)
    ]


def test_basic_pipe():
    egg_code = 'a | b'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('PIPE', '|'),
        ('EXEC_ARG', 'b'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_basic_pipe3():
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


def test_try():
    egg_code = 'try{\n\t`a` }'
    expected_tokens = [
        ('TRY', 'try'),
        ('CURLY_OPEN', '{'),
        ('EXEC_ARG', 'a'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_try_catch():
    egg_code = 'try{ `a` }\ncatch{ b }'
    expected_tokens = [
        ('TRY', 'try'),
        ('CURLY_OPEN', '{'),
        ('EXEC_ARG', 'a'),
        ('CURLY_CLOSE', '}'),
        ('CATCH', 'catch'),
        ('CURLY_OPEN', '{'),
        ('NAME', 'b'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_semicolons():
    egg_code = 'a ; b ; c'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('SEMICOLON', ';'),
        ('EXEC_ARG', 'b'),
        ('SEMICOLON', ';'),
        ('EXEC_ARG', 'c'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_function_basic():
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


def test_function_return():
    egg_code = 'fn foo(): int {\n  ret 2\n}'
    expected_tokens = [
        ('FN', 'fn'),
        ('NAME', 'foo'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
        ('COLON', ':'),
        ('NAME', 'int'),
        ('CURLY_OPEN', '{'),
        ('RETURN', 'ret'),
        ('INTEGER', '2'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_function_arg():
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


def test_lambda():
    egg_code = '\\a -> b'
    expected_tokens = [
        ('LAMBDA', '\\'),
        ('NAME', 'a'),
        ('ARROW', '->'),
        ('EXEC_ARG', 'b'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_lambda2():
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


def test_lambda3():
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


def test_lambda_multi():
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


def test_identifiers():
    egg_code = '@a b @c'
    expected_tokens = [
        ('NAME', 'a'),
        ('EXEC_ARG', 'b'),
        ('NAME', 'c'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_declaration():
    egg_code = 'a := 1'
    expected_tokens = [
        ('NAME', 'a'),
        ('DECLARE', ':='),
        ('INTEGER', '1'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_typed_declaration():
    egg_code = 'a : int = 1'
    expected_tokens = [
        ('NAME', 'a'),
        ('COLON', ':'),
        ('NAME', 'int'),
        ('ASSIGN', '='),
        ('INTEGER', '1'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_quoted_executions():
    egg_code = '`a` {`b`}'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('CURLY_OPEN', '{'),
        ('EXEC_ARG', 'b'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_list():
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


def test_list_types():
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


def test_list_access():
    egg_code = 'a[1]'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('SQUARE_OPEN', '['),
        ('INTEGER', '1'),
        ('SQUARE_CLOSE', ']'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_list_access2():
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


def test_list_access3():
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


def test_list_access_var():
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


def test_currying():
    egg_code = 'a $ b $ c'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('CURRY', '$'),
        ('EXEC_ARG', 'b'),
        ('CURRY', '$'),
        ('EXEC_ARG', 'c'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_field_access():
    egg_code = '@a.b.c'
    expected_tokens = [
        ('NAME', 'a'),
        ('DOT', 'a.'),
        ('NAME', 'b'),
        ('DOT', 'b.'),
        ('NAME', 'c'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_comment():
    egg_code = 'a # hello \n #world \n b'
    expected_tokens = [
        ('EXEC_ARG', 'a'),
        ('EXEC_ARG', 'b'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_pass_by_function():
    egg_code = '@a...'
    expected_tokens = [
        ('NAME', 'a'),
        ('ELLIPSIS', '...'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_error_handling():
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


def test_try():
    egg_code = 'try{\n\t`a` }'
    expected_tokens = [
        ('TRY', 'try'),
        ('CURLY_OPEN', '{'),
        ('EXEC_ARG', 'a'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_try_catch():
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


def test_try_catch_arg():
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


def test_range():
    egg_code = '(a..b)'
    expected_tokens = [
        ('PAREN_OPEN', '('),
        ('NAME', 'a'),
        ('RANGE', '..'),
        ('NAME', 'b'),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_loop():
    egg_code = 'loop { }'
    expected_tokens = [
        ('ALWAYS_LOOP', 'loop'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_while():
    egg_code = 'while true { }'
    expected_tokens = [
        ('WHILE', 'while'),
        ('TRUE', 'true'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_for():
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


def test_async():
    egg_code = '~(`b`)'
    expected_tokens = [
        ('ASYNC', '~'),
        ('PAREN_OPEN', '('),
        ('EXEC_ARG', 'b'),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_import():
    egg_code = 'import "a"'
    expected_tokens = [
        ('IMPORT', 'import'),
        ('QUOTED_STRING', 'a'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_class():
    egg_code = 'class Thing {a: Int = 1, b: Int = 2 fn c(){}}'
    expected_tokens = [
        ('CLASS', 'class'),
        ('NAME', 'Thing'),
        ('CURLY_OPEN', '{'),
        ('NAME', 'a'),
        ('COLON', ':'),
        ('NAME', 'Int'),
        ('ASSIGN', '='),
        ('INTEGER', '1'),
        ('COMMA', ','),
        ('NAME', 'b'),
        ('COLON', ':'),
        ('NAME', 'Int'),
        ('ASSIGN', '='),
        ('INTEGER', '2'),
        ('FN', 'fn'),
        ('NAME', 'c'),
        ('PAREN_OPEN', '('),
        ('PAREN_CLOSE', ')'),
        ('CURLY_OPEN', '{'),
        ('CURLY_CLOSE', '}'),
        ('CURLY_CLOSE', '}'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_derived_class():
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


def test_map():
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


def test_math():
    egg_code = '(1 + 2 - 3 * 4 / 5 // 6 ** 7 ^ 8 % -9)'
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
        ('POWER', '^'),
        ('INTEGER', '8'),
        ('MOD', '%'),
        ('MINUS', '-'),
        ('INTEGER', '9'),
        ('PAREN_CLOSE', ')'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_math_root_level():
    egg_code = '1 (**) 2 (//) 3 (*) 4 (/) 5'
    expected_tokens = [
        ('INTEGER', '1'),
        ('POWER', '(**)'),
        ('INTEGER', '2'),
        ('INT_DIV', '(//)'),
        ('INTEGER', '3'),
        ('TIMES', '(*)'),
        ('INTEGER', '4'),
        ('DIVIDE', '(/)'),
        ('INTEGER', '5'),
    ]
    assert get_tokens(egg_code) == expected_tokens


def test_comparison():
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


def test_logic():
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
