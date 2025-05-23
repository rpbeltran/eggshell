from typing import List, NamedTuple, Optional


class Name(NamedTuple):
    name: str
    namespace: Optional[List[str]] = None


class Block:
    __slots__ = ('lines',)
    memory_instance = '_m'

    def __init__(self, lines: List[str]):
        self.lines: List[str] = self.fix_multilines(lines) or ['pass']

    @staticmethod
    def fix_multilines(lines: List[str]) -> List[str]:
        fixed = []
        for line in lines:
            fixed.extend(line.split('\n'))
        return fixed

    def join(self, indentation_level: int = 0) -> str:
        indentation = '\t' * indentation_level
        return indentation + f'\n{indentation}'.join(self.lines)

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

    def make_function(
        self, name: str, param_list: List[str], extra_indentation: int = 0
    ) -> 'Block':
        indent = '\t' * extra_indentation
        backing_name = f'___{name}_backing_function'
        signature = f'{indent}def {backing_name}({",".join(param_list)}):'
        start_scope = f'{indent}\t{Block.memory_instance}.push_scope()'
        end_scope = f'{indent}\t{Block.memory_instance}.pop_scope()'
        pre_body = [
            f'{indent}\t{Block.memory_instance}.new({p}, name={repr(p)})'
            for p in param_list
        ]
        body = self.join(1)
        push_backing = f'{indent}{Block.memory_instance}.new({backing_name}, name="{backing_name}")'
        return Block(
            [signature, start_scope, *pre_body, body, end_scope, push_backing]
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
    headers: List[Block] = []

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

    @classmethod
    def add_header(cls, block: Block) -> None:
        cls.headers.append(block)

    @classmethod
    def pop_headers(cls) -> List[Block]:
        headers = cls.headers
        cls.headers = []
        return headers
