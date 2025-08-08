package grammar

import (
	"eggo/lexer"
	"eggo/parser"
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

func (expr SelectElementExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	new_head := head
	lhs, new_head, err := p.Require(new_head, SelectableAtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	open, new_head, err := p.RequireToken(new_head, lexer.SQUARE_OPEN)
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	rhs, new_head, err := p.Require(new_head, ExpressionExpr{})
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	close, new_head, err := p.RequireToken(new_head, lexer.SQUARE_CLOSE)
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	return parser.SyntaxTree{
		Expr:     expr,
		Children: []parser.SyntaxTree{lhs, rhs},
		Data:     []lexer.Token{open, close},
	}, new_head, nil
}

// Select Slice

type SelectSliceExpr struct{}

func (expr SelectSliceExpr) DebugName() string {
	return "SelectSlice"
}

func (expr SelectSliceExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	lhs, new_head, err := p.Require(head, SelectableAtomicExpr{})
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	open, new_head, err := p.RequireToken(new_head, lexer.SQUARE_OPEN)
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	start, new_head, has_start := p.Accept(new_head, _sliceStartExpr{})

	colon, new_head, err := p.RequireToken(new_head, lexer.COLON)
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	end, new_head, has_end := p.Accept(new_head, _sliceEndExpr{})

	children := []parser.SyntaxTree{lhs}
	if has_start {
		children = append(children, start)
	}
	if has_end {
		children = append(children, end)
	}

	by, new_head, has_by := p.AcceptToken(new_head, lexer.BY)
	if has_by {
		jump, head_j, err := p.Require(new_head, _sliceJumpExpr{})
		if err != nil {
			return parser.SyntaxTree{}, head, err
		}
		children = append(children, jump)
		new_head = head_j
	}

	close, new_head, err := p.RequireToken(new_head, lexer.SQUARE_CLOSE)
	if err != nil {
		return parser.SyntaxTree{}, head, err
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
	}, new_head, nil
}

// -- inner

type _sliceStartExpr struct{}

func (expr _sliceStartExpr) DebugName() string {
	return "_sliceStartExpr"
}

func (expr _sliceStartExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleChild(expr, SelectableAtomicExpr{}, p, head)
}

type _sliceEndExpr struct{}

func (expr _sliceEndExpr) DebugName() string {
	return "_sliceEndExpr"
}

func (expr _sliceEndExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleChild(expr, SelectableAtomicExpr{}, p, head)
}

type _sliceJumpExpr struct{}

func (expr _sliceJumpExpr) DebugName() string {
	return "_sliceJumpExpr"
}

func (expr _sliceJumpExpr) Parse(p parser.Parser, head int) (parser.SyntaxTree, int, error) {
	return parser.ParseSingleChildCustomError(expr, SelectableAtomicExpr{}, p, head, "slices with BY require an expression after BY")
}
