package parser

type Expression interface {
	DebugName() string

	accept(parser *Parser) (SyntaxTree, bool)
	require(parser *Parser) (SyntaxTree, error)
}
