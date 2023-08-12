#![allow(dead_code)]

use std::io;

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

    // Parser Errors
    ParserTokenOutOfBounds,
    ParserCouldNotParseProgram,
    ParserTreeHasNoRootNode,
    ParserTreeNodeOutOfBounds,
    ParserLexemeNodeMissingToken,
    ParserSerializedBeforeBuilding,
    ParserExpectedPlaceholder,
    ParserReceivedPlaceholder,
    ParserHeadPastLastToken,
}
