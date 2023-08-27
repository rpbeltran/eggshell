use std::collections::{HashMap, HashSet};

use egg_context::context_manager::ContextManager;
use egg_context::data_types::*;

use crate::errors::Result;

pub fn add_base(ctx_man: &mut ContextManager) -> Result<()> {
    ctx_man.add_data_type(CompositeTypeDef {
        name: String::from("Base"),
        fields: HashMap::new(),
        extends: HashSet::new(),
    });
    Ok(())
}
