import os

import parsing.lexer_test as lexer_test
import parsing.parser_test as parser_test


here = os.path.dirname(__file__)
lexer_test_path = f'{here}/parsing/lexer_test.py'
parser_test_path = f'{here}/parsing/parser_test.py'


def get_lexer_test_code(test_name, src) -> str:
    token_string = '\n'.join( ' '*8 + tok for tok in lexer_test.get_tokens(src))
    return f"""\n
def test_{test_name}():
    src = {repr(src)}
    expected_tokens = [\n{token_string}\n    ]
    assert get_tokens(src) == expected_tokens\n"""


def make_parser_test_code(test_name, src) -> str:
    ast_lines = parser_test.get_ast(src).split('\n')
    expected_ast_inner = '\n'.join(
        ' '*8 + repr(f'\n{line}' if i != 0 else line)
        for i, line in enumerate(ast_lines)
    )

    return f"""\n
def test_{test_name}():
    src = {repr(src)}
    expected_ast = (\n{expected_ast_inner}\n    )
    assert get_ast(src) == expected_ast\n"""


def main():
    with open(lexer_test_path, 'a') as test_file:
        for name, code in lexer_test.new_test_cases.items():
            test_file.write(get_lexer_test_code(name, code))

    with open(parser_test_path, 'a') as test_file:
        for name, code in parser_test.new_test_cases.items():
            test_file.write(make_parser_test_code(name, code))


main()
