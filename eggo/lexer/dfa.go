package lexer

import "eggo/source"

type DFANode interface {
	DebugString() string
	consume(c byte, lexer *Lexer, state *DFAState)
}

type DFAState struct {
	token_start     int
	head            int
	curly_depth     int16
	paren_depth     int16
	square_depth    int16
	prev_token_type TokenType
	state_node      DFANode
}

func (state *DFAState) Transition(node DFANode) {
	state.state_node = node
	state.token_start = state.head + 1
}

func (state *DFAState) StepBack() {
	state.head--
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
