#![allow(dead_code)]

use std::path::PathBuf;

use crate::errors::*;
use crate::location::Span;
use crate::source_file::SourceFile;

pub struct SourceManager {
    pub files: Vec<SourceFile>,
}

impl Default for SourceManager {
    fn default() -> Self {
        Self::new()
    }
}

impl SourceManager {
    pub fn new() -> Self {
        SourceManager { files: Vec::new() }
    }

    /// Attept to retrieve the SourceFile with the given file_id.
    pub fn get_file(&self, id: usize) -> Result<&SourceFile> {
        self.files
            .get(id)
            .ok_or(Error::SourceManagerFileIndexNotFound(id))
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
