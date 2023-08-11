#![allow(dead_code)]

use std::{io, path::PathBuf};

use egg_source::location::SourceLocation;

use crate::parser;
use crate::token::Token;

pub type Result<T> = std::result::Result<T, Error>;

#[derive(Debug)]
pub enum Error {
    // Internal Errors
    InternalError(String),
    NotImplementedYet,

    // Internal Source Managment Errors
    SourceError(egg_source::errors::Error),

    // Invocation Errors
    FileNotFound(io::Error),
    FileReadError(io::Error),

    // Lexer Errors
    LexerCouldNotCreateToken(SourceLocation),

    // Parser Errors
    ParserTokenOutOfBounds,
    ParserUnexpectedToken(Token),
    ParserCouldNotParseProgram,
    ParserTreeHasNoRootNode,
    ParserTreeNodeOutOfBounds,
    ParserLexemeNodeMissingToken,
    ParserSerializedBeforeBuilding,
    ParserExpectedPlaceholder,
    ParserReceivedPlaceholder,
    ParserTriedToBuildSymbolWithNoRule(parser::Symbol),
    ParserHeadPastLastToken,

    // Testing Errors
    TestFileNotFound(io::Error),
    TestLineReadFailed(io::Error),
    TestYamlError {
        file: PathBuf,
        line: usize,
    },
    TestYamlLineError,
    TestCaseFailedWithError {
        test_file: PathBuf,
        test_number: usize,
        error: Box<Error>,
    },
    TestCaseFailedAssertion {
        test_file: PathBuf,
        test_number: usize,
        error: String,
    },
    InternalTestCaseFailedAssertion {
        category: Box<str>,
        test_number: usize,
        error: Box<str>,
    },
}
