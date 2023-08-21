use crate::context::Context;
use crate::data_types::DataType;
use crate::errors::*;

pub type ContextID = usize;
pub type TypeID = usize;

pub struct ContextManager {
    contexts: Vec<Context>,
    data_types: Vec<DataType>,
}

impl ContextManager {
    pub fn get_data_type(&self, data_type: TypeID) -> Result<&DataType> {
        return self
            .data_types
            .get(data_type)
            .ok_or(Error::ContextManagerInvalidDataTypeID(data_type));
    }

    pub fn get_data_type_id(&self, context_id: ContextID, name: &String) -> Result<Option<TypeID>> {
        let mut current_context_id = Some(context_id);
        while current_context_id.is_some() {
            let context = self
                .contexts
                .get(context_id)
                .ok_or(Error::ContextManagerInvalidContextID(context_id))?;
            if let Some(type_id) = context.types.get(name) {
                return Ok(Some(*type_id));
            }
            current_context_id = context.parent
        }
        Ok(None)
    }
}
