package grammar

import (
	"eggo/lexer"
	"eggo/parser"
)

/*
# -- Arithmetic --

?arith_level_unary: unary_negate | unary_not | atomic

unary_negate: "MINUS" atomic
unary_not: "NOT" atomic
*/

// Unary Arithmetic Level

type ArithLevelUnaryExpr struct{}

func (expr ArithLevelUnaryExpr) DebugName() string {
	return "UnaryNegate"
}

func (expr ArithLevelUnaryExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleAnyOfChildUnwrapped(expr, []parser.Expression{
		UnaryNegateExpr{}, UnaryNotExpr{}, AtomicExpr{},
	}, p, head)
}

// Unary Negate

type UnaryNegateExpr struct{}

func (expr UnaryNegateExpr) DebugName() string {
	return "UnaryNegate"
}

func (expr UnaryNegateExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	neg_token, new_head, err := p.RequireToken(head, lexer.MINUS)
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	atomic, new_head, err := p.Require(new_head, AtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{atomic},
		Data:     []lexer.Token{neg_token},
	}, new_head, nil
}

// Unary Not

type UnaryNotExpr struct{}

func (expr UnaryNotExpr) DebugName() string {
	return "UnaryNot"
}

func (expr UnaryNotExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	not_token, new_head, err := p.RequireToken(head, lexer.NOT)
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	atomic, new_head, err := p.Require(new_head, AtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{atomic},
		Data:     []lexer.Token{not_token},
	}, new_head, nil
}
