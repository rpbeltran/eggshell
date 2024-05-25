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
