package lexer

type StartNode struct{}

func (node StartNode) DebugString() string {
	return "<StartNode>"
}

func (node StartNode) consume(c byte, lexer *Lexer) {
	// TODO
}

type OperatorsNode struct{}

func (node OperatorsNode) DebugString() string {
	return "<OperatorsNode>"
}

func (node OperatorsNode) consume(c byte, lexer *Lexer) {
	// TODO
}

type CommentNode struct{}

func (node CommentNode) DebugString() string {
	return "<CommentNode>"
}

func (node CommentNode) consume(c byte, lexer *Lexer) {
	// TODO
}

type IdentifierNode struct{}

func (node IdentifierNode) DebugString() string {
	return "<IdentifierNode>"
}

func (node IdentifierNode) consume(c byte, lexer *Lexer) {
	// TODO
}

type QuotedLiteralNode struct{}

func (node QuotedLiteralNode) DebugString() string {
	return "<QuotedLiteralNode>"
}

func (node QuotedLiteralNode) consume(c byte, lexer *Lexer) {
	// TODO
}

type QuotedArgListNode struct{}

func (node QuotedArgListNode) DebugString() string {
	return "<QuotedArgListNode>"
}

func (node QuotedArgListNode) consume(c byte, lexer *Lexer) {
	// TODO
}
