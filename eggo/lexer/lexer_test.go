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

func TestFunctionReturn(t *testing.T) {
	test_case := LexerTestCase{
		input: "fn foo(): int {\n  ret 2\n}",
		tokens: []TestCaseToken{
			{FN, "fn"},
			{NAME, "foo"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
			{COLON, ":"},
			{NAME, "int"},
			{CURLY_OPEN, "{"},
			{SEMICOLON, ""},
			{RETURN, "ret"},
			{INT, "2"},
			{SEMICOLON, ""},
			{CURLY_CLOSE, "}"},
		}}

	validateTestCase(t, test_case)
}

func TestFunctionParam(t *testing.T) {
	test_case := LexerTestCase{
		input: "fn foo(a, b := 1, c: int = 2) {}",
		tokens: []TestCaseToken{
			{FN, "fn"},
			{NAME, "foo"},
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{COMMA, ","},
			{NAME, "b"},
			{DECLARE, ":="},
			{INT, "1"},
			{COMMA, ","},
			{NAME, "c"},
			{COLON, ":"},
			{NAME, "int"},
			{ASSIGN, "="},
			{INT, "2"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}

	validateTestCase(t, test_case)
}

func TestLambda(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\a -> b",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{NAME, "a"},
			{ARROW, "->"},
			{EXEC_ARG, "b"},
		}}

	validateTestCase(t, test_case)
}

func TestLambda2(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\(a,b) -> c",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{COMMA, ","},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{ARROW, "->"},
			{EXEC_ARG, "c"},
		}}

	validateTestCase(t, test_case)
}

func TestLambda3(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\(a,b,c) -> d",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{COMMA, ","},
			{NAME, "b"},
			{COMMA, ","},
			{NAME, "c"},
			{PAREN_CLOSE, ")"},
			{ARROW, "->"},
			{EXEC_ARG, "d"},
		}}

	validateTestCase(t, test_case)
}

func TestMulti(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\a {ret 1}",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{NAME, "a"},
			{CURLY_OPEN, "{"},
			{RETURN, "ret"},
			{INT, "1"},
			{CURLY_CLOSE, "}"},
		}}

	validateTestCase(t, test_case)
}

func TestIdentifiers(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a b @c",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{EXEC_ARG, "b"},
			{NAME, "c"},
		}}

	validateTestCase(t, test_case)
}

func TestDeclaration(t *testing.T) {
	test_case := LexerTestCase{
		input: "a := 1",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{DECLARE, ":="},
			{INT, "1"},
		}}

	validateTestCase(t, test_case)
}

func TestTypedDeclaration(t *testing.T) {
	test_case := LexerTestCase{
		input: "a : int = 1",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{COLON, ":"},
			{NAME, "int"},
			{ASSIGN, "="},
			{INT, "1"},
		}}

	validateTestCase(t, test_case)
}

func TestQuotedExecution(t *testing.T) {
	test_case := LexerTestCase{
		input: "`a` {`b`}",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{CURLY_OPEN, "{"},
			{EXEC_ARG, "b"},
			{CURLY_CLOSE, "}"},
		}}

	validateTestCase(t, test_case)
}

func TestList(t *testing.T) {
	test_case := LexerTestCase{
		input: "a := [1,2,3]",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{DECLARE, ":="},
			{SQUARE_OPEN, "["},
			{INT, "1"},
			{COMMA, ","},
			{INT, "2"},
			{COMMA, ","},
			{INT, "3"},
			{SQUARE_CLOSE, "]"},
		}}

	validateTestCase(t, test_case)
}

func TestListTypes(t *testing.T) {
	test_case := LexerTestCase{
		input: "a : [int] = ",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{COLON, ":"},
			{SQUARE_OPEN, "["},
			{NAME, "int"},
			{SQUARE_CLOSE, "]"},
			{ASSIGN, "="},
		}}

	validateTestCase(t, test_case)
}

func TestListAccess(t *testing.T) {
	test_case := LexerTestCase{
		input: "a[1]",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{SQUARE_OPEN, "["},
			{INT, "1"},
			{SQUARE_CLOSE, "]"},
		}}

	validateTestCase(t, test_case)
}

func TestListAccess2(t *testing.T) {
	test_case := LexerTestCase{
		input: "a[1:2]",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{SQUARE_OPEN, "["},
			{INT, "1"},
			{COLON, ":"},
			{INT, "2"},
			{SQUARE_CLOSE, "]"},
		}}

	validateTestCase(t, test_case)
}

func TestListAccess3(t *testing.T) {
	test_case := LexerTestCase{
		input: "a[1:2:3]",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{SQUARE_OPEN, "["},
			{INT, "1"},
			{COLON, ":"},
			{INT, "2"},
			{COLON, ":"},
			{INT, "3"},
			{SQUARE_CLOSE, "]"},
		}}

	validateTestCase(t, test_case)
}

func TestListAccessVars(t *testing.T) {
	test_case := LexerTestCase{
		input: "a[b:c:d]",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{SQUARE_OPEN, "["},
			{NAME, "b"},
			{COLON, ":"},
			{NAME, "c"},
			{COLON, ":"},
			{NAME, "d"},
			{SQUARE_CLOSE, "]"},
		}}

	validateTestCase(t, test_case)
}

func TestCurrying(t *testing.T) {
	test_case := LexerTestCase{
		input: "a $ b $ c",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{CURRY, "$"},
			{EXEC_ARG, "b"},
			{CURRY, "$"},
			{EXEC_ARG, "c"},
		}}

	validateTestCase(t, test_case)
}

func TestFieldAccess(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a.b.c",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{DOT, "."},
			{NAME, "b"},
			{DOT, "."},
			{NAME, "c"},
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
