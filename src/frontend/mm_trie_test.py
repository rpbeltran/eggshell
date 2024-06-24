from .mm_trie import *


def test_ab() -> None:
    trie = MaxMunchTrie({
        'a': '1',
        'aab': '2',
        'aba': '3',
        'b': '4'
    })
    assert trie.largest_prefix('', 0) is None
    assert trie.largest_prefix('cd', 0) is None
    assert trie.largest_prefix('ac', 0) == TrieResult('1', 1)
    assert trie.largest_prefix('aab', 0) == TrieResult('2', 3)
    assert trie.largest_prefix('aabrah', 0) == TrieResult('2', 3)
    assert trie.largest_prefix('ababrah', 0) == TrieResult('3', 3)
    assert trie.largest_prefix('baabrah', 0) == TrieResult('4', 1)

    assert trie.largest_prefix('xx', 2) is None
    assert trie.largest_prefix('xxcd', 2) is None
    assert trie.largest_prefix('xxac', 2) == TrieResult('1', 1)
    assert trie.largest_prefix('xxaab', 2) == TrieResult('2', 3)
    assert trie.largest_prefix('xxaabrah', 2) == TrieResult('2', 3)
    assert trie.largest_prefix('xxababrah', 2) == TrieResult('3', 3)
    assert trie.largest_prefix('xxbaabrah', 2) == TrieResult('4', 1)
