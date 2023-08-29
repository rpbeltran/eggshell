use egg_grammar::Symbol;

pub type Result<T> = std::result::Result<T, Error>;

#[derive(Debug)]
pub enum Error {
    ReceivedPlaceholderSymbol,
    AstNodeMissingExpectedChildren(Symbol),
    AstNodeHasUnexpectedChild {
        node_type: Symbol,
        child_type: Symbol,
        child_position: usize,
    },

    // Pass Through Errors
    AstError(egg_ast::errors::Error),
    ContextError(egg_context::errors::Error),
}
