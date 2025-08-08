package parser

import (
	"eggo/lexer"
	"fmt"
	"slices"
)

type Parser struct {
	lex                  *lexer.Lexer
	top_level_expression Expression
}

func NewParser(lex *lexer.Lexer, top_level_expression Expression) Parser {
	return Parser{
		lex:                  lex,
		top_level_expression: top_level_expression,
	}
}

func (p Parser) Accept(head int, expr Expression) (SyntaxTree, int, bool) {
	tree, new_head, err := expr.Parse(p, head)
	if err != nil {
		return SyntaxTree{}, head, false
	}
	return tree, new_head, true
}

func (p Parser) AcceptAnyOf(head int, exprs ...Expression) (SyntaxTree, int, bool) {
	for _, expr := range exprs {
		if tree, head, ok := p.Accept(head, expr); ok {
			return tree, head, true
		}
	}
	return SyntaxTree{}, head, false
}

func (p Parser) AcceptAnyOfToken(head int, token_types ...lexer.TokenType) (lexer.Token, int, bool) {
	if head >= len(p.lex.Tokens) {
		return lexer.Token{}, head, false
	}
	next_token := p.lex.Tokens[head]
	if slices.Contains(token_types, next_token.Type) {
		return next_token, head + 1, true
	}
	return lexer.Token{}, head, false
}

func (p Parser) AcceptToken(head int, token_type lexer.TokenType) (lexer.Token, int, bool) {
	if head >= len(p.lex.Tokens) {
		return lexer.Token{}, head, false
	}
	next_token := p.lex.Tokens[head]
	if next_token.Type != token_type {
		return lexer.Token{}, head, false
	}
	return next_token, head + 1, true
}

func (p Parser) Require(head int, e Expression) (SyntaxTree, int, error) {
	tree, new_head, err := e.Parse(p, head)
	if err != nil {
		return SyntaxTree{}, head, fmt.Errorf("error parsing: %w", err)
	}
	return tree, new_head, nil
}

func (p Parser) RequireToken(head int, token_type lexer.TokenType) (lexer.Token, int, error) {
	if head >= len(p.lex.Tokens) {
		return lexer.Token{}, head, fmt.Errorf("unexpected end of file")
	}
	next_token := p.lex.Tokens[head]
	if next_token.Type != token_type {
		return lexer.Token{}, head, fmt.Errorf("expected token %s, got %s", token_type.DebugName(), next_token.Type.DebugName())
	}
	return next_token, head + 1, nil
}

func (p Parser) Parse(head int) (SyntaxTree, int, error) {
	if err := p.lex.Lex(); err != nil {
		return SyntaxTree{}, head, fmt.Errorf("error lexing: %w", err)
	}
	return p.top_level_expression.Parse(p, head)
}
