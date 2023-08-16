#[derive(Debug, Default, PartialEq, Eq)]
pub struct Annotations {
    /// Unique id for each unique value stored in memory
    pub mem_id: Option<usize>,
    /// Signifies that this AST Node is never read
    pub discard: bool,
}

impl Annotations {
    pub fn new() -> Self {
        Self {
            mem_id: None,
            discard: true,
        }
    }
}
