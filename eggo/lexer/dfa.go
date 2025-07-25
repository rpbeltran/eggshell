package lexer

import "eggo/source"

type DFANode interface {
	DebugString() string
	consume(c byte, lexer *Lexer, state *DFAState) error
}

type DFAState struct {
	token_start              int
	head                     int
	curly_depth              int16
	paren_depth              int16
	square_depth             int16
	prev_token_type          TokenType
	state_node               DFANode
	all_operators            MaxMuchTrie
	non_arithmetic_operators MaxMuchTrie
	keywords                 map[string]TokenType
}

func NewDfaState() DFAState {
	return DFAState{
		token_start:              0,
		head:                     0,
		curly_depth:              0,
		paren_depth:              0,
		square_depth:             0,
		prev_token_type:          Unspecified,
		state_node:               StartNode{},
		all_operators:            AllOperatorsTrie(),
		non_arithmetic_operators: NonArithmeticOperatorsTrie(),
		keywords:                 KeywordPatterns(),
	}
}

func (state *DFAState) Transition(node DFANode) {
	state.state_node = node
	state.token_start = state.head + 1
}

func (state *DFAState) StepBack() {
	state.head--
}

func (state *DFAState) InBlock() bool {
	return state.curly_depth > 0 || state.paren_depth > 0 || state.square_depth > 0
}

func (state *DFAState) Yield(lexer *Lexer, token TokenType, inclusive bool) {
	lexer.Tokens = append(lexer.Tokens, Token{
		Type: token,
		Loc:  state.GetLocation(inclusive),
	})
	state.prev_token_type = token
}

func (state *DFAState) GetLocation(inclusive bool) source.SourceLocation {
	length := state.head - state.token_start
	if inclusive {
		length += 1
	}
	return source.SourceLocation{
		Offset: state.token_start,
		Length: length,
	}

}

func (state *DFAState) Peek(Lexer *Lexer) byte {
	return Lexer.GetSource().Data()[state.head+1]
}

func (state *DFAState) next_nonwhitespace(lexer Lexer) byte {
	for i := state.head; i < lexer.GetSource().Length(); i++ {
		c := lexer.GetSource().Data()[i]
		if c != ' ' && c != '\t' && c != '\n' {
			return c
		}
	}
	return ';'
}
