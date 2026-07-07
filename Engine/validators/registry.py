"""
Question Factory OS
Validator Registry

Central registry for all validators.
"""

from validators.schema_validator import SchemaValidator
from validators.required_field_validator import RequiredFieldValidator


VALIDATORS = [

    SchemaValidator(),

    RequiredFieldValidator()

]
