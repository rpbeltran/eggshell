package parser

import (
	"eggo/lexer"
	"fmt"
)

type Parser struct {
	lex                  *lexer.Lexer
	tokens_parsed        int
	top_level_expression Expression
}

func NewParser(lex *lexer.Lexer) Parser {
	return Parser{
		lex:           lex,
		tokens_parsed: 0,
	}
}

func (p *Parser) Parse() (SyntaxTree, error) {
	if err := p.lex.Lex(); err != nil {
		return SyntaxTree{}, fmt.Errorf("error lexing: %w", err)
	}
	return p.top_level_expression.require(p)
}
