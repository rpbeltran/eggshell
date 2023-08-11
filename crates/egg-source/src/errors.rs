#![allow(dead_code)]

use std::io;

use crate::location::*;

pub type Result<T> = std::result::Result<T, Error>;

#[derive(Debug)]
pub enum Error {
    // Internal Source Managment Errors
    LineReadFailed(io::Error),
    SpanOutOfBounds(Span),
    LocationOutOfBounds(SourceLocation),
    OffsetOutOfBounds(usize),
    SourceManagerFileIndexNotFound(usize),

    // Invocation Errors
    FileNotFound(io::Error),
    FileReadError(io::Error),
}
