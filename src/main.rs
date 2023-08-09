mod ast;
mod egg_error;
mod lexer;
mod lexer_util;
mod meta_parse;
mod parser;
mod source;
mod token;

use egg_error::*;
use std::path::PathBuf;

fn main() -> Result<()> {
    let mut source_manager = source::SourceManager::new();

    source_manager.load_file(PathBuf::from(
        "/Users/ryanbeltran/Development/eggshell/examples/split.egg",
    ))?;

    for source in source_manager.files.iter() {
        let lexer = lexer_util::Lexer::new();
        let tokens = lexer.tokenize(source)?;

        println!(
            "==========\n= Tokens =\n==========\n---\n - {}\n",
            tokens
                .iter()
                .map(|t| t.to_string(&source_manager))
                .collect::<Result<Vec<String>>>()?
                .join("\n - ")
        );

        let mut parser = parser::Parser::new();
        let ast = parser.parse(&tokens)?;

        println!(
            "===============\n= Syntax Tree =\n===============\n{}",
            ast.to_string(&tokens, &source_manager)?
        );
    }

    Ok(())
}
