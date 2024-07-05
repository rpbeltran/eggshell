from typing import Any, Iterable

from ..runtime import types


class ExternalCommand:
    def __init__(self, args: Iterable[str]):
        self.args = args


class Pipeline:
    def __init__(self, children: Iterable[ExternalCommand | types.Object]):
        self.children = children
