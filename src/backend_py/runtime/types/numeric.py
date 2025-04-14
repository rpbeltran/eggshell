from abc import abstractmethod

from ..types.objects import ComparisonResult, Object


class Number(Object):
    @abstractmethod
    def val(self) -> int | float:
        ...

    def add(self, other: 'Number') -> 'Number':
        return self.wrap(value=self.val() + other.val())

    def subtract(self, other: 'Number') -> 'Number':
        return self.wrap(self.val() - other.val())

    def multiply(self, other: 'Number') -> 'Number':
        return self.wrap(self.val() * other.val())

    def divide(self, other: 'Number') -> 'Number':
        return self.wrap(self.val() / other.val())

    def int_divide(self, other: 'Number') -> 'Number':
        return self.wrap(self.val() // other.val())

    def modulus(self, other: 'Number') -> 'Number':
        return self.wrap(self.val() % other.val())

    def raise_power(self, other: 'Number') -> 'Number':
        return self.wrap(self.val() ** other.val())

    def negate(self) -> 'Number':
        return self.wrap(-self.val())

    def equals(self, other: 'Object') -> bool:
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

    def __str__(self) -> str:
        return str(self.val())

    def __repr__(self) -> str:
        return repr(self.val())

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

    def equals(self, other: 'Object') -> bool:
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

    def __bool__(self) -> bool:
        return self.__value

    def __str__(self) -> str:
        return 'true' if self.__value else 'false'

    __repr__ = __str__


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

    def __str__(self) -> str:
        return f'{self.__value}{self.__unit}'

    def __repr__(self) -> str:
        return f'{self.__value}{self.__unit}'

    def base_val(self) -> int | float:
        # todo: implement getting value in base unit quantity
        return self.__value

    def equals(self, other: 'Object') -> bool:
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
