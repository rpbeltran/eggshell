mod cli;

use std::path::PathBuf;

use egg_parser::ast::Ast;
use egg_parser::lexer_util::Lexer;
use egg_parser::token::Token;
use egg_source::source_manager::SourceManager;

use clap::Parser;

fn main() -> egg_errors::Result<()> {
    let args = cli::Args::parse();

    let mut source_manager = SourceManager::new();

    source_manager
        .load_file(PathBuf::from(
            "/Users/ryanbeltran/Development/eggshell/examples/split.egg",
        ))
        .map_err(egg_errors::Error::SourceError)?;

    for source in source_manager.files.iter() {
        let lexer = Lexer::new();
        let tokens = lexer
            .tokenize(source)
            .map_err(egg_errors::Error::ParserError)?;

        if args.show_lexer {
            show_tokens(&tokens, &source_manager)?;
        }

        let mut parser = egg_parser::parser::Parser::new();
        let ast = parser
            .parse(&tokens)
            .map_err(egg_errors::Error::ParserError)?;

        if args.show_ast {
            show_ast(&ast, &tokens, &source_manager)?;
        }
    }

    Ok(())
}

fn show_tokens(tokens: &[Token], source_manager: &SourceManager) -> egg_errors::Result<()> {
    println!(
        "==========\n= Tokens =\n==========\n---\n - {}\n",
        tokens
            .iter()
            .map(|t| t.to_string(source_manager))
            .collect::<egg_parser::errors::Result<Vec<String>>>()
            .map_err(egg_errors::Error::ParserError)?
            .join("\n - ")
    );
    Ok(())
}

fn show_ast(ast: &Ast, tokens: &[Token], source_manager: &SourceManager) -> egg_errors::Result<()> {
    println!(
        "===============\n= Syntax Tree =\n===============\n{}",
        ast.to_string(tokens, source_manager)
            .map_err(egg_errors::Error::ParserError)?
    );
    Ok(())
}
