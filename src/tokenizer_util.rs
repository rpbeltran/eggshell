#![allow(dead_code)]

use crate::egg_error::*;
use crate::source::*;
use crate::tokenizer::*;
use crate::token::Token;

pub enum QuoteType {
    /// Quoted with double quotes.
    Single,
    /// Quoted with single quotes.
    Double,
    /// Quoted with backticks.
    Back,
}

pub struct Tokenizer {
    pub tokens: Vec<Token>,

    // State Machine
    pub head: Option<SourceLocation>,
    pub state: TokenizerState,
    pub token_start: Option<SourceLocation>,
    pub prev_location_non_whitespace: Option<SourceLocation>,

    // Current Charecter Info
    pub is_whitespace: bool,
    pub is_newline: bool,

    // Modifiers
    pub escaped: bool,
    pub quoted: Option<QuoteType>,
}



impl Tokenizer {
    pub fn new() -> Self {
        Tokenizer {
            tokens: Vec::new(),
            head: None,
            state: TokenizerState::Start,
            token_start: None,
            prev_location_non_whitespace: None,
            escaped: false,
            quoted: None,
            is_whitespace: false,
            is_newline: false,
        }
    }

    /// Reset state of tokenizer
    fn reset(&mut self) {
        self.tokens = Vec::new();
        self.state = TokenizerState::Start;
        self.head = None;
        self.token_start = None;
        self.prev_location_non_whitespace = None;
        self.escaped = false;
        self.quoted = None;
        self.is_newline = false;
    }

    /// Push a new token to list of tokens and clear last_transition.
    /// Does not include the current charecter in the token.
    pub fn transition(&mut self, lexeme: Lexeme, new_state: TokenizerState) -> Result<()> {
        self.emit(lexeme)?;
        self.state = new_state;
        self.token_start = None;
        Ok(())
    }

    /// Push a new token to list of tokens and clear last_transition.
    /// Includes the current charecter in the token.
    pub fn transition_inclusive(&mut self, lexeme: Lexeme, new_state: TokenizerState) -> Result<()> {
        self.emit_inclusive(lexeme)?;
        self.state = new_state;
        self.token_start = None;
        Ok(())
    }

    /// Push a new token to list of tokens
    /// ending at the last non_whitespace charecter before the current one.
    pub fn emit(&mut self, lexeme: Lexeme) -> Result<()> {
        if let Some(prev_loc) = self.prev_location_non_whitespace {
            self.tokens.push(Token {
                lexeme,
                location: SourceSlice {
                    file_id: prev_loc.file_id,
                    start: self.token_start.ok_or(EggError::StartOfTokenNotSet)?.offset,
                    end: prev_loc.offset,
                },
            });
            Ok(())
        } else {
            Err(EggError::EndOfTokenNotSet)
        }
    }

    /// Push a new token to list of tokens ending at and including the current char.
    pub fn emit_inclusive(&mut self, lexeme: Lexeme) -> Result<()> {
        let head = self.head.ok_or(EggError::EndOfTokenNotSet)?;
        self.tokens.push(Token {
            lexeme,
            location: SourceSlice {
                file_id: head.file_id,
                start: self.token_start.ok_or(EggError::StartOfTokenNotSet)?.offset,
                end: head.offset,
            },
        });
        Ok(())
    }

    /// Set new state and clear token_start.
    /// Does not emit a new token.
    pub fn transition_without_emiting(&mut self, new_state: TokenizerState) {
        self.state = new_state;
        self.token_start = None;
    }

    /// Set new state and set token_start to current token.
    /// Does not emit a new token.
    pub fn transition_without_emiting_inclusive(&mut self, new_state: TokenizerState) {
        self.state = new_state;
        self.token_start = self.head;
    }

    /// Returns true iff the current token is more than one charecter long.
    pub fn current_token_length(&self) -> Result<usize> {
        match self.token_start.as_ref() {
            Some(last_loc) => {
                let head = self.head.ok_or(EggError::TokenizerHeadNotSet)?;
                Ok(head.offset - last_loc.offset)
            }
            _ => Ok(0),
        }
    }

    /// Returns true iff a nonwhitespace charecter has been consumed since the last transition.
    pub fn current_token_not_empty(&self) -> bool {
        self.token_start.is_some()
    }

    /// Returns true iff c matches sym and the current charecter is not escaped.
    pub fn is_unescaped_sym(&self, c: &char, sym: char) -> bool {
        (*c == sym) && !self.escaped
    }

    /// Check if c is a whitespace or newline charecter and
    /// handle escape sequences and quotes.
    pub fn handle_whitespace_and_modifiers(&mut self, c: &char) {
        self.handle_modifiers(c);
        self.handle_whitespace(c);
    }

    /// Handle escape sequences and quotes.
    fn handle_modifiers(&mut self, c: &char) {
        if *c == '\\' {
            self.escaped = !self.escaped;
        } else if !self.escaped {
            match self.quoted {
                Some(QuoteType::Single) => {
                    if *c == '"' {
                        self.quoted = None;
                    }
                }
                Some(QuoteType::Double) => {
                    if *c == '\'' {
                        self.quoted = None;
                    }
                }
                Some(QuoteType::Back) => {
                    if *c == '`' {
                        self.quoted = None;
                    }
                }
                None => match *c {
                    '"' => {
                        self.quoted = Some(QuoteType::Single);
                    }
                    '\'' => {
                        self.quoted = Some(QuoteType::Double);
                    }
                    '`' => {
                        self.quoted = Some(QuoteType::Back);
                    }
                    _ => {}
                },
            };
        }
    }

    /// Set token start iff it is currently unset and the current char is not whitespace.
    pub fn handle_token_start(&mut self) {
        if self.token_start.is_none() && !self.is_whitespace {
            self.token_start = self.head;
        }
    }

    /// Check if c is an unquoted/escaped whitespace or newline charecter.
    /// Updates self.is_whitespace and self.is_newline.
    fn handle_whitespace(&mut self, c: &char) {
        self.is_whitespace = false;
        self.is_newline = false;
        if self.quoted.is_none() && !self.escaped {
            if *c == '\n' {
                self.is_whitespace = true;
                self.is_newline = true;
            } else if *c == ' ' || *c == '\t' {
                self.is_whitespace = true;
                self.is_newline = false;
            }
        }
    }

    /// Consume each charecter of each line, return the generated tokens.
    pub fn tokenize(&mut self, file: &SourceFile) -> Result<&Vec<Token>> {
        self.reset();
        for (offset, c) in file.contents.chars().enumerate() {
            let loc = SourceLocation {
                offset,
                file_id: file.file_id,
            };
            self.head = Some(loc);
            self.consume(&c)?;
        }
        Ok(&self.tokens)
    }
}

impl Default for Tokenizer {
    fn default() -> Self {
        Self::new()
    }
}
