pub type Result<T> = std::result::Result<T, Error>;

#[derive(Debug)]
pub enum Error {
    // Pass Through Errors
    EggContextError(egg_context::errors::Error),
}
