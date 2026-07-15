"""
Question Factory OS
Validation Engine
"""

from validators.schema_validator import SchemaValidator
from validators.required_field_validator import RequiredFieldValidator
from validators.metadata_validator import MetadataValidator
from validators.identity_validator import IdentityValidator
from validators.difficulty_validator import DifficultyValidator


class ValidationEngine:

    def __init__(self):

        self.validators = [
            SchemaValidator(),
            RequiredFieldValidator(),
            MetadataValidator(),
            IdentityValidator(),
            DifficultyValidator(),
        ]

    def validate(self, question):

        report = {
            "passed": True,
            "total_validators": len(self.validators),
            "passed_validators": 0,
            "failed_validators": 0,
            "errors": [],
        }

        for validator in self.validators:

            result = validator.validate(question)

            if result["passed"]:

                report["passed_validators"] += 1

            else:

                report["passed"] = False

                report["failed_validators"] += 1

                report["errors"].extend(result["errors"])

        return report
