package grammar

import (
	"eggo/lexer"
	"eggo/parser"
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

func (expr LiteralExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleAnyOfChildUnwrapped(expr, []parser.Expression{
		StringLiteralExpr{}, IntLiteralExpr{}, FloatLiteralExpr{}, BoolLiteralExpr{},
	}, p, head)
}

// Literal String Expressions

type StringLiteralExpr struct{}

func (expr StringLiteralExpr) DebugName() string {
	return "StringLiteral"
}

func (expr StringLiteralExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleToken(expr, lexer.QUOTED_STRING, p, head)
}

// Literal Int Expressions

type IntLiteralExpr struct{}

func (expr IntLiteralExpr) DebugName() string {
	return "IntLiteral"
}

func (expr IntLiteralExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleToken(expr, lexer.INT, p, head)
}

// Literal Float Expressions

type FloatLiteralExpr struct{}

func (expr FloatLiteralExpr) DebugName() string {
	return "FloatLiteral"
}

func (expr FloatLiteralExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleToken(expr, lexer.FLOAT, p, head)
}

// Literal Boolean Expressions

type BoolLiteralExpr struct{}

func (expr BoolLiteralExpr) DebugName() string {
	return "BoolLiteral"
}

func (expr BoolLiteralExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleAnyOfToken(expr, []lexer.TokenType{lexer.TRUE, lexer.FALSE}, p, head)
}
