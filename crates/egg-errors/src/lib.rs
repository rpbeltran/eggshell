pub type Result<T> = std::result::Result<T, Error>;

#[derive(Debug)]
pub enum Error {
    AstError(egg_ast::errors::Error),
    ParserError(egg_parser::errors::Error),
    SourceError(egg_source::errors::Error),
    SemaError(egg_sema::errors::Error),
}
