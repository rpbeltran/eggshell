package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"testing"
)

func TestLiteralExpr_QuotedString_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.QUOTED_STRING, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: StringLiteralExpr{},
		Data: tokens,
	}

	assertParse(t, tokens, expected_tree, LiteralExpr{})
}

func TestLiteralExpr_Int_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: IntLiteralExpr{},
		Data: tokens,
	}

	assertParse(t, tokens, expected_tree, LiteralExpr{})
}

func TestLiteralExpr_Float_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.FLOAT, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: FloatLiteralExpr{},
		Data: tokens,
	}

	assertParse(t, tokens, expected_tree, LiteralExpr{})
}

func TestLiteralExpr_Bool_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.FALSE, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: BoolLiteralExpr{},
		Data: tokens,
	}

	assertParse(t, tokens, expected_tree, LiteralExpr{})
}

func TestLiteralExpr_Other_ParsingFails(t *testing.T) {
	assertParseFails(t, []lexer.Token{
		{Type: lexer.TEST_A, Loc: exampleSourceLocation()},
	}, LiteralExpr{})
}

func TestStringLiteralExpr_QuotedString_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.QUOTED_STRING, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: StringLiteralExpr{},
		Data: tokens,
	}

	assertParse(t, tokens, expected_tree, StringLiteralExpr{})
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

	assertParse(t, tokens, expected_tree, LiteralExpr{})
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

	assertParse(t, tokens, expected_tree, FloatLiteralExpr{})
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
	assertParse(t, tokens, expected_tree, BoolLiteralExpr{})
}

func TestBoolLiteralExpr_False_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.TRUE, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: BoolLiteralExpr{},
		Data: tokens,
	}
	assertParse(t, tokens, expected_tree, BoolLiteralExpr{})
}

func TestBoolLiteralExpr_Other_ParsingFails(t *testing.T) {
	assertParseFails(t, []lexer.Token{
		{Type: lexer.TEST_A, Loc: exampleSourceLocation()},
	}, BoolLiteralExpr{})
}
