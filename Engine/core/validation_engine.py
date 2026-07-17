"""
Question Factory OS
Validation Engine
"""

from typing import Any

from Engine.validators.difficulty_validator import DifficultyValidator
from Engine.validators.identity_validator import IdentityValidator
from Engine.validators.metadata_validator import MetadataValidator
from Engine.validators.required_field_validator import RequiredFieldValidator
from Engine.validators.schema_validator import SchemaValidator


class ValidationEngine:
    def __init__(self) -> None:
        self.validators: list[Any] = [
            SchemaValidator(),
            RequiredFieldValidator(),
            MetadataValidator(),
            IdentityValidator(),
            DifficultyValidator(),
        ]

    def validate(self, question: Any) -> dict[str, Any]:
        report: dict[str, Any] = {
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