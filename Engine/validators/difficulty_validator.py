"""
Question Factory OS
Difficulty Validator
"""

from core.rule_manager import RuleManager


class DifficultyValidator:

    def __init__(self):

        self.rules = RuleManager()

    def validate(self, question):

        errors = []

        set_no = question.get("set_no")

        if not set_no:

            errors.append(
                "set_no is missing"
            )

            return {

                "validator": "DifficultyValidator",

                "passed": False,

                "errors": errors

            }

        expected = self.rules.difficulty(
            set_no
        )

        actual = question.get(
            "difficulty"
        )

        if actual != expected:

            errors.append(
                f"Difficulty mismatch: expected '{expected}', got '{actual}'"
            )

        return {

            "validator": "DifficultyValidator",

            "passed": len(errors) == 0,

            "errors": errors

        }