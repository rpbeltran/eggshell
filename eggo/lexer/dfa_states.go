package lexer

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
				Loc:  state.GetLocation(false),
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

type QuotedLiteralNode struct {
	quote_char  byte
	escape_next bool
}

func NewQuotedLiteralNode(quote_char byte) QuotedLiteralNode {
	return QuotedLiteralNode{
		quote_char:  quote_char,
		escape_next: false,
	}
}

func (node QuotedLiteralNode) DebugString() string {
	return "<QuotedLiteralNode>"
}

func (node *QuotedLiteralNode) consume(c byte, lexer *Lexer, state *DFAState) {
	if node.escape_next || c == '\\' {
		node.escape_next = !node.escape_next
	} else if c == node.quote_char {
		token_type := QUOTED_STRING
		if lexer.LastTokenType() == EXEC_ARG {
			token_type = EXEC_ARG
		}
		lexer.Tokens = append(lexer.Tokens, Token{
			Type: token_type,
			Loc:  state.GetLocation(false),
		})
		state.Transition(StartNode{})
	}
}

type QuotedArgListNode struct{}

func (node QuotedArgListNode) DebugString() string {
	return "<QuotedArgListNode>"
}

func (node QuotedArgListNode) consume(c byte, lexer *Lexer, state *DFAState) {
	// TODO
}
