from enum import Enum
from typing import NamedTuple

from runtime import external_commands
from runtime import types


def make_external_command(*args):
    return external_commands.ExternalCommand(args)


def make_pipeline(*args):
    return external_commands.Pipeline(args)


def make_integer(value: int) -> types.Integer:
    return types.Integer(value)


def make_float(value: float) -> types.Float:
    return types.Float(value)


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
        if op == ComparisonType.EQUAL:
            if not (a == b):
                return False
        elif op == ComparisonType.UNEQUAL:
            if not (a != b):
                return False
        elif op == ComparisonType.LTE:
            if not (a <= b):
                return False
        elif op == ComparisonType.LESS:
            if not (a < b):
                return False
        elif op == ComparisonType.GREATER:
            if not (a > b):
                return False
        elif op == ComparisonType.GTE:
            if not (a >= b):
                return False
    return True


def logical_or(a, b):
    return a or b


def logical_xor(a, b):
    return bool(a) != bool(b)


def logical_and(a, b):
    return a and b


class UnitValue(NamedTuple):
    unit_type: str
    unit: str
    value: int | float
