"""
Factory Orchestrator

Coordinates the complete Question Factory generation workflow.

Responsibilities
----------------
- Accept generation requests
- Coordinate runtime state
- Load blueprints
- Build prompts
- Execute AI generation
- Parse responses
- Run validation and repair
- Persist generated questions
- Return generation results

The orchestrator intentionally contains orchestration logic only.
Generation, parsing, validation and persistence are delegated to
their respective subsystems.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from Engine.factory.ai.ai_engine import AIEngine
from Engine.factory.ai.models.prompt_package import PromptPackage
from Engine.factory.ai.response_parser import ResponseParser
from Engine.factory.ai.prompt_builder import PromptBuilder
from Engine.factory.repair.repair_engine import RepairEngine
from Engine.factory.validation.question_validator import QuestionValidator


LOGGER = logging.getLogger(__name__)


class FactoryOrchestrator:
    """
    Coordinates the complete Question Factory pipeline.

    The orchestrator owns workflow sequencing but delegates all
    domain-specific work to specialized components.
    """

    

    def __init__(
        self,
        *,
        ai_engine: AIEngine,
        prompt_builder: PromptBuilder,
        response_parser: ResponseParser,
        validator: QuestionValidator,
        repair_engine: RepairEngine,
        workspace: Path | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """
        Create a new orchestrator.

        Parameters
        ----------
        ai_engine:
            AI execution engine.

        prompt_builder:
            Builds prompt packages.

        response_parser:
            Converts raw AI responses into structured objects.

        workspace:
            Optional workspace used for temporary artifacts.

        logger:
            Optional logger.
        """

        self._ai_engine = ai_engine
        self._prompt_builder = prompt_builder
        self._response_parser = response_parser

        self._validator = validator
        self._repair_engine = repair_engine

        self._workspace = workspace or Path.cwd()

        self._logger = logger or LOGGER

        self._started_at = time.monotonic()

        self._generation_count = 0

        self._shutdown = False

        self._logger.debug(
            "FactoryOrchestrator initialized "
            "(workspace=%s)",
            self._workspace,
        )
    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        job: Any,
    ) -> Any:
        """
        Execute a complete generation workflow.

        Parameters
        ----------
        job:
            AI job describing the requested generation.

        Returns
        -------
        Any
            Parsed generation result.
        """

        self._ensure_running()

        self._generation_count += 1

        self._logger.info(
            "Starting generation #%d",
            self._generation_count,
        )

        return self._run_pipeline(job)

    def generate_batch(
        self,
        jobs: list[Any],
    ) -> list[Any]:
        """
        Execute multiple generation jobs sequentially.
        """

        self._ensure_running()

        results: list[Any] = []

        self._logger.info(
            "Generating %d job(s).",
            len(jobs),
        )

        for job in jobs:
            results.append(
                self.generate(job)
            )

        return results

    def resume(
        self,
        job: Any,
    ) -> Any:
        """
        Resume an interrupted generation.

        Current implementation resumes by
        executing the standard pipeline.
        """

        self._logger.info(
            "Resuming generation."
        )

        return self.generate(job)

    def shutdown(
        self,
    ) -> None:
        """
        Shut down the orchestrator.

        After shutdown no additional
        generation requests are accepted.
        """

        if self._shutdown:
            return

        self._shutdown = True

        elapsed = (
            time.monotonic()
            - self._started_at
        )

        self._logger.info(
            "FactoryOrchestrator shutdown "
            "(generations=%d, uptime=%.2fs)",
            self._generation_count,
            elapsed,
        )

    # ------------------------------------------------------------------
    # Internal lifecycle
    # ------------------------------------------------------------------

    def _ensure_running(
        self,
    ) -> None:
        """
        Ensure the orchestrator
        has not been shut down.
        """

        if self._shutdown:

            raise RuntimeError(
                "FactoryOrchestrator "
                "has been shut down."
            )
    # ------------------------------------------------------------------
    # Core Pipeline
    # ------------------------------------------------------------------

    def _run_pipeline(
        self,
        job: Any,
    ) -> Any:
        """
        Execute the complete manufacturing pipeline.

        Workflow
        --------
            AI Job
               │
               ▼
           AI Engine
               │
               ▼
        Parsed Generation
               │
               ▼
          Validation
               │
               ▼
            Repair
               │
               ▼
          Final Result
        """

        self._logger.info(
            "Executing generation pipeline."
        )

        parsed_result = self._execute_ai(
            job,
        )

        batch = self._extract_batch(
            parsed_result,
        )

        validation_results = (
            self._run_validation(
                batch,
            )
        )

        repair_results = (
            self._run_repair(
                batch,
            )
        )

        return self._build_result(
            parsed_result=parsed_result,
            validation_results=validation_results,
            repair_results=repair_results,
        )

    # ------------------------------------------------------------------
    # AI Execution
    # ------------------------------------------------------------------

    def _execute_ai(
        self,
        job: Any,
    ) -> Any:
        """
        Execute the AI engine.
        """

        self._logger.info(
            "Executing AI engine."
        )

        return self._ai_engine.execute(
            job,
        )

    # ------------------------------------------------------------------
    # Batch Extraction
    # ------------------------------------------------------------------

    def _extract_batch(
        self,
        parsed_result: Any,
    ) -> Any:
        """
        Extract the generated question batch.

        Current implementation expects the parsed
        response to expose the generated batch.

        This method provides a single extension
        point for future runtime models.
        """

        if hasattr(
            parsed_result,
            "batch",
        ):
            return parsed_result.batch

        return parsed_result

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _run_validation(
        self,
        batch: Any,
    ) -> list[Any]:
        """
        Execute the validator pipeline.
        """

        self._logger.info(
            "Running validation."
        )

        return self._validator.execute(
            batch,
        )

    # ------------------------------------------------------------------
    # Repair
    # ------------------------------------------------------------------

    def _run_repair(
        self,
        batch: Any,
    ) -> list[Any]:
        """
        Execute every registered repair module.
        """

        self._logger.info(
            "Running repair pipeline."
        )

        return self._repair_engine.execute(
            batch,
        )
    # ------------------------------------------------------------------
    # Result Construction
    # ------------------------------------------------------------------

    def _build_result(
        self,
        *,
        parsed_result: Any,
        validation_results: list[Any],
        repair_results: list[Any],
    ) -> dict[str, Any]:
        """
        Build the final orchestration result.

        The orchestrator currently returns a
        serializable dictionary. A dedicated
        GenerationResult model will replace this
        structure in a future release.
        """

        return {
            "parsed_result": parsed_result,
            "validation_results": validation_results,
            "repair_results": repair_results,
            "generation_number": self._generation_count,
            "status": "SUCCESS",
        }

    # ------------------------------------------------------------------
    # Logging Helpers
    # ------------------------------------------------------------------

    def _log_pipeline_start(
        self,
        job: Any,
    ) -> None:
        """
        Log pipeline start information.
        """

        self._logger.info(
            "Pipeline started for job '%s'.",
            getattr(
                job,
                "job_id",
                "<unknown>",
            ),
        )

    def _log_pipeline_complete(
        self,
        result: dict[str, Any],
    ) -> None:
        """
        Log pipeline completion.
        """

        self._logger.info(
            "Pipeline completed successfully "
            "(generation=%d).",
            result["generation_number"],
        )

    def _log_pipeline_failure(
        self,
        exc: Exception,
    ) -> None:
        """
        Log pipeline failure.
        """

        self._logger.exception(
            "Pipeline execution failed: %s",
            exc,
        )

    # ------------------------------------------------------------------
    # Runtime Information
    # ------------------------------------------------------------------

    def uptime_seconds(
        self,
    ) -> float:
        """
        Return orchestrator uptime.
        """

        return (
            time.monotonic()
            - self._started_at
        )

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return runtime statistics.
        """

        return {
            "generation_count": (
                self._generation_count
            ),
            "uptime_seconds": round(
                self.uptime_seconds(),
                2,
            ),
            "shutdown": self._shutdown,
        }

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return orchestrator diagnostics.
        """

        return {
            "component": (
                self.__class__.__name__
            ),
            "statistics": (
                self.statistics()
            ),
            "workspace": str(
                self._workspace,
            ),
        }

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return orchestrator health.
        """

        return {
            "component": (
                "FactoryOrchestrator"
            ),
            "status": (
                "READY"
                if not self._shutdown
                else "SHUTDOWN"
            ),
            "ai_engine": (
                self._ai_engine.is_ready
            ),
            "validator": (
                not self._validator.is_empty()
            ),
            "repair_engine": (
                not self._repair_engine.is_empty()
            ),
        }
