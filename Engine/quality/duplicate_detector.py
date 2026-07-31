"""
Question Factory OS v3.0

Duplicate Detector
"""

from __future__ import annotations

from Engine.models.generated_question_model import GeneratedQuestionModel
from Engine.quality.quality_report import QualityReport


class DuplicateDetector:
    """
    Detects duplicate and near-duplicate questions.

    Current implementation is a framework.
    Semantic and repository-based duplicate detection
    will be added in later sprints.
    """

    def validate(
        self,
        question: GeneratedQuestionModel,
    ) -> QualityReport:
        """
        Validate duplicate status.
        """

        report = QualityReport()

        text = question.question_text.strip()

        if not text:
            report.add_error(
                "Question text is missing."
            )

        report.calculate_score()

        return report