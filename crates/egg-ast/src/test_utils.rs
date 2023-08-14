use egg_grammar::*;

use crate::annotations::Annotations;
use crate::ast::*;

pub fn example_ast() -> Ast {
    /*
    Input:
        a a | b | c > d
        say "hi" >> file_name
    */
    Ast {
        nodes: Vec::from([
            AstNode {
                symbol: Symbol::Program,
                children: Vec::from([1, 19]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::ExecChain,
                children: Vec::from([2, 5]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Exec,
                children: Vec::from([3, 4]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(0),
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(1),
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::PipeExec,
                children: Vec::from([6, 7]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(2),
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::ExecChain,
                children: Vec::from([8, 10]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Exec,
                children: Vec::from([9]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(3),
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::PipeExec,
                children: Vec::from([11, 12]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(4),
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::ExecChain,
                children: Vec::from([13, 15]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Exec,
                children: Vec::from([14]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(5),
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::RedirectExec,
                children: Vec::from([16, 17]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(6),
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::RedirectTarget,
                children: Vec::from([18]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(7),
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::ExecChain,
                children: Vec::from([20, 23]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Exec,
                children: Vec::from([21, 22]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(9),
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(10),
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::RedirectExec,
                children: Vec::from([24, 25]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(11),
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::RedirectTarget,
                children: Vec::from([26]),
                token: None,
                annotations: Annotations::new(),
            },
            AstNode {
                symbol: Symbol::Lexeme,
                children: Vec::from([]),
                token: Some(12),
                annotations: Annotations::new(),
            },
        ]),
    }
}
