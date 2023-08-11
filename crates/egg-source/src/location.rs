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
