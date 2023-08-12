#![allow(dead_code)]

use std::{io, path::PathBuf};

use egg_grammar::Symbol;
use egg_source::location::SourceLocation;
use egg_source::token::Token;

pub type Result<T> = std::result::Result<T, Error>;

#[derive(Debug)]
pub enum Error {
    // Internal Errors
    InternalError(String),
    NotImplementedYet,

    // Internal Source Managment Errors
    SourceError(egg_source::errors::Error),

    // AST Errors
    AstError(egg_ast::errors::Error),

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
    ParserTriedToBuildSymbolWithNoRule(Symbol),
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
