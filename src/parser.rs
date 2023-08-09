use std::collections::HashMap;

use crate::lexer::Lexeme;

use crate::meta_parse::*;

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

/// Grammar Rule for program.
/// program := exec_chain*$
fn program() -> Rule {
    Rule::from_sym(Symbol::ExecChain).star()
}

/// Grammar Rule for exec_chain.
/// exec_chain := exec (pipe_exec | redirect_exec)? (?=LineEnd+)
fn exec_chain() -> Rule {
    Rule::from_sym(Symbol::Exec)
        .then(
            Rule::from_sym(Symbol::PipeExec)
                .or_sym(Symbol::RedirectExec)
                .maybe(),
        )
        .then(Rule::from_tok(Lexeme::LineEnd).plus().discard())
}

/// Grammar Rule for exec.
/// exec := LITERAL+
fn exec() -> Rule {
    Rule::from_tok(Lexeme::Literal).plus()
}

/// Grammar Rule for pipe_exec.
/// pipe_exec := PIPE exec_chain
fn pipe_exec() -> Rule {
    Rule::from_tok(Lexeme::Pipe).then_sym(Symbol::ExecChain)
}

/// Grammar Rule for redirect_exec.
/// redirect_exec := (REDIRECT | REDIRECT_APPEND) redirect_target
fn redirect_exec() -> Rule {
    Rule::from_tok(Lexeme::Redirect)
        .or_tok(Lexeme::RedirectAppend)
        .then_sym(Symbol::RedirectTarget)
}

/// Grammar Rule for redirect_target.
/// redirect_target := LITERAL (pipe_exec | redirect_exec)?
fn redirect_target() -> Rule {
    Rule::from_tok(Lexeme::Literal).then(
        Rule::from_sym(Symbol::PipeExec)
            .or_sym(Symbol::RedirectExec)
            .maybe(),
    )
}

pub struct Parser {
    pub rules: HashMap<Symbol, Rule>,
    pub entry: Symbol,
}

impl Parser {
    /// Construct a new parser instance from a vector of tokens.
    pub fn new() -> Self {
        Self {
            rules: HashMap::from([
                (Symbol::Program, program()),
                (Symbol::ExecChain, exec_chain()),
                (Symbol::Exec, exec()),
                (Symbol::PipeExec, pipe_exec()),
                (Symbol::RedirectExec, redirect_exec()),
                (Symbol::RedirectTarget, redirect_target()),
            ]),
            entry: Symbol::Program,
        }
    }
}
