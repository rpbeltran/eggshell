package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"testing"
)

func TestArithLevelAdditionExpr_unaryExpression_ParsingSucceeds(t *testing.T) {
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
	assertParse(t, tokens, expected_tree, ArithLevelAdditionExpr{})
}

func TestArithLevelAdditionExpr_multiply_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.TIMES, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: MultiplyExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(2)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.TIMES, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelAdditionExpr{})
}

func TestArithLevelAdditionExpr_addition_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.PLUS, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: AdditionExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(2)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.PLUS, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelAdditionExpr{})
}

func TestArithLevelAdditionExpr_subtraction_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.MINUS, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: SubtractionExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(2)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.MINUS, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelAdditionExpr{})
}

func TestArithLevelAdditionExpr_concat_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.CONCAT, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: ConcatExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(2)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.CONCAT, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelAdditionExpr{})
}

func TestArithLevelAdditionExpr_plusPlus_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.PLUS, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
		{Type: lexer.PLUS, Loc: getTestLoc(3)},
		{Type: lexer.INT, Loc: getTestLoc(4)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: AdditionExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: AdditionExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(2)},
						},
					},
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(4)},
						},
					},
				},
				Data: []lexer.Token{
					{Type: lexer.PLUS, Loc: getTestLoc(3)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.PLUS, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelAdditionExpr{})
}

func TestArithLevelAdditionExpr_plusTimes_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.PLUS, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
		{Type: lexer.TIMES, Loc: getTestLoc(3)},
		{Type: lexer.INT, Loc: getTestLoc(4)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: AdditionExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: MultiplyExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(2)},
						},
					},
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(4)},
						},
					},
				},
				Data: []lexer.Token{
					{Type: lexer.TIMES, Loc: getTestLoc(3)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.PLUS, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelAdditionExpr{})
}
