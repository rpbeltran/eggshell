package parser

import "eggo/lexer"

type SyntaxTree struct {
	Expr     Expression
	Children []SyntaxTree
	Data     []lexer.Token
}
