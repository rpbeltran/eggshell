import os

import parsing.lexer_test as lexer_test


here = os.path.dirname(__file__)
lexer_test_path = f"{here}/parsing/lexer_test.py"


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


def update_lexer_tests():
    with open(lexer_test_path, "a") as test_file:
        for name, code in lexer_test.new_test_cases.items():
            test_file.write(get_lexer_test_code(name, code))


update_lexer_tests()