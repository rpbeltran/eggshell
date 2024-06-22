from .mm_trie import MaxMunchTrie


def _make_max_munch_safe(d):
    return dict(sorted(d.items(), reverse=True))


NON_ARITHMETIC_OPERATORS = {
    '...': 'ELLIPSIS',
    ':=': 'DECLARE',
    '+=': 'PLUS_ASSIGN',
    '-=': 'MINUS_ASSIGN',
    '*=': 'TIMES_ASSIGN',
    '/=': 'DIVIDE_ASSIGN',
    '%=': 'MOD_ASSIGN',
    '**=': 'POWER_ASSIGN',
    '//=': 'INT_DIV_ASSIGN',
    '++=': 'CONCAT_ASSIGN',
    '|=': 'PIPE_ASSIGN',
    '&&=': 'SEQ_AND_ASSIGN',
    '||=': 'SEQ_OR_ASSIGN',
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
}
non_arithmetic_ps_trie = MaxMunchTrie(NON_ARITHMETIC_OPERATORS)

all_operators_trie = MaxMunchTrie(
    {
        **NON_ARITHMETIC_OPERATORS,
        '**': 'POWER',
        '//': 'INT_DIV',
        '*': 'TIMES',
        '/': 'DIVIDE',
        '+': 'PLUS',
        '-': 'MINUS',
        '%': 'MOD',
    }
)

KEYWORDS = _make_max_munch_safe(
    {
        'assert': 'ASSERT',
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
        'with': 'WITH',
        'by': 'BY',
        'say': 'SAY',
    }
)

UNITS = _make_max_munch_safe(
    {
        'b': 'size',
        'kb': 'size',
        'mb': 'size',
        'gb': 'size',
        'tb': 'size',
        'pb': 'size',
        'kib': 'size',
        'mib': 'size',
        'gib': 'size',
        'tib': 'size',
        'pib': 'size',
        'ns': 'time',
        'us': 'time',
        'ms': 'time',
        'sec': 'time',
        'min': 'time',
        'hr': 'time',
        'day': 'time',
        'wk': 'time',
    }
)
