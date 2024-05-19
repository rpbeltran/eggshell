# Keep operators sorted by length plz.
OPERATORS = {
    # 2-Char Operators
    ':=': 'DECLARE',
    '>>': 'APPEND_FILE',
    '//': 'INT_DIV',
    # 1-Char Operators
    ':': 'COLON',
    '=': 'ASSIGN',
    '|': 'PIPE',
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
    '+': 'PLUS',
    '-': 'MINUS',
    '/': 'DIVIDE',
    '%': 'MOD',
}

OPERATOR_STARTS = {op[0] for op in OPERATORS}

KEYWORDS = {
    'fn': 'FN',
    'for': 'FOR',
    'while': 'WHILE',
    'continue': 'CONTINUE',
    'break': 'BREAK',
    'true': 'TRUE',
    'false': 'FALSE',
    'and': 'AND',
    'or': 'OR',
    'xor': 'XOR',
    'not': 'NOT',
    'ret': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'use': 'USE',
    'try': 'TRY',
    'catch': 'CATCH',
}
