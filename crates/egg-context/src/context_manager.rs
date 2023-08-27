use std::collections::HashMap;

use crate::context::Context;
use crate::data_types::{CompositeTypeDef, DataType};
use crate::errors::*;

pub type ContextID = usize;
pub type TypeID = usize;

pub struct ContextManager {
    contexts: Vec<Context>,
    data_types: Vec<DataType>,
    active_context: ContextID,
}

impl ContextManager {
    pub fn new() -> Self {
        let default_types = [DataType::String];
        Self {
            contexts: Vec::from([Context {
                types: (0..default_types.len())
                    .map(|i| (default_types.get(i).unwrap().get_name(), i))
                    .collect::<HashMap<String, usize>>(),
                parent: None,
            }]),
            data_types: Vec::from(default_types),
            active_context: 0,
        }
    }

    fn get_context(&mut self) -> &mut Context {
        self.contexts.get_mut(self.active_context).unwrap()
    }

    pub fn add_data_type(&mut self, new_composite: CompositeTypeDef) {
        let name = new_composite.name.clone();
        let position = self.data_types.len();
        self.data_types.push(DataType::CompositeType(new_composite));
        self.get_context().types.insert(name, position);
    }

    pub fn get_data_type(&self, data_type: TypeID) -> Result<&DataType> {
        self.data_types
            .get(data_type)
            .ok_or(Error::ContextManagerInvalidDataTypeID(data_type))
    }

    pub fn get_data_type_id(&self, name: &String) -> Result<Option<TypeID>> {
        let mut current_context_id = Some(self.active_context);
        while current_context_id.is_some() {
            let context = self
                .contexts
                .get(current_context_id.unwrap())
                .ok_or_else(|| {
                    Error::ContextManagerInvalidContextID(current_context_id.unwrap())
                })?;
            if let Some(type_id) = context.types.get(name) {
                return Ok(Some(*type_id));
            }
            current_context_id = context.parent;
        }
        Ok(None)
    }

    pub fn get_required_data_type_id(&self, name: &String) -> Result<TypeID> {
        self.get_data_type_id(name)?
            .ok_or_else(|| Error::ContextManagerMissingRequiredDataTypeID(name.clone()))
    }

    pub fn push_context(&mut self) {
        self.contexts.push(Context {
            types: HashMap::new(),
            parent: Some(self.active_context),
        });
        self.active_context = self.contexts.len() - 1;
    }
}

impl Default for ContextManager {
    fn default() -> Self {
        Self::new()
    }
}
