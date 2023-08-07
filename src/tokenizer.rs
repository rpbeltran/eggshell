#![allow(dead_code)]

use crate::egg_error::*;
use crate::tokenizer_util::*;

#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum Lexeme {
    // Commands
    Command,

    // Literals
    StringLiteral,

    // Redirection
    Pipe,           // |
    Redirect,       // >
    RedirectAppend, // >>
}

mod symbols {
    pub const PIPE: char = '|';
    pub const FILE_REDIRECT: char = '>';
}

pub enum TokenizerState {
    Start,
    Command,
    ArgString,
    FileRedirect,
    End,
}

impl Tokenizer {
    /// Consume a charecter and update state of the tokenizer.
    pub fn consume(&mut self, c: &char) -> Result<()> {
        self.handle_whitespace_and_modifiers(c);
        self.handle_token_start();

        match self.state {
            TokenizerState::Start => {
                if !self.is_whitespace {
                    self.state = TokenizerState::Command;
                }
            }
            TokenizerState::Command => {
                if self.is_whitespace && self.current_token_not_empty() {
                    self.transition(
                        Lexeme::Command,
                        if self.is_newline {
                            TokenizerState::Command
                        } else {
                            TokenizerState::ArgString
                        },
                    )?;
                }
            }
            TokenizerState::ArgString => {
                if self.is_newline {
                    if self.current_token_not_empty() {
                        self.transition(Lexeme::StringLiteral, TokenizerState::Command)?;
                    } else {
                        self.transition_without_emiting(TokenizerState::Command)
                    }
                } else if self.is_unescaped_sym(c, symbols::PIPE) {
                    if self.current_token_length()? > 1 {
                        self.transition(Lexeme::StringLiteral, TokenizerState::Command)?;
                        self.token_start = self.head;
                    }
                    self.transition_inclusive(Lexeme::Pipe, TokenizerState::Command)?;
                } else if self.is_unescaped_sym(c, symbols::FILE_REDIRECT) {
                    if self.current_token_length()? > 1 {
                        self.emit(Lexeme::StringLiteral)?;
                    }
                    self.transition_without_emiting_inclusive(TokenizerState::FileRedirect);
                }
            }
            TokenizerState::FileRedirect => {
                if self.is_unescaped_sym(c, symbols::FILE_REDIRECT) {
                    self.transition_inclusive(Lexeme::RedirectAppend, TokenizerState::ArgString)?;
                } else {
                    self.transition(Lexeme::Redirect, TokenizerState::ArgString)?;
                }
            }
            TokenizerState::End => {
                if self.escaped {
                    return Err(EggError::LexerUnclosedEscapeSequence);
                } else if self.quoted.is_some() {
                    return Err(EggError::LexerUnclosedQuotation);
                } else if self.is_newline {
                    self.transition_without_emiting(TokenizerState::Start);
                } else if !self.is_whitespace {
                    return Err(EggError::LexerUnexpectedSymbol);
                }
            }
        }
        if !self.is_whitespace {
            self.prev_location_non_whitespace = self.head;
        }
        Ok(())
    }
}