package lexer

import "maps"

func NonArithmeticOperatorsTrie() MaxMuchTrie {
	return NewMMTrie(nonArithmeticOperatorPatterns())
}

func AllOperatorsTrie() MaxMuchTrie {
	all_operators := arithmeticOperatorPatterns()
	maps.Copy(all_operators, nonArithmeticOperatorPatterns())
	return NewMMTrie(all_operators)
}

func KeywordPatterns() map[string]TokenType {
	return map[string]TokenType{
		"assert":   ASSERT,
		"fn":       FN,
		"for":      FOR,
		"while":    WHILE,
		"loop":     ALWAYS_LOOP,
		"continue": CONTINUE,
		"break":    BREAK,
		"true":     TRUE,
		"false":    FALSE,
		"and":      AND,
		"or":       OR,
		"xor":      XOR,
		"not":      NOT,
		"return":   RETURN,
		"ret":      RETURN,
		"if":       IF,
		"do":       DO,
		"in":       IN,
		"import":   IMPORT,
		"else":     ELSE,
		"elif":     ELIF,
		"try":      TRY,
		"catch":    CATCH,
		"as":       AS,
		"var":      VAR,
		"const":    CONST,
		"class":    CLASS,
		"with":     WITH,
		"by":       BY,
		"say":      SAY,
	}
}

func UnitsPatterns() map[string]TokenType {
	return map[string]TokenType{
		"b":   UNIT_SIZE,
		"kb":  UNIT_SIZE,
		"mb":  UNIT_SIZE,
		"gb":  UNIT_SIZE,
		"tb":  UNIT_SIZE,
		"pb":  UNIT_SIZE,
		"kib": UNIT_SIZE,
		"mib": UNIT_SIZE,
		"gib": UNIT_SIZE,
		"tib": UNIT_SIZE,
		"pib": UNIT_SIZE,
		"ns":  UNIT_TIME,
		"us":  UNIT_TIME,
		"ms":  UNIT_TIME,
		"sec": UNIT_TIME,
		"min": UNIT_TIME,
		"hr":  UNIT_TIME,
		"day": UNIT_TIME,
		"wk":  UNIT_TIME,
	}
}

func nonArithmeticOperatorPatterns() map[string]TokenType {
	return map[string]TokenType{
		"...": ELLIPSIS,
		":=":  DECLARE,
		"+=":  PLUS_ASSIGN,
		"-=":  MINUS_ASSIGN,
		"*=":  TIMES_ASSIGN,
		"/=":  DIVIDE_ASSIGN,
		"%=":  MOD_ASSIGN,
		"**=": POWER_ASSIGN,
		"//=": INT_DIV_ASSIGN,
		"++=": CONCAT_ASSIGN,
		"|=":  PIPE_ASSIGN,
		"&&=": SEQ_AND_ASSIGN,
		"||=": SEQ_OR_ASSIGN,
		">>":  APPEND_FILE,
		"\\":  LAMBDA,
		"->":  ARROW,
		"&&":  SEQ_AND,
		"||":  SEQ_OR,
		"::":  NAMESPACE,
		"==":  EQUALS,
		"!=":  NOT_EQUALS,
		">=":  GTE,
		"<=":  LTE,
		"..":  RANGE,
		"++":  CONCAT,
		":":   COLON,
		"=":   ASSIGN,
		"|":   PIPE,
		",":   COMMA,
		"(":   PAREN_OPEN,
		")":   PAREN_CLOSE,
		"{":   CURLY_OPEN,
		"}":   CURLY_CLOSE,
		"<":   ANGLE_OPEN,
		">":   ANGLE_CLOSE,
		"[":   SQUARE_OPEN,
		"]":   SQUARE_CLOSE,
		";":   SEMICOLON,
		"$":   CURRY,
		"!":   NOT,
		"~":   ASYNC,
	}
}

func arithmeticOperatorPatterns() map[string]TokenType {
	return map[string]TokenType{
		"**": POWER,
		"//": INT_DIV,
		"*":  TIMES,
		"/":  DIVIDE,
		"+":  PLUS,
		"-":  MINUS,
		"%":  MOD,
	}
}
