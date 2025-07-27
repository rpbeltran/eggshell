package parser

type Expression interface {
	DebugName() string

	Require(parser *Parser) (SyntaxTree, error)
}
