mod base;
pub mod errors;

use egg_context::context_manager::ContextManager;

use errors::Result;

pub fn add_standard_composite_types(ctx_man: &mut ContextManager) -> Result<()> {
    base::add_base(ctx_man)?;
    Ok(())
}
