from typing import Dict

from ..frontend.parser import get_parser
from .py_generator import PythonGenerator, transform_pygen_result

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
pygen = PythonGenerator()


def get_gen_code(src: str) -> str:
    ast = parser.parse(src)
    return transform_pygen_result(pygen.transform(ast))


def test_add() -> None:
    src = '1 + 2'
    expected_gen_code = '_e.make_integer(1).add(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_subtract() -> None:
    src = '1 - 2'
    expected_gen_code = '_e.make_integer(1).subtract(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_multiply() -> None:
    src = '1 * 2'
    expected_gen_code = '_e.make_integer(1).multiply(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_divide() -> None:
    src = '1 / 2'
    expected_gen_code = '_e.make_integer(1).divide(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_int_divide() -> None:
    src = '1 // 2'
    expected_gen_code = '_e.make_integer(1).int_divide(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_modulus() -> None:
    src = '1 % 2'
    expected_gen_code = '_e.make_integer(1).modulus(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_raise_power() -> None:
    src = '1 ** 2'
    expected_gen_code = '_e.make_integer(1).raise_power(_e.make_integer(2))'
    assert get_gen_code(src) == expected_gen_code


def test_external_command() -> None:
    src = 'foo -o bar'
    expected_gen_code = "_e.make_external_command('foo','-o','bar')"
    assert get_gen_code(src) == expected_gen_code


def test_explicit_exec() -> None:
    src = '`"foo bar" -o hello`'
    expected_gen_code = "_e.make_external_command('foo bar','-o','hello')"
    assert get_gen_code(src) == expected_gen_code


def test_pipeline() -> None:
    src = 'a b | c d'
    expected_gen_code = (
        "_e.make_pipeline(_e.make_external_command('a','b')"
        ",_e.make_external_command('c','d'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_pipeline_data() -> None:
    src = '1 | a'
    expected_gen_code = (
        "_e.make_pipeline(_e.make_integer(1),_e.make_external_command('a'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_comparison_chain() -> None:
    src = '1 < 2 <= 3 == 3 != 20 >= 18 > 1'
    expected_gen_code = (
        '_e.do_comparisons(_e.make_integer(1),_e.ComparisonType.LESS,'
        '_e.make_integer(2),_e.ComparisonType.LTE,'
        '_e.make_integer(3),_e.ComparisonType.EQUAL,'
        '_e.make_integer(3),_e.ComparisonType.UNEQUAL,'
        '_e.make_integer(20),_e.ComparisonType.GTE,'
        '_e.make_integer(18),_e.ComparisonType.GREATER,_e.make_integer(1))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_unit_values() -> None:
    src = '10gb'
    expected_gen_code = "_e.make_unit_value('size', 'gb', 10)"
    assert get_gen_code(src) == expected_gen_code


def test_floats_and_ints() -> None:
    src = '1 + 1.0 - 2 * 3.0'
    expected_gen_code = (
        '_e.make_integer(1).add(_e.make_float(1.0))'
        '.subtract(_e.make_integer(2).multiply(_e.make_float(3.0)))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_and() -> None:
    src = 'true and false and true'
    expected_gen_code = (
        '_e.make_boolean(True).logical_and(_e.make_boolean(False))'
        '.logical_and(_e.make_boolean(True))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_or() -> None:
    src = 'true or false or true'
    expected_gen_code = (
        '_e.make_boolean(True).logical_or(_e.make_boolean(False))'
        '.logical_or(_e.make_boolean(True))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_xor() -> None:
    src = 'true xor false xor true'
    expected_gen_code = (
        '_e.make_boolean(True).logical_xor(_e.make_boolean(False))'
        '.logical_xor(_e.make_boolean(True))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_assertions() -> None:
    src = 'assert true'
    expected_gen_code = '_e.assertion(_e.make_boolean(True))'
    assert get_gen_code(src) == expected_gen_code


def test_string() -> None:
    src = '"hello world"'
    expected_gen_code = "_e.make_string('hello world')"
    assert get_gen_code(src) == expected_gen_code


def test_concatenate() -> None:
    src = '"hello " ++ "world" ++ "!!!"'
    expected_gen_code = (
        "_e.make_string('hello ').concatenate(_e.make_string('world'))"
        ".concatenate(_e.make_string('!!!'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_unary_not() -> None:
    src = '! true'
    expected_gen_code = '_e.make_boolean(True).logical_not()'
    assert get_gen_code(src) == expected_gen_code


def test_unary_not2() -> None:
    src = 'not true'
    expected_gen_code = '_e.make_boolean(True).logical_not()'
    assert get_gen_code(src) == expected_gen_code


def test_unary_negate() -> None:
    src = '-(10)'
    expected_gen_code = '_e.make_integer(10).negate()'
    assert get_gen_code(src) == expected_gen_code


def test_make_list() -> None:
    src = '[1,`a`]'
    expected_gen_code = (
        "_e.make_list(_e.make_integer(1),_e.make_external_command('a'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_make_empty_list() -> None:
    src = '[]'
    expected_gen_code = '_e.make_list()'
    assert get_gen_code(src) == expected_gen_code


def test_make_list_one_elem() -> None:
    src = '[1]'
    expected_gen_code = '_e.make_list(_e.make_integer(1))'
    assert get_gen_code(src) == expected_gen_code


def test_select_element() -> None:
    src = '[1,2,3][1]'
    expected_gen_code = (
        '_e.make_list(_e.make_integer(1),_e.make_integer(2),_e.make_integer(3))'
        '.select_element(_e.make_integer(1))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_select_element_str() -> None:
    src = '"hello world"[1]'
    expected_gen_code = (
        "_e.make_string('hello world')"
        ".select_element(_e.make_integer(1))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_select_slice() -> None:
    src = '[1,2,3][1:3]'
    expected_gen_code = (
        '_e.make_list(_e.make_integer(1),_e.make_integer(2),_e.make_integer(3))'
        '.select_slice(_e.make_integer(1),_e.make_integer(3),None)'
    )
    assert get_gen_code(src) == expected_gen_code


def test_select_slice_str() -> None:
    src = '"hello world"[1:3]'
    expected_gen_code = (
        "_e.make_string('hello world')"
        ".select_slice(_e.make_integer(1),_e.make_integer(3),None)"
    )
    assert get_gen_code(src) == expected_gen_code


def test_select_slice_jump() -> None:
    src = '[1,2,3][1:2 by 3]'
    expected_gen_code =(
        '_e.make_list(_e.make_integer(1),_e.make_integer(2),_e.make_integer(3))'
        '.select_slice(_e.make_integer(1),_e.make_integer(2),_e.make_integer(3))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_select_slice_str_jump() -> None:
    src = '"hello world"[:3 by -1]'
    expected_gen_code = (
        "_e.make_string('hello world')"
        ".select_slice(None,_e.make_integer(3),_e.make_integer(1).negate())"
    )
    assert get_gen_code(src) == expected_gen_code


def test_ranges() -> None:
    src = '(5..15)'
    src_square = '[5..15]'
    expected_gen_code = '_e.make_range(_e.make_integer(5),_e.make_integer(15))'
    assert get_gen_code(src) == get_gen_code(src_square) == expected_gen_code


def test_declare_untyped_variable() -> None:
    src = 'a := 1'
    expected_gen_code = "_m.new(_e.make_integer(1), name='a')"
    assert get_gen_code(src) == expected_gen_code


def test_const_declare() -> None:
    src = 'const a := 1'
    expected_gen_code = "_m.new(_e.make_integer(1), name='a', const=True)"
    assert get_gen_code(src) == expected_gen_code


def test_identifier() -> None:
    src = '@foo'
    expected_gen_code = "_m.get_object_by_name('foo')"
    assert get_gen_code(src) == expected_gen_code


def test_reassignment() -> None:
    src = 'a = 5'
    expected_gen_code = "_m.update_var('a', _e.make_integer(5))"
    assert get_gen_code(src) == expected_gen_code


def test_say() -> None:
    src = 'say 1 + 10'
    expected_gen_code = '_e.say(_e.make_integer(1).add(_e.make_integer(10)))'
    assert get_gen_code(src) == expected_gen_code


def test_say_resolve_name() -> None:
    src = 'say @i'
    expected_gen_code = "_e.say(_m.get_object_by_name('i'))"
    assert get_gen_code(src) == expected_gen_code


def test_add_resolve_name() -> None:
    src = '@a + @b'
    expected_gen_code = (
        "_m.get_object_by_name('a').add(_m.get_object_by_name('b'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_multiple_lines() -> None:
    src = 'a := 5; a = 7; say @a ** 2'
    expected_gen_code = (
        "_m.new(_e.make_integer(5), name='a')"
        "\n_m.update_var('a', _e.make_integer(7))"
        "\n_e.say(_m.get_object_by_name('a').raise_power(_e.make_integer(2)))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_if_basic() -> None:
    src = 'if true {say "hello world"}'
    expected_gen_code = (
        'if _e.make_boolean(True):'
        "\n\t_e.say(_e.make_string('hello world'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_if_elif_else() -> None:
    src = 'if @x {say 1} elif @y {say 2} else if @z {say 3} else {say 4}'
    expected_gen_code = (
        "if _m.get_object_by_name('x'):"
        '\n\t_e.say(_e.make_integer(1))'
        "\nelif _m.get_object_by_name('y'):"
        '\n\t_e.say(_e.make_integer(2))'
        "\nelif _m.get_object_by_name('z'):"
        '\n\t_e.say(_e.make_integer(3))'
        '\nelse:'
        '\n\t_e.say(_e.make_integer(4))'
    )
    assert get_gen_code(src) == expected_gen_code


def test_declare_name_via_name() -> None:
    src = 'a := @b'
    expected_gen_code = "_m.new(_m.get_object_by_name('b'), name='a')"
    assert get_gen_code(src) == expected_gen_code


def test_lambda() -> None:
    src = '\\x -> @x'
    expected_gen_code = (
        "_e.make_lambda(_m,['x'],lambda: _m.get_object_by_name('x'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_lambda2() -> None:
    src = '\\(x, y) -> @x + @y'
    expected_gen_code = (
        "_e.make_lambda(_m,['x', 'y'],"
        "lambda: _m.get_object_by_name('x').add(_m.get_object_by_name('y')))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_implicit_lambda() -> None:
    src = '_'
    expected_gen_code = (
        "_e.make_lambda(_m,['@@implicit_lambda@@'],"
        "lambda: _m.get_object_by_name('@@implicit_lambda@@'))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_implicit_lambda2() -> None:
    src = '_ + _'
    expected_gen_code = (
        "_e.make_lambda(_m,['@@implicit_lambda@@'],"
        "lambda: _m.get_object_by_name('@@implicit_lambda@@')"
        ".add(_m.get_object_by_name('@@implicit_lambda@@')))"
    )
    assert get_gen_code(src) == expected_gen_code


def test_empty_if() -> None:
    src = 'if true {}'
    expected_gen_code = (
        'if _e.make_boolean(True):'
        '\n\tpass'
    )
    assert get_gen_code(src) == expected_gen_code


def test_while() -> None:
    src = 'x := 5\nwhile @x > 0 {\n\tsay x\n\tx -= 1}'
    expected_gen_code = (
        "_m.new(_e.make_integer(5), name='x')"
        "\nwhile _e.do_comparisons(_m.get_object_by_name('x'),_e.ComparisonType.GREATER,_e.make_integer(0)):"
        "\n\t_e.say(_m.get_object_by_name('x'))"
        "\n\t_m.update_var('x', _m.get_object_by_name('x').subtract(_e.make_integer(1)))"
    )
    assert get_gen_code(src) == expected_gen_code
