package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"fmt"
)

/*
	select_element: selectable_atomic "SQUARE_OPEN" expression "SQUARE_CLOSE"

	select_slice: selectable_atomic "SQUARE_OPEN" slice_start? "COLON" slice_end? slice_jump? "SQUARE_CLOSE"
	slice_start: expression
	slice_end: expression
	slice_jump: ("BY" expression)
*/

type SelectElementExpr struct{}

func (expr SelectElementExpr) DebugName() string {
	return "SelectElement"
}

func (expr SelectElementExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	lhs, err := p.Require(SelectableAtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	open, err := p.RequireToken(lexer.SQUARE_OPEN)
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	rhs, err := p.Require(ExpressionExpr{})
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	close, err := p.RequireToken(lexer.SQUARE_CLOSE)
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{lhs, rhs},
		Data:     []lexer.Token{open, close},
	}, nil
}

// Select Slice

type SelectSliceExpr struct{}

func (expr SelectSliceExpr) DebugName() string {
	return "SelectSlice"
}

func (expr SelectSliceExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	lhs, err := p.Require(SelectableAtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	open, err := p.RequireToken(lexer.SQUARE_OPEN)
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	start, has_start := p.Accept(_sliceStartExpr{})

	colon, err := p.RequireToken(lexer.COLON)
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	end, has_end := p.Accept(_sliceEndExpr{})

	children := []parser.SyntaxTree{lhs}
	if has_start {
		children = append(children, start)
	}
	if has_end {
		children = append(children, end)
	}

	by, has_by := p.AcceptToken(lexer.BY)
	if has_by {
		jump, err := p.Require(_sliceJumpExpr{})
		if err != nil {
			return parser.SyntaxTree{}, err
		}
		children = append(children, jump)
	}

	close, err := p.RequireToken(lexer.SQUARE_CLOSE)
	if err != nil {
		return parser.SyntaxTree{}, err
	}

	var data []lexer.Token
	if has_by {
		data = []lexer.Token{open, colon, by, close}
	} else {
		data = []lexer.Token{open, colon, close}
	}

	return parser.SyntaxTree{
		Expr:     expr,
		Children: children,
		Data:     data,
	}, nil
}

// -- inner

type _sliceStartExpr struct{}

func (expr _sliceStartExpr) DebugName() string {
	return "_sliceStartExpr"
}

func (expr _sliceStartExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	child, err := p.Require(SelectableAtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, err
	}
	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{child},
	}, nil
}

type _sliceEndExpr struct{}

func (expr _sliceEndExpr) DebugName() string {
	return "_sliceEndExpr"
}

func (expr _sliceEndExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	child, err := p.Require(SelectableAtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, err
	}
	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{child},
	}, nil
}

type _sliceJumpExpr struct{}

func (expr _sliceJumpExpr) DebugName() string {
	return "_sliceJumpExpr"
}

func (expr _sliceJumpExpr) Parse(p *parser.Parser) (parser.SyntaxTree, error) {
	child, err := p.Require(SelectableAtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, fmt.Errorf("slices with BY require an expression after BY: %w", err)
	}
	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{child},
	}, nil
}
