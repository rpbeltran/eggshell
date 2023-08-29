use std::collections::{HashMap, HashSet};

use egg_context::context_manager::ContextManager;
use egg_context::data_types::*;

use crate::errors::{Error, Result};

pub(crate) fn add_result(ctx_man: &mut ContextManager) -> Result<()> {
    ctx_man.add_data_type(CompositeTypeDef {
        name: String::from("Result"),
        fields: [
            (
                String::from("out"),
                ctx_man
                    .get_required_data_type_id(&DataType::String.get_name())
                    .map_err(Error::EggContextError)?,
            ),
            (
                String::from("err"),
                ctx_man
                    .get_required_data_type_id(&DataType::String.get_name())
                    .map_err(Error::EggContextError)?,
            ),
            (
                String::from("both"),
                ctx_man
                    .get_required_data_type_id(&DataType::String.get_name())
                    .map_err(Error::EggContextError)?,
            ),
        ]
        .into_iter()
        .collect(),
        extends: HashSet::new(),
    });
    Ok(())
}
