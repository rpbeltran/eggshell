from typing import List, NamedTuple, Optional


class Name(NamedTuple):
    name: str
    namespace: Optional[List[str]] = None
