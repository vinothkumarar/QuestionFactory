"""
Question Factory OS v3.2

Production Planner

Responsible for converting an academic analysis
into a manufacturing plan.

This planner does NOT generate questions.
"""

from __future__ import annotations

import logging

from Engine.factory.planning.models.academic_analysis_model import (
    AcademicAnalysisModel,
)

from Engine.factory.planning.models.manufacturing_plan import (
    ManufacturingPlan,
)

from Engine.models.production_order_model import (
    ProductionOrderModel,
)

LOGGER = logging.getLogger(__name__)


class ProductionPlanner:
    """
    Converts AI academic analysis into a
    ManufacturingPlan.
    """

    def __init__(self) -> None:

        self._logger = LOGGER

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def build_plan(
        self,
        order: ProductionOrderModel,
        analysis: AcademicAnalysisModel,
    ) -> ManufacturingPlan:
        """
        Build a ManufacturingPlan from the
        AI academic analysis.
        """

        analysis.validate()

        plan = ManufacturingPlan(
            subject_id=order.subject,
            unit_id=order.unit,
            chapter_id=order.chapter,
            subtopic_id=order.subtopic,
            total_questions=(
                analysis.estimated_total_questions
            ),
            difficulty_distribution=dict(
                analysis.difficulty_distribution
            ),
            archetype_distribution=dict(
                analysis.archetype_distribution
            ),
            analysis_summary=(
                analysis.analysis_summary
            ),
            manufacturing_notes=list(
                analysis.manufacturing_notes
            ),
        )

        self.validate_plan(
            plan,
        )

        self._logger.info(
            "Manufacturing plan created for '%s'.",
            order.subtopic,
        )

        return plan
    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_plan(
        self,
        plan: ManufacturingPlan,
    ) -> None:
        """
        Validate a ManufacturingPlan.
        """

        if plan.total_questions <= 0:
            raise ValueError(
                "Manufacturing plan must contain at least one question."
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

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _validate_distribution(
        self,
        distribution: dict[str, int],
        expected_total: int,
    ) -> None:
        """
        Validate a distribution.
        """

        if not distribution:
            raise ValueError(
                "Distribution cannot be empty."
            )

        actual_total = sum(
            distribution.values()
        )

        if actual_total <= 0:
            raise ValueError(
                "Distribution total must be greater than zero."
            )

        for name, value in distribution.items():

            if value < 0:
                raise ValueError(
                    f"Negative allocation detected for '{name}'."
                )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        plan: ManufacturingPlan,
    ) -> dict[str, object]:
        """
        Return planner statistics.
        """

        return {
            "subject": plan.subject_id,
            "unit": plan.unit_id,
            "chapter": plan.chapter_id,
            "subtopic": plan.subtopic_id,
            "total_questions": plan.total_questions,
            "difficulty_distribution": dict(
                plan.difficulty_distribution
            ),
            "archetype_distribution": dict(
                plan.archetype_distribution
            ),
        }
    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return planner health.
        """

        return {
            "component": "ProductionPlanner",
            "status": "READY",
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return planner diagnostics.
        """

        return {
            "component": "ProductionPlanner",
            "health": self.health(),
        }

    # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset planner runtime state.
        """

        self._logger.info(
            "ProductionPlanner reset."
        )

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    @property
    def component_name(
        self,
    ) -> str:
        """
        Component name.
        """

        return self.__class__.__name__


__all__ = [
    "ProductionPlanner",
]
