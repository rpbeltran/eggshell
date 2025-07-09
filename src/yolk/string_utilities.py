# Wrap a string in double quotes.
# Like repr() but always double quoted
def repr_double_quoted(text: str) -> str:
    inner = ''.join('\\"' if c == '"' else c for c in text)
    return f'"{inner}"'
