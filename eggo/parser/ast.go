package parser

type SyntaxTree struct {
	expr     ExpressionType
	children []SyntaxTree
}
