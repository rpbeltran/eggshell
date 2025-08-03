package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"fmt"
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

func (expr ArithLevelUnaryExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	if child, has_match := p.AcceptAnyOf(UnaryNegateExpr{}, UnaryNotExpr{}, AtomicExpr{}); has_match {
		return child, nil
	}
	return parser.SyntaxTree{}, fmt.Errorf("expected an atomic or a unary expression")
}

// Unary Negate

type UnaryNegateExpr struct{}

func (expr UnaryNegateExpr) DebugName() string {
	return "UnaryNegate"
}

func (expr UnaryNegateExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	neg_token, err := p.RequireToken(lexer.MINUS)
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	atomic, err := p.Require(AtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{atomic},
		Data:     []lexer.Token{neg_token},
	}, nil
}

// Unary Not

type UnaryNotExpr struct{}

func (expr UnaryNotExpr) DebugName() string {
	return "UnaryNot"
}

func (expr UnaryNotExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	not_token, err := p.RequireToken(lexer.NOT)
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	atomic, err := p.Require(AtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{atomic},
		Data:     []lexer.Token{not_token},
	}, nil
}
