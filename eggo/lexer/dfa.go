package lexer

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
