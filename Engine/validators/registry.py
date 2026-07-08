"""
Question Factory OS
Validator Registry

Central registry for all validators.
"""

from validators.schema_validator import SchemaValidator
from validators.required_field_validator import RequiredFieldValidator
from validators.metadata_validator import MetadataValidator
from validators.identity_validator import IdentityValidator

VALIDATORS = [
    SchemaValidator(),
    RequiredFieldValidator(),
    MetadataValidator(),
    IdentityValidator()
]

