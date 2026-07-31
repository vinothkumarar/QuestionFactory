"""
Question Factory OS v3.2

Planning Result

Represents the complete output of the
PlanningDirector.

The PlanningResult becomes the contract
between the Planning Layer and the
Manufacturing Layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from Engine.factory.planning.models.academic_analysis_model import (
    AcademicAnalysisModel,
)

from Engine.factory.planning.models.manufacturing_plan import (
    ManufacturingPlan,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


@dataclass(slots=True)
class PlanningResult:
    """
    Complete planning output.
    """

    academic_analysis: AcademicAnalysisModel

    manufacturing_plan: ManufacturingPlan

    question_batches: list[
        QuestionBatchModel
    ] = field(
        default_factory=list,
    )

    def total_batches(
        self,
    ) -> int:
        """
        Return batch count.
        """

        return len(
            self.question_batches
        )

    def total_questions(
        self,
    ) -> int:
        """
        Return planned question count.
        """

        return (
            self.manufacturing_plan.total_questions
        )
    def has_batches(
        self,
    ) -> bool:
        """
        Return whether batches exist.
        """

        return bool(
            self.question_batches
        )

    def is_empty(
        self,
    ) -> bool:
        """
        Return whether planning produced
        any batches.
        """

        return not self.has_batches()

    def to_dict(
        self,
    ) -> dict[str, object]:
        """
        Serialize planning result.
        """

        return {
            "academic_analysis": (
                self.academic_analysis.to_dict()
            ),
            "manufacturing_plan": {
                "subject_id": self.manufacturing_plan.subject_id,
                "unit_id": self.manufacturing_plan.unit_id,
                "chapter_id": self.manufacturing_plan.chapter_id,
                "subtopic_id": self.manufacturing_plan.subtopic_id,
                "total_questions": (
                    self.manufacturing_plan.total_questions
                ),
            },
            "batch_count": (
                self.total_batches()
            ),
            "question_count": (
                self.total_questions()
            ),
        }


__all__ = [
    "PlanningResult",
]