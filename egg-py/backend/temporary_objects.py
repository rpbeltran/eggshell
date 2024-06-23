from typing import List, NamedTuple, Optional


class Name(NamedTuple):
    name: str
    namespace: Optional[List[str]] = None


class Block(NamedTuple):
    lines: List[str]

    def join(self, indentation=0):
        indent = '\t' * indentation
        return indent + f'{indent}\n'.join(self.lines)

    def make_if(self, condition, extra_indentation=0):
        extra_indent = '\t' * extra_indentation
        indent = f'{extra_indent}\t'
        return Block(
            [f'{extra_indent}if {condition}:']
            + [f'{indent}{line}' for line in self.lines]
        )
