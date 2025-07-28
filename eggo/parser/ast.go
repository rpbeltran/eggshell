package parser

import "eggo/lexer"

type SyntaxTree struct {
	Expr     Expression
	Children []SyntaxTree
	Data     []lexer.Token
}

func (tree *SyntaxTree) Unwrap() {
	if tree.Expr.AllowsUnwrap() && len(tree.Children) == 1 {
		tree.Expr = tree.Children[0].Expr
		tree.Data = tree.Children[0].Data
		tree.Children = tree.Children[0].Children
	}
}
