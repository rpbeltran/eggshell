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
		"a":   A,
		"aab": B,
		"aba": C,
		"b":   D,
	}
	test_cases := []TestCase{
		{"", 0, MaxMunchResult{}, false},
		{"cd", 0, MaxMunchResult{}, false},
		{"a", 0, MaxMunchResult{A, 1}, true},
		{"ac", 0, MaxMunchResult{A, 1}, true},
		{"aab", 0, MaxMunchResult{B, 3}, true},
		{"aabrah", 0, MaxMunchResult{B, 3}, true},
		{"ababrah", 0, MaxMunchResult{C, 3}, true},
		{"baabrah", 0, MaxMunchResult{D, 1}, true},
		{"xxx", 3, MaxMunchResult{}, false},
		{"xxxcd", 3, MaxMunchResult{}, false},
		{"xxxa", 3, MaxMunchResult{A, 1}, true},
		{"xxxac", 3, MaxMunchResult{A, 1}, true},
		{"xxxaab", 3, MaxMunchResult{B, 3}, true},
		{"xxxaabrah", 3, MaxMunchResult{B, 3}, true},
		{"xxxababrah", 3, MaxMunchResult{C, 3}, true},
		{"xxxbaabrah", 3, MaxMunchResult{D, 1}, true},
	}

	trie := NewMMTrie(patterns)
	for _, tc := range test_cases {
		actual, found := trie.LargestPrefix(tc.input, tc.start_from)
		if found != tc.found {

			if tc.found {
				t.Fatalf("LargestPrefix(%q, %d) gave no result; expected %v", tc.input, tc.start_from, tc.expected)
			} else {
				t.Fatalf("LargestPrefix(%q, %d) gave %v; expected no result", tc.input, tc.start_from, actual)
			}
		}
		if actual != tc.expected {
			t.Fatalf("LargestPrefix(%q, %d) gave %v; expected %v", tc.input, tc.start_from, actual, tc.expected)
		}
	}
}
