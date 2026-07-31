"""
Question Factory OS v3.2

Manufacturing Director

Coordinates the complete planning pipeline.

ProductionOrder
        │
        ▼
AcademicAnalyzer
        │
        ▼
ProductionPlanner
        │
        ▼
BatchPlanner
        │
        ▼
QuestionBatchModel[]
"""

from __future__ import annotations

import logging

from Engine.factory.planning.academic_analyzer import (
    AcademicAnalyzer,
)

from Engine.factory.planning.batch_planner import (
    BatchPlanner,
)

from Engine.factory.planning.production_planner import (
    ProductionPlanner,
)

from Engine.factory.planning.models.academic_analysis_model import (
    AcademicAnalysisModel,
)

from Engine.factory.planning.models.manufacturing_plan import (
    ManufacturingPlan,
)

from Engine.models.production_order_model import (
    ProductionOrderModel,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)

from Engine.factory.planning.models.planning_result import (
    PlanningResult,
)

LOGGER = logging.getLogger(__name__)


class PlanningDirector:
    """
    Coordinates the complete planning pipeline.
    """

    def __init__(
        self,
        academic_analyzer: AcademicAnalyzer,
        production_planner: ProductionPlanner,
        batch_planner: BatchPlanner,
    ) -> None:

        self._logger = LOGGER

        self._academic_analyzer = (
            academic_analyzer
        )

        self._production_planner = (
            production_planner
        )

        self._batch_planner = (
            batch_planner
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def plan(
        self,
        order: ProductionOrderModel,
    ) -> PlanningResult:
        """
        Execute the complete planning pipeline.
        """

        self._logger.info(
            "Planning manufacturing for '%s'.",
            order.subtopic,
        )

        analysis: AcademicAnalysisModel = (
            self._academic_analyzer.analyze(
                order,
            )
        )

        plan: ManufacturingPlan = (
            self.build_manufacturing_plan(
                order,
                analysis,
            )
        )

        batches = (
            self.build_batches(
                plan,
            )
        )

        self._logger.info(
            "Manufacturing planning completed. %d batches created.",
            len(batches),
        )

        return PlanningResult(
            academic_analysis=analysis,
            manufacturing_plan=plan,
            question_batches=batches,
        )
    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_order(
        self,
        order: ProductionOrderModel,
    ) -> None:
        """
        Validate the production order.
        """

        if not order.subject:
            raise ValueError(
                "Subject is required."
            )

        if not order.unit:
            raise ValueError(
                "Unit is required."
            )

        if not order.chapter:
            raise ValueError(
                "Chapter is required."
            )

        if not order.subtopic:
            raise ValueError(
                "Subtopic is required."
            )

    # ---------------------------------------------------------
    # Planning Stages
    # ---------------------------------------------------------

    def analyze(
        self,
        order: ProductionOrderModel,
    ) -> AcademicAnalysisModel:
        """
        Execute academic analysis only.
        """

        self.validate_order(
            order,
        )

        return self._academic_analyzer.analyze(
            order,
        )

    def build_manufacturing_plan(
        self,
        order: ProductionOrderModel,
        analysis: AcademicAnalysisModel,
    ) -> ManufacturingPlan:
        """
        Build a ManufacturingPlan.
        """

        return self._production_planner.build_plan(
            order,
            analysis,
        )

    def build_batches(
        self,
        plan: ManufacturingPlan,
    ) -> list[QuestionBatchModel]:
        """
        Build executable manufacturing batches.
        """

        return self._batch_planner.create_batches(
            plan,
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        batches: list[QuestionBatchModel],
    ) -> dict[str, int]:
        """
        Return planning statistics.
        """

        return self._batch_planner.statistics(
            batches,
        )
    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return PlanningDirector health.
        """

        return {
            "component": self.component_name,
            "status": "READY",
            "academic_analyzer": (
                self._academic_analyzer.__class__.__name__
            ),
            "production_planner": (
                self._production_planner.__class__.__name__
            ),
            "batch_planner": (
                self._batch_planner.__class__.__name__
            ),
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
            "component": self.component_name,
            "health": self.health(),
        }

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset runtime state.
        """

        self._logger.info(
            "PlanningDirector reset."
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
    "PlanningDirector",
]