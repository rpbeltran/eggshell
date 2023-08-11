#![allow(dead_code)]

use std::fs::File;
use std::io::prelude::Read;
use std::path::PathBuf;

use crate::errors::*;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SourceLocation {
    pub file_id: usize,
    pub offset: usize,
}

/// Denotes a slice of charecters from a source file.
/// Both start and end are inclusive.
#[derive(Debug, Clone)]
pub struct Span {
    pub file_id: usize,
    /// Offset of first char in span (inclusive).
    pub start: usize,
    /// Offset of last char in span (inclusive).
    pub end: usize,
}

#[derive(Debug)]
pub struct SourceFile {
    pub contents: String,
    pub file_id: usize,
    pub line_indexes: Vec<usize>,
    pub char_count: usize,
}

pub struct SourceManager {
    pub files: Vec<SourceFile>,
    pub file_paths: Vec<PathBuf>,
}

impl SourceFile {
    fn from(file_id: usize, filename: &PathBuf) -> Result<Self> {
        let contents = Self::read_file(filename)?;

        let mut line_indexes: Vec<usize> = contents.match_indices('\n').map(|(i, _)| i).collect();
        line_indexes.insert(0, 0);

        let char_count = contents.len();

        Ok(SourceFile {
            contents,
            file_id,
            line_indexes,
            char_count,
        })
    }

    /// Attempts to read file into a \n terminated string.
    fn read_file(file_path: &PathBuf) -> Result<String> {
        let mut buf: String = String::new();
        File::open(file_path)
            .map_err(Error::FileNotFound)?
            .read_to_string(&mut buf)
            .map_err(Error::LineReadFailed)?;
        if !buf.ends_with('\n') {
            buf += "\n";
        }
        Ok(buf)
    }

    pub fn get_line_and_col(&self, offset: usize) -> Result<(usize, usize)> {
        if offset < self.char_count {
            let line: usize = self
                .line_indexes
                .binary_search(&offset)
                .unwrap_or_else(|line| line - 1);
            let col = offset - self.line_indexes[line];
            Ok((line, col))
        } else {
            Err(Error::OffsetOutOfBounds(offset))
        }
    }

    /// Attempts to fetch the text corresponding to a Span within this file.
    pub fn get_text(&self, span: &Span) -> Result<String> {
        if span.end < span.start {
            Err(Error::SpanOutOfBounds(span.clone()))
        } else {
            Ok(self
                .contents
                .chars()
                .skip(span.start)
                .take(span.end - span.start + 1)
                .collect())
        }
    }
}

impl Default for SourceManager {
    fn default() -> Self {
        Self::new()
    }
}

impl SourceManager {
    pub fn new() -> Self {
        SourceManager {
            files: Vec::new(),
            file_paths: Vec::new(),
        }
    }

    /// Attept to retrieve the SourceFile with the given file_id.
    pub fn get_file(&self, id: usize) -> Result<&SourceFile> {
        self.files
            .get(id)
            .ok_or(Error::TestSourceManagerFileIndexNotFound(id))
    }

    /// Load a new file into the file manager.
    pub fn load_file(&mut self, file_path: PathBuf) -> Result<()> {
        let source_file = SourceFile::from(self.files.len(), &file_path)?;
        self.files.push(source_file);
        Ok(())
    }

    /// Attempts to fetch the text corresponding to the Span.
    pub fn get_text(&self, span: &Span) -> Result<String> {
        self.files
            .get(span.file_id)
            .ok_or_else(|| Error::SpanOutOfBounds(span.clone()))?
            .get_text(span)
    }
}
