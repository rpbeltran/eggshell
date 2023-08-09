use clap::Parser;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
pub struct Args {
    /// Display the generated AST
    #[arg(long)]
    pub show_ast: bool,

    /// Display the lexer output
    #[arg(long)]
    pub show_lexer: bool,
}
