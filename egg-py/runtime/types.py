from abc import ABC, abstractmethod
from enum import Enum
import typing


class ComparisonResult(Enum):
    EQUAL = (0,)
    LESS = (1,)
    GREATER = 2


class Object(ABC):
    @abstractmethod
    def equals(self, other: 'Object'):
        ...

    @abstractmethod
    def compare(self, other: 'Object') -> ComparisonResult:
        ...


class Number(Object):
    @abstractmethod
    def val(self) -> int | float:
        ...

    def add(self, other) -> 'Number':
        return self.wrap(value=self.val() + other.val())

    def subtract(self, other) -> 'Number':
        return self.wrap(self.val() - other.val())

    def multiply(self, other) -> 'Number':
        return self.wrap(self.val() * other.val())

    def divide(self, other) -> 'Number':
        return self.wrap(self.val() / other.val())

    def int_divide(self, other) -> 'Number':
        return self.wrap(self.val() // other.val())

    def modulus(self, other) -> 'Number':
        return self.wrap(self.val() % other.val())

    def raise_power(self, other) -> 'Number':
        return self.wrap(self.val() ** other.val())

    def negate(self) -> 'Number':
        return self.wrap(-self.val())

    def equals(self, other: 'Object'):
        assert isinstance(other, Number)
        return self.val() == other.val()

    def compare(self, other: 'Object') -> ComparisonResult:
        assert isinstance(other, Number)
        a = self.val()
        b = other.val()
        if a == b:
            return ComparisonResult.EQUAL
        elif a < b:
            return ComparisonResult.LESS
        return ComparisonResult.GREATER

    def __str__(self):
        return str(self.val())

    @staticmethod
    def wrap(value: int | float) -> 'Number':
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


class Boolean(Object):
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

    def logical_not(self) -> 'Boolean':
        return Boolean(not self.val())

    def equals(self, other: 'Object'):
        assert isinstance(other, Boolean)
        return self.val() == other.val()

    def compare(self, other: 'Object') -> ComparisonResult:
        assert isinstance(other, Boolean)
        a = self.val()
        b = other.val()
        if a == b:
            return ComparisonResult.EQUAL
        elif a < b:
            return ComparisonResult.LESS
        return ComparisonResult.GREATER

    def __bool__(self):
        return self.__value

    def __str__(self):
        return 'true' if self.__value else 'false'


class UnitValue(Object):
    __slots__ = (
        '__unit_type',
        '__unit',
        '__value',
    )

    def __init__(self, unit_type: str, unit: str, value: int | float):
        self.__unit_type = unit_type
        self.__unit = unit
        self.__value = value

    def __str__(self):
        return f'{self.__value}{self.__unit}'

    def base_val(self) -> int | float:
        # todo: implement getting value in base unit quantity
        return self.__value

    def equals(self, other: 'Object'):
        assert isinstance(other, UnitValue)
        assert self.__unit_type == other.__unit_type
        return self.base_val() == other.base_val()

    def compare(self, other: 'Object') -> ComparisonResult:
        assert isinstance(other, UnitValue)
        assert self.__unit_type == other.__unit_type
        a = self.base_val()
        b = other.base_val()
        if a == b:
            return ComparisonResult.EQUAL
        elif a < b:
            return ComparisonResult.LESS
        return ComparisonResult.GREATER


class Collection(Object):
    @abstractmethod
    def data(self) -> str | list:
        ...

    def concatenate(self, other: 'Collection') -> 'Collection':
        assert (type(self) is String) == (type(other) is String)
        return self.wrap(self.data() + other.data())

    def size(self) -> int:
        return len(self.data())

    def select_element(self, index):
        return self.data()[index.val()]

    def select_slice(self, start, end, jump):
        if start is not None:
            start = start.val()
        if end is not None:
            end = end.val()
        if jump is not None:
            jump = jump.val()
        return self.wrap(self.data()[start:end:jump])

    def __str__(self):
        return repr(self.data())

    @staticmethod
    def wrap(data) -> 'Collection':
        if isinstance(data, str):
            return String(data)
        if isinstance(data, list):
            return List(data)
        raise TypeError(
            f'Collection cannot be made from {type(data)} data: {data}'
        )


class String(Collection):
    __slots__ = ('__data',)

    def __init__(self, data: str):
        assert isinstance(data, str)
        self.__data = data

    def data(self) -> str:
        return self.__data

    def equals(self, other: 'Object'):
        assert isinstance(other, String)
        return self.data() == other.data()

    def compare(self, other: 'Object') -> ComparisonResult:
        assert isinstance(other, String)
        a = self.data()
        b = other.data()
        if a == b:
            return ComparisonResult.EQUAL
        elif a < b:
            return ComparisonResult.LESS
        return ComparisonResult.GREATER


class List(Collection):
    __slots__ = ('__data',)

    def __init__(self, data: tuple | list):
        self.__data: typing.List = list(data)

    def data(self) -> typing.List:
        return self.__data

    def append(self, item):
        self.__data.append(item)

    def equals(self, other: 'Object'):
        assert isinstance(other, List) or isinstance(other, Range)
        return self.data() == other.data()

    def compare(self, other: 'Object') -> ComparisonResult:
        raise NotImplementedError('Comparing lists is not yet implemented')

    def __str__(self):
        inner = ','.join(str(i) for i in self.data())
        return f'[{inner}]'


class Range(Collection):
    __slots__ = ('__start', '__end', '__jump')

    def __init__(self, start: Number, end: Number, jump: Number):
        self.__start: int = start.val()
        self.__end: int = end.val()
        self.__jump: int = jump.val()

    def data(self) -> typing.List:
        return list(range(self.__start, self.__end, self.__jump))

    def size(self) -> int:
        return (self.__end - self.__start) // self.__jump

    def select_element(self, index: Number):
        if (element := self.__start + index.val()) < self.__end:
            return element
        raise (
            f'Cannot read index {index} from {self.__start} '
            f'which has length {self.size()}.'
        )

    def constrain(self, index):
        return min(max(index, self.__start), self.__end)

    def select_slice(
        self, start: Number, end: Number, jump: Number
    ) -> 'Range':
        if start:
            start = min(
                max(start.val() + self.__start, self.__start), self.__end - 1
            )
        else:
            start = self.__start

        if end:
            end = min(max(end.val() + self.__start, self.__start), self.__end)
        else:
            end = self.__end

        if jump:
            jump = jump.val() * self.__jump
        else:
            jump = self.__jump

        return Range(Integer(start), Integer(end), Integer(jump))

    def equals(self, other: 'Object'):
        assert isinstance(other, Range) or isinstance(other, List)
        if isinstance(other, Range):
            return (
                self.size() == other.size()
                and self.__start == other.__start
                and self.__jump == other.__jump
            )
        return self.data() == other.data()

    def compare(self, other: 'Object') -> ComparisonResult:
        raise NotImplementedError('Comparing ranges is not yet implemented')

    def __str__(self):
        if self.__jump == 1:
            return f'({self.__start}..{self.__end})'
        return f'({self.__start}..{self.__end} by {self.__jump})'
