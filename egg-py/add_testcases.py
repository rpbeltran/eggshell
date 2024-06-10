#!/usr/bin/env python3

import os

import frontend.lexer_test as lexer_test
import frontend.parser_test as parser_test
import frontend.lowering_test as lowering_test
import backend.py_generator_test as pygen_test


here = os.path.dirname(__file__)
lexer_test_path = f'{here}/parsing/lexer_test.py'
parser_test_path = f'{here}/parsing/parser_test.py'
lowering_test_path = f'{here}/parsing/lowering_test.py'
pygen_test_path = f'{here}/backend/py_generator_test.py'


def make_lexer_test_code(test_name, src) -> str:
    token_string = '\n'.join(
        f'        {tok},' for tok in lexer_test.get_tokens(src)
    )
    return f"""\n
def test_{test_name}():
    src = {repr(src)}
    expected_tokens = [\n{token_string}\n    ]
    assert get_tokens(src) == expected_tokens\n"""


def make_parser_test_code(test_name, src, ast) -> str:
    ast_lines = ast.split('\n')
    expected_ast_inner = '\n'.join(
        ' ' * 8 + repr(f'\n{line}' if i != 0 else line)
        for i, line in enumerate(ast_lines)
    )
    return f"""\n
def test_{test_name}():
    src = {repr(src)}
    expected_ast = (\n{expected_ast_inner}\n    )
    assert get_ast(src) == expected_ast\n"""


def make_backend_test_code(test_name, src, gen_code) -> str:
    gen_code_lines = gen_code.split('\n')
    if len(gen_code_lines) > 1:
        expected_gen_code_inner = '\n'.join(
            ' ' * 8 + repr(f'\n{line}' if i != 0 else line)
            for i, line in enumerate(gen_code_lines)
        )
        expected_gen_code = f'(\n{expected_gen_code_inner}\n    )'
    else:
        expected_gen_code = repr(gen_code)

    return f"""\n
def test_{test_name}():
    src = {repr(src)}
    expected_gen_code = {expected_gen_code}
    assert get_gen_code(src) == expected_gen_code\n"""


def main():
    with open(lexer_test_path, 'a') as test_file:
        for name, code in lexer_test.new_test_cases.items():
            test_file.write(make_lexer_test_code(name, code))

    with open(parser_test_path, 'a') as test_file:
        for name, code in parser_test.new_test_cases.items():
            ast = parser_test.get_ast(code)
            test_file.write(make_parser_test_code(name, code, ast))

    with open(lowering_test_path, 'a') as test_file:
        for name, code in lowering_test.new_test_cases.items():
            ast = lowering_test.get_ast(code)
            test_file.write(make_parser_test_code(name, code, ast))

    with open(pygen_test_path, 'a') as test_file:
        for name, code in pygen_test.new_test_cases.items():
            code_gen = pygen_test.get_gen_code(code)
            test_file.write(make_backend_test_code(name, code, code_gen))


if __name__ == '__main__':
    main()
