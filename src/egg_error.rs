pub type Result<T> = std::result::Result<T, EggError>;

#[derive(Debug)]
pub enum EggError {
    ParserError(egg_parser::errors::Error),
}
