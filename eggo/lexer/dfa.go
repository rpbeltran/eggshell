package lexer

type DFANode interface {
	DebugString() string
	consume(c byte, lexer *Lexer)
}

type Lexer struct {
	source          string
	source_length   int
	token_start     int
	head            int
	curly_depth     int16
	paren_depth     int16
	square_depth    int16
	prev_token_type TokenType
	state_node      DFANode
}

func NewLexer(source string) Lexer {
	return Lexer{
		source:          source,
		source_length:   len(source),
		token_start:     0,
		head:            0,
		curly_depth:     0,
		paren_depth:     0,
		square_depth:    0,
		prev_token_type: Unspecified,
		state_node:      StartNode{},
	}
}
