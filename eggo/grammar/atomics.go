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

func (expr AtomicExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	child, err := p.Require(SelectableAtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, fmt.Errorf("expected literal: %w", err)
	}
	return child, nil
}

// Selectable atomics

type SelectableAtomicExpr struct{}

func (expr SelectableAtomicExpr) DebugName() string {
	return "SelectableAtomic"
}

func (expr SelectableAtomicExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	child, err := p.Require(LiteralExpr{})
	if err != nil {
		return parser.SyntaxTree{}, fmt.Errorf("expected literal: %w", err)
	}
	return child, nil
}
