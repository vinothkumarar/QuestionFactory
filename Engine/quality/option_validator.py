"""
Question Factory OS v3.0

Option Validator
"""

from __future__ import annotations

from Engine.models.generated_question_model import GeneratedQuestionModel
from Engine.quality.quality_report import QualityReport


class OptionValidator:
    """
    Validates question options.
    """

    def validate(
        self,
        question: GeneratedQuestionModel,
    ) -> QualityReport:
        """
        Validate question options.
        """

        report = QualityReport()

        # -----------------------------------------------------
        # Minimum Options
        # -----------------------------------------------------

        if len(question.options) < 2:
            report.add_error(
                "Question must contain at least two options."
            )

        # -----------------------------------------------------
        # Empty Options
        # -----------------------------------------------------

        for index, option in enumerate(question.options, start=1):
            if not option.strip():
                report.add_error(
                    f"Option {index} is empty."
                )

        # -----------------------------------------------------
        # Duplicate Options
        # -----------------------------------------------------

        normalized = [option.strip().lower() for option in question.options]

        if len(normalized) != len(set(normalized)):
            report.add_error(
                "Duplicate options detected."
            )

        # -----------------------------------------------------
        # Correct Option
        # -----------------------------------------------------

        if not question.correct_option.strip():
            report.add_error(
                "Correct option is missing."
            )

        report.calculate_score()

        return report