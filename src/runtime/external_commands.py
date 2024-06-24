from typing import Any, Iterable


class ExternalCommand:
    def __init__(self, args: Iterable[Any]):
        self.args = args


class Pipeline:
    def __init__(self, children: Iterable[Any]):
        self.children = children
