use std::{io, path::PathBuf};

use crate::parser;
use crate::source;
use crate::tokenizer;

extern crate yaml_rust;

pub type Result<T> = std::result::Result<T, EggError>;

#[derive(Debug)]
pub enum EggError {
    // Internal Tokenizer Errors
    InternalError(String),
    LineReadFailed(io::Error),
    SliceOutOfBounds(source::SourceSlice),
    LocationOutOfBounds(source::SourceLocation),
    OffsetOutOfBounds(usize),
    LineOutOfBounds(usize),
    StartOfTokenNotSet,
    EndOfTokenNotSet,
    TokenizerHeadNotSet,
    NotImplementedYet,

    // Invocation Errors
    FileNotFound(io::Error),
    FileReadError(io::Error),

    // Tokenizer Errors
    LexerUnclosedQuotation,
    LexerUnclosedEscapeSequence,
    LexerUnexpectedSymbol,

    // Parser Errors
    ParserTokenOutOfBounds,
    ParserUnexpectedToken(tokenizer::Token),
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
    TestSourceManagerFileIndexNotFound(usize),
    TestLineReadFailed(io::Error),
    TestYamlError(yaml_rust::ScanError),
    TestYamlLineError,
    TestCaseFailedWithError {
        test_file: PathBuf,
        test_number: usize,
        error: Box<EggError>,
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
