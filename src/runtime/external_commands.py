from typing import Optional, Tuple

from ..runtime import types


class ExternalCommand:
    def __init__(self, args: Tuple[str, ...]):
        self.args = args

    def evaluate(self, stdin: Optional[types.Object] = None) -> types.String:
        command_inner = ' '.join(str(arg) for arg in self.args)
        if stdin:
            return types.String(str(stdin) + f' -> Exec[{command_inner}]')
        return types.String(f'Exec[{command_inner}]')


class Pipeline:
    def __init__(self, children: Tuple[ExternalCommand | types.Object, ...]):
        self.children = children

    def evaluate(self) -> Optional[types.Object]:
        value: Optional[types.Object] = (
            self.children[0].evaluate()
            if isinstance(self.children[0], ExternalCommand | Pipeline)
            else self.children[0]
        )
        stage: Optional[types.Object | ExternalCommand | Pipeline]
        for stage in self.children[1:]:
            if isinstance(stage, ExternalCommand):
                value = stage.evaluate(value)
            else:
                assert isinstance(stage, types.Functional)
                value = stage.call([] if value is None else [value])
        return value
