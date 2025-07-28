package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"testing"
)

func TestAtomicExpr_Int_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: IntLiteralExpr{},
		Data: tokens,
	}

	assertParse(t, tokens, expected_tree, AtomicExpr{})
}

func TestAtomicExpr_Other_ParsingFails(t *testing.T) {
	assertParseFails(t, []lexer.Token{
		{Type: lexer.TEST_A, Loc: exampleSourceLocation()},
	}, AtomicExpr{})
}

func TestSelectableAtomicExpr_Int_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: exampleSourceLocation()},
	}
	expected_tree := parser.SyntaxTree{
		Expr: IntLiteralExpr{},
		Data: tokens,
	}

	assertParse(t, tokens, expected_tree, SelectableAtomicExpr{})
}

func TestSelectableAtomicExpr_Other_ParsingFails(t *testing.T) {
	assertParseFails(t, []lexer.Token{
		{Type: lexer.TEST_A, Loc: exampleSourceLocation()},
	}, SelectableAtomicExpr{})
}
