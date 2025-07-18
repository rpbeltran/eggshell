package lexer

import (
	"eggo/source"
	"fmt"
)

type TokenType int

type Token struct {
	Type TokenType
	Loc  source.SourceLocation
}

const (
	Unspecified TokenType = iota
	_TEST_A
	_TEST_B
	_TEST_C
	_TEST_D
	ALWAYS_LOOP
	AND
	ANGLE_CLOSE
	ANGLE_OPEN
	APPEND_FILE
	ARROW
	AS
	ASSERT
	ASSIGN
	ASYNC
	BREAK
	BY
	CATCH
	CLASS
	COLON
	COMMA
	CONCAT
	CONCAT_ASSIGN
	CONST
	CONTINUE
	CURLY_CLOSE
	CURLY_OPEN
	CURRY
	DECLARE
	DIVIDE
	DIVIDE_ASSIGN
	DO
	ELIF
	ELLIPSIS
	ELSE
	EQUALS
	FALSE
	FN
	FOR
	GTE
	IF
	IMPORT
	IN
	INT_DIV
	INT_DIV_ASSIGN
	LAMBDA
	LTE
	MINUS
	MINUS_ASSIGN
	MOD
	MOD_ASSIGN
	NAMESPACE
	NOT
	NOT_EQUALS
	OR
	PAREN_CLOSE
	PAREN_OPEN
	PIPE
	PIPE_ASSIGN
	PLUS
	PLUS_ASSIGN
	POWER
	POWER_ASSIGN
	RANGE
	RETURN
	SAY
	SEMICOLON
	SEQ_AND
	SEQ_AND_ASSIGN
	SEQ_OR
	SEQ_OR_ASSIGN
	UNIT_SIZE
	SQUARE_CLOSE
	SQUARE_OPEN
	UNIT_TIME
	TIMES
	TIMES_ASSIGN
	TRUE
	TRY
	VAR
	WHILE
	WITH
	XOR
)

func (t TokenType) DebugName() string {
	switch t {
	case Unspecified:
		return "Unspecified"
	case _TEST_A:
		return "_TEST_A"
	case _TEST_B:
		return "_TEST_B"
	case _TEST_C:
		return "_TEST_C"
	case _TEST_D:
		return "_TEST_D"
	case ALWAYS_LOOP:
		return "ALWAYS_LOOP"
	case AND:
		return "AND"
	case ANGLE_CLOSE:
		return "ANGLE_CLOSE"
	case ANGLE_OPEN:
		return "ANGLE_OPEN"
	case APPEND_FILE:
		return "APPEND_FILE"
	case ARROW:
		return "ARROW"
	case AS:
		return "AS"
	case ASSERT:
		return "ASSERT"
	case ASSIGN:
		return "ASSIGN"
	case ASYNC:
		return "ASYNC"
	case BREAK:
		return "BREAK"
	case BY:
		return "BY"
	case CATCH:
		return "CATCH"
	case CLASS:
		return "CLASS"
	case COLON:
		return "COLON"
	case COMMA:
		return "COMMA"
	case CONCAT:
		return "CONCAT"
	case CONCAT_ASSIGN:
		return "CONCAT_ASSIGN"
	case CONST:
		return "CONST"
	case CONTINUE:
		return "CONTINUE"
	case CURLY_CLOSE:
		return "CURLY_CLOSE"
	case CURLY_OPEN:
		return "CURLY_OPEN"
	case CURRY:
		return "CURRY"
	case DECLARE:
		return "DECLARE"
	case DIVIDE:
		return "DIVIDE"
	case DIVIDE_ASSIGN:
		return "DIVIDE_ASSIGN"
	case DO:
		return "DO"
	case ELIF:
		return "ELIF"
	case ELLIPSIS:
		return "ELLIPSIS"
	case ELSE:
		return "ELSE"
	case EQUALS:
		return "EQUALS"
	case FALSE:
		return "FALSE"
	case FN:
		return "FN"
	case FOR:
		return "FOR"
	case GTE:
		return "GTE"
	case IF:
		return "IF"
	case IMPORT:
		return "IMPORT"
	case IN:
		return "IN"
	case INT_DIV:
		return "INT_DIV"
	case INT_DIV_ASSIGN:
		return "INT_DIV_ASSIGN"
	case LAMBDA:
		return "LAMBDA"
	case LTE:
		return "LTE"
	case MINUS:
		return "MINUS"
	case MINUS_ASSIGN:
		return "MINUS_ASSIGN"
	case MOD:
		return "MOD"
	case MOD_ASSIGN:
		return "MOD_ASSIGN"
	case NAMESPACE:
		return "NAMESPACE"
	case NOT:
		return "NOT"
	case NOT_EQUALS:
		return "NOT_EQUALS"
	case OR:
		return "OR"
	case PAREN_CLOSE:
		return "PAREN_CLOSE"
	case PAREN_OPEN:
		return "PAREN_OPEN"
	case PIPE:
		return "PIPE"
	case PIPE_ASSIGN:
		return "PIPE_ASSIGN"
	case PLUS:
		return "PLUS"
	case PLUS_ASSIGN:
		return "PLUS_ASSIGN"
	case POWER:
		return "POWER"
	case POWER_ASSIGN:
		return "POWER_ASSIGN"
	case RANGE:
		return "RANGE"
	case RETURN:
		return "RETURN"
	case SAY:
		return "SAY"
	case SEMICOLON:
		return "SEMICOLON"
	case SEQ_AND:
		return "SEQ_AND"
	case SEQ_AND_ASSIGN:
		return "SEQ_AND_ASSIGN"
	case SEQ_OR:
		return "SEQ_OR"
	case SEQ_OR_ASSIGN:
		return "SEQ_OR_ASSIGN"
	case UNIT_SIZE:
		return "UNIT_SIZE"
	case SQUARE_CLOSE:
		return "SQUARE_CLOSE"
	case SQUARE_OPEN:
		return "SQUARE_OPEN"
	case UNIT_TIME:
		return "UNIT_TIME"
	case TIMES:
		return "TIMES"
	case TIMES_ASSIGN:
		return "TIMES_ASSIGN"
	case TRUE:
		return "TRUE"
	case TRY:
		return "TRY"
	case VAR:
		return "VAR"
	case WHILE:
		return "WHILE"
	case WITH:
		return "WITH"
	case XOR:
		return "XOR"
	}
	panic(fmt.Sprintf("Unknown token type: %v", t))
}
