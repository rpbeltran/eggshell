from .string_utilities import repr_double_quoted


def test_repr_double_quoted() -> None:

    test_cases = {
        'foo': '"foo"',
        "h'i": '"h\'i"',
        "'foo'": '"\'foo\'"',
        'h"i': '"h\\"i"',
        '"foo"': '"\\"foo\\""',
    }

    for test_case, expected in test_cases.items():
        assert repr_double_quoted(test_case) == expected
