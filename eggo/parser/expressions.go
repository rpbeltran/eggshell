package parser

type Expression interface {
	DebugName() string

	Parse(parser *Parser) (SyntaxTree, error)
}
