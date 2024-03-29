use crate::context_manager::{ContextID, TypeID};

pub type Result<T> = std::result::Result<T, Error>;

#[derive(Debug)]
pub enum Error {
    ContextManagerInvalidContextID(ContextID),
    ContextManagerInvalidDataTypeID(TypeID),
    ContextManagerMissingRequiredDataTypeID(String),
    DataTypeCannotExtendPrimitiveType {
        data_type: String,
        extends: String,
    },
    DatatypeConflictingFieldDefinitions {
        data_type: String,
        field_type_a: String,
        field_type_b: String,
    },
}
