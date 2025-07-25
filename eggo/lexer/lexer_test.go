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

func TestComment(t *testing.T) {
	test_case := LexerTestCase{
		input: "a # hello \n #world \n b",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{SEMICOLON, "# hello "},
			{SEMICOLON, "#world "},
			{EXEC_ARG, "b"},
		}}

	validateTestCase(t, test_case)
}

func TestPassByFunction(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a...",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{ELLIPSIS, "..."},
		}}
	validateTestCase(t, test_case)
}

func TestErrorHandling(t *testing.T) {
	test_case := LexerTestCase{
		input: "(a && b) || c",
		tokens: []TestCaseToken{
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{SEQ_AND, "&&"},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{SEQ_OR, "||"},
			{EXEC_ARG, "c"},
		}}
	validateTestCase(t, test_case)
}

func TestTry(t *testing.T) {
	test_case := LexerTestCase{
		input: "try{\n\t`a` }",
		tokens: []TestCaseToken{
			{TRY, "try"},
			{CURLY_OPEN, "{"},
			{SEMICOLON, ""},
			{EXEC_ARG, "a"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestTryCatch(t *testing.T) {
	test_case := LexerTestCase{
		input: "try { `a` } catch { `b` }",
		tokens: []TestCaseToken{
			{TRY, "try"},
			{CURLY_OPEN, "{"},
			{EXEC_ARG, "a"},
			{CURLY_CLOSE, "}"},
			{CATCH, "catch"},
			{CURLY_OPEN, "{"},
			{EXEC_ARG, "b"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestTryCatchParam(t *testing.T) {
	test_case := LexerTestCase{
		input: "try { `a` } catch e { `b` }",
		tokens: []TestCaseToken{
			{TRY, "try"},
			{CURLY_OPEN, "{"},
			{EXEC_ARG, "a"},
			{CURLY_CLOSE, "}"},
			{CATCH, "catch"},
			{NAME, "e"},
			{CURLY_OPEN, "{"},
			{EXEC_ARG, "b"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestRange(t *testing.T) {
	test_case := LexerTestCase{
		input: "(a..b)",
		tokens: []TestCaseToken{
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{RANGE, ".."},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestLoop(t *testing.T) {
	test_case := LexerTestCase{
		input: "loop { }",
		tokens: []TestCaseToken{
			{ALWAYS_LOOP, "loop"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestWhile(t *testing.T) {
	test_case := LexerTestCase{
		input: "while true { }",
		tokens: []TestCaseToken{
			{WHILE, "while"},
			{TRUE, "true"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

/// new

func TestFor(t *testing.T) {
	test_case := LexerTestCase{
		input: "for a in @b { }",
		tokens: []TestCaseToken{
			{FOR, "for"},
			{NAME, "a"},
			{IN, "in"},
			{NAME, "b"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestAsync(t *testing.T) {
	test_case := LexerTestCase{
		input: "~(`b`)",
		tokens: []TestCaseToken{
			{ASYNC, "~"},
			{PAREN_OPEN, "("},
			{EXEC_ARG, "b"},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestImport(t *testing.T) {
	test_case := LexerTestCase{
		input: "import \"a\"",
		tokens: []TestCaseToken{
			{IMPORT, "import"},
			{QUOTED_STRING, "a"},
		}}
	validateTestCase(t, test_case)
}

func TestClass(t *testing.T) {
	test_case := LexerTestCase{
		input: "class Thing {a: Int = 1\n b: Int = 2; fn c(){}}",
		tokens: []TestCaseToken{
			{CLASS, "class"},
			{NAME, "Thing"},
			{CURLY_OPEN, "{"},
			{NAME, "a"},
			{COLON, ":"},
			{NAME, "Int"},
			{ASSIGN, "="},
			{INT, "1"},
			{SEMICOLON, ""},
			{NAME, "b"},
			{COLON, ":"},
			{NAME, "Int"},
			{ASSIGN, "="},
			{INT, "2"},
			{SEMICOLON, ";"},
			{FN, "fn"},
			{NAME, "c"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestDerivedClass(t *testing.T) {
	test_case := LexerTestCase{
		input: "class Cow: Animal {}",
		tokens: []TestCaseToken{
			{CLASS, "class"},
			{NAME, "Cow"},
			{COLON, ":"},
			{NAME, "Animal"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestMap(t *testing.T) {
	test_case := LexerTestCase{
		input: "{ 1: 10, 2: 20}",
		tokens: []TestCaseToken{
			{CURLY_OPEN, "{"},
			{INT, "1"},
			{COLON, ":"},
			{INT, "10"},
			{COMMA, ","},
			{INT, "2"},
			{COLON, ":"},
			{INT, "20"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestMath(t *testing.T) {
	test_case := LexerTestCase{
		input: "(1 + 2 - 3 * 4 / 5 // 6 ** 7 ** 8 % -9)",
		tokens: []TestCaseToken{
			{PAREN_OPEN, "("},
			{INT, "1"},
			{PLUS, "+"},
			{INT, "2"},
			{MINUS, "-"},
			{INT, "3"},
			{TIMES, "*"},
			{INT, "4"},
			{DIVIDE, "/"},
			{INT, "5"},
			{INT_DIV, "//"},
			{INT, "6"},
			{POWER, "**"},
			{INT, "7"},
			{POWER, "**"},
			{INT, "8"},
			{MOD, "%"},
			{MINUS, "-"},
			{INT, "9"},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestMathRootLevel(t *testing.T) {
	test_case := LexerTestCase{
		input: "1 ** 2 // 3 * 4 / 5",
		tokens: []TestCaseToken{
			{INT, "1"},
			{POWER, "**"},
			{INT, "2"},
			{INT_DIV, "//"},
			{INT, "3"},
			{TIMES, "*"},
			{INT, "4"},
			{DIVIDE, "/"},
			{INT, "5"},
		}}
	validateTestCase(t, test_case)
}

func TestComparison(t *testing.T) {
	test_case := LexerTestCase{
		input: "1 < 2 <= 3 == 4 != 5 >= 6 > 7",
		tokens: []TestCaseToken{
			{INT, "1"},
			{ANGLE_OPEN, "<"},
			{INT, "2"},
			{LTE, "<="},
			{INT, "3"},
			{EQUALS, "=="},
			{INT, "4"},
			{NOT_EQUALS, "!="},
			{INT, "5"},
			{GTE, ">="},
			{INT, "6"},
			{ANGLE_CLOSE, ">"},
			{INT, "7"},
		}}
	validateTestCase(t, test_case)
}

func TestLogic(t *testing.T) {
	test_case := LexerTestCase{
		input: "(a and b or c cor not !d)",
		tokens: []TestCaseToken{
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{AND, "and"},
			{NAME, "b"},
			{OR, "or"},
			{NAME, "c"},
			{NAME, "cor"},
			{NOT, "not"},
			{NOT, "!"},
			{NAME, "d"},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestFunctionCall(t *testing.T) {
	test_case := LexerTestCase{
		input: "a()",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestFunctionCallParams(t *testing.T) {
	test_case := LexerTestCase{
		input: "a(b,c)",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{PAREN_OPEN, "("},
			{NAME, "b"},
			{COMMA, ","},
			{NAME, "c"},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestFunctionCallInBlock(t *testing.T) {
	test_case := LexerTestCase{
		input: "{a(b)}",
		tokens: []TestCaseToken{
			{CURLY_OPEN, "{"},
			{NAME, "a"},
			{PAREN_OPEN, "("},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestEnvAccess(t *testing.T) {
	test_case := LexerTestCase{
		input: "env[\"foo\"]",
		tokens: []TestCaseToken{
			{EXEC_ARG, "env"},
			{SQUARE_OPEN, "["},
			{QUOTED_STRING, "foo"},
			{SQUARE_CLOSE, "]"},
		}}
	validateTestCase(t, test_case)
}

func TestEnvGet(t *testing.T) {
	test_case := LexerTestCase{
		input: "env.get()",
		tokens: []TestCaseToken{
			{NAME, "env"},
			{DOT, "."},
			{NAME, "get"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestMethodCall(t *testing.T) {
	test_case := LexerTestCase{
		input: "@thing.method()",
		tokens: []TestCaseToken{
			{NAME, "thing"},
			{DOT, "."},
			{NAME, "method"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestDoBlock(t *testing.T) {
	test_case := LexerTestCase{
		input: "do {}",
		tokens: []TestCaseToken{
			{DO, "do"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestMultilineParenthetical(t *testing.T) {
	test_case := LexerTestCase{
		input: "(a\n+\n\n\n\t2)",
		tokens: []TestCaseToken{
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{PLUS, "+"},
			{INT, "2"},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestSlice(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a[1:2:3]",
		tokens: []TestCaseToken{
			{NAME, "a"},
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

func TestSliceRev(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a[: by 2]",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{SQUARE_OPEN, "["},
			{COLON, ":"},
			{BY, "by"},
			{INT, "2"},
			{SQUARE_CLOSE, "]"},
		}}
	validateTestCase(t, test_case)
}

func TestWith(t *testing.T) {
	test_case := LexerTestCase{
		input: "with a.y() {}",
		tokens: []TestCaseToken{
			{WITH, "with"},
			{NAME, "a"},
			{DOT, "."},
			{NAME, "y"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestWithAs(t *testing.T) {
	test_case := LexerTestCase{
		input: "with a.y() as x {}",
		tokens: []TestCaseToken{
			{WITH, "with"},
			{NAME, "a"},
			{DOT, "."},
			{NAME, "y"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
			{AS, "as"},
			{NAME, "x"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestWithAs2(t *testing.T) {
	test_case := LexerTestCase{
		input: "with foo.spam.bar() as hello {}",
		tokens: []TestCaseToken{
			{WITH, "with"},
			{NAME, "foo"},
			{DOT, "."},
			{NAME, "spam"},
			{DOT, "."},
			{NAME, "bar"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
			{AS, "as"},
			{NAME, "hello"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestExplicitPipeline(t *testing.T) {
	test_case := LexerTestCase{
		input: "`a | b | c`",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{PIPE, "|"},
			{EXEC_ARG, "b"},
			{PIPE, "|"},
			{EXEC_ARG, "c"},
		}}
	validateTestCase(t, test_case)
}

func TestExplicitPipelineMinified(t *testing.T) {
	test_case := LexerTestCase{
		input: "`a|b|c`",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{PIPE, "|"},
			{EXEC_ARG, "b"},
			{PIPE, "|"},
			{EXEC_ARG, "c"},
		}}
	validateTestCase(t, test_case)
}

func TestQuotedExplicitParam(t *testing.T) {
	test_case := LexerTestCase{
		input: "`a \"b ' c\" d`",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{EXEC_ARG, "b ' c"},
			{EXEC_ARG, "d"},
		}}
	validateTestCase(t, test_case)
}

func TestQuotedExplicitParam2(t *testing.T) {
	test_case := LexerTestCase{
		input: "`\"a b c\" d e `",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a b c"},
			{EXEC_ARG, "d"},
			{EXEC_ARG, "e"},
		}}
	validateTestCase(t, test_case)
}

func TestListComprehension(t *testing.T) {
	test_case := LexerTestCase{
		input: "[10**x for x in (0..10)]",
		tokens: []TestCaseToken{
			{SQUARE_OPEN, "["},
			{INT, "10"},
			{POWER, "**"},
			{NAME, "x"},
			{FOR, "for"},
			{NAME, "x"},
			{IN, "in"},
			{PAREN_OPEN, "("},
			{INT, "0"},
			{RANGE, ".."},
			{INT, "10"},
			{PAREN_CLOSE, ")"},
			{SQUARE_CLOSE, "]"},
		}}
	validateTestCase(t, test_case)
}

func TestMapComprehension(t *testing.T) {
	test_case := LexerTestCase{
		input: "{-x: 100**-x for x in (0..10)]",
		tokens: []TestCaseToken{
			{CURLY_OPEN, "{"},
			{MINUS, "-"},
			{NAME, "x"},
			{COLON, ":"},
			{INT, "100"},
			{POWER, "**"},
			{MINUS, "-"},
			{NAME, "x"},
			{FOR, "for"},
			{NAME, "x"},
			{IN, "in"},
			{PAREN_OPEN, "("},
			{INT, "0"},
			{RANGE, ".."},
			{INT, "10"},
			{PAREN_CLOSE, ")"},
			{SQUARE_CLOSE, "]"},
		}}
	validateTestCase(t, test_case)
}

func TestFnNormalMultiAndKwParam(t *testing.T) {
	test_case := LexerTestCase{
		input: "fn foo (a, b, *c, **d){}",
		tokens: []TestCaseToken{
			{FN, "fn"},
			{NAME, "foo"},
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{COMMA, ","},
			{NAME, "b"},
			{COMMA, ","},
			{TIMES, "*"},
			{NAME, "c"},
			{COMMA, ","},
			{POWER, "**"},
			{NAME, "d"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestFnMultiAndKwParam(t *testing.T) {
	test_case := LexerTestCase{
		input: "fn foo (*a, **b){}",
		tokens: []TestCaseToken{
			{FN, "fn"},
			{NAME, "foo"},
			{PAREN_OPEN, "("},
			{TIMES, "*"},
			{NAME, "a"},
			{COMMA, ","},
			{POWER, "**"},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestFnMultiParam(t *testing.T) {
	test_case := LexerTestCase{
		input: "fn foo (a, *b){}",
		tokens: []TestCaseToken{
			{FN, "fn"},
			{NAME, "foo"},
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{COMMA, ","},
			{TIMES, "*"},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestFnMultiParamOnly(t *testing.T) {
	test_case := LexerTestCase{
		input: "fn foo (*b){}",
		tokens: []TestCaseToken{
			{FN, "fn"},
			{NAME, "foo"},
			{PAREN_OPEN, "("},
			{TIMES, "*"},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestFnKwParam(t *testing.T) {
	test_case := LexerTestCase{
		input: "fn foo (a, **b){}",
		tokens: []TestCaseToken{
			{FN, "fn"},
			{NAME, "foo"},
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{COMMA, ","},
			{POWER, "**"},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestFnKwParamOnly(t *testing.T) {
	test_case := LexerTestCase{
		input: "fn foo (**b){}",
		tokens: []TestCaseToken{
			{FN, "fn"},
			{NAME, "foo"},
			{PAREN_OPEN, "("},
			{POWER, "**"},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestLambdaNormalMultiAndKwParam(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\(a, b, *c, **d){}",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{COMMA, ","},
			{NAME, "b"},
			{COMMA, ","},
			{TIMES, "*"},
			{NAME, "c"},
			{COMMA, ","},
			{POWER, "**"},
			{NAME, "d"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestLambdaMultiAndKwParam(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\(*a, **b){}",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{PAREN_OPEN, "("},
			{TIMES, "*"},
			{NAME, "a"},
			{COMMA, ","},
			{POWER, "**"},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestLambdaMultiParam(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\(a, *b){}",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{COMMA, ","},
			{TIMES, "*"},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestLambdaMultiParamOnly(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\(*b){}",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{PAREN_OPEN, "("},
			{TIMES, "*"},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestLambdaMultiParamOnlyNoParen(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\*b{}",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{TIMES, "*"},
			{NAME, "b"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestLambdaKwParam(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\(a, **b){}",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{COMMA, ","},
			{POWER, "**"},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestLambdaKwParamOnly(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\(**b){}",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{PAREN_OPEN, "("},
			{POWER, "**"},
			{NAME, "b"},
			{PAREN_CLOSE, ")"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestLambdaKwParamOnlyNoParen(t *testing.T) {
	test_case := LexerTestCase{
		input: "\\**b{}",
		tokens: []TestCaseToken{
			{LAMBDA, "\\"},
			{POWER, "**"},
			{NAME, "b"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestKwArgs(t *testing.T) {
	test_case := LexerTestCase{
		input: "foo(a, b=c, d=e)",
		tokens: []TestCaseToken{
			{NAME, "foo"},
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{COMMA, ","},
			{NAME, "b"},
			{ASSIGN, "="},
			{NAME, "c"},
			{COMMA, ","},
			{NAME, "d"},
			{ASSIGN, "="},
			{NAME, "e"},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestDeclareGenericTyped(t *testing.T) {
	test_case := LexerTestCase{
		input: "a : t[g] = [1]",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{COLON, ":"},
			{NAME, "t"},
			{SQUARE_OPEN, "["},
			{NAME, "g"},
			{SQUARE_CLOSE, "]"},
			{ASSIGN, "="},
			{SQUARE_OPEN, "["},
			{INT, "1"},
			{SQUARE_CLOSE, "]"},
		}}
	validateTestCase(t, test_case)
}

func TestImplicitLambda(t *testing.T) {
	test_case := LexerTestCase{
		input: "_",
		tokens: []TestCaseToken{
			{IMPLICIT_LAMBDA_PARAM, "_"},
		}}
	validateTestCase(t, test_case)
}

func TestImplicitLambdaMethod(t *testing.T) {
	test_case := LexerTestCase{
		input: "_.hello() + _.world()",
		tokens: []TestCaseToken{
			{IMPLICIT_LAMBDA_PARAM, "_"},
			{DOT, "."},
			{NAME, "hello"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
			{PLUS, "+"},
			{IMPLICIT_LAMBDA_PARAM, "_"},
			{DOT, "."},
			{NAME, "world"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestImplicitLambdaPiped(t *testing.T) {
	test_case := LexerTestCase{
		input: "a | _.sort | b",
		tokens: []TestCaseToken{
			{EXEC_ARG, "a"},
			{PIPE, "|"},
			{IMPLICIT_LAMBDA_PARAM, "_"},
			{DOT, "."},
			{NAME, "sort"},
			{PIPE, "|"},
			{EXEC_ARG, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestSelectionLambdaShorthand(t *testing.T) {
	test_case := LexerTestCase{
		input: "utils::list_files | ...date",
		tokens: []TestCaseToken{
			{NAME, "utils"},
			{NAMESPACE, "::"},
			{NAME, "list_files"},
			{PIPE, "|"},
			{ELLIPSIS, "..."},
			{NAME, "date"},
		}}
	validateTestCase(t, test_case)
}

func TestPlusAssignment(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a += @b",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{PLUS_ASSIGN, "+="},
			{NAME, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestMinusAssignment(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a -= @b",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{MINUS_ASSIGN, "-="},
			{NAME, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestTimesAssignment(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a *= @b",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{TIMES_ASSIGN, "*="},
			{NAME, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestDivideAssignment(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a /= @b",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{DIVIDE_ASSIGN, "/="},
			{NAME, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestModAssignment(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a %= @b",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{MOD_ASSIGN, "%="},
			{NAME, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestPowerAssignment(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a **= @b",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{POWER_ASSIGN, "**="},
			{NAME, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestIntDivAssignment(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a //= @b",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{INT_DIV_ASSIGN, "//="},
			{NAME, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestConcatAssignment(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a ++= @b",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{CONCAT_ASSIGN, "++="},
			{NAME, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestSeqAndAssignment(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a &&= @b",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{SEQ_AND_ASSIGN, "&&="},
			{NAME, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestSeqOrAssignment(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a ||= @b",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{SEQ_OR_ASSIGN, "||="},
			{NAME, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestPipeAssignment(t *testing.T) {
	test_case := LexerTestCase{
		input: "@a |= @b",
		tokens: []TestCaseToken{
			{NAME, "a"},
			{PIPE_ASSIGN, "|="},
			{NAME, "b"},
		}}
	validateTestCase(t, test_case)
}

func TestAssertion(t *testing.T) {
	test_case := LexerTestCase{
		input: "assert 1 == one()",
		tokens: []TestCaseToken{
			{ASSERT, "assert"},
			{INT, "1"},
			{EQUALS, "=="},
			{NAME, "one"},
			{PAREN_OPEN, "("},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestConstDeclare(t *testing.T) {
	test_case := LexerTestCase{
		input: "const a := 1",
		tokens: []TestCaseToken{
			{CONST, "const"},
			{NAME, "a"},
			{DECLARE, ":="},
			{INT, "1"},
		}}
	validateTestCase(t, test_case)
}

func TestSay(t *testing.T) {
	test_case := LexerTestCase{
		input: "say a b c",
		tokens: []TestCaseToken{
			{SAY, "say"},
			{EXEC_ARG, "a"},
			{EXEC_ARG, "b"},
			{EXEC_ARG, "c"},
		}}
	validateTestCase(t, test_case)
}

func TestIfElifElse(t *testing.T) {
	test_case := LexerTestCase{
		input: "if true {} elif false {} else if true {} else {}",
		tokens: []TestCaseToken{
			{IF, "if"},
			{TRUE, "true"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
			{ELIF, "elif"},
			{FALSE, "false"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
			{ELSE, "else"},
			{IF, "if"},
			{TRUE, "true"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
			{ELSE, "else"},
			{CURLY_OPEN, "{"},
			{CURLY_CLOSE, "}"},
		}}
	validateTestCase(t, test_case)
}

func TestFunctionCall3(t *testing.T) {
	test_case := LexerTestCase{
		input: "foo(1, @a, @x + 1)",
		tokens: []TestCaseToken{
			{NAME, "foo"},
			{PAREN_OPEN, "("},
			{INT, "1"},
			{COMMA, ","},
			{NAME, "a"},
			{COMMA, ","},
			{NAME, "x"},
			{PLUS, "+"},
			{INT, "1"},
			{PAREN_CLOSE, ")"},
		}}
	validateTestCase(t, test_case)
}

func TestNoSpaceArithmetic(t *testing.T) {
	test_case := LexerTestCase{
		input: "(a+c*d * b**a%d)",
		tokens: []TestCaseToken{
			{PAREN_OPEN, "("},
			{NAME, "a"},
			{PLUS, "+"},
			{NAME, "c"},
			{TIMES, "*"},
			{NAME, "d"},
			{TIMES, "*"},
			{NAME, "b"},
			{POWER, "**"},
			{NAME, "a"},
			{MOD, "%"},
			{NAME, "d"},
			{PAREN_CLOSE, ")"},
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
