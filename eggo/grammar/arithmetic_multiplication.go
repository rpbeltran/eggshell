package grammar

import (
	"eggo/lexer"
	"eggo/parser"
)

/*
# --- Multiplication/Division

?arithmetic_mul: multiply | divide | int_divide | modulus | arithmetic_pow

multiply: arithmetic_mul "TIMES" arithmetic_pow
divide: arithmetic_mul "DIVIDE" arithmetic_pow
int_divide: arithmetic_mul "INT_DIV" arithmetic_pow
modulus: arithmetic_mul "MOD" arithmetic_pow

# --- Exponentiation

?arithmetic_pow: raise_power | arith_level_unary

raise_power: arith_level_unary "POWER" arithmetic_pow
*/

// Arithmetic at the multiplication level

type ArithLevelMultiplicationExpr struct{}

func (expr ArithLevelMultiplicationExpr) DebugName() string {
	return "ArithLevelMultiplicationExpr"
}

func (expr ArithLevelMultiplicationExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	child, new_head, err := p.Require(head, _right_recurse_ArithLevelMultiplicationExpr{})
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}
	return makeBinopLeftAssociative(child, []parser.Expression{
		MultiplyExpr{}, DivideExpr{}, IntDivideExpr{}, ModulusExpr{}, ArithLevelExponentExpr{},
	}), new_head, nil
}

type _right_recurse_ArithLevelMultiplicationExpr struct{}

func (expr _right_recurse_ArithLevelMultiplicationExpr) DebugName() string {
	return "_right_recurse_ArithLevelMultiplicationExpr"
}

func (expr _right_recurse_ArithLevelMultiplicationExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleAnyOfChildUnwrappedCustomError(expr, []parser.Expression{
		MultiplyExpr{}, DivideExpr{}, IntDivideExpr{}, ModulusExpr{}, ArithLevelExponentExpr{}}, p, head,
		"expected an arithmetic expression of precedence >= multiplication")
}

// Multiply

type MultiplyExpr struct{}

func (expr MultiplyExpr) DebugName() string {
	return "Multiply"
}

func (expr MultiplyExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parseBinOp(expr, p, head, ArithLevelExponentExpr{}, lexer.TIMES, _right_recurse_ArithLevelMultiplicationExpr{})
}

// Divide

type DivideExpr struct{}

func (expr DivideExpr) DebugName() string {
	return "Divide"
}

func (expr DivideExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parseBinOp(expr, p, head, ArithLevelExponentExpr{}, lexer.DIVIDE, _right_recurse_ArithLevelMultiplicationExpr{})
}

// Integer Divide

type IntDivideExpr struct{}

func (expr IntDivideExpr) DebugName() string {
	return "IntDivide"
}

func (expr IntDivideExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parseBinOp(expr, p, head, ArithLevelExponentExpr{}, lexer.INT_DIV, _right_recurse_ArithLevelMultiplicationExpr{})
}

// Modulus

type ModulusExpr struct{}

func (expr ModulusExpr) DebugName() string {
	return "Modulus"
}

func (expr ModulusExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parseBinOp(expr, p, head, ArithLevelExponentExpr{}, lexer.MOD, _right_recurse_ArithLevelMultiplicationExpr{})
}

// Exponential Arithmetic Level

type ArithLevelExponentExpr struct{}

func (expr ArithLevelExponentExpr) DebugName() string {
	return "ArithLevelExponent"
}

func (expr ArithLevelExponentExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleAnyOfChildUnwrappedCustomError(expr, []parser.Expression{
		RaisePowerExpr{}, ArithLevelUnaryExpr{},
	}, p, head, "expected an arithmetic expression of precedence >= exponentiation")
}

// Raise Power

type RaisePowerExpr struct{}

func (expr RaisePowerExpr) DebugName() string {
	return "RaisePower"
}

func (expr RaisePowerExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parseBinOp(expr, p, head, ArithLevelUnaryExpr{}, lexer.POWER, ArithLevelExponentExpr{})
}
