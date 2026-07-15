"""
Question Factory OS v2.0
Production Scheduler

File
----
Engine/director/production_scheduler.py

Description
-----------
The Production Scheduler is responsible for determining the
next manufacturing order for the factory.

It consumes:

    • RuntimeModel
    • Blueprint

It produces:

    • ProductionNodeModel

The scheduler contains no question generation logic.
"""

from __future__ import annotations

import logging
from typing import Any

from Engine.models.runtime_model import RuntimeModel
from Engine.models.production_node_model import (
    ProductionNodeModel,
    ProductionLocation,
    QuestionRange,
)


class ProductionScheduler:
    """
    Determines the next production node.

    This component is the factory planner.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger(self.__class__.__name__)

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def get_next_node(
        self,
        runtime: RuntimeModel,
        blueprint: Any,
    ) -> ProductionNodeModel:
        """
        Determine the next manufacturing node.

        Parameters
        ----------
        runtime
            Current factory runtime.

        blueprint
            Loaded blueprint.

        Returns
        -------
        ProductionNodeModel
        """

        self.logger.info("Determining next production node.")

        node = self._build_node(
            runtime=runtime,
            blueprint=blueprint,
        )

        self.logger.info(
            "Production node created: %s",
            node.production_node,
        )

        return node

    # ---------------------------------------------------------
    # Internal Planning
    # ---------------------------------------------------------

    def _build_node(
        self,
        runtime: RuntimeModel,
        blueprint: Any,
    ) -> ProductionNodeModel:
        """
        Build one production node.

        This method orchestrates the planning process.
        """

        node = ProductionNodeModel()

        self._assign_location(
            node=node,
            runtime=runtime,
            blueprint=blueprint,
        )

        self._assign_question_range(
            node=node,
            runtime=runtime,
        )

        self._assign_execution(
            node=node,
        )

        self._assign_metadata(
            node=node,
        )

        return node

    def _assign_location(
        self,
        node: ProductionNodeModel,
        runtime: RuntimeModel,
        blueprint: Any,
    ) -> None:
        """
        Determine where the next manufacturing batch
        should be produced.

        Current implementation follows the runtime position.

        Future versions will incorporate blueprint saturation,
        workload balancing and priority scheduling.
        """

        production = runtime.production

        location = ProductionLocation(
            subject=production.subject,
            unit=production.unit,
            chapter=production.chapter,
            subtopic=production.subtopic,
            set_number=production.set_number,
            batch_number=production.batch_number,
        )

        node.location = location

        self.logger.info(
            "Location assigned: %s/%s/%s/%s " "(Set %s Batch %s)",
            location.subject,
            location.unit,
            location.chapter,
            location.subtopic,
            location.set_number,
            location.batch_number,
        )

    def _assign_question_range(
        self,
        node: ProductionNodeModel,
        runtime: RuntimeModel,
    ) -> None:
        """
        Determine the question range for this production node.
        """

        production = runtime.production

        question_range = QuestionRange(
            question_from=production.question_from,
            question_to=production.question_to,
            expected_questions=(production.question_to - production.question_from + 1),
        )

        node.question_range = question_range

        self.logger.info(
            "Question range assigned: %d-%d",
            question_range.question_from,
            question_range.question_to,
        )

    def _assign_execution(
        self,
        node: ProductionNodeModel,
    ) -> None:
        """
        Populate execution planning information.

        This is the initial execution plan. More advanced
        scheduling logic can be introduced later.
        """

        execution = node.execution

        execution.priority = 100

        execution.retry_count = 0

        execution.max_retry = 3

        execution.execution_order = 1

        execution.estimated_duration_seconds = node.question_count * 60

        self.logger.info(
            "Execution plan prepared " "(priority=%d, estimated=%ds)",
            execution.priority,
            execution.estimated_duration_seconds,
        )

    def _assign_metadata(
        self,
        node: ProductionNodeModel,
    ) -> None:
        """
        Build scheduler metadata.
        """

        location = node.location

        metadata = node.metadata

        metadata.production_node = (
            f"{location.subject}_"
            f"{location.unit}_"
            f"{location.chapter}_"
            f"{location.subtopic}_"
            f"S{location.set_number}_"
            f"B{location.batch_number}"
        )

        metadata.batch_id = (
            f"{location.subject}_"
            f"{location.unit}_"
            f"{location.chapter}_"
            f"{location.subtopic}_"
            f"S{location.set_number}_"
            f"B{location.batch_number}"
        )

        self.logger.info(
            "Production node created: %s",
            metadata.production_node,
        )
        # ---------------------------------------------------------

    # Validation
    # ---------------------------------------------------------

    def validate_runtime(
        self,
        runtime: RuntimeModel,
    ) -> None:
        """
        Validate that the runtime contains sufficient
        information to schedule the next manufacturing node.
        """

        production = runtime.production

        required_fields = {
            "subject": production.subject,
            "unit": production.unit,
            "chapter": production.chapter,
            "subtopic": production.subtopic,
        }

        missing = [field for field, value in required_fields.items() if not value]

        if missing:
            raise ValueError("Runtime is incomplete. " f"Missing: {', '.join(missing)}")

        if production.question_from <= 0:
            raise ValueError("question_from must be greater than zero.")

        if production.question_to < production.question_from:
            raise ValueError(
                "question_to must be greater than or equal " "to question_from."
            )

        self.logger.info("Runtime validation successful.")

    def validate_blueprint(
        self,
        blueprint: Any,
    ) -> None:
        """
        Validate that a usable blueprint has been supplied.

        Detailed blueprint validation belongs to the Blueprint
        subsystem; this method only performs scheduler-level
        sanity checks.
        """

        if blueprint is None:
            raise ValueError("Blueprint cannot be None.")

        self.logger.info("Blueprint validation successful.")

    def validate_node(
        self,
        node: ProductionNodeModel,
    ) -> None:
        """
        Validate the generated production node.
        """

        if node.question_count <= 0:
            raise ValueError("Production node contains no questions.")

        if not node.location.subject:
            raise ValueError("Production node subject is missing.")

        if not node.location.unit:
            raise ValueError("Production node unit is missing.")

        if not node.location.chapter:
            raise ValueError("Production node chapter is missing.")

        if not node.location.subtopic:
            raise ValueError("Production node subtopic is missing.")

        self.logger.info("Production node validation successful.")

    # ---------------------------------------------------------
    # Planning Diagnostics
    # ---------------------------------------------------------

    def planning_summary(
        self,
        node: ProductionNodeModel,
    ) -> dict:
        """
        Return a concise scheduling summary.
        """

        return {
            "production_node": node.production_node,
            "batch_id": node.batch_id,
            "subject": node.location.subject,
            "unit": node.location.unit,
            "chapter": node.location.chapter,
            "subtopic": node.location.subtopic,
            "set": node.location.set_number,
            "batch": node.location.batch_number,
            "question_from": (node.question_range.question_from),
            "question_to": (node.question_range.question_to),
            "priority": node.execution.priority,
            "estimated_duration": (node.execution.estimated_duration_seconds),
        }

    def log_schedule(
        self,
        node: ProductionNodeModel,
    ) -> None:
        """
        Write a detailed scheduling log entry.
        """

        summary = self.planning_summary(node)

        self.logger.info(
            "Scheduled %s | Questions %d-%d | " "Priority %d",
            summary["production_node"],
            summary["question_from"],
            summary["question_to"],
            summary["priority"],
        )
        # ---------------------------------------------------------

    # Scheduling Policy
    # ---------------------------------------------------------

    def supports(
        self,
        runtime: RuntimeModel,
        blueprint: Any,
    ) -> bool:
        """
        Determine whether the scheduler can create a valid
        production node for the supplied runtime and blueprint.
        """

        try:

            self.validate_runtime(runtime)

            self.validate_blueprint(blueprint)

            return True

        except Exception as ex:

            self.logger.warning(
                "Scheduler support check failed: %s",
                ex,
            )

            return False

    def estimate_duration(
        self,
        question_count: int,
    ) -> int:
        """
        Estimate manufacturing duration.

        Current heuristic:
            60 seconds per question.

        Future implementations may estimate using
        difficulty, question archetypes and historical
        production metrics.
        """

        return max(question_count, 1) * 60

    def calculate_priority(
        self,
        runtime: RuntimeModel,
    ) -> int:
        """
        Determine scheduling priority.

        Lower values indicate higher priority.

        Current implementation always returns the default
        priority. Future versions may incorporate backlog,
        deadlines, saturation and workload balancing.
        """

        return 100

    # ---------------------------------------------------------
    # Factory Hooks
    # ---------------------------------------------------------

    def before_schedule(
        self,
        runtime: RuntimeModel,
        blueprint: Any,
    ) -> None:
        """
        Hook executed immediately before scheduling.

        Override in derived schedulers if additional
        preparation is required.
        """

        return

    def after_schedule(
        self,
        node: ProductionNodeModel,
    ) -> None:
        """
        Hook executed after a production node has been created.

        Override for custom scheduling workflows.
        """

        return

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def health(self) -> dict:
        """
        Return scheduler health information.
        """

        return {
            "component": self.__class__.__name__,
            "status": "READY",
            "scheduler_version": "2.0.0",
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return "ProductionScheduler(" "version='2.0.0')"

    def __str__(self) -> str:
        return "ProductionScheduler"
