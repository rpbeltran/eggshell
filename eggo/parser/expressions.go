package parser

import (
	"eggo/lexer"
	"fmt"
)

type Expression interface {
	DebugName() string

	Parse(parser Parser, head int) (SyntaxTree, int, error)
}

func ParseSingleToken(expr Expression, tok lexer.TokenType, p Parser, head int) (SyntaxTree, int, error) {
	token, new_head, err := p.RequireToken(head, tok)
	if err != nil {
		return SyntaxTree{}, head, err
	}
	return SyntaxTree{
		Expr: expr,
		Data: []lexer.Token{token},
	}, new_head, nil
}

func ParseSingleAnyOfToken(expr Expression, toks []lexer.TokenType, p Parser, head int) (SyntaxTree, int, error) {
	token, new_head, ok := p.AcceptAnyOfToken(head, toks...)
	if !ok {
		return SyntaxTree{}, head, fmt.Errorf("next token not permitted for %s", expr.DebugName())
	}
	return SyntaxTree{
		Expr: expr,
		Data: []lexer.Token{token},
	}, new_head, nil
}

func ParseSingleChild(parent_type Expression, child_type Expression, p Parser, head int) (SyntaxTree, int, error) {
	child, new_head, err := p.Require(head, child_type)
	if err != nil {
		return SyntaxTree{}, head, err
	}
	return SyntaxTree{
		Expr:     parent_type,
		Children: []SyntaxTree{child},
	}, new_head, nil
}

func ParseSingleChildUnwrapped(parent_type Expression, child_type Expression, p Parser, head int) (SyntaxTree, int, error) {
	child, new_head, err := p.Require(head, child_type)
	if err != nil {
		return SyntaxTree{}, head, err
	}
	return child, new_head, nil
}

func ParseSingleChildCustomError(parent_type Expression, child_type Expression, p Parser, head int, err_msg string) (SyntaxTree, int, error) {
	child, new_head, err := p.Require(head, child_type)
	if err != nil {
		return SyntaxTree{}, head, fmt.Errorf("%s: %w", err_msg, err)
	}
	return SyntaxTree{
		Expr:     parent_type,
		Children: []SyntaxTree{child},
	}, new_head, nil
}

func ParseSingleChildUnwrappedCustomError(parent_type Expression, child_type Expression, p Parser, head int, err_msg string) (SyntaxTree, int, error) {
	child, new_head, err := p.Require(head, child_type)
	if err != nil {
		return SyntaxTree{}, head, fmt.Errorf("%s: %w", err_msg, err)
	}
	return child, new_head, nil
}

func ParseSingleAnyOfChild(parent_type Expression, child_types []Expression, p Parser, head int) (SyntaxTree, int, error) {
	child, new_head, ok := p.AcceptAnyOf(head, child_types...)
	if !ok {
		return SyntaxTree{}, head, fmt.Errorf("stream does not match %s", parent_type.DebugName())
	}
	return SyntaxTree{
		Expr:     parent_type,
		Children: []SyntaxTree{child},
	}, new_head, nil
}

func ParseSingleAnyOfChildUnwrapped(parent_type Expression, child_types []Expression, p Parser, head int) (SyntaxTree, int, error) {
	child, new_head, ok := p.AcceptAnyOf(head, child_types...)
	if !ok {
		return SyntaxTree{}, head, fmt.Errorf("stream does not match %s", parent_type.DebugName())
	}
	return child, new_head, nil
}

func ParseSingleAnyOfChildCustomError(parent_type Expression, child_types []Expression, p Parser, head int, err_msg string) (SyntaxTree, int, error) {
	child, new_head, ok := p.AcceptAnyOf(head, child_types...)
	if !ok {
		return SyntaxTree{}, head, fmt.Errorf("%s", err_msg)
	}
	return SyntaxTree{
		Expr:     parent_type,
		Children: []SyntaxTree{child},
	}, new_head, nil
}

func ParseSingleAnyOfChildUnwrappedCustomError(parent_type Expression, child_types []Expression, p Parser, head int, err_msg string) (SyntaxTree, int, error) {
	child, new_head, ok := p.AcceptAnyOf(head, child_types...)
	if !ok {
		return SyntaxTree{}, head, fmt.Errorf("%s", err_msg)
	}
	return child, new_head, nil
}
