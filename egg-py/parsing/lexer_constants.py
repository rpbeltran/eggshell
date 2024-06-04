# Keep operators sorted by length plz.
OPERATORS = {
    # 4-Char Operators
    '(**)': 'POWER',
    '(//)': 'INT_DIV',
    # 3-Char Operators
    '(*)': 'TIMES',
    '(/)': 'DIVIDE',
    '(+)': 'PLUS',
    '(-)': 'MINUS',
    '(%)': 'MOD',
    '...': 'ELLIPSIS',
    # 2-Char Operators
    ':=': 'DECLARE',
    '+=': 'PLUS_ASSIGN',
    '-=': 'MINUS_ASSIGN',
    '*=': 'TIMES_ASSIGN',
    '/=': 'DIVIDE_ASSIGN',
    '%=': 'MOD_ASSIGN',
    '|=': 'PIPE_ASSIGN',
    '>>': 'APPEND_FILE',
    '\\': 'LAMBDA',
    '->': 'ARROW',
    '&&': 'SEQ_AND',
    '||': 'SEQ_OR',
    '::': 'NAMESPACE',
    '==': 'EQUALS',
    '!=': 'NOT_EQUALS',
    '>=': 'GTE',
    '<=': 'LTE',
    '..': 'RANGE',
    '++': 'CONCAT',
    # 1-Char Operators
    ':': 'COLON',
    '=': 'ASSIGN',
    '|': 'PIPE',
    ',': 'COMMA',
    '(': 'PAREN_OPEN',
    ')': 'PAREN_CLOSE',
    '{': 'CURLY_OPEN',
    '}': 'CURLY_CLOSE',
    '<': 'ANGLE_OPEN',
    '>': 'ANGLE_CLOSE',
    '[': 'SQUARE_OPEN',
    ']': 'SQUARE_CLOSE',
    ';': 'SEMICOLON',
    '$': 'CURRY',
    '^': 'POWER',
    '!': 'NOT',
    '~': 'ASYNC',
}

BLOCK_OPERATORS = {
    '**': 'POWER',
    '//': 'INT_DIV',
    **OPERATORS,
    '*': 'TIMES',
    '/': 'DIVIDE',
    '+': 'PLUS',
    '-': 'MINUS',
    '%': 'MOD',
}

OPERATOR_STARTS = {op[0] for op in OPERATORS}
BLOCK_OPERATOR_STARTS = {op[0] for op in BLOCK_OPERATORS}

KEYWORDS = {
    'fn': 'FN',
    'for': 'FOR',
    'while': 'WHILE',
    'loop': 'ALWAYS_LOOP',
    'continue': 'CONTINUE',
    'break': 'BREAK',
    'true': 'TRUE',
    'false': 'FALSE',
    'and': 'AND',
    'or': 'OR',
    'xor': 'XOR',
    'not': 'NOT',
    'return': 'RETURN',
    'ret': 'RETURN',
    'if': 'IF',
    'do': 'DO',
    'in': 'IN',
    'import': 'IMPORT',
    'else': 'ELSE',
    'elif': 'ELIF',
    'use': 'USE',
    'try': 'TRY',
    'catch': 'CATCH',
    'as': 'AS',
    'var': 'VAR',
    'const': 'CONST',
    'class': 'CLASS',
}
