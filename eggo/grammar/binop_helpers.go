package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"slices"
)

func parseBinOp(expr parser.Expression, p parser.Parser, head int, left parser.Expression, op lexer.TokenType, right parser.Expression) (parser.SyntaxTree, int, error) {
	left_child, new_head, err := p.Require(head, left)
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	op_token, new_head, err := p.RequireToken(new_head, op)
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	right_child, new_head, err := p.Require(new_head, right)
	if err != nil {
		return parser.SyntaxTree{}, head, err
	}

	return parser.SyntaxTree{
		Expr: expr,
		Data: []lexer.Token{op_token},
		Children: []parser.SyntaxTree{
			left_child,
			right_child,
		},
	}, new_head, nil
}

func makeBinopLeftAssociative(ast parser.SyntaxTree, group []parser.Expression) parser.SyntaxTree {
	if !slices.Contains(group, ast.Expr) {
		return ast
	}
	var ops []parser.Expression
	var data []lexer.Token
	var terms []*parser.SyntaxTree

	head := &ast
	for {
		ops = append(ops, head.Expr)
		terms = append(terms, &head.Children[0])
		data = append(data, head.Data[0])
		head = &head.Children[1]
		if !slices.Contains(group, head.Expr) {
			terms = append(terms, head)
			break
		}
	}
	opn := len(ops)
	if opn == 1 {
		return ast
	}
	tree := parser.SyntaxTree{
		Expr:     ops[0],
		Children: []parser.SyntaxTree{*terms[0], *terms[1]},
		Data:     []lexer.Token{data[0]},
	}
	for i := 1; i < opn; i++ {
		tree = parser.SyntaxTree{
			Expr:     ops[i],
			Children: []parser.SyntaxTree{tree, *terms[i+1]},
			Data:     []lexer.Token{data[i]},
		}
	}
	return tree
}
