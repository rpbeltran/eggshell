pub mod errors;
mod memory;

use egg_ast::ast::Ast;

/// Annotate the AST with memory information.
pub fn annotate_ast(ast: &mut Ast) -> errors::Result<()> {
    let postorder = ast.postorder().collect::<Vec<usize>>();

    // Pass 1: Memory mapping.
    for i in postorder {
        memory::label_mem_ids(i, ast)?;
        memory::label_dont_discard(i, ast)?;
    }

    Ok(())
}
