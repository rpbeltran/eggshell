from collections import defaultdict

from typing import DefaultDict, Dict, NamedTuple, Optional, Set


class TrieResult(NamedTuple):
    token: str
    length: int


class TrieNode:
    def __init__(self, prefix_len, named_patterns: Dict[str, str]):
        self.children: Dict[str, TrieNode] = {}
        self.value: Optional[str] = None

        children_data: DefaultDict[str, Dict[str, str]] = defaultdict(dict)
        for pattern, name in named_patterns.items():
            if len(pattern) == prefix_len:
                self.value = TrieResult(name, prefix_len)
            else:
                children_data[pattern[prefix_len]][pattern] = name
        for c, c_patterns in children_data.items():
            self.children[c] = TrieNode(prefix_len + 1, c_patterns)


class MaxMunchTrie:
    def __init__(self, named_patterns: Dict[str, str]):
        self.root_node = TrieNode(0, named_patterns)

    def largest_prefix(self, s) -> Optional[TrieResult]:
        node = self.root_node
        for i in range(len(s)):
            if s[i] not in node.children:
                return node.value
            node = node.children[s[i]]
        return node.value
