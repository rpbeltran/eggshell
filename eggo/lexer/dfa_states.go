package lexer

type StartNode struct{}

func (node StartNode) DebugString() string {
	return "<StartNode>"
}

func (node StartNode) consume(c byte, lexer *Lexer) {
	// TODO
}
