from abc import ABC, abstractmethod
from typing import NamedTuple


class Number(ABC):
    @abstractmethod
    def val(self) -> int | float:
        pass

    def add(self, other):
        return self.wrap(value=self.val() + other.val())

    def subtract(self, other):
        return self.wrap(value=self.val() - other.val())

    def multiply(self, other):
        return self.wrap(value=self.val() * other.val())

    def divide(self, other):
        return self.wrap(value=self.val() / other.val())

    def int_divide(self, other):
        return self.wrap(value=self.val() // other.val())

    def modulus(self, other):
        return self.wrap(value=self.val() % other.val())

    def raise_power(self, other):
        return self.wrap(value=self.val() ** other.val())

    def __str__(self):
        return str(self.val())

    @staticmethod
    def wrap(value: int | float):
        if isinstance(value, int):
            return Integer(value)
        elif isinstance(value, float):
            return Float(value)
        raise TypeError(f'Number type cannot wrap value {value}')


class Integer(Number):
    __slots__ = ('__value',)

    def __init__(self, value: int):
        assert isinstance(value, int)
        self.__value = value

    def val(self) -> int:
        return self.__value


class Float(Number):
    __slots__ = ('__value',)

    def __init__(self, value: float):
        assert isinstance(value, float)
        self.__value = value

    def val(self) -> float:
        return self.__value


class Boolean:
    __slots__ = ('__value',)

    def __init__(self, value: bool):
        assert isinstance(value, bool)
        self.__value = value

    def val(self) -> bool:
        return self.__value

    def logical_and(self, other: 'Boolean') -> 'Boolean':
        return Boolean(self.val() and other.val())

    def logical_or(self, other: 'Boolean') -> 'Boolean':
        return Boolean(self.val() or other.val())

    def logical_xor(self, other: 'Boolean') -> 'Boolean':
        return Boolean(self.val() != other.val())

    def __bool__(self):
        return self.__value

    def __str__(self):
        return 'true' if self.__value else 'false'


class UnitValue(NamedTuple):
    unit_type: str
    unit: str
    value: int | float

    def __str__(self):
        return f'{self.value}{self.unit}'


class String:
    __slots__ = ('__data',)

    def __init__(self, data: str):
        assert isinstance(data, str)
        self.__data = data

    def concatenate(self, other: 'String') -> 'String':
        return String(self.data() + other.data())

    def data(self) -> str:
        return self.__data

    def __str__(self):
        return self.__data
