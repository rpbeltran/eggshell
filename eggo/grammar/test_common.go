package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"eggo/source"
	"testing"

	"github.com/google/go-cmp/cmp"
)

func assertParse(t *testing.T, tokens []lexer.Token, expected_tree parser.SyntaxTree) {
	lex := lexer.MockLexer(tokens)
	parser := parser.NewParser(&lex, expected_tree.Expr)
	tree, err := parser.Parse()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if diff := cmp.Diff(tree, expected_tree); diff != "" {
		t.Fatalf("Parse() mismatch (-want +got):\n%s", diff)
	}
}

func assertParseFails(t *testing.T, tokens []lexer.Token, expr parser.Expression) {
	lex := lexer.MockLexer(tokens)
	parser := parser.NewParser(&lex, expr)
	if tree, err := parser.Parse(); err == nil {
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
