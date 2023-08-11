use crate::errors::*;
use crate::lexer::Lexeme;
use crate::source;

#[derive(Clone, Debug)]
pub struct Token {
    pub lexeme: Lexeme,
    pub location: source::SourceSlice,
}

impl Token {
    pub fn to_string(&self, source_manager: &source::SourceManager) -> Result<String> {
        Ok(format!(
            "{:?}: {:?}",
            self.lexeme,
            self.get_contents(source_manager)?
        ))
    }

    pub fn get_contents(&self, source_manager: &source::SourceManager) -> Result<String> {
        source_manager.get_slice(&self.location)
    }
}
