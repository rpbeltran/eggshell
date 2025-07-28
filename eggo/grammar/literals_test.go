package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"eggo/source"
	"testing"

	"github.com/google/go-cmp/cmp"
)

func TestStringLiteralExpr_QuotedString_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.QUOTED_STRING, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: StringLiteralExpr{},
		Data: tokens,
	}

	assertParse(t, tokens, expected_tree)
}

func TestStringLiteralExpr_Other_ParsingFails(t *testing.T) {
	assertParseFails(t, []lexer.Token{
		{Type: lexer.TEST_A, Loc: exampleSourceLocation()},
	}, StringLiteralExpr{})
}

func TestIntLiteralExpr_Int_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: IntLiteralExpr{},
		Data: tokens,
	}

	assertParse(t, tokens, expected_tree)
}

func TestIntLiteralExpr_Other_ParsingFails(t *testing.T) {
	assertParseFails(t, []lexer.Token{
		{Type: lexer.TEST_A, Loc: exampleSourceLocation()},
	}, IntLiteralExpr{})
}

func TestFloatLiteralExpr_Float_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.FLOAT, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: FloatLiteralExpr{},
		Data: tokens,
	}

	assertParse(t, tokens, expected_tree)
}

func TestFloatLiteralExpr_Other_ParsingFails(t *testing.T) {
	assertParseFails(t, []lexer.Token{
		{Type: lexer.TEST_A, Loc: exampleSourceLocation()},
	}, FloatLiteralExpr{})
}

func TestBoolLiteralExpr_True_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.TRUE, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: BoolLiteralExpr{},
		Data: tokens,
	}
	assertParse(t, tokens, expected_tree)
}

func TestBoolLiteralExpr_False_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.TRUE, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: BoolLiteralExpr{},
		Data: tokens,
	}
	assertParse(t, tokens, expected_tree)
}

func TestBoolLiteralExpr_Other_ParsingFails(t *testing.T) {
	assertParseFails(t, []lexer.Token{
		{Type: lexer.TEST_A, Loc: exampleSourceLocation()},
	}, BoolLiteralExpr{})
}

func assertParse(t *testing.T, tokens []lexer.Token, expected_tree parser.SyntaxTree) {
	lex := lexer.MockLexer(tokens)
	parser := parser.NewParser(&lex, expected_tree.Expr)
	tree, err := parser.Parse()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if diff := cmp.Diff(tree, expected_tree); diff != "" {
		t.Fatalf("Parse() mismatch (-want +got):\n%s", diff)
	}
}

func assertParseFails(t *testing.T, tokens []lexer.Token, expr parser.Expression) {
	lex := lexer.MockLexer(tokens)
	parser := parser.NewParser(&lex, expr)
	if tree, err := parser.Parse(); err == nil {
		t.Fatalf("Expected error but got: %v", tree.Expr.DebugName())
	}
}

func exampleSourceLocation() source.SourceLocation {
	return source.SourceLocation{
		FilePath: "foo",
		Offset:   0,
		Length:   5,
	}
}
