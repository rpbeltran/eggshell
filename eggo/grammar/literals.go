package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"fmt"
)

/* GRAMMAR
	literal: StringLiteral
       | IntegerLiteral
       | FloatLiteral
       | BooleanLiteral
	StringLiteral: QUOTED_STRING
	IntegerLiteral: INTEGER
	FloatLiteral: FLOAT
	BooleanLiteral: TRUE | FALSE

	TODO: support literals with units
*/

type LiteralExpr struct{}

func (expr LiteralExpr) DebugName() string {
	return "Literal"
}

func (expr LiteralExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	child, ok := p.AcceptAnyOf(
		StringLiteralExpr{}, IntLiteralExpr{}, FloatLiteralExpr{}, BoolLiteralExpr{})
	if !ok {
		return parser.SyntaxTree{}, fmt.Errorf("expected literal")
	}
	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{child},
	}, nil
}

// Literal String Expressions

type StringLiteralExpr struct{}

func (expr StringLiteralExpr) DebugName() string {
	return "StringLiteral"
}

func (expr StringLiteralExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	token, err := p.RequireToken(lexer.QUOTED_STRING)
	if err != nil {
		return parser.SyntaxTree{}, err
	}
	return parser.SyntaxTree{
		Expr: expr,
		Data: []lexer.Token{token},
	}, nil
}

// Literal Int Expressions

type IntLiteralExpr struct{}

func (expr IntLiteralExpr) DebugName() string {
	return "IntLiteral"
}

func (expr IntLiteralExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	token, err := p.RequireToken(lexer.INT)
	if err != nil {
		return parser.SyntaxTree{}, err
	}
	return parser.SyntaxTree{
		Expr: expr,
		Data: []lexer.Token{token},
	}, nil
}

// Literal Float Expressions

type FloatLiteralExpr struct{}

func (expr FloatLiteralExpr) DebugName() string {
	return "FloatLiteral"
}

func (expr FloatLiteralExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	token, err := p.RequireToken(lexer.FLOAT)
	if err != nil {
		return parser.SyntaxTree{}, err
	}
	return parser.SyntaxTree{
		Expr: expr,
		Data: []lexer.Token{token},
	}, nil
}

// Literal Boolean Expressions

type BoolLiteralExpr struct{}

func (expr BoolLiteralExpr) DebugName() string {
	return "BoolLiteral"
}

func (expr BoolLiteralExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	token, ok := p.AcceptAnyOfToken(lexer.TRUE, lexer.FALSE)
	if !ok {
		return parser.SyntaxTree{}, fmt.Errorf("expected bool literal")
	}
	return parser.SyntaxTree{
		Expr: expr,
		Data: []lexer.Token{token},
	}, nil
}
