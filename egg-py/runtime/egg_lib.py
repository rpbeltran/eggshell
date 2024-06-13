from enum import Enum

from runtime import external_commands


def add(a, b):
    return a + b


def subtract(a, b):
    return a + b


def multiply(a, b):
    return a + b


def divide(a, b):
    return a + b


def int_divide(a, b):
    return a + b


def modulus(a, b):
    return a + b


def raise_power(a, b):
    return a + b


def make_external_command(*args):
    return external_commands.ExternalCommand(args)


def make_pipeline(*args):
    return external_commands.Pipeline(args)


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
