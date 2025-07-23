package lexer

import (
	"eggo/source"
)

type Lexer struct {
	Tokens   []Token
	source   *source.Source
	dfaState DFAState
}

func NewLexer(src *source.Source) Lexer {
	return Lexer{
		Tokens:   make([]Token, 0),
		source:   src,
		dfaState: NewDfaState(),
	}
}

func (lexer *Lexer) GetSource() *source.Source {
	return lexer.source
}

func (lexer *Lexer) Lex() error {
	for lexer.dfaState.head < len(lexer.source.Data()) {
		c := lexer.source.Data()[lexer.dfaState.head]
		if err := lexer.dfaState.state_node.consume(c, lexer, &lexer.dfaState); err != nil {
			return err
		}
		lexer.dfaState.head++
	}
	return nil
}
