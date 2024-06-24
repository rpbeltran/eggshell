from enum import Enum
import typing

from ..runtime import external_commands
from ..runtime import types


def make_external_command(*args):
    return external_commands.ExternalCommand(args)


def make_pipeline(*args):
    return external_commands.Pipeline(args)


def make_string(data: str) -> types.String:
    return types.String(data)


def make_integer(value: int) -> types.Integer:
    return types.Integer(value)


def make_float(value: float) -> types.Float:
    return types.Float(value)


def make_boolean(value: bool) -> types.Boolean:
    return types.Boolean(value)


def make_unit_value(
    unit_type: str, unit: str, quantity: int | float
) -> types.UnitValue:
    return types.UnitValue(unit_type, unit, quantity)


def make_list(*data: typing.List) -> types.List:
    return types.List(data)


def make_range(start: types.Integer, end: types.Integer) -> types.List:
    return types.Range(start, end, types.Integer(1))


class ComparisonType(Enum):
    EQUAL = 1
    UNEQUAL = 2
    LESS = 3
    LTE = 4
    GREATER = 5
    GTE = 6


def do_comparisons(*args):
    assert len(args) >= 3
    assert len(args) % 2 == 1
    for i in range(0, len(args) - 2, 2):
        a, op, b = args[i : i + 3]
        assert isinstance(a, types.Object)
        assert isinstance(b, types.Object)
        if op == ComparisonType.EQUAL:
            if not (a.equals(b)):
                return False
        elif op == ComparisonType.UNEQUAL:
            if not (not a.equals(b)):
                return False
        elif op == ComparisonType.LESS:
            if not (a.compare(b) == types.ComparisonResult.LESS):
                return False
        elif op == ComparisonType.LTE:
            if not (a.compare(b) != types.ComparisonResult.GREATER):
                return False
        elif op == ComparisonType.GREATER:
            if not (a.compare(b) == types.ComparisonResult.GREATER):
                return False
        elif op == ComparisonType.GTE:
            if not (a.compare(b) != types.ComparisonResult.LESS):
                return False
    return True


def assertion(condition: types.Boolean):
    assert condition


def say(arg):
    print(arg)
