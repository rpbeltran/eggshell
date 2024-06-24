from .egg_lib import *
from .types import Integer, Float


def test_do_comparisons() -> None:
    true_cases: typing.List[typing.List[types.Object | ComparisonType]] = [
        [Integer(1), ComparisonType.LESS, Integer(2)],
        [Integer(1), ComparisonType.LTE, Integer(2)],
        [Integer(1), ComparisonType.LTE, Integer(1)],
        [Integer(2), ComparisonType.GREATER, Integer(1)],
        [Integer(2), ComparisonType.GTE, Integer(1)],
        [Float(2.0), ComparisonType.GTE, Integer(2)],
        [Float(2.0), ComparisonType.EQUAL, Integer(2)],
        [Integer(2), ComparisonType.UNEQUAL, Float(1.0)],
        [Integer(2), ComparisonType.UNEQUAL, Float(3.0)],
        [Integer(1), ComparisonType.UNEQUAL, Integer(2), ComparisonType.UNEQUAL, Integer(3)],
    ]
    false_cases: typing.List[typing.List[types.Object | ComparisonType]] = [
        [Integer(2), ComparisonType.LESS, Integer(1)],
        [Integer(2), ComparisonType.LESS, Integer(2)],
        [Integer(3), ComparisonType.LTE, Integer(2)],
        [Integer(1), ComparisonType.GREATER, Integer(2)],
        [Integer(1), ComparisonType.GREATER, Integer(1)],
        [Float(1.0), ComparisonType.GTE, Integer(2)],
        [Float(1.0), ComparisonType.EQUAL, Integer(2)],
        [Integer(2), ComparisonType.EQUAL, Float(1.0)],
        [Integer(1), ComparisonType.UNEQUAL, Float(1.0)],
        [Integer(1), ComparisonType.UNEQUAL, Integer(2), ComparisonType.UNEQUAL, Integer(2)],
        [Integer(2), ComparisonType.UNEQUAL, Integer(2), ComparisonType.UNEQUAL, Integer(1)],
    ]
    for case in true_cases:
        assert do_comparisons(*case)
    for case in false_cases:
        assert not do_comparisons(*case)
