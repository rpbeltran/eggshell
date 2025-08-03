package grammar

import (
	"eggo/lexer"
	"eggo/parser"
	"testing"
)

func TestSelectElement_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
		{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
		{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(3)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: SelectElementExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: StringLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: IntLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.INT, Loc: getTestLoc(2)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
			{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(3)},
		},
	}
	assertParse(t, tokens, expected_tree, SelectElementExpr{})
}

func TestSelectSlice_bare_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
		{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
		{Type: lexer.COLON, Loc: getTestLoc(3)},
		{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(4)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: SelectSliceExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: StringLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
			{Type: lexer.COLON, Loc: getTestLoc(3)},
			{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(4)},
		},
	}
	assertParse(t, tokens, expected_tree, SelectSliceExpr{})
}

func TestSelectSlice_startOnly_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
		{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
		{Type: lexer.COLON, Loc: getTestLoc(3)},
		{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(4)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: SelectSliceExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: StringLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: _sliceStartExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(2)},
						},
					},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
			{Type: lexer.COLON, Loc: getTestLoc(3)},
			{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(4)},
		},
	}
	assertParse(t, tokens, expected_tree, SelectSliceExpr{})
}

func TestSelectSlice_endOnly_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
		{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
		{Type: lexer.COLON, Loc: getTestLoc(2)},
		{Type: lexer.INT, Loc: getTestLoc(3)},
		{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(4)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: SelectSliceExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: StringLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: _sliceEndExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(3)},
						},
					},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
			{Type: lexer.COLON, Loc: getTestLoc(2)},
			{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(4)},
		},
	}
	assertParse(t, tokens, expected_tree, SelectSliceExpr{})
}

func TestSelectSlice_startEnd_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
		{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
		{Type: lexer.COLON, Loc: getTestLoc(3)},
		{Type: lexer.INT, Loc: getTestLoc(4)},
		{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(5)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: SelectSliceExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: StringLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: _sliceStartExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(2)},
						},
					},
				},
			},
			{
				Expr: _sliceEndExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(4)},
						},
					},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
			{Type: lexer.COLON, Loc: getTestLoc(3)},
			{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(5)},
		},
	}
	assertParse(t, tokens, expected_tree, SelectSliceExpr{})
}

func TestSelectSlice_startEndBy_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
		{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
		{Type: lexer.INT, Loc: getTestLoc(2)},
		{Type: lexer.COLON, Loc: getTestLoc(3)},
		{Type: lexer.INT, Loc: getTestLoc(4)},
		{Type: lexer.BY, Loc: getTestLoc(5)},
		{Type: lexer.INT, Loc: getTestLoc(6)},
		{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(7)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: SelectSliceExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: StringLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: _sliceStartExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(2)},
						},
					},
				},
			},
			{
				Expr: _sliceEndExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(4)},
						},
					},
				},
			},
			{
				Expr: _sliceJumpExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(6)},
						},
					},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
			{Type: lexer.COLON, Loc: getTestLoc(3)},
			{Type: lexer.BY, Loc: getTestLoc(5)},
			{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(7)},
		},
	}
	assertParse(t, tokens, expected_tree, SelectSliceExpr{})
}

func TestSelectSlice_onlyBy_ParsingSucceeds(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
		{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
		{Type: lexer.COLON, Loc: getTestLoc(3)},
		{Type: lexer.BY, Loc: getTestLoc(5)},
		{Type: lexer.INT, Loc: getTestLoc(6)},
		{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(7)},
	}
	expected_tree := parser.SyntaxTree{
		Expr: SelectSliceExpr{},
		Children: []parser.SyntaxTree{
			{
				Expr: StringLiteralExpr{},
				Data: []lexer.Token{
					{Type: lexer.QUOTED_STRING, Loc: getTestLoc(0)},
				},
			},
			{
				Expr: _sliceJumpExpr{},
				Children: []parser.SyntaxTree{
					{
						Expr: IntLiteralExpr{},
						Data: []lexer.Token{
							{Type: lexer.INT, Loc: getTestLoc(6)},
						},
					},
				},
			},
		},
		Data: []lexer.Token{
			{Type: lexer.SQUARE_OPEN, Loc: getTestLoc(1)},
			{Type: lexer.COLON, Loc: getTestLoc(3)},
			{Type: lexer.BY, Loc: getTestLoc(5)},
			{Type: lexer.SQUARE_CLOSE, Loc: getTestLoc(7)},
		},
	}
	assertParse(t, tokens, expected_tree, SelectSliceExpr{})
}
