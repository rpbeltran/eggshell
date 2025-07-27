package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"eggo/source"
	"testing"

	"github.com/google/go-cmp/cmp"
)

func TestStringLiteralExpr_QuotedString_ParsingSucceeds(t *testing.T) {
	location := source.SourceLocation{
		FilePath: "foo",
		Offset:   0,
		Length:   5,
	}
	lex := lexer.MockLexer([]lexer.Token{
		{Type: lexer.QUOTED_STRING, Loc: location},
	})
	expected_tree := parser.SyntaxTree{
		Expr: StringLiteralExpr{},
		Data: []lexer.Token{
			{Type: lexer.QUOTED_STRING, Loc: location},
		},
	}
	parser := parser.NewParser(&lex, StringLiteralExpr{})
	tree, err := parser.Parse()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if diff := cmp.Diff(tree, expected_tree); diff != "" {
		t.Fatalf("Parse() mismatch (-want +got):\n%s", diff)
	}
}

func TestStringLiteralExpr_Other_ParsingFails(t *testing.T) {
	location := source.SourceLocation{
		FilePath: "foo",
		Offset:   0,
		Length:   5,
	}
	lex := lexer.MockLexer([]lexer.Token{
		{Type: lexer.INT_DIV, Loc: location},
	})
	parser := parser.NewParser(&lex, StringLiteralExpr{})

	if tree, err := parser.Parse(); err == nil {
		t.Fatalf("Expected error but got: %v", tree.Expr.DebugName())
	}
}

func TestIntLiteralExpr_Int_ParsingSucceeds(t *testing.T) {
	location := source.SourceLocation{
		FilePath: "foo",
		Offset:   0,
		Length:   5,
	}
	lex := lexer.MockLexer([]lexer.Token{
		{Type: lexer.INT, Loc: location},
	})
	expected_tree := parser.SyntaxTree{
		Expr: IntLiteralExpr{},
		Data: []lexer.Token{
			{Type: lexer.INT, Loc: location},
		},
	}
	parser := parser.NewParser(&lex, IntLiteralExpr{})
	tree, err := parser.Parse()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if diff := cmp.Diff(tree, expected_tree); diff != "" {
		t.Fatalf("Parse() mismatch (-want +got):\n%s", diff)
	}
}

func TestIntLiteralExpr_Other_ParsingFails(t *testing.T) {
	location := source.SourceLocation{
		FilePath: "foo",
		Offset:   0,
		Length:   5,
	}
	lex := lexer.MockLexer([]lexer.Token{
		{Type: lexer.INT_DIV, Loc: location},
	})
	parser := parser.NewParser(&lex, IntLiteralExpr{})

	if tree, err := parser.Parse(); err == nil {
		t.Fatalf("Expected error but got: %v", tree.Expr.DebugName())
	}
}

func TestFloatLiteralExpr_Float_ParsingSucceeds(t *testing.T) {
	location := source.SourceLocation{
		FilePath: "foo",
		Offset:   0,
		Length:   5,
	}
	lex := lexer.MockLexer([]lexer.Token{
		{Type: lexer.FLOAT, Loc: location},
	})
	expected_tree := parser.SyntaxTree{
		Expr: FloatLiteralExpr{},
		Data: []lexer.Token{
			{Type: lexer.FLOAT, Loc: location},
		},
	}
	parser := parser.NewParser(&lex, FloatLiteralExpr{})
	tree, err := parser.Parse()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if diff := cmp.Diff(tree, expected_tree); diff != "" {
		t.Fatalf("Parse() mismatch (-want +got):\n%s", diff)
	}
}

func TestFloatLiteralExpr_Other_ParsingFails(t *testing.T) {
	location := source.SourceLocation{
		FilePath: "foo",
		Offset:   0,
		Length:   5,
	}
	lex := lexer.MockLexer([]lexer.Token{
		{Type: lexer.INT_DIV, Loc: location},
	})
	parser := parser.NewParser(&lex, FloatLiteralExpr{})

	if tree, err := parser.Parse(); err == nil {
		t.Fatalf("Expected error but got: %v", tree.Expr.DebugName())
	}
}
