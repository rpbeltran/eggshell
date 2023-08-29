mod base;
pub mod errors;
mod result;

use egg_context::context_manager::ContextManager;

use errors::Result;

pub fn add_standard_composite_types(ctx_man: &mut ContextManager) -> Result<()> {
    base::add_base(ctx_man)?;
    result::add_result(ctx_man)?;
    Ok(())
}
