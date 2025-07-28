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
		Expr: AtomicExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: SelectableAtomicExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: LiteralExpr{},
						Children: []parser.SyntaxTree{
							{
								Expr: IntLiteralExpr{},
								Data: tokens,
							},
						},
					},
				},
			},
		},
	}

	assertParse(t, tokens, expected_tree)
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
		Expr: SelectableAtomicExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: LiteralExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: tokens,
					},
				},
			},
		},
	}

	assertParse(t, tokens, expected_tree)
}

func TestSelectableAtomicExpr_Other_ParsingFails(t *testing.T) {
	assertParseFails(t, []lexer.Token{
		{Type: lexer.TEST_A, Loc: exampleSourceLocation()},
	}, SelectableAtomicExpr{})
}
