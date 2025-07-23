package lexer

import (
	"eggo/source"
	"fmt"
	"strings"
	"testing"

	"github.com/google/go-cmp/cmp"
)

type TestCaseToken struct {
	Type  TokenType
	Value string
}

type LexerTestCase struct {
	input  string
	tokens []TestCaseToken
	fails  bool
}

func TestCommand1(t *testing.T) {
	test_case := LexerTestCase{
		input: "foo",
		tokens: []TestCaseToken{
			{EXEC_ARG, "foo"},
		}}

	validateTestCase(t, test_case)
}

func TestCommand2(t *testing.T) {
	test_case := LexerTestCase{
		input: "foo bar",
		tokens: []TestCaseToken{
			{EXEC_ARG, "foo"},
			{EXEC_ARG, "bar"},
		}}

	validateTestCase(t, test_case)
}

func TestPipe2(t *testing.T) {
	test_case := LexerTestCase{
		input: "foo | bar",
		tokens: []TestCaseToken{
			{EXEC_ARG, "foo"},
			{PIPE, "|"},
			{EXEC_ARG, "bar"},
		}}

	validateTestCase(t, test_case)
}

func TestPipe3(t *testing.T) {
	test_case := LexerTestCase{
		input: "aaa bbb | c | ddd",
		tokens: []TestCaseToken{
			{EXEC_ARG, "aaa"},
			{EXEC_ARG, "bbb"},
			{PIPE, "|"},
			{EXEC_ARG, "c"},
			{PIPE, "|"},
			{EXEC_ARG, "ddd"},
		}}

	validateTestCase(t, test_case)
}

func TestSemicolons(t *testing.T) {
	test_case := LexerTestCase{
		input: "a ; b ; c",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{SEMICOLON, ";"},
			{EXEC_ARG, "b"},
			{SEMICOLON, ";"},
			{EXEC_ARG, "c"},
		}}

	validateTestCase(t, test_case)
}

func TestFunctionBasic(t *testing.T) {
	test_case := LexerTestCase{
		input: "fn foo(){`b`}",
		tokens: []TestCaseToken{
			{FN, "fn"},
			{NAME, "foo"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{EXEC_ARG, "b"},
			{CURLY_CLOSE, "}"},
		}}

	validateTestCase(t, test_case)
}

func validateTestCase(t *testing.T, tc LexerTestCase) {
	source := source.NewSource("", tc.input, true)
	lexer := NewLexer(&source)
	err := lexer.Lex()
	if tc.fails {
		if err == nil {
			t.Fatalf("Lexing %q should have failed but did not", tc.input)
		}
		return
	}
	if err != nil {
		t.Fatalf("Lexing %q failed: %v", tc.input, err)
	}
	expected_tokens := make([]string, 0)
	for _, token := range tc.tokens {
		expected_tokens = append(expected_tokens, fmt.Sprintf("<%s %q>", token.Type.DebugName(), token.Value))
	}
	expected := strings.Join(expected_tokens, "\n")

	actual_tokens := make([]string, 0)
	for _, token := range lexer.Tokens {
		token_src := source.Data()[token.Loc.Offset : token.Loc.Offset+token.Loc.Length]
		actual_tokens = append(actual_tokens, fmt.Sprintf("<%s %q>", token.Type.DebugName(), token_src))
	}
	actual := strings.Join(actual_tokens, "\n")

	diff := cmp.Diff(expected, actual)
	if diff != "" {
		t.Fatalf("Expected and actual tokens had a diff:\n%s\n", diff)
	}
}
