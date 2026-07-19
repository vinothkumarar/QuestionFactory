"""
Question Factory OS v2.1

Factory Orchestrator

Coordinates the complete autonomous
question manufacturing pipeline.

Pipeline
--------
Blueprint
    ↓
AI Engine
    ↓
Batch Adapter
    ↓
Validation
    ↓
Repair (if required)
    ↓
Statistics
    ↓
Orchestration Result
"""

from __future__ import annotations

import logging

from Engine.factory.ai.ai_engine import AIEngine
from Engine.factory.ai.models.ai_job import AIJob
from Engine.factory.orchestrator.batch_adapter import BatchAdapter
from Engine.factory.orchestrator.generation_statistics import (
    GenerationStatistics,
)
from Engine.factory.orchestrator.orchestration_result import (
    OrchestrationResult,
)

from Engine.factory.repair.repair_engine import RepairEngine
from Engine.factory.validation.validation_engine import (
    ValidationEngine,
)
from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


class FactoryOrchestrator:
    """
    Coordinates the complete autonomous
    manufacturing workflow.
    """

    VERSION = "2.1.0"

    COMPONENT_NAME = "Factory Orchestrator"

    def __init__(
        self,
        ai_engine: AIEngine,
        validation_engine: ValidationEngine,
        repair_engine: RepairEngine,
        batch_adapter: BatchAdapter,
    ) -> None:
        """
        Initialize orchestrator.
        """

        self._logger = logging.getLogger(
            self.__class__.__name__,
        )

        self._ai_engine = ai_engine
        self._validation_engine = validation_engine
        self._repair_engine = repair_engine
        self._batch_adapter = batch_adapter

        self._statistics = (
            GenerationStatistics()
        )
    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def orchestrate(
        self,
        job: AIJob,
    ) -> OrchestrationResult:
        """
        Execute a complete manufacturing cycle.

        Steps
        -----
        1. AI Generation
        2. Batch Construction
        3. Validation
        4. Repair (if required)
        5. Statistics
        6. Result Construction
        """

        self._statistics.reset()
        self._statistics.start()

        self._logger.info(
            "Starting manufacturing pipeline."
        )

        try:

            parsed_response = (
                self._ai_engine.execute(
                    job,
                )
            )

            batch = self._batch_adapter.build(
                parsed_response,
            )

            self._statistics.batch_id = (
                batch.batch_id
            )

            self._statistics.unit_code = (
                batch.unit_code
            )

            self._statistics.chapter_code = (
                batch.chapter_code
            )

            self._statistics.subtopic_code = (
                batch.subtopic_code
            )

            self._statistics.requested_questions = (
                len(batch.questions)
            )

            self._statistics.generated_questions = (
                len(batch.questions)
            )

            validated_batch = (
                self._validate_batch(
                    batch,
                )
            )

            repaired_batch = (
                self._repair_batch(
                    validated_batch,
                )
            )

            return self._build_success_result(
                repaired_batch,
            )

        except Exception as exc:

            self._logger.exception(
                "Manufacturing pipeline failed."
            )

            return self._build_failure_result(
                exc,
            )

        finally:

            self._statistics.finish()
    # ---------------------------------------------------------
    # Internal Pipeline
    # ---------------------------------------------------------

    def _validate_batch(
        self,
        batch: QuestionBatchModel,
    ) -> QuestionBatchModel:
        """
        Execute the validation pipeline.
        """

        validation_result = (
            self._validation_engine.validate(
                batch,
            )
        )

        self._statistics.validated_questions = (
            validation_result.valid_question_count
        )

        self._statistics.failed_questions = (
            validation_result.invalid_question_count
        )

        self._statistics.add_metadata(
            "validation_passed",
            validation_result.is_valid,
        )

        self._statistics.add_metadata(
            "validation_errors",
            validation_result.error_count,
        )

        return validation_result.batch

    def _repair_batch(
        self,
        batch: QuestionBatchModel,
    ) -> QuestionBatchModel:
        """
        Execute the repair pipeline if required.
        """

        repair_result = (
            self._repair_engine.repair(
                batch,
            )
        )

        self._statistics.repaired_questions = (
            repair_result.repaired_question_count
        )

        self._statistics.add_metadata(
            "repair_executed",
            repair_result.repair_executed,
        )

        self._statistics.add_metadata(
            "repair_success",
            repair_result.success,
        )

        return repair_result.batch

    # ---------------------------------------------------------
    # Result Builders
    # ---------------------------------------------------------

    def _build_success_result(
        self,
        batch: QuestionBatchModel,
    ) -> OrchestrationResult:
        """
        Build a successful orchestration result.
        """

        self._statistics.finish()

        return OrchestrationResult(
            success=True,
            batch=batch,
            statistics=self._statistics,
            message="Manufacturing completed successfully.",
        )
    def _build_failure_result(
        self,
        exc: Exception,
    ) -> OrchestrationResult:
        """
        Build a failed orchestration result.
        """

        self._statistics.finish()

        self._statistics.add_metadata(
            "exception_type",
            exc.__class__.__name__,
        )

        self._statistics.add_metadata(
            "exception_message",
            str(exc),
        )

        return OrchestrationResult(
            success=False,
            batch=None,
            statistics=self._statistics,
            message=str(exc),
        )

    # ---------------------------------------------------------
    # Runtime Information
    # ---------------------------------------------------------

    @property
    def statistics(
        self,
    ) -> GenerationStatistics:
        """
        Return the current generation statistics.
        """

        return self._statistics

    @property
    def component_name(
        self,
    ) -> str:
        """
        Human-readable component name.
        """

        return self.COMPONENT_NAME

    @property
    def version(
        self,
    ) -> str:
        """
        Component version.
        """

        return self.VERSION

    def runtime_summary(
        self,
    ) -> dict[str, object]:
        """
        Return a concise runtime summary.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
            "statistics": (
                self._statistics.runtime_summary()
            ),
        }

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return orchestrator health information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "healthy": True,
            "ai_engine": True,
            "batch_adapter": True,
            "validation_engine": True,
            "repair_engine": True,
        }
    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return detailed diagnostics for the orchestrator.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "ai_engine": self._ai_engine.__class__.__name__,
            "validation_engine": (
                self._validation_engine.__class__.__name__
            ),
            "repair_engine": (
                self._repair_engine.__class__.__name__
            ),
            "batch_adapter": (
                self._batch_adapter.__class__.__name__
            ),
            "statistics": (
                self._statistics.to_dict()
            ),
        }

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset the orchestrator state.
        """

        self._statistics.reset()

        self._logger.debug(
            "%s reset completed.",
            self.COMPONENT_NAME,
        )

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.COMPONENT_NAME}"
            f"(version='{self.VERSION}')"
        )

    def __str__(
        self,
    ) -> str:
        """
        Human-readable representation.
        """

        return (
            f"{self.COMPONENT_NAME} "
            f"v{self.VERSION}"
        )