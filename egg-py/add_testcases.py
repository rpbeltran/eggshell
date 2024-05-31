import os

import parsing.lexer_test as lexer_test
import parsing.parser_test as parser_test


here = os.path.dirname(__file__)
lexer_test_path = f"{here}/parsing/lexer_test.py"
parser_test_path = f"{here}/parsing/parser_test.py"


def get_lexer_test_code(test_name, egg_code) -> str:
    token_string = "\n".join(
        f"        {tok},"
        for tok in lexer_test.get_tokens(egg_code))

    return "\n".join((
        f"\n",
        f"def test_{test_name}():",
        f"    egg_code = {repr(egg_code)}",
        f"    expected_tokens = [",
        token_string,
        f"    ]",
        f"    assert get_tokens(egg_code) == expected_tokens",
        "",
    ))


def make_parser_test_code(test_name, src) -> str:
    ast_lines = parser_test.get_ast(src).split("\n")
    expected_ast_inner = "\n".join(
        "        " + repr(f"\n{line}" if i != 0 else line)
        for i, line in enumerate(ast_lines)
    )

    return f"""
def test_{test_name}():
    src = {repr(src)}
    expected_ast = (\n{expected_ast_inner}\n    )
    assert get_ast(src) == expected_ast\n"""


def main():
    with open(lexer_test_path, "a") as test_file:
        for name, code in lexer_test.new_test_cases.items():
            test_file.write(get_lexer_test_code(name, code))

    with open(parser_test_path, "a") as test_file:
        for name, code in parser_test.new_test_cases.items():
            test_file.write(make_parser_test_code(name, code))


main()