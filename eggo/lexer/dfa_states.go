package lexer

import (
	"eggo/source"
	"fmt"
	"strings"
)

type StartNode struct{}

func (node StartNode) DebugString() string {
	return "<StartNode>"
}

func matchOperator(lexer *Lexer, state *DFAState) (Token, bool) {
	allow_arithmetic := state.InBlock() || state.prev_token_type != EXEC_ARG
	trie := state.non_arithmetic_operators
	if allow_arithmetic {
		trie = state.all_operators
	}
	if match, found := trie.LargestPrefix(lexer.GetSource().Data(), state.head); found {
		return Token{
			Type: match.token,
			Loc: source.SourceLocation{
				FilePath: lexer.source.FilePath(),
				Offset:   state.token_start,
				Length:   match.length,
			},
		}, true
	}
	return Token{}, false
}

func (node StartNode) consumeOperator(tok Token, lexer *Lexer, state *DFAState) {
	lexer.Tokens = append(lexer.Tokens, tok)
	state.prev_token_type = tok.Type
	state.head += tok.Loc.Length
	switch tok.Type {
	case PAREN_OPEN:
		state.paren_depth++
	case PAREN_CLOSE:
		state.paren_depth--
	case CURLY_OPEN:
		state.curly_depth++
	case CURLY_CLOSE:
		state.curly_depth--
	case SQUARE_OPEN:
		state.square_depth++
	case SQUARE_CLOSE:
		state.square_depth--
	}
	state.Transition(StartNode{})
}

func isDigit(c byte) bool {
	return c >= '0' && c <= '9'
}

func isAlpha(c byte) bool {
	return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
}

// Check if c is a letter or if it's in "./*+-%_"
func isIdentifierStart(c byte) bool {
	if isAlpha(c) {
		return true
	}
	switch c {
	case '.', '*', '/', '+', '%', '_':
		return true
	}
	return false
}

func (node StartNode) consume(c byte, lexer *Lexer, state *DFAState) error {
	switch c {
	case '\n':
		if state.paren_depth == 0 {
			state.Yield(lexer, SEMICOLON, false)
		}
		state.prev_token_type = Unspecified
		state.Transition(StartNode{})
		return nil
	case ' ', '\t':
		return nil
	case '#':
		state.StepBack()
		state.Transition(CommentNode{})
		return nil
	case '@':
		state.Transition(IdentifierNode{})
		return nil
	case '"', '\'':
		state.Transition(NewQuotedLiteralNode(c))
		return nil
	case '`':
		state.Transition(NewQuotedArgListNode())
		return nil
	}
	if state.all_operators.FirstByte[c] {
		if token, found := matchOperator(lexer, state); found {
			node.consumeOperator(token, lexer, state)
			return nil
		}
	}
	if isDigit(c) || (c == '-' && isDigit(state.Peek(lexer))) {
		state.StepBack()
		state.Transition(newNumberNode())
		return nil
	} else if isIdentifierStart(c) {
		state.StepBack()
		if state.InBlock() {
			state.Transition(IdentifierNode{})
		} else {
			state.Transition(UnquotedLiteralNode{})
		}
		return nil
	}
	return fmt.Errorf("unexpected character: %c", c)
}

type CommentNode struct{}

func (node CommentNode) DebugString() string {
	return "<CommentNode>"
}

func (node CommentNode) consume(c byte, lexer *Lexer, state *DFAState) error {
	if c == '\n' {
		if state.paren_depth == 0 {
			lexer.Tokens = append(lexer.Tokens, Token{
				Type: SEMICOLON,
				Loc:  state.GetLocation(false),
			})
		}
		state.Transition(StartNode{})
	}
	return nil
}

type NumberNode struct {
	hasDecimal bool
	firstChar  bool
}

func newNumberNode() NumberNode {
	return NumberNode{
		hasDecimal: false,
		firstChar:  true,
	}
}

func (node NumberNode) DebugString() string {
	return "<NumberNode>"
}

func (node NumberNode) getUnits(c byte, state DFAState) (TokenType, bool) {
	// TODO
	return Unspecified, false
}

func (node NumberNode) getTokenType(state DFAState) TokenType {
	if state.prev_token_type == EXEC_ARG {
		return EXEC_ARG
	}
	if node.hasDecimal {
		return FLOAT
	}
	return INT
}

func (node NumberNode) consume(c byte, lexer *Lexer, state *DFAState) error {
	if c == '.' {
		if state.Peek(lexer) == '.' {
			token_type := node.getTokenType(*state)
			state.Yield(lexer, token_type, false)
			state.StepBack()
			state.Transition(StartNode{})
		} else if node.hasDecimal {
			return fmt.Errorf("unexpected decimal point")
		} else {
			node.hasDecimal = true
		}
	} else if !(isDigit(c) || (node.firstChar && c == '-')) {
		token_type := node.getTokenType(*state)
		if token_type != EXEC_ARG {
			if _, has_unit := node.getUnits(c, *state); has_unit {
				return fmt.Errorf("literals w/ units not supported yet")
			}
		}
		state.Yield(lexer, token_type, false)
		state.Transition(StartNode{})
	}
	node.firstChar = false
	return nil
}

type UnquotedLiteralNode struct{}

func (node UnquotedLiteralNode) DebugString() string {
	return "<UnquotedLiteralNode>"
}

func (node UnquotedLiteralNode) consume(c byte, lexer *Lexer, state *DFAState) error {
	space := false
	if c == ' ' || c == '\t' {
		c = state.next_nonwhitespace(*lexer)
		space = true
	}
	text := lexer.GetSource().Data()[state.token_start:state.head]
	tok := node.getTokenType(*state, text)

	if c == '.' && state.Peek(lexer) != '.' && (tok == NAME || tok == IMPLICIT_LAMBDA_PARAM) {
		if len(text) > 0 {
			state.Yield(lexer, tok, false)
		}
		state.token_start = state.head
		state.Yield(lexer, DOT, true)
	} else if c == '(' || c == ':' || c == '=' {
		if kw, has_kw := state.keywords[text]; has_kw {
			state.Yield(lexer, kw, false)
		} else {
			name_parts := strings.Split(text, ".")
			head := state.head
			for i, part := range name_parts {
				if len(part) != 0 {
					part_type := NAME
					if part == "_" {
						part_type = IMPLICIT_LAMBDA_PARAM
					}
					lexer.Tokens = append(lexer.Tokens, Token{
						Type: part_type,
						Loc: source.SourceLocation{
							FilePath: lexer.source.FilePath(),
							Offset:   head,
							Length:   len(part),
						},
					})
					head += len(part)
				} else if i < len(name_parts)-1 {
					lexer.Tokens = append(lexer.Tokens, Token{
						Type: DOT,
						Loc: source.SourceLocation{
							FilePath: lexer.source.FilePath(),
							Offset:   head + 1,
							Length:   1,
						},
					})
				}
				head += 1
			}
		}
		state.Transition(StartNode{})
		state.StepBack()
	} else if space || strings.Contains("<>{}[])|;,\n", string(c)) || (c == '.' && state.Peek(lexer) == '.') {
		state.Yield(lexer, tok, false)
		if c == '\n' && state.paren_depth == 0 {
			lexer.Tokens = append(lexer.Tokens, Token{
				Type: SEMICOLON,
				Loc: source.SourceLocation{
					FilePath: lexer.source.FilePath(),
					Offset:   state.head,
					Length:   1,
				},
			})
		}
		state.Transition(StartNode{})
		state.StepBack()
	} else if c == '@' {
		return fmt.Errorf("unexpected symbol @ in unquoted expression")
	}
	return nil
}

func tokenCanComeBeforeName(token TokenType) bool {
	switch token {
	case AS, BREAK, CATCH, CLASS, COLON, CONTINUE, DOT, ELLIPSIS, FOR, FN, USE, LAMBDA,
		NAMESPACE, PAREN_CLOSE, SQUARE_CLOSE, POWER, INT_DIV, TIMES, DIVIDE, PLUS, MINUS, MOD:
		return true
	}
	return false
}

func (node UnquotedLiteralNode) getTokenType(state DFAState, text string) TokenType {
	if state.prev_token_type == EXEC_ARG {
		return EXEC_ARG
	}
	if kw, has_kw := state.keywords[text]; has_kw {
		return kw
	}
	if text == "_" || strings.HasPrefix(text, "_.") {
		return IMPLICIT_LAMBDA_PARAM
	}
	if state.InBlock() || tokenCanComeBeforeName(state.prev_token_type) {
		return NAME
	}
	return EXEC_ARG
}

type IdentifierNode struct{}

func (node IdentifierNode) DebugString() string {
	return "<IdentifierNode>"
}

func (node IdentifierNode) consume(c byte, lexer *Lexer, state *DFAState) error {
	if c == '.' && state.Peek(lexer) != '.' {
		if state.token_start == state.head {
			return fmt.Errorf("identifier is empty")
		}
		token_type := node.getTokenType(*state, *lexer)
		state.Yield(lexer, token_type, false)
		state.token_start = state.head
		state.Yield(lexer, DOT, true)
		state.token_start += 1
	}
	switch c {
	case ' ', '\t', '\n',
		':', '=', '+', '-', '*', '/', '%', '[', ']', '{', '}', '(', ')', '<', '>', '.', ',', ';':
		if state.token_start == state.head {
			return fmt.Errorf("identifier is empty")
		}
		state.Yield(lexer, node.getTokenType(*state, *lexer), false)
		state.Transition(StartNode{})
		state.StepBack()
	case '@':
		return fmt.Errorf("unexpected symbol @")
	}
	return nil
}

func (node IdentifierNode) getTokenType(state DFAState, lexer Lexer) TokenType {
	text := lexer.GetSource().Data()[state.token_start:state.head]
	if text == "_" {
		return IMPLICIT_LAMBDA
	}
	if kw, has_kw := state.keywords[text]; has_kw {
		return kw
	}
	return NAME
}

type QuotedLiteralNode struct {
	quote_char  byte
	escape_next bool
}

func NewQuotedLiteralNode(quote_char byte) *QuotedLiteralNode {
	return &QuotedLiteralNode{
		quote_char:  quote_char,
		escape_next: false,
	}
}

func (node *QuotedLiteralNode) DebugString() string {
	return "<QuotedLiteralNode>"
}

func (node *QuotedLiteralNode) consume(c byte, lexer *Lexer, state *DFAState) error {
	if node.escape_next || c == '\\' {
		node.escape_next = !node.escape_next
	} else if c == node.quote_char {
		token_type := QUOTED_STRING
		if lexer.dfaState.prev_token_type == EXEC_ARG {
			token_type = EXEC_ARG
		}
		state.Yield(lexer, token_type, true)
		state.Transition(StartNode{})
	}
	return nil
}

type QuotedArgListNode struct {
	escaped    bool
	quoted     bool
	quote_type byte
}

func NewQuotedArgListNode() *QuotedArgListNode {
	return &QuotedArgListNode{
		escaped:    false,
		quoted:     false,
		quote_type: 0,
	}
}

func (node *QuotedArgListNode) DebugString() string {
	return "<QuotedArgListNode>"
}

func (node *QuotedArgListNode) consume(c byte, lexer *Lexer, state *DFAState) error {
	if node.escaped {
		node.escaped = false
	} else if c == '\\' {
		node.escaped = true
	} else if c == '"' || c == '\'' {
		if !node.quoted {
			node.quoted = true
			node.quote_type = c
			state.token_start = state.head + 1
		} else if node.quote_type == c {
			node.quoted = false
			state.Yield(lexer, EXEC_ARG, false)
			state.token_start = state.head + 1
		}
	} else if node.quoted {
		// do nothing
	} else if c == '|' {
		if state.head != state.token_start {
			state.Yield(lexer, EXEC_ARG, false)
		}
		state.token_start = state.head
		state.Yield(lexer, PIPE, true)
		state.token_start += 1
	} else if c == ' ' || c == '\t' || c == '\n' {
		if state.head != state.token_start {
			state.Yield(lexer, EXEC_ARG, false)
		}
		state.token_start = state.head + 1
	} else if c == '`' {
		if state.head != state.token_start {
			state.Yield(lexer, EXEC_ARG, false)
		}
		state.Transition(StartNode{})
	}
	return nil
}
