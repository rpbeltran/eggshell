from typing import List, NamedTuple, Optional


class Name(NamedTuple):
    name: str
    namespace: Optional[List[str]] = None


class Block(NamedTuple):
    expressions: List[str]

    def join(self, indentation=0):
        indent = '\t' * indentation
        return indent + f'{indent}\n'.join(self.expressions)
