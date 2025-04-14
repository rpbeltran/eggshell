from abc import abstractmethod
from typing import Callable, List, Optional

from ..memory import Memory
from ..types.objects import ComparisonResult, Object


class Functional(Object):
    @abstractmethod
    def call(self, args: List[Object]) -> Optional[Object]:
        ...

    def compare(self, other: Object) -> ComparisonResult:
        raise NotImplementedError('Functional types are not comparable.')

    def equals(self, other: Object) -> bool:
        raise NotImplementedError('Functional types are not comparable.')


class LambdaExpression(Functional):
    def __init__(
        self,
        memory: Memory,
        params: List[str],
        expression: Callable[[], Optional[Object]],
    ):
        self.memory = memory
        self.params = params
        self.expression = expression

    def call(self, args: List['Object']) -> Optional[Object]:
        assert len(args) == len(self.params)
        self.memory.push_scope()
        for arg, param in zip(args, self.params):
            self.memory.new(arg, name=param)
        output = self.expression()
        self.memory.push_scope()
        return output
