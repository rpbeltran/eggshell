use egg_ast::ast::*;
use egg_context::context_manager::ContextManager;
use egg_grammar::*;

use crate::errors::*;

pub fn label_type(root: usize, ast: &mut Ast, ctx_man: &ContextManager) -> Result<()> {
    let node = ast.get_node_mut(root).map_err(Error::AstError)?;
    node.annotations.type_id = match node.symbol {
        Symbol::Program => None,
        Symbol::ExecChain => Some(
            ctx_man
                .get_required_data_type_id(&String::from("Result"))
                .map_err(Error::ContextError)?,
        ),
        Symbol::Exec => Some(
            ctx_man
                .get_required_data_type_id(&String::from("Result"))
                .map_err(Error::ContextError)?,
        ),
        Symbol::PipeExec => Some(
            ctx_man
                .get_required_data_type_id(&String::from("Result"))
                .map_err(Error::ContextError)?,
        ),
        Symbol::RedirectExec => Some(
            ctx_man
                .get_required_data_type_id(&String::from("Result"))
                .map_err(Error::ContextError)?,
        ),
        Symbol::RedirectTarget => Some(
            ctx_man
                .get_required_data_type_id(&String::from("Result"))
                .map_err(Error::ContextError)?,
        ),
        Symbol::Lexeme => Some(
            ctx_man
                .get_required_data_type_id(&String::from("String"))
                .map_err(Error::ContextError)?,
        ),
        Symbol::_Placeholder => Err(Error::ReceivedPlaceholderSymbol)?,
    };
    Ok(())
}
