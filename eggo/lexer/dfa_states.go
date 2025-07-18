package lexer

import "eggo/source"

type StartNode struct{}

func (node StartNode) DebugString() string {
	return "<StartNode>"
}

func (node StartNode) consume(c byte, lexer *Lexer, state *DFAState) {
	// TODO
}

type OperatorsNode struct{}

func (node OperatorsNode) DebugString() string {
	return "<OperatorsNode>"
}

func (node OperatorsNode) consume(c byte, lexer *Lexer, state *DFAState) {
	// TODO
}

type CommentNode struct{}

func (node CommentNode) DebugString() string {
	return "<CommentNode>"
}

func (node CommentNode) consume(c byte, lexer *Lexer, state *DFAState) {
	if c == '\n' {
		if state.paren_depth == 0 {
			lexer.Tokens = append(lexer.Tokens, Token{
				Type: SEMICOLON,
				Loc: source.SourceLocation{
					Offset: state.token_start,
					Length: state.head - state.token_start + 1,
				},
			})
		}
		state.Transition(StartNode{})
	}
}

type IdentifierNode struct{}

func (node IdentifierNode) DebugString() string {
	return "<IdentifierNode>"
}

func (node IdentifierNode) consume(c byte, lexer *Lexer, state *DFAState) {
	// TODO
}

type QuotedLiteralNode struct{}

func (node QuotedLiteralNode) DebugString() string {
	return "<QuotedLiteralNode>"
}

func (node QuotedLiteralNode) consume(c byte, lexer *Lexer, state *DFAState) {
	// TODO
}

type QuotedArgListNode struct{}

func (node QuotedArgListNode) DebugString() string {
	return "<QuotedArgListNode>"
}

func (node QuotedArgListNode) consume(c byte, lexer *Lexer, state *DFAState) {
	// TODO
}
