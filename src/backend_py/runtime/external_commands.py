from typing import Optional, Tuple

from ..runtime.types.collections import String
from ..runtime.types.functional import Functional
from ..runtime.types.objects import Object


class ExternalCommand:
    def __init__(self, args: Tuple[str, ...]):
        self.args = args

    def evaluate(self, stdin: Optional[Object] = None) -> String:
        command_inner = ' '.join(str(arg) for arg in self.args)
        if stdin:
            return String(str(stdin) + f' -> Exec[{command_inner}]')
        return String(f'Exec[{command_inner}]')


class Pipeline:
    def __init__(self, children: Tuple[ExternalCommand | Object, ...]):
        self.children = children

    def evaluate(self) -> Optional[Object]:
        value: Optional[Object] = (
            self.children[0].evaluate()
            if isinstance(self.children[0], ExternalCommand | Pipeline)
            else self.children[0]
        )
        stage: Optional[Object | ExternalCommand | Pipeline]
        for stage in self.children[1:]:
            if isinstance(stage, ExternalCommand):
                value = stage.evaluate(value)
            else:
                assert isinstance(stage, Functional)
                value = stage.call([] if value is None else [value])
        return value
