package parser

type Expression interface {
	DebugName() string

	AllowsUnwrap() bool

	Parse(parser *Parser) (SyntaxTree, error)
}
