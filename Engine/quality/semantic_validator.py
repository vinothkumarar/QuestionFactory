"""
Question Factory OS v3.0

Semantic Validator
"""

from __future__ import annotations

from Engine.models.generated_question_model import GeneratedQuestionModel
from Engine.quality.quality_report import QualityReport


class SemanticValidator:
    """
    Performs basic semantic quality checks on a question.
    """

    MINIMUM_QUESTION_LENGTH = 15

    def validate(
        self,
        question: GeneratedQuestionModel,
    ) -> QualityReport:
        """
        Validate semantic quality.
        """

        report = QualityReport()

        text = question.question_text.strip()

        # -----------------------------------------------------
        # Question Presence
        # -----------------------------------------------------

        if not text:
            report.add_error(
                "Question text is missing."
            )
            report.calculate_score()
            return report

        # -----------------------------------------------------
        # Minimum Length
        # -----------------------------------------------------

        if len(text) < self.MINIMUM_QUESTION_LENGTH:
            report.add_warning(
                "Question text appears too short."
            )

        # -----------------------------------------------------
        # Explanation Presence
        # -----------------------------------------------------

        if not question.explanation.strip():
            report.add_warning(
                "Explanation is missing."
            )

        report.calculate_score()

        return report