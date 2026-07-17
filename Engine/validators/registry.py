"""
Question Factory OS
Validator Registry

Central registry for all validators.
"""

from .identity_validator import IdentityValidator
from .metadata_validator import MetadataValidator
from .required_field_validator import RequiredFieldValidator
from .schema_validator import SchemaValidator

VALIDATORS = [
    SchemaValidator(),
    RequiredFieldValidator(),
    MetadataValidator(),
    IdentityValidator(),
]
