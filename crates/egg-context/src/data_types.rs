use std::collections::{HashMap, HashSet};

use crate::context_manager::*;
use crate::errors::*;

pub struct DataType {
    pub name: String,
    pub fields: HashMap<String, TypeID>,
    pub extends: HashSet<TypeID>,
}

impl DataType {
    pub fn new(
        ctx_man: &ContextManager,
        name: String,
        fields: Vec<(String, TypeID)>,
        extends: HashSet<TypeID>,
    ) -> Result<Self> {
        Ok(Self {
            fields: Self::compute_fields(ctx_man, &name, fields, &extends)?,
            extends: Self::compute_parents(ctx_man, extends)?,
            name,
        })
    }

    fn compute_fields(
        ctx_man: &ContextManager,
        name: &str,
        fields: Vec<(String, TypeID)>,
        extends: &HashSet<TypeID>,
    ) -> Result<HashMap<String, TypeID>> {
        let mut computed_fields: HashMap<String, TypeID> = fields.into_iter().collect();
        for base in extends {
            let base_dt = ctx_man.get_data_type(*base)?;
            // Add parent fields to computed fields
            for (field, field_type) in base_dt.fields.iter() {
                if let Some(old_value) = computed_fields.insert(field.clone(), *field_type) {
                    if old_value != *field_type {
                        return Err(Error::DatatypeConflictingFieldDefinitions {
                            data_type: name.to_string(),
                            field_type_a: ctx_man.get_data_type(old_value)?.name.to_string(),
                            field_type_b: ctx_man.get_data_type(*field_type)?.name.to_string(),
                        });
                    }
                }
            }
            // validate that there are no naming conflicts from two parents with different definitions of the same field.
        }
        Ok(computed_fields)
    }

    fn compute_parents(
        ctx_man: &ContextManager,
        mut extends: HashSet<TypeID>,
    ) -> Result<HashSet<TypeID>> {
        for ancestor in extends.clone() {
            extends.extend(ctx_man.get_data_type(ancestor)?.extends.iter());
        }
        Ok(extends)
    }
}
