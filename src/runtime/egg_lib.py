import typing
from enum import Enum

from ..runtime import external_commands
from ..runtime.memory import Memory
from ..runtime.types.collections import List, Range, String
from ..runtime.types.functional import LambdaExpression
from ..runtime.types.numeric import Boolean, Float, Integer, UnitValue
from ..runtime.types.objects import ComparisonResult, Object


def make_external_command(*args: str) -> external_commands.ExternalCommand:
    return external_commands.ExternalCommand(args)


def make_pipeline(*args: Object) -> external_commands.Pipeline:
    return external_commands.Pipeline(args)


def make_string(data: str) -> String:
    return String(data)


def make_integer(value: int) -> Integer:
    return Integer(value)


def make_float(value: float) -> Float:
    return Float(value)


def make_boolean(value: bool) -> Boolean:
    return Boolean(value)


def make_unit_value(
    unit_type: str, unit: str, quantity: int | float
) -> UnitValue:
    return UnitValue(unit_type, unit, quantity)


def make_list(*data: typing.List) -> List:
    return List(data)


def make_range(start: Integer, end: Integer) -> Range:
    return Range(start, end, Integer(1))


def make_lambda(
    memory: Memory,
    args: typing.List[str],
    expr: typing.Callable[[], Object | None],
) -> LambdaExpression:
    return LambdaExpression(memory, args, expr)


class ComparisonType(Enum):
    EQUAL = 1
    UNEQUAL = 2
    LESS = 3
    LTE = 4
    GREATER = 5
    GTE = 6


def do_comparisons(*args: Object | ComparisonType) -> bool:
    assert len(args) >= 3
    assert len(args) % 2 == 1
    for i in range(0, len(args) - 2, 2):
        a, op, b = args[i : i + 3]
        assert isinstance(a, Object)
        assert isinstance(b, Object)
        if op == ComparisonType.EQUAL:
            if not (a.equals(b)):
                return False
        elif op == ComparisonType.UNEQUAL:
            if not (not a.equals(b)):
                return False
        elif op == ComparisonType.LESS:
            if not (a.compare(b) == ComparisonResult.LESS):
                return False
        elif op == ComparisonType.LTE:
            if not (a.compare(b) != ComparisonResult.GREATER):
                return False
        elif op == ComparisonType.GREATER:
            if not (a.compare(b) == ComparisonResult.GREATER):
                return False
        elif op == ComparisonType.GTE:
            if not (a.compare(b) != ComparisonResult.LESS):
                return False
    return True


def assertion(condition: Boolean) -> None:
    assert condition


def say(arg: Object) -> None:
    print(arg)
