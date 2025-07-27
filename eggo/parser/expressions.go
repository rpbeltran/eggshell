package parser

import "fmt"

type Expression interface {
	getType() ExpressionType

	accept(parser *Parser) (SyntaxTree, bool)
	require(parser *Parser) (SyntaxTree, error)
}

type ExpressionType int

const (
	Unspecified ExpressionType = iota
	_TEST_A
	_TEST_B
	_TEST_C
	_TEST_D
)

func (t ExpressionType) DebugName() string {
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
	}
	panic(fmt.Sprintf("Unknown expression type: %v", t))
}
