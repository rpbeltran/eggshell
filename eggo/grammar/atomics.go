package grammar

import (
	"eggo/parser"
)

/*
	atomic: selectable_atomic

	selectable_atomic: literal

	TODO: Support other types of atomics
*/

// All atomics

type AtomicExpr struct{}

func (expr AtomicExpr) DebugName() string {
	return "Atomic"
}

func (expr AtomicExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleAnyOfChildUnwrapped(expr, []parser.Expression{
		SelectableAtomicExpr{},
	}, p, head)
}

// Selectable atomics

type SelectableAtomicExpr struct{}

func (expr SelectableAtomicExpr) DebugName() string {
	return "SelectableAtomic"
}

func (expr SelectableAtomicExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleChildUnwrapped(expr, LiteralExpr{}, p, head)
}
