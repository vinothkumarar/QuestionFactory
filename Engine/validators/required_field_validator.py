"""
Question Factory OS
Required Field Validator

Ensures required fields contain values.
"""

from core.schema import QUESTION_REQUIRED_FIELDS


class RequiredFieldValidator:

    def validate(self, question: dict):

        errors = []

        for field in QUESTION_REQUIRED_FIELDS:

            value = question.get(field)

            if value is None:
                errors.append(f"{field} is required")

            elif isinstance(value, str) and value.strip() == "":
                errors.append(f"{field} is required")

        return {
    "validator": "RequiredFieldValidator",
    "passed": len(errors) == 0,
    "errors": errors
}
