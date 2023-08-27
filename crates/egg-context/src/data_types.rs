use std::collections::{HashMap, HashSet};

use crate::context_manager::*;
use crate::errors::*;

#[derive(Debug)]
pub struct CompositeTypeDef {
    pub name: String,
    pub fields: HashMap<String, TypeID>,
    pub extends: HashSet<TypeID>,
}

#[derive(Debug)]
pub enum DataType {
    String,
    CompositeType(CompositeTypeDef),
}

impl DataType {
    pub fn get_name(&self) -> String {
        match self {
            DataType::CompositeType(ctd) => ctd.name.clone(),
            _ => format!("{:?}", self),
        }
    }
}

#[test]
fn test_get_name_primitive() {
    assert_eq!(DataType::String.get_name(), "String")
}

#[test]
fn test_get_name_composite() {
    let dt = DataType::CompositeType(CompositeTypeDef {
        name: "foo".to_string(),
        fields: HashMap::new(),
        extends: HashSet::new(),
    });
    assert_eq!(dt.get_name(), "foo")
}

impl CompositeTypeDef {
    pub fn new_composite(
        ctx_man: &ContextManager,
        name: String,
        fields: Vec<(String, TypeID)>,
        extends: HashSet<TypeID>,
    ) -> Result<Self> {
        Ok(Self {
            fields: Self::compute_fields(ctx_man, &name, fields, &extends)?,
            extends: Self::compute_parents(ctx_man, &name, extends)?,
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
            // Add parent fields to computed fields
            if let DataType::CompositeType(ctd) = ctx_man.get_data_type(*base)? {
                for (field, field_type) in ctd.fields.iter() {
                    if let Some(old_value) = computed_fields.insert(field.clone(), *field_type) {
                        if old_value != *field_type {
                            return Err(Error::DatatypeConflictingFieldDefinitions {
                                data_type: name.to_string(),
                                field_type_a: ctx_man.get_data_type(old_value)?.get_name(),
                                field_type_b: ctx_man.get_data_type(*field_type)?.get_name(),
                            });
                        }
                    }
                }
            } else {
                return Err(Error::DataTypeCannotExtendPrimitiveType {
                    data_type: name.to_string(),
                    extends: ctx_man.get_data_type(*base)?.get_name(),
                });
            }
        }
        Ok(computed_fields)
    }

    fn compute_parents(
        ctx_man: &ContextManager,
        name: &str,
        mut extends: HashSet<TypeID>,
    ) -> Result<HashSet<TypeID>> {
        for ancestor in extends.clone() {
            if let DataType::CompositeType(ctd) = ctx_man.get_data_type(ancestor)? {
                extends.extend(ctd.extends.iter());
            } else {
                return Err(Error::DataTypeCannotExtendPrimitiveType {
                    data_type: name.to_string(),
                    extends: ctx_man.get_data_type(ancestor)?.get_name(),
                });
            }
        }
        Ok(extends)
    }
}
