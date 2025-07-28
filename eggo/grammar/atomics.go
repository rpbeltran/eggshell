package grammar

import (
	"eggo/parser"
	"fmt"
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

func (expr AtomicExpr) AllowsUnwrap() bool {
	return true
}

func (expr AtomicExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	child, ok := p.AcceptAnyOf(SelectableAtomicExpr{})
	if !ok {
		return parser.SyntaxTree{}, fmt.Errorf("expected literal")
	}
	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{child},
	}, nil
}

// Selectable atomics

type SelectableAtomicExpr struct{}

func (expr SelectableAtomicExpr) DebugName() string {
	return "SelectableAtomic"
}

func (expr SelectableAtomicExpr) AllowsUnwrap() bool {
	return true
}

func (expr SelectableAtomicExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	child, ok := p.AcceptAnyOf(LiteralExpr{})
	if !ok {
		return parser.SyntaxTree{}, fmt.Errorf("expected literal")
	}
	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{child},
	}, nil
}
