from collections import deque
from typing import Dict, List, Optional, Set

from ..runtime.types.objects import Object


class Instance:
    __slots__ = ('data', 'deps', 'const')

    def __init__(self, data: Object, deps: Set[int], const: bool = False):
        self.data = data
        self.deps = deps
        self.const = const


class Scope:
    __slots__ = ('names',)

    def __init__(self) -> None:
        self.names: Dict[str, int] = {}

    def store(self, name: str, ref_id: int) -> None:
        self.names[name] = ref_id

    def has_name(self, name: str) -> bool:
        return name in self.names

    def get_id(self, name: str) -> int:
        return self.names[name]


class Memory:
    def __init__(self) -> None:
        self.instances: Dict[int, Instance] = {}
        self.scopes: List[Scope] = [Scope()]
        self.__next_ref_id_counter = 0

    def new(
        self,
        data: Object,
        deps: Optional[Set[int]] = None,
        name: Optional[str] = None,
        const: bool = False,
    ) -> None:
        ref_id = self.__next_ref_id()
        self.instances[ref_id] = Instance(
            data, set() if deps is None else deps, const=const
        )
        if name is not None:
            self.store(name, ref_id)

    def update_var(
        self, name: str, new_value: Object, deps: Optional[Set[int]] = None
    ) -> None:
        old_id = self.get_id(name)
        assert old_id is not None
        assert not self.instances[old_id].const
        self.new(new_value, deps=deps, name=name)

    def current_scope(self) -> Scope:
        return self.scopes[-1]

    def store(self, name: str, ref_id: int) -> None:
        self.current_scope().store(name, ref_id)

    def push_scope(self) -> None:
        self.scopes.append(Scope())

    def pop_scope(self, garbage_collect: bool = True) -> None:
        self.scopes.pop()
        if garbage_collect:
            self.garbage_collect()

    def get_object(self, ref_id: int) -> Object:
        return self.instances[ref_id].data

    def get_object_by_name(self, name: str) -> Object:
        ref_id = self.get_id(name)
        assert ref_id is not None
        return self.instances[ref_id].data

    def get_id(self, name: str) -> Optional[int]:
        for scope in self.scopes[::-1]:
            if name in scope.names:
                return scope.names[name]
        return None

    def free(self, ref_id: int) -> None:
        del self.instances[ref_id]

    def add_dependency(self, from_id: int, dep_id: int) -> None:
        self.instances[from_id].deps.add(dep_id)

    def garbage_collect(self) -> None:
        deps = self._get_used_ids()
        for ref_id in self.instances.keys() - deps:
            self.free(ref_id)

    def _get_used_ids(self) -> Set[int]:
        named_ids = {ref for s in self.scopes for ref in s.names.values()}
        discovered = set(named_ids)
        frontier = deque(named_ids)
        while frontier:
            next_visit = frontier.pop()
            discovered.update(self.instances[next_visit].deps)
            frontier.extend(self.instances[next_visit].deps - discovered)
        return discovered

    def __next_ref_id(self) -> int:
        next_ref_id = self.__next_ref_id_counter
        self.__next_ref_id_counter += 1
        return next_ref_id
