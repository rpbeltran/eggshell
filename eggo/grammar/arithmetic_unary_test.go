package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"testing"
)

func TestArithLevelUnaryExpr_unaryNegate_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.MINUS, Loc: getTestLoc(0)},
		{Type: lexer.INT, Loc: getTestLoc(1)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: UnaryNegateExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(1)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.MINUS, Loc: getTestLoc(0)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelUnaryExpr{})
}

func TestArithLevelUnaryExpr_unaryNot_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.NOT, Loc: getTestLoc(0)},
		{Type: lexer.INT, Loc: getTestLoc(1)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: UnaryNotExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(1)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.NOT, Loc: getTestLoc(0)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelUnaryExpr{})
}

func TestArithLevelUnaryExpr_atomic_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(1)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: IntLiteralExpr{},
		Data: []lexer.Token{
			{Type: lexer.INT, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelUnaryExpr{})
}

func TestUnaryNegateExpr_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.MINUS, Loc: getTestLoc(0)},
		{Type: lexer.INT, Loc: getTestLoc(1)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: UnaryNegateExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(1)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.MINUS, Loc: getTestLoc(0)},
		},
	}
	assertParse(t, tokens, expected_tree, UnaryNegateExpr{})
}

func TestUnaryNotExpr_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.NOT, Loc: getTestLoc(0)},
		{Type: lexer.INT, Loc: getTestLoc(1)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: UnaryNotExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(1)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.NOT, Loc: getTestLoc(0)},
		},
	}
	assertParse(t, tokens, expected_tree, UnaryNotExpr{})
}
