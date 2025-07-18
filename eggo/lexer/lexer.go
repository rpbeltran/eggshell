package lexer

import "eggo/source"

type Lexer struct {
	Tokens   []Token
	source   *source.Source
	dfaState DFAState
}

func NewLexer(src *source.Source) Lexer {
	return Lexer{
		Tokens: make([]Token, 0),
		source: src,
		dfaState: DFAState{
			token_start:     0,
			head:            0,
			curly_depth:     0,
			paren_depth:     0,
			square_depth:    0,
			prev_token_type: Unspecified,
			state_node:      StartNode{},
		},
	}
}
