package grammar

import (
	"eggo/lexer"
	"eggo/parser"
)

/*
# --- Addition/Subtraction

?arith_level_add: addition | subtraction | concatenate | arithmetic_mul

addition: arithmetic_mul "PLUS" arith_level_add
subtraction: arithmetic_mul "MINUS" arith_level_add
concatenate: arithmetic_mul "CONCAT" arith_level_add
*/

// Arithmetic at the multiplication level

type ArithLevelAdditionExpr struct{}

func (expr ArithLevelAdditionExpr) DebugName() string {
	return "ArithLevelAdditionExpr"
}

func (expr ArithLevelAdditionExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleAnyOfChildUnwrapped(expr, []parser.Expression{
		AdditionExpr{}, SubtractionExpr{}, ConcatExpr{}, ArithLevelMultiplicationExpr{},
	}, p, head)
}

// Addition

type AdditionExpr struct{}

func (expr AdditionExpr) DebugName() string {
	return "Addition"
}

func (expr AdditionExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parseBinOp(expr, p, head, ArithLevelMultiplicationExpr{}, lexer.PLUS, ArithLevelAdditionExpr{})
}

// Subtraction

type SubtractionExpr struct{}

func (expr SubtractionExpr) DebugName() string {
	return "Subtraction"
}

func (expr SubtractionExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parseBinOp(expr, p, head, ArithLevelMultiplicationExpr{}, lexer.MINUS, ArithLevelAdditionExpr{})
}

// String Concatenation

type ConcatExpr struct{}

func (expr ConcatExpr) DebugName() string {
	return "Concat"
}

func (expr ConcatExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parseBinOp(expr, p, head, ArithLevelMultiplicationExpr{}, lexer.CONCAT, ArithLevelAdditionExpr{})
}
