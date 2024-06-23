from typing import List, NamedTuple, Optional


class Name(NamedTuple):
    name: str
    namespace: Optional[List[str]] = None


class Block:
    __slots__ = ('lines',)

    def __init__(self, lines: List[str]):
        self.lines: List[str] = lines

    def join(self, indentation=0):
        indent = '\t' * indentation
        return indent + f'{indent}\n'.join(self.lines)

    def make_if(self, condition, extra_indentation=0):
        extra_indent = '\t' * extra_indentation
        indent = f'{extra_indent}\t'
        return IfBlock(
            [f'{extra_indent}if {condition}:']
            + [f'{indent}{line}' for line in self.lines]
        )


class IfBlock(Block):
    def __init__(self, lines: List[str]):
        super().__init__(lines)

    def add_elif(self, condition, block, extra_indentation=0):
        extra_indent = '\t' * extra_indentation
        indent = f'{extra_indent}\t'
        self.lines.append(f'{extra_indent}elif {condition}:')
        self.lines.extend(f'{indent}{line}' for line in block.lines)

    def add_else(self, block, extra_indentation=0):
        extra_indent = '\t' * extra_indentation
        indent = f'{extra_indent}\t'
        self.lines.append(f'{extra_indent}else:')
        self.lines.extend(f'{indent}{line}' for line in block.lines)
