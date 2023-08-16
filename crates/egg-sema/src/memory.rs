use egg_ast::ast::*;
use egg_grammar::*;

use crate::errors::*;

/// Mark the memory id of all node values.
pub fn label_mem_ids(root: usize, ast: &mut Ast) -> Result<()> {
    ast.get_node_mut(root)
        .map_err(Error::AstError)?
        .annotations
        .mem_id = Some(root);
    Ok(())
}

/// Mark which nodes have values that get read.
pub fn label_dont_discard(root: usize, ast: &mut Ast) -> Result<()> {
    fn mark_all_children(root: usize, ast: &mut Ast) -> Result<()> {
        for c in ast
            .get_node(root)
            .map_err(Error::AstError)?
            .children
            .clone()
        {
            ast.get_node_mut(c)
                .map_err(Error::AstError)?
                .annotations
                .discard = false;
        }
        Ok(())
    }

    fn mark_child(root: usize, ast: &mut Ast, child_pos: usize) -> Result<()> {
        let node = ast.get_node(root).map_err(Error::AstError)?;
        let pos = node
            .children
            .get(child_pos)
            .ok_or(Error::AstNodeMissingExpectedChildren(node.symbol))?;
        ast.get_node_mut(*pos)
            .map_err(Error::AstError)?
            .annotations
            .discard = false;
        Ok(())
    }

    match ast.get_node(root).map_err(Error::AstError)?.symbol {
        Symbol::Program => {}
        Symbol::ExecChain => mark_all_children(root, ast)?,
        Symbol::Exec => mark_all_children(root, ast)?,
        Symbol::PipeExec => mark_child(root, ast, 1)?,
        Symbol::RedirectExec => mark_child(root, ast, 1)?,
        Symbol::RedirectTarget => mark_all_children(root, ast)?,
        Symbol::Lexeme => {}
        Symbol::_Placeholder => Err(Error::ReceivedPlaceholderSymbol)?,
    }

    Ok(())
}
