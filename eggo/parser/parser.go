package parser

import (
	"eggo/lexer"
	"fmt"
	"slices"
)

type Parser struct {
	lex                  *lexer.Lexer
	tokens_parsed        int
	top_level_expression Expression
}

func NewParser(lex *lexer.Lexer, top_level_expression Expression) Parser {
	return Parser{
		lex:                  lex,
		tokens_parsed:        0,
		top_level_expression: top_level_expression,
	}
}

func (p *Parser) Accept(expr Expression) (SyntaxTree, bool) {
	tree, err := expr.Parse(p)
	if err != nil {
		return SyntaxTree{}, false
	}
	return tree, true
}

func (p *Parser) AcceptAnyOf(exprs ...Expression) (SyntaxTree, bool) {
	for _, expr := range exprs {
		if tree, ok := p.Accept(expr); ok {
			return tree, true
		}
	}
	return SyntaxTree{}, false
}

func (p *Parser) AcceptAnyOfToken(token_types ...lexer.TokenType) (lexer.Token, bool) {
	if p.tokens_parsed >= len(p.lex.Tokens) {
		return lexer.Token{}, false
	}
	next_token := p.lex.Tokens[p.tokens_parsed]
	if slices.Contains(token_types, next_token.Type) {
		p.tokens_parsed++
		return next_token, true
	}
	return lexer.Token{}, false
}

func (p *Parser) AcceptToken(token_type lexer.TokenType) (lexer.Token, bool) {
	if p.tokens_parsed >= len(p.lex.Tokens) {
		return lexer.Token{}, false
	}
	next_token := p.lex.Tokens[p.tokens_parsed]
	if next_token.Type != token_type {
		return lexer.Token{}, false
	}
	p.tokens_parsed++
	return next_token, true
}

func (p *Parser) Require(e Expression) (SyntaxTree, error) {
	tree, err := e.Parse(p)
	if err != nil {
		return SyntaxTree{}, fmt.Errorf("error parsing: %w", err)
	}
	return tree, nil
}

func (p *Parser) RequireToken(token_type lexer.TokenType) (lexer.Token, error) {
	if p.tokens_parsed >= len(p.lex.Tokens) {
		return lexer.Token{}, fmt.Errorf("unexpected end of file")
	}
	next_token := p.lex.Tokens[p.tokens_parsed]
	if next_token.Type != token_type {
		return lexer.Token{}, fmt.Errorf("expected token %s, got %s", token_type.DebugName(), next_token.Type.DebugName())
	}
	p.tokens_parsed++
	return next_token, nil
}

func (p *Parser) Parse() (SyntaxTree, error) {
	if err := p.lex.Lex(); err != nil {
		return SyntaxTree{}, fmt.Errorf("error lexing: %w", err)
	}
	return p.top_level_expression.Parse(p)
}
