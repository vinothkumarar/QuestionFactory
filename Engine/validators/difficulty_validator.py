"""
Question Factory OS
Difficulty Validator

Milestone : M12
Sprint    : S2
Release   : R1
"""

from core.rule_manager import RuleManager


class DifficultyValidator:

    def __init__(self):

        self.rules = RuleManager()

        self.valid_exam_levels = {"JEE Main", "JEE Advanced", "JEE Main + Advanced"}

        self.valid_exam_relevance = {"Low", "Medium", "High", "Very High"}

        self.valid_source_types = {"Original", "AI Generated", "PYQ Inspired"}

    def validate(self, question):

        errors = []

        #
        # Difficulty Validation
        #

        set_no = question.get("set_no")

        if not set_no:

            errors.append("set_no is missing")

        else:

            expected = self.rules.difficulty(set_no)

            actual = question.get("difficulty")

            if actual != expected:

                errors.append(
                    f"Difficulty mismatch: "
                    f"expected '{expected}', "
                    f"got '{actual}'"
                )

        #
        # Exam Level
        #

        exam_level = question.get("exam_level")

        if exam_level not in self.valid_exam_levels:

            errors.append(f"Invalid exam_level: " f"{exam_level}")

        #
        # Exam Relevance
        #

        exam_relevance = question.get("exam_relevance")

        if exam_relevance not in self.valid_exam_relevance:

            errors.append(f"Invalid exam_relevance: " f"{exam_relevance}")

        #
        # Source Type
        #

        source_type = question.get("source_type")

        if source_type not in self.valid_source_types:

            errors.append(f"Invalid source_type: " f"{source_type}")

        return {
            "validator": "DifficultyValidator",
            "passed": len(errors) == 0,
            "errors": errors,
        }
