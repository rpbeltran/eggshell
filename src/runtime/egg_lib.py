import typing
from enum import Enum

from ..runtime import external_commands, types


def make_external_command(
    *args: typing.Iterable[types.Object],
) -> external_commands.ExternalCommand:
    return external_commands.ExternalCommand(args)


def make_pipeline(
    *args: typing.Iterable[types.Object],
) -> external_commands.Pipeline:
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


def make_range(start: types.Integer, end: types.Integer) -> types.Range:
    return types.Range(start, end, types.Integer(1))


def make_lambda(args: typing.List[str], expr: str) -> types.LambdaExpression:
    return types.LambdaExpression(args, expr)


class ComparisonType(Enum):
    EQUAL = 1
    UNEQUAL = 2
    LESS = 3
    LTE = 4
    GREATER = 5
    GTE = 6


def do_comparisons(*args: types.Object | ComparisonType) -> bool:
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


def assertion(condition: types.Boolean) -> None:
    assert condition


def say(arg: types.Object) -> None:
    print(arg)
