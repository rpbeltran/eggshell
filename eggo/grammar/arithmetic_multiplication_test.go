package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"testing"
)

func TestArithLevelExponentExpr_unaryExpression_ParsingSucceeds(t *testing.T) {
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
	assertParse(t, tokens, expected_tree, ArithLevelExponentExpr{})
}

func TestArithLevelExponentExpr_pow_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.POWER, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: RaisePowerExpr{},
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
			{Type: lexer.POWER, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelExponentExpr{})
}

func TestArithLevelMultiplicationExpr_pow_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.POWER, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: RaisePowerExpr{},
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
			{Type: lexer.POWER, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelMultiplicationExpr{})
}

func TestArithLevelMultiplicationExpr_unaryExpression_ParsingSucceeds(t *testing.T) {
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
	assertParse(t, tokens, expected_tree, ArithLevelMultiplicationExpr{})
}

func TestArithLevelMultiplicationExpr_multiply_ParsingSucceeds(t *testing.T) {
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
	assertParse(t, tokens, expected_tree, ArithLevelMultiplicationExpr{})
}

func TestArithLevelMultiplicationExpr_Divide_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.DIVIDE, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: DivideExpr{},
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
			{Type: lexer.DIVIDE, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelMultiplicationExpr{})
}
func TestArithLevelMultiplicationExpr_IntDivide_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.INT_DIV, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: IntDivideExpr{},
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
			{Type: lexer.INT_DIV, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelMultiplicationExpr{})
}
func TestArithLevelMultiplicationExpr_Modulus_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.MOD, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: ModulusExpr{},
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
			{Type: lexer.MOD, Loc: getTestLoc(1)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelMultiplicationExpr{})
}

func TestArithLevelMultiplicationExpr_divIntDiv_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.DIVIDE, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
		{Type: lexer.INT_DIV, Loc: getTestLoc(3)},
		{Type: lexer.INT, Loc: getTestLoc(4)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: IntDivideExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: DivideExpr{},
				Data: []lexer.Token{
					{Type: lexer.DIVIDE, Loc: getTestLoc(1)},
				},
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
			},
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(4)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.INT_DIV, Loc: getTestLoc(3)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelMultiplicationExpr{})
}

func TestArithLevelMultiplicationExpr_timesIntDivNeg_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.TIMES, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
		{Type: lexer.INT_DIV, Loc: getTestLoc(3)},
		{Type: lexer.MINUS, Loc: getTestLoc(4)},
		{Type: lexer.INT, Loc: getTestLoc(5)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: IntDivideExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: MultiplyExpr{},
				Data: []lexer.Token{
					{Type: lexer.TIMES, Loc: getTestLoc(1)},
				},
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
			},
			{
				Expr: UnaryNegateExpr{},
				Data: []lexer.Token{
					{Type: lexer.MINUS, Loc: getTestLoc(4)},
				},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(5)},
						},
					},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.INT_DIV, Loc: getTestLoc(3)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelMultiplicationExpr{})
}

func TestArithLevelMultiplicationExpr_divIntDivTimes_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.DIVIDE, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
		{Type: lexer.INT_DIV, Loc: getTestLoc(3)},
		{Type: lexer.INT, Loc: getTestLoc(4)},
		{Type: lexer.TIMES, Loc: getTestLoc(5)},
		{Type: lexer.INT, Loc: getTestLoc(6)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: MultiplyExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: IntDivideExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: DivideExpr{},
						Data: []lexer.Token{
							{Type: lexer.DIVIDE, Loc: getTestLoc(1)},
						},
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
					},
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(4)},
						},
					},
				},
				Data: []lexer.Token{
					{Type: lexer.INT_DIV, Loc: getTestLoc(3)},
				},
			},
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(6)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.TIMES, Loc: getTestLoc(5)},
		},
	}

	assertParse(t, tokens, expected_tree, ArithLevelMultiplicationExpr{})
}

func TestArithLevelMultiplicationExpr_TimesDivNegIntDiv_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.INT, Loc: getTestLoc(0)},
		{Type: lexer.TIMES, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
		{Type: lexer.DIVIDE, Loc: getTestLoc(3)},
		{Type: lexer.MINUS, Loc: getTestLoc(4)},
		{Type: lexer.INT, Loc: getTestLoc(5)},
		{Type: lexer.INT_DIV, Loc: getTestLoc(6)},
		{Type: lexer.INT, Loc: getTestLoc(7)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: IntDivideExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: DivideExpr{},
				Data: []lexer.Token{
					{Type: lexer.DIVIDE, Loc: getTestLoc(3)},
				},
				Children: []parser.SyntaxTree{
					{
						Expr: MultiplyExpr{},
						Data: []lexer.Token{
							{Type: lexer.TIMES, Loc: getTestLoc(1)},
						},
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
					},
					{
						Expr: UnaryNegateExpr{},
						Data: []lexer.Token{
							{Type: lexer.MINUS, Loc: getTestLoc(4)},
						},
						Children: []parser.SyntaxTree{
							{
								Expr: IntLiteralExpr{},
								Data: []lexer.Token{
									{Type: lexer.INT, Loc: getTestLoc(5)},
								},
							},
						},
					},
				},
			},
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(7)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.INT_DIV, Loc: getTestLoc(6)},
		},
	}
	assertParse(t, tokens, expected_tree, ArithLevelMultiplicationExpr{})
}
