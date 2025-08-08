package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"eggo/source"
	"testing"

	"github.com/google/go-cmp/cmp"
)

func assertParse(t *testing.T, tokens []lexer.Token, expected parser.SyntaxTree, expr parser.Expression) {
	lex := lexer.MockLexer(tokens)
	parser := parser.NewParser(&lex, expr)
	tree, _, err := parser.Parse(0)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if diff := cmp.Diff(expected, tree); diff != "" {
		t.Fatalf("Parse() mismatch (-want +got):\n%s", diff)
	}
}

func assertParseFails(t *testing.T, tokens []lexer.Token, expr parser.Expression) {
	lex := lexer.MockLexer(tokens)
	parser := parser.NewParser(&lex, expr)
	if tree, _, err := parser.Parse(0); err == nil {
		t.Fatalf("Expected error but got: %v", tree.Expr.DebugName())
	}
}

func exampleSourceLocation() source.SourceLocation {
	return source.SourceLocation{
		FilePath: "foo",
		Offset:   0,
		Length:   5,
	}
}
func getTestLoc(index int) source.SourceLocation {
	return source.SourceLocation{
		FilePath: "",
		Offset:   10 * index,
		Length:   10,
	}
}
