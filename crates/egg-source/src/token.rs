use crate::errors::*;
use crate::location;
use crate::source_manager::SourceManager;
use egg_grammar::Lexeme;

#[derive(Clone, Debug)]
pub struct Token {
    pub lexeme: Lexeme,
    pub location: location::Span,
}

impl Token {
    pub fn to_string(&self, source_manager: &SourceManager) -> Result<String> {
        Ok(format!(
            "{:?}: {:?}",
            self.lexeme,
            self.get_contents(source_manager)?
        ))
    }

    pub fn get_contents(&self, source_manager: &SourceManager) -> Result<String> {
        source_manager.get_text(&self.location)
    }
}
