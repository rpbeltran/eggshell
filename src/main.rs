#![allow(dead_code)]

mod ast;
mod egg_error;
mod meta_parse;
mod parser;
mod source;
mod token;
mod tokenizer;
mod tokenizer_util;

use egg_error::*;
use std::path::PathBuf;

fn main() -> Result<()> {
    let mut source_manager = source::SourceManager::new();

    source_manager.load_file(PathBuf::from(
        "/Users/ryanbeltran/Development/eggshell/examples/split.egg",
    ))?;

    for source in source_manager.files.iter() {
        let tokenizer = tokenizer_util::Tokenizer::new();
        let tokens = tokenizer.tokenize(source)?;

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
            ast.to_string_standardized(&tokens, &source_manager)?
        );
    }

    Ok(())
}
