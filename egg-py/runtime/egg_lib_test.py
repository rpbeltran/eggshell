from .egg_lib import *


def do_comparisons_test():
    true_cases = [
        [1, ComparisonType.LESS, 2],
        [1, ComparisonType.LTE, 2],
        [1, ComparisonType.LTE, 1],
        [2, ComparisonType.GREATER, 1],
        [2, ComparisonType.GTE, 1],
        [2, ComparisonType.GTE, 2],
        [2, ComparisonType.EQUAL, 2],
        [2, ComparisonType.UNEQUAL, 1],
        [2, ComparisonType.UNEQUAL, 3],
        [1, ComparisonType.UNEQUAL, 2, ComparisonType.UNEQUAL, 3],
    ]
    false_cases = [
        [2, ComparisonType.LESS, 1],
        [2, ComparisonType.LESS, 2],
        [3, ComparisonType.LTE, 2],
        [1, ComparisonType.GREATER, 2],
        [1, ComparisonType.GREATER, 1],
        [1, ComparisonType.GTE, 2],
        [1, ComparisonType.EQUAL, 2],
        [2, ComparisonType.EQUAL, 1],
        [1, ComparisonType.UNEQUAL, 1],
        [1, ComparisonType.UNEQUAL, 2, ComparisonType.UNEQUAL, 2],
        [2, ComparisonType.UNEQUAL, 2, ComparisonType.UNEQUAL, 1],
    ]
    for case in true_cases:
        assert do_comparisons(*case)
    for case in false_cases:
        assert not do_comparisons(*case)
