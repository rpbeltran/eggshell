import typing
from abc import abstractmethod

from ..memory import Memory
from ..types.objects import ComparisonResult, Object


class Functional(Object):
    @abstractmethod
    def call(self, args: typing.List['Object']) -> typing.Optional[Object]:
        ...

    def compare(self, other: 'Object') -> ComparisonResult:
        raise NotImplementedError('Functional types are not comparable.')

    def equals(self, other: 'Object') -> bool:
        raise NotImplementedError('Functional types are not comparable.')


class LambdaExpression(Functional):
    def __init__(
        self, memory: Memory, args: typing.List[str], expression: str
    ):
        self.memory = memory
        self.args = args
        self.expression = expression

    def call(self, args: typing.List['Object']) -> typing.Optional[Object]:
        # todo: implement this soon
        raise NotImplementedError(
            'Calling lambdas has not yet been implemented.'
        )
