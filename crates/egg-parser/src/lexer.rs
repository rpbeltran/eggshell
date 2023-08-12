use egg_grammar::Lexeme;

use crate::lexer_util::*;

mod patterns {
    // Control Flow
    pub const SEMICOLON: &str = ";";
    pub const END_LINE: &str = "\n";

    // Operators
    pub const PIPE: &str = r"\|";
    pub const REDIRECT: &str = r#">"#;
    pub const REDIRECTAPPEND: &str = r">>";

    // Literals
    pub const UNQUOTEDLITERALPART: &str = r#"([^\s\\'"`]|(\\((\\){2})*[\s"'`]))"#;
    pub const DOUBLEQUOTEDLITERAL: &str = r#""((\\{2})*|((.|\n)*?[^\\](\\{2})*))""#;
    pub const SINGLEQUOTEDLITERAL: &str = r#"'((\\{2})*|((.|\n)*?[^\\](\\{2})*))'"#;
    pub const BACKQUOTEDLITERAL: &str = r#"`((\\{2})*|((.|\n)*?[^\\](\\{2})*))`"#;
}

use patterns::*;

impl Lexer {
    pub fn new() -> Self {
        let literal_pattern: String = format!(
            "({}|{}|{}|{})+",
            UNQUOTEDLITERALPART, DOUBLEQUOTEDLITERAL, SINGLEQUOTEDLITERAL, BACKQUOTEDLITERAL
        );
        Self {
            patterns: vec![
                (Lexeme::LineEnd, rgx_must(SEMICOLON)),
                (Lexeme::LineEnd, rgx_must(END_LINE)),
                (Lexeme::Pipe, rgx_must(PIPE)),
                (Lexeme::Redirect, rgx_must(REDIRECT)),
                (Lexeme::RedirectAppend, rgx_must(REDIRECTAPPEND)),
                (Lexeme::Literal, rgx_must(literal_pattern.as_str())),
            ],
        }
    }
}
