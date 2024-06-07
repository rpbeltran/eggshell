
def _make_max_munch_safe(d):
    return dict(sorted(d.items(), reverse=True))


# TODO: Add POWER_ASSIGN and INT_DIVIDE_ASSIGN
NON_ARITHMETIC_OPERATORS = _make_max_munch_safe({
    '...': 'ELLIPSIS',
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
    '!': 'NOT',
    '~': 'ASYNC',
})

ALL_OPERATORS = _make_max_munch_safe({
    **NON_ARITHMETIC_OPERATORS,
    '**': 'POWER',
    '//': 'INT_DIV',
    '*': 'TIMES',
    '/': 'DIVIDE',
    '+': 'PLUS',
    '-': 'MINUS',
    '%': 'MOD',
})

NON_ARITHMETIC_OPERATOR_STARTS = {op[0] for op in NON_ARITHMETIC_OPERATORS}
ALL_OPERATOR_STARTS = {op[0] for op in ALL_OPERATORS}

KEYWORDS = _make_max_munch_safe({
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
    'try': 'TRY',
    'catch': 'CATCH',
    'as': 'AS',
    'var': 'VAR',
    'const': 'CONST',
    'class': 'CLASS',
    'with': 'WITH'
})
