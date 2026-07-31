"""
Question Factory OS v3.0

Difficulty Validator
"""

from __future__ import annotations

from Engine.models.generated_question_model import GeneratedQuestionModel
from Engine.quality.quality_report import QualityReport


class DifficultyValidator:
    """
    Validates question difficulty.
    """

    VALID_DIFFICULTIES = {
        "Foundation",
        "Easy",
        "Easy+",
        "Medium",
        "Hard",
        "Elite",
    }

    def validate(
        self,
        question: GeneratedQuestionModel,
    ) -> QualityReport:
        """
        Validate question difficulty.
        """

        report = QualityReport()

        difficulty = question.difficulty.strip()

        if not difficulty:
            report.add_error(
                "Difficulty is missing."
            )
        elif difficulty not in self.VALID_DIFFICULTIES:
            report.add_error(
                f"Invalid difficulty '{difficulty}'."
            )

        report.calculate_score()

        return report