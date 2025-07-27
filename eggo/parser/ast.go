package parser

type SyntaxTree struct {
	Expr     Expression
	Children []SyntaxTree
}
