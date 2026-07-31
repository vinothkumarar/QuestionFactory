"""
Question Factory OS v3.1

Academic Analysis Model

Represents the academic planning output returned
by the AI subsystem.
"""

from __future__ import annotations


from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(slots=True)
class AcademicAnalysisModel:
    """
    Result of AI academic analysis.
    """

    estimated_total_questions: int

    difficulty_distribution: dict[str, int]

    archetype_distribution: dict[str, int]

    analysis_summary: str

    manufacturing_notes: list[str] = field(
        default_factory=list
    )

    confidence_score: float = 0.0

    pyq_similarity: float = 0.0

    academic_complexity: float = 0.0

    recommended_batch_size: int = 20

    metadata: dict[str, str] = field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
    ) -> None:

        if self.estimated_total_questions <= 0:
            raise ValueError(
                "estimated_total_questions "
                "must be greater than zero."
            )

        if (
            sum(
                self.difficulty_distribution.values()
            )
            != self.estimated_total_questions
        ):
            raise ValueError(
                "Difficulty distribution mismatch."
            )

        if (
            sum(
                self.archetype_distribution.values()
            )
            != self.estimated_total_questions
        ):
            raise ValueError(
                "Archetype distribution mismatch."
            )

        if not self.analysis_summary.strip():
            raise ValueError(
                "Analysis summary cannot be empty."
            )

    @property
    def is_valid(
        self,
    ) -> bool:

        try:
            self.validate()
            return True
        except ValueError:
            return False
    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, object]:
        """
        Convert the analysis into a dictionary.
        """

        return {
            "estimated_total_questions": (
                self.estimated_total_questions
            ),
            "difficulty_distribution": dict(
                self.difficulty_distribution
            ),
            "archetype_distribution": dict(
                self.archetype_distribution
            ),
            "analysis_summary": (
                self.analysis_summary
            ),
            "manufacturing_notes": list(
                self.manufacturing_notes
            ),
            "confidence_score": (
                self.confidence_score
            ),
            "pyq_similarity": (
                self.pyq_similarity
            ),
            "academic_complexity": (
                self.academic_complexity
            ),
            "recommended_batch_size": (
                self.recommended_batch_size
            ),
            "metadata": dict(
                self.metadata
            ),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "AcademicAnalysisModel":
        """
        Construct AcademicAnalysisModel from a dictionary.
        """

        estimated_total_questions = int(
            data.get(
                "estimated_total_questions",
                0,
            )
        )

        difficulty_distribution = data.get(
            "difficulty_distribution",
            {},
        )

        if not isinstance(
            difficulty_distribution,
            dict,
        ):
            difficulty_distribution = {}

        archetype_distribution = data.get(
            "archetype_distribution",
            {},
        )

        if not isinstance(
            archetype_distribution,
            dict,
        ):
            archetype_distribution = {}

        manufacturing_notes = data.get(
            "manufacturing_notes",
            [],
        )

        if not isinstance(
            manufacturing_notes,
            list,
        ):
            manufacturing_notes = []

        metadata = data.get(
            "metadata",
            {},
        )

        if not isinstance(
            metadata,
            dict,
        ):
            metadata = {}

        return cls(
            estimated_total_questions=estimated_total_questions,
            difficulty_distribution=difficulty_distribution,
            archetype_distribution=archetype_distribution,
            analysis_summary=str(
                data.get(
                    "analysis_summary",
                    "",
                )
            ),
            manufacturing_notes=manufacturing_notes,
            confidence_score=float(
                data.get(
                    "confidence_score",
                    0.0,
                )
            ),
            pyq_similarity=float(
                data.get(
                    "pyq_similarity",
                    0.0,
                )
            ),
            academic_complexity=float(
                data.get(
                    "academic_complexity",
                    0.0,
                )
            ),
            recommended_batch_size=int(
                data.get(
                    "recommended_batch_size",
                    20,
                )
            ),
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict[str, object]:
        """
        Return a concise summary.
        """

        return {
            "questions": (
                self.estimated_total_questions
            ),
            "confidence": (
                self.confidence_score
            ),
            "complexity": (
                self.academic_complexity
            ),
            "recommended_batch_size": (
                self.recommended_batch_size
            ),
            "valid": self.is_valid,
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return model diagnostics.
        """

        return {
            "component": (
                "AcademicAnalysisModel"
            ),
            "valid": self.is_valid,
            "summary": self.summary(),
            "metadata": dict(
                self.metadata
            ),
        }


__all__ = [
    "AcademicAnalysisModel",
]