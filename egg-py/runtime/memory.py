from collections import deque
from typing import Dict, List, Optional, Set

from runtime.types import Object


class Instance:
    __slots__ = ('data', 'deps')

    def __init__(self, data: Object, deps: Set[int]):
        self.data = data
        self.deps = deps


class Scope:
    __slots__ = ('names',)

    def __init__(self):
        self.names: Dict[str, int] = {}

    def store(self, name, ref_id):
        self.names[name] = ref_id

    def has_name(self, name) -> bool:
        return name in self.names

    def get_id(self, name) -> int:
        return self.names[name]


class Memory:
    def __init__(self):
        self.instances: Dict[int, Instance] = {}
        self.scopes: List[Scope] = [Scope()]
        self.__next_ref_id_counter = 0

    def new(
        self,
        data: Object,
        deps: Optional[Set[int]] = None,
        name: Optional[str] = None,
    ) -> int:
        ref_id = self.__next_ref_id()
        self.instances[ref_id] = Instance(
            data, set() if deps is None else deps
        )
        if name is not None:
            self.store(name, ref_id)
        return ref_id

    def current_scope(self) -> Scope:
        return self.scopes[-1]

    def store(self, name: str, ref_id: int):
        self.current_scope().store(name, ref_id)

    def push_scope(self):
        self.scopes.append(Scope())

    def pop_scope(self, garbage_collect=True):
        self.scopes.pop()
        if garbage_collect:
            self.garbage_collect()

    def get_object(self, ref_id: int) -> Object:
        return self.instances[ref_id].data

    def get_id(self, name: str) -> Optional[int]:
        for scope in self.scopes[::-1]:
            if name in scope.names:
                return scope.names[name]
        return None

    def free(self, ref_id: int):
        del self.instances[ref_id]

    def add_dependency(self, from_id: int, dep_id: int):
        self.instances[from_id].deps.add(dep_id)

    def garbage_collect(self):
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
