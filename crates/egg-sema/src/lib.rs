pub mod errors;
mod memory;
mod types;

use egg_ast::ast::Ast;
use egg_context::context_manager::ContextManager;

/// Annotate the AST with memory information.
pub fn annotate_ast(ast: &mut Ast, ctx_man: &ContextManager) -> errors::Result<()> {
    let postorder = ast.postorder().collect::<Vec<usize>>();

    // Pass 1: Memory mapping and type annotations.
    for i in postorder {
        memory::label_mem_id(i, ast)?;
        memory::label_dont_discard(i, ast)?;
        types::label_type(i, ast, ctx_man)?;
    }

    Ok(())
}
