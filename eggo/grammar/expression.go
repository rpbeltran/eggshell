package grammar

import (
	"eggo/parser"
)

type ExpressionExpr struct{}

func (expr ExpressionExpr) DebugName() string {
	return "Atomic"
}

// TODO: Implement expression properly
func (expr ExpressionExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleAnyOfChildUnwrapped(expr, []parser.Expression{AtomicExpr{}}, p, head)
}
