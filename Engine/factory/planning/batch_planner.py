"""
Question Factory OS v3.2

Batch Planner

Responsible for converting a ManufacturingPlan
into executable production batches.

This component does NOT generate questions.
"""

from __future__ import annotations

import logging

from Engine.factory.planning.models.manufacturing_plan import (
    ManufacturingPlan,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)

LOGGER = logging.getLogger(__name__)


class BatchPlanner:
    """
    Creates executable manufacturing batches
    from a ManufacturingPlan.
    """

    DEFAULT_BATCH_SIZE = 20

    def __init__(
        self,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:

        if batch_size <= 0:
            raise ValueError(
                "batch_size must be greater than zero."
            )

        self._logger = LOGGER
        self._batch_size = batch_size

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def create_batches(
        self,
        plan: ManufacturingPlan,
    ) -> list[QuestionBatchModel]:
        """
        Split a ManufacturingPlan into
        QuestionBatchModel objects.
        """

        self._validate_plan(
            plan,
        )

        batches: list[QuestionBatchModel] = []

        remaining = plan.total_questions

        batch_number = 1

        start_question = 1

        while remaining > 0:

            question_count = min(
                self._batch_size,
                remaining,
            )

            batches.append(
                self._create_batch(
                    plan=plan,
                    batch_number=batch_number,
                    start_question=start_question,
                    question_count=question_count,
                )
            )

            remaining -= question_count

            start_question += question_count

            batch_number += 1

        self._logger.info(
            "Created %d manufacturing batches.",
            len(batches),
        )

        return batches
    # ---------------------------------------------------------
    # Batch Factory
    # ---------------------------------------------------------

    def _create_batch(
        self,
        plan: ManufacturingPlan,
        batch_number: int,
        start_question: int,
        question_count: int,
    ) -> QuestionBatchModel:
        """
        Create one manufacturing batch.
        """

        batch = QuestionBatchModel()

        batch.batch_id = (
            f"{plan.subtopic_id}"
            f"_B{batch_number}"
        )

        batch.unit_code = plan.unit_id

        batch.chapter_code = plan.chapter_id

        batch.subtopic_code = plan.subtopic_id

        batch.batch_number = batch_number

        batch.status = "PLANNED"

        batch.set_metadata(
            "planned_question_count",
            question_count,
        )

        batch.set_metadata(
            "start_question",
            start_question,
        )

        batch.set_metadata(
            "end_question",
            start_question
            + question_count
            - 1,
        )

        batch.set_metadata(
            "difficulty_distribution",
            dict(
                plan.difficulty_distribution,
            ),
        )

        batch.set_metadata(
            "archetype_distribution",
            dict(
                plan.archetype_distribution,
            ),
        )

        batch.set_metadata(
            "manufacturing_notes",
            list(
                plan.manufacturing_notes,
            ),
        )

        return batch

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def _validate_plan(
        self,
        plan: ManufacturingPlan,
    ) -> None:
        """
        Validate ManufacturingPlan.
        """

        if plan.total_questions <= 0:
            raise ValueError(
                "ManufacturingPlan contains no questions."
            )

        if not plan.analysis_summary.strip():
            raise ValueError(
                "Analysis summary cannot be empty."
            )

        if sum(
            plan.difficulty_distribution.values()
        ) != plan.total_questions:
            raise ValueError(
                "Difficulty distribution mismatch."
            )

        if sum(
            plan.archetype_distribution.values()
        ) != plan.total_questions:
            raise ValueError(
                "Archetype distribution mismatch."
            )
    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        batches: list[QuestionBatchModel],
    ) -> dict[str, int]:
        """
        Return batch statistics.
        """

        total_questions = sum(
            batch.question_count
            for batch in batches
        )

        return {
            "batch_count": len(batches),
            "total_questions": total_questions,
            "batch_size": self._batch_size,
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
            "component": "BatchPlanner",
            "status": "READY",
            "batch_size": self._batch_size,
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
            "component": "BatchPlanner",
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
            "BatchPlanner reset."
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
    "BatchPlanner",
]