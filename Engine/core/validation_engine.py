"""
Question Factory OS
Validation Engine

Runs all validators on a Question object.
"""

from validators.registry import VALIDATORS


class ValidationEngine:

    def __init__(self):

        self.validators = VALIDATORS

    def validate(self, question: dict):

        report = {
            "passed": True,
            "total_validators": len(self.validators),
            "passed_validators": 0,
            "failed_validators": 0,
            "errors": []
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
