use std::collections::HashMap;

use crate::context_manager::{ContextID, TypeID};

pub struct Context {
    pub(crate) types: HashMap<String, TypeID>,
    pub(crate) parent: Option<ContextID>,
}
