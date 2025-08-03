package grammar

import (
	"eggo/parser"
	"fmt"
)

type ExpressionExpr struct{}

func (expr ExpressionExpr) DebugName() string {
	return "Atomic"
}

func (expr ExpressionExpr) AllowsUnwrap() bool {
	return true
}

// TODO: Implement expression properly
func (expr ExpressionExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	child, err := p.Require(AtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, fmt.Errorf("expected literal: %w", err)
	}
	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{child},
	}, nil
}
