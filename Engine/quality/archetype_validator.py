"""
Question Factory OS v3.0

Archetype Validator
"""

from __future__ import annotations

from Engine.models.generated_question_model import GeneratedQuestionModel
from Engine.quality.quality_report import QualityReport


class ArchetypeValidator:
    """
    Validates question archetypes.
    """

    VALID_ARCHETYPES = {
        "Conceptual",
        "Computational",
        "Analytical",
        "Application",
        "Assertion-Reason",
        "Integer",
        "Multi-Concept",
    }

    def validate(
        self,
        question: GeneratedQuestionModel,
    ) -> QualityReport:
        """
        Validate question archetype.
        """

        report = QualityReport()

        archetype = question.archetype.strip()

        if not archetype:
            report.add_error(
                "Archetype is missing."
            )
        elif archetype not in self.VALID_ARCHETYPES:
            report.add_warning(
                f"Unknown archetype '{archetype}'."
            )

        report.calculate_score()

        return report