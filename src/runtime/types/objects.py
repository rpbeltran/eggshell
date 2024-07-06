import typing
from abc import ABC, abstractmethod
from enum import Enum


class ComparisonResult(Enum):
    EQUAL = (0,)
    LESS = (1,)
    GREATER = 2


class Object(ABC):
    @abstractmethod
    def equals(self, other: 'Object') -> bool:
        ...

    @abstractmethod
    def compare(self, other: 'Object') -> ComparisonResult:
        ...
