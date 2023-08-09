#![allow(dead_code)]

use regex::Regex;

use crate::egg_error::*;
use crate::lexer::*;
use crate::source::*;
use crate::token::Token;

pub enum QuoteType {
    /// Quoted with double quotes.
    Single,
    /// Quoted with single quotes.
    Double,
    /// Quoted with backticks.
    Back,
}

pub struct Lexer {
    pub patterns: Vec<(Lexeme, Regex)>,
}

struct LexerState<'s> {
    input_suffix: std::str::Chars<'s>,
}

impl Lexer {
    pub fn tokenize(&self, source_file: &SourceFile) -> Result<Vec<Token>> {
        let mut tokens: Vec<Token> = Vec::new();
        let mut next_token_start = 0;
        while next_token_start < source_file.char_count {
            if let Some(pos) = self.get_next_nonwhitespace(source_file, next_token_start) {
                next_token_start = pos;
            } else {
                break;
            }
            let next_token = self.get_next_token(source_file, next_token_start)?;
            next_token_start = next_token.location.end + 1;
            tokens.push(next_token);
        }
        Ok(tokens)
    }

    fn get_next_nonwhitespace(
        &self,
        source_file: &SourceFile,
        search_from: usize,
    ) -> Option<usize> {
        for (i, c) in source_file.contents.char_indices().skip(search_from) {
            if !(c == ' ' || c == '\t') {
                return Some(i);
            }
        }
        None
    }

    fn get_next_token(&self, source_file: &SourceFile, search_from: usize) -> Result<Token> {
        let mut best_match: Option<(&Lexeme, usize)> = None;

        for (lexeme, pattern) in self.patterns.iter() {
            if let Some(m) = pattern.find_at(&source_file.contents, search_from) {
                if m.start() == search_from {
                    let end = m.end();
                    match best_match {
                        Some((_, prev_end)) => {
                            if end > prev_end {
                                best_match = Some((lexeme, end));
                            }
                        }
                        _ => {
                            best_match = Some((lexeme, end));
                        }
                    }
                }
            }
        }

        match best_match {
            Some((lexeme, end_pos)) => Ok(Token {
                lexeme: *lexeme,
                location: SourceSlice {
                    file_id: source_file.file_id,
                    start: search_from,
                    end: end_pos - 1,
                },
            }),
            _ => Err(EggError::LexerCouldNotCreateToken(SourceLocation {
                file_id: source_file.file_id,
                offset: search_from,
            })),
        }
    }
}

impl Default for Lexer {
    fn default() -> Self {
        Self::new()
    }
}

pub fn rgx_must(pattern: &str) -> Regex {
    Regex::new(pattern).unwrap()
}
