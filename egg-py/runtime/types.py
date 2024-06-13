from abc import ABC, abstractmethod


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
