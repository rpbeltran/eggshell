mod ast;
mod cli;
mod egg_error;
mod lexer;
mod lexer_util;
mod meta_parse;
mod parser;
mod source;
mod token;

use std::path::PathBuf;

use egg_error::*;
use source::SourceManager;

use clap::Parser;

fn main() -> Result<()> {
    let args = cli::Args::parse();

    let mut source_manager = SourceManager::new();

    source_manager.load_file(PathBuf::from(
        "/Users/ryanbeltran/Development/eggshell/examples/split.egg",
    ))?;

    for source in source_manager.files.iter() {
        let lexer = lexer_util::Lexer::new();
        let tokens = lexer.tokenize(source)?;

        if args.show_lexer {
            show_tokens(&tokens, &source_manager)?;
        }

        let mut parser = parser::Parser::new();
        let ast = parser.parse(&tokens)?;

        if args.show_ast {
            show_ast(&ast, &tokens, &source_manager)?;
        }
    }

    Ok(())
}

fn show_tokens(tokens: &Vec<token::Token>, source_manager: &SourceManager) -> Result<()> {
    println!(
        "==========\n= Tokens =\n==========\n---\n - {}\n",
        tokens
            .iter()
            .map(|t| t.to_string(&source_manager))
            .collect::<Result<Vec<String>>>()?
            .join("\n - ")
    );
    Ok(())
}

fn show_ast(
    ast: &ast::Ast,
    tokens: &Vec<token::Token>,
    source_manager: &SourceManager,
) -> Result<()> {
    println!(
        "===============\n= Syntax Tree =\n===============\n{}",
        ast.to_string(tokens, &source_manager)?
    );
    Ok(())
}
