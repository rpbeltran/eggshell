from .mm_trie import *


def test_ab():
    trie = MaxMunchTrie({
        'a': '1',
        'aab': '2',
        'aba': '3',
        'b': '4'
    })
    assert trie.largest_prefix('') is None
    assert trie.largest_prefix('cd') is None
    assert trie.largest_prefix('ac') == TrieResult('1', 1)
    assert trie.largest_prefix('aab') == TrieResult('2', 3)
    assert trie.largest_prefix('aabrah') == TrieResult('2', 3)
    assert trie.largest_prefix('ababrah') == TrieResult('3', 3)
    assert trie.largest_prefix('baabrah') == TrieResult('4', 1)
