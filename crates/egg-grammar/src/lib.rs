#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum Lexeme {
    Literal,
    Pipe,
    Redirect,
    RedirectAppend,
    LineEnd,
}

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
pub enum Symbol {
    Program,
    ExecChain,
    Exec,
    PipeExec,
    RedirectExec,
    RedirectTarget,
    Lexeme,
    _Placeholder,
}
