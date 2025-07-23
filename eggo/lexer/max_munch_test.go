package lexer

import "testing"

type TestCase struct {
	input      string
	start_from int
	expected   MaxMunchResult
	found      bool
}

func TestMMTrie(t *testing.T) {
	patterns := map[string]TokenType{
		"a":   _TEST_A,
		"aab": _TEST_B,
		"aba": _TEST_C,
		"b":   _TEST_D,
	}
	test_cases := []TestCase{
		{"", 0, MaxMunchResult{}, false},
		{"cd", 0, MaxMunchResult{}, false},
		{"a", 0, MaxMunchResult{_TEST_A, 1}, true},
		{"ac", 0, MaxMunchResult{_TEST_A, 1}, true},
		{"aab", 0, MaxMunchResult{_TEST_B, 3}, true},
		{"aabrah", 0, MaxMunchResult{_TEST_B, 3}, true},
		{"ababrah", 0, MaxMunchResult{_TEST_C, 3}, true},
		{"baabrah", 0, MaxMunchResult{_TEST_D, 1}, true},
		{"xxx", 3, MaxMunchResult{}, false},
		{"xxxcd", 3, MaxMunchResult{}, false},
		{"xxxa", 3, MaxMunchResult{_TEST_A, 1}, true},
		{"xxxac", 3, MaxMunchResult{_TEST_A, 1}, true},
		{"xxxaab", 3, MaxMunchResult{_TEST_B, 3}, true},
		{"xxxaabrah", 3, MaxMunchResult{_TEST_B, 3}, true},
		{"xxxababrah", 3, MaxMunchResult{_TEST_C, 3}, true},
		{"xxxbaabrah", 3, MaxMunchResult{_TEST_D, 1}, true},
	}

	trie := NewMMTrie(patterns)
	for _, tc := range test_cases {
		actual, found := trie.LargestPrefix(tc.input, tc.start_from)
		if found != tc.found {

			if tc.found {
				t.Fatalf("LargestPrefix(%q, %d) gave no result; expected %v", tc.input, tc.start_from, tc.expected.token.DebugName())
			} else {
				t.Fatalf("LargestPrefix(%q, %d) gave %v; expected no result", tc.input, tc.start_from, actual.token.DebugName())
			}
		}
		if actual != tc.expected {
			t.Fatalf("LargestPrefix(%q, %d) gave %v; expected %v", tc.input, tc.start_from, actual.token.DebugName(), tc.expected.token.DebugName())
		}
	}
}

func TestFirstByte(t *testing.T) {
	patterns := map[string]TokenType{
		"apple":       _TEST_A,
		"banana":      _TEST_B,
		"cherry":      _TEST_C,
		"dragonfruit": _TEST_D,
	}
	trie := NewMMTrie(patterns)
	if len(trie.FirstByte) != 4 {
		t.Fatalf("Expected 4 first bytes but there were %d", len(trie.FirstByte))
	}
	for _, c := range "abcd" {
		if _, has_byte := trie.FirstByte[byte(c)]; !has_byte {
			t.Fatalf("Expected %q to be a first byte", string(c))
		}
	}
}
