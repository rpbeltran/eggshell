from typing import Any, List


class ExternalCommand:
    def __init__(self, args: List[Any]):
        self.args = args


class Pipeline:
    def __init__(self, children: List[Any]):
        self.children = children
