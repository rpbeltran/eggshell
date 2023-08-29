mod cli;

use std::path::PathBuf;

use egg_ast::ast::Ast;
use egg_context::context_manager::ContextManager;
use egg_errors::*;
use egg_parser::lexer_util::Lexer;
use egg_source::source_manager::SourceManager;
use egg_source::token::Token;

use clap::Parser;

fn main() -> Result<()> {
    let args = cli::Args::parse();

    let mut source_manager = SourceManager::new();

    source_manager
        .load_file(PathBuf::from(
            "/Users/ryanbeltran/Development/eggshell/examples/split.egg",
        ))
        .map_err(Error::SourceError)?;

    for source in source_manager.files.iter() {
        let lexer = Lexer::new();
        let tokens = lexer.tokenize(source).map_err(Error::ParserError)?;

        if args.show_lexer {
            show_tokens(&tokens, &source_manager)?;
        }

        let mut parser = egg_parser::parser::Parser::new();
        let mut ast = parser.parse(&tokens).map_err(Error::ParserError)?;

        let mut ctx_man = ContextManager::new();
        egg_types::add_standard_composite_types(&mut ctx_man).map_err(Error::TypesError)?;

        egg_sema::annotate_ast(&mut ast, &ctx_man).map_err(Error::SemaError)?;

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
            .collect::<egg_source::errors::Result<Vec<String>>>()
            .map_err(egg_errors::Error::SourceError)?
            .join("\n - ")
    );
    Ok(())
}

fn show_ast(ast: &Ast, tokens: &[Token], source_manager: &SourceManager) -> egg_errors::Result<()> {
    println!(
        "===============\n= Syntax Tree =\n===============\n{}",
        ast.to_string(tokens, source_manager)
            .map_err(egg_errors::Error::AstError)?
    );
    Ok(())
}
