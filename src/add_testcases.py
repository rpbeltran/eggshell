#!/usr/bin/env python3

import os
import sys
from typing import Optional

src_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(src_dir)

import src.frontend.lexer_test as lexer_test
import src.frontend.lowering_test as lowering_test
import src.frontend.parser_test as parser_test
import src.yolk.yolk_test as yolk_test

here = os.path.dirname(__file__)
lexer_test_path = f'{here}/frontend/lexer_test.py'
parser_test_path = f'{here}/frontend/parser_test.py'
lowering_test_path = f'{here}/frontend/lowering_test.py'
pygen_test_path = f'{here}/backend_py/py_generator_test.py'
runtime_test_path = f'{here}/backend_py/runtime/runtime_test.py'
yolk_test_path = f'{here}/yolk/yolk_test.py'


def make_lexer_test_code(test_name: str, src: str) -> str:
    token_string = '\n'.join(
        f'        {tok},' for tok in lexer_test.get_tokens(src)
    )
    return f"""\n
def test_{test_name}() -> None:
    src = {repr(src)}
    expected_tokens = [\n{token_string}\n    ]
    assert get_tokens(src) == expected_tokens\n"""


def make_parser_test_code(test_name: str, src: str, ast: str) -> str:
    ast_lines = ast.split('\n')
    expected_ast_inner = '\n'.join(
        ' ' * 8 + repr(f'\n{line}' if i != 0 else line)
        for i, line in enumerate(ast_lines)
    )
    return f"""\n
def test_{test_name}() -> None:
    src = {repr(src)}
    expected_ast = (\n{expected_ast_inner}\n    )
    assert get_ast(src) == expected_ast\n"""


def make_backend_test_code(test_name: str, src: str, gen_code: str) -> str:
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
def test_{test_name}() -> None:
    src = {repr(src)}
    expected_gen_code = {expected_gen_code}
    assert get_gen_code(src) == expected_gen_code\n"""


def make_runtime_test_code(
    test_name: str, src: str, output: Optional[str]
) -> str:
    output_lines = output.split('\n') if output is not None else []
    if len(output_lines) > 1:
        expected_gen_code_inner = '\n'.join(
            ' ' * 8 + repr(f'\n{line}' if i != 0 else line)
            for i, line in enumerate(output_lines)
        )
        expected_output = f'(\n{expected_gen_code_inner}\n    )'
    else:
        expected_output = repr(output)
    return f"""\n
def test_{test_name}() -> None:
    src = {repr(src)}
    expected_output = {expected_output}
    assert execute_src(src) == expected_output\n"""


def main() -> None:
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

    with open(yolk_test_path, 'a') as test_file:
        for name, code in yolk_test.new_test_cases.items():
            code_gen = yolk_test.get_gen_code(code)
            test_file.write(make_backend_test_code(name, code, code_gen))


if __name__ == '__main__':
    main()
