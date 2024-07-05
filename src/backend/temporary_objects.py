from typing import List, NamedTuple, Optional


class Name(NamedTuple):
    name: str
    namespace: Optional[List[str]] = None


class Block:
    __slots__ = ('lines',)

    def __init__(self, lines: List[str]):
        self.lines: List[str] = lines or ['pass']

    def join(self, indentation: int = 0) -> str:
        indent = '\t' * indentation
        return indent + f'{indent}\n'.join(self.lines)

    def make_if(self, condition: str, extra_indentation: int = 0) -> 'IfBlock':
        extra_indent = '\t' * extra_indentation
        indent = f'{extra_indent}\t'
        return IfBlock(
            [f'{extra_indent}if {condition}:']
            + [f'{indent}{line}' for line in self.lines]
        )

    def make_while(
        self, condition: str, extra_indentation: int = 0
    ) -> 'Block':
        extra_indent = '\t' * extra_indentation
        indent = f'{extra_indent}\t'
        return Block(
            [f'{extra_indent}while {condition}:']
            + [f'{indent}{line}' for line in self.lines]
        )


class IfBlock(Block):
    def __init__(self, lines: List[str]):
        super().__init__(lines)

    def add_elif(
        self, condition: str, block: Block, extra_indentation: int = 0
    ) -> None:
        extra_indent = '\t' * extra_indentation
        indent = f'{extra_indent}\t'
        self.lines.append(f'{extra_indent}elif {condition}:')
        self.lines.extend(f'{indent}{line}' for line in block.lines)

    def add_else(self, block: Block, extra_indentation: int = 0) -> None:
        extra_indent = '\t' * extra_indentation
        indent = f'{extra_indent}\t'
        self.lines.append(f'{extra_indent}else:')
        self.lines.extend(f'{indent}{line}' for line in block.lines)


class PygenIntermediary:

    memory_instance = '_m'

    def __init__(self, inline: str | Name | Block):
        self.inline = inline

    def finalize(self) -> str:
        if isinstance(self.inline, Name):
            return (
                f'{PygenIntermediary.memory_instance}'
                f'.get_object_by_name({repr(self.inline.name)})'
            )
        if isinstance(self.inline, Block):
            return self.inline.join()
        return self.inline
