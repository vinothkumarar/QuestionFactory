"""
Question Factory OS v3.1
Subtopic Analyzer

Responsible for producing an academic ManufacturingPlan
for a single ProductionOrder.

This component DOES NOT generate questions.

Responsibilities
----------------
* Analyse manufacturing context
* Estimate production volume
* Build difficulty distribution
* Build archetype distribution
* Produce ManufacturingPlan

Future versions may replace the deterministic analysis
with AI-driven analysis without changing callers.
"""

from __future__ import annotations

from typing import Dict
from typing import List

from Engine.factory.planning.models.manufacturing_plan import (
    ManufacturingPlan,
)

from Engine.models.production_order_model import (
    ProductionOrderModel,
)


class SubtopicAnalyzer:
    """
    Academic manufacturing planner.

    Converts a ProductionOrderModel into a
    ManufacturingPlan.

    This class intentionally contains no OpenAI
    implementation. AI based analysis can later be
    injected without changing the public API.
    """

    def __init__(self) -> None:
        pass

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def analyze(
        self,
        order: ProductionOrderModel,
    ) -> ManufacturingPlan:
        """
        Analyse a production order and create a
        ManufacturingPlan.
        """

        total_questions = self._determine_total_questions(
            order,
        )

        difficulty_distribution = (
            self._difficulty_distribution(
                total_questions,
            )
        )

        archetype_distribution = (
            self._archetype_distribution(
                total_questions,
            )
        )

        return ManufacturingPlan(
            subject_id=order.subject,
            unit_id=order.unit,
            chapter_id=order.chapter,
            subtopic_id=order.subtopic,
            total_questions=total_questions,
            difficulty_distribution=(
                difficulty_distribution
            ),
            archetype_distribution=(
                archetype_distribution
            ),
            analysis_summary=self._summary(
                order,
                total_questions,
            ),
            manufacturing_notes=self._notes(
                order,
            ),
        )

    # ---------------------------------------------------------
    # Question Planning
    # ---------------------------------------------------------

    def _determine_total_questions(
        self,
        order: ProductionOrderModel,
    ) -> int:
        """
        Determine manufacturing quantity.

        Current implementation preserves the
        requested batch size.

        Future AI implementations may calculate
        this dynamically from academic richness.
        """

        return max(
            1,
            order.question_count,
        )

    # ---------------------------------------------------------
    # Difficulty Distribution
    # ---------------------------------------------------------

    def _difficulty_distribution(
        self,
        total: int,
    ) -> Dict[str, int]:
        """
        Build difficulty distribution.
        """

        easy = int(total * 0.30)

        medium = int(total * 0.45)

        hard = total - easy - medium

        return {
            "Easy": easy,
            "Medium": medium,
            "Hard": hard,
        }
    # ---------------------------------------------------------
    # Archetype Distribution
    # ---------------------------------------------------------

    def _archetype_distribution(
        self,
        total: int,
    ) -> Dict[str, int]:
        """
        Build archetype distribution.

        Current implementation uses a deterministic
        allocation. Future AI versions may return
        dynamic distributions.
        """

        conceptual = int(total * 0.30)

        computational = int(total * 0.35)

        analytical = int(total * 0.20)

        application = total - (
            conceptual
            + computational
            + analytical
        )

        distribution = {
            "Conceptual": conceptual,
            "Computational": computational,
            "Analytical": analytical,
            "Application": application,
        }

        self._validate_distribution(
            distribution,
            total,
        )

        return distribution

    # ---------------------------------------------------------
    # Analysis Summary
    # ---------------------------------------------------------

    def _summary(
        self,
        order: ProductionOrderModel,
        total: int,
    ) -> str:
        """
        Produce a concise manufacturing summary.
        """

        return (
            f"Manufacturing plan created for "
            f"{order.subject} / "
            f"{order.unit} / "
            f"{order.chapter} / "
            f"{order.subtopic}. "
            f"Target questions: {total}."
        )

    # ---------------------------------------------------------
    # Manufacturing Notes
    # ---------------------------------------------------------

    def _notes(
        self,
        order: ProductionOrderModel,
    ) -> List[str]:
        """
        Build manufacturing notes.
        """

        return [
            (
                "Manufacturing plan generated "
                "by SubtopicAnalyzer."
            ),
            (
                "Production order preserved "
                "without modification."
            ),
            (
                "Difficulty distribution "
                "automatically calculated."
            ),
            (
                "Archetype distribution "
                "automatically calculated."
            ),
            (
                "Ready for ProductionPlanner."
            ),
        ]

    # ---------------------------------------------------------
    # Validation Helpers
    # ---------------------------------------------------------

    def _validate_distribution(
        self,
        distribution: Dict[str, int],
        expected_total: int,
    ) -> None:
        """
        Validate a generated distribution.
        """

        actual_total = sum(
            distribution.values()
        )

        if actual_total != expected_total:
            raise ValueError(
                "Distribution total mismatch "
                f"({actual_total} != "
                f"{expected_total})"
            )

        for name, value in distribution.items():

            if value < 0:

                raise ValueError(
                    f"Negative allocation "
                    f"detected for '{name}'."
                )
    # ---------------------------------------------------------
    # Manufacturing Plan Validation
    # ---------------------------------------------------------

    def validate_plan(
        self,
        plan: ManufacturingPlan,
    ) -> None:
        """
        Validate a completed ManufacturingPlan.

        Raises
        ------
        ValueError
            If the plan is structurally invalid.
        """

        if plan.total_questions <= 0:
            raise ValueError(
                "Manufacturing plan must contain at least "
                "one question."
            )

        self._validate_distribution(
            plan.difficulty_distribution,
            plan.total_questions,
        )

        self._validate_distribution(
            plan.archetype_distribution,
            plan.total_questions,
        )

        if not plan.analysis_summary.strip():
            raise ValueError(
                "Analysis summary cannot be empty."
            )

        if plan.manufacturing_notes is None:
            raise ValueError(
                "Manufacturing notes cannot be None."
            )

    # ---------------------------------------------------------
    # Capability
    # ---------------------------------------------------------

    def supports(
        self,
        order: ProductionOrderModel,
    ) -> bool:
        """
        Determine whether this analyzer can process
        the supplied production order.

        Future implementations may inspect curriculum,
        subject or blueprint version.

        Current implementation accepts every order.
        """

        return (
            bool(order.subject)
            and bool(order.unit)
            and bool(order.chapter)
            and bool(order.subtopic)
        )

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    def create_plan(
        self,
        order: ProductionOrderModel,
    ) -> ManufacturingPlan:
        """
        Create and validate a ManufacturingPlan.
        """

        if not self.supports(order):
            raise ValueError(
                "Unsupported production order."
            )

        plan = self.analyze(order)

        self.validate_plan(plan)

        return plan


__all__ = [
    "SubtopicAnalyzer",
]
