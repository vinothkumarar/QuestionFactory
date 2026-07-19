"""
Question Factory OS v2.1

Question Generator

Coordinates the manufacturing of question batches.

The QuestionGenerator is intentionally lightweight.
Its responsibilities are:

    • Build an AIJob
    • Delegate execution to FactoryOrchestrator
    • Return the generated questions

All AI execution, validation and repair are delegated
to the orchestration subsystem.
"""

from __future__ import annotations

import logging

from typing import Any

from Engine.blueprint.blueprint_model import (
    BlueprintModel,
)

from Engine.models.production_node_model import (
    ProductionNodeModel,
)

from Engine.models.runtime_model import (
    RuntimeModel,
)

from Engine.factory.generation.ai_job_builder import (
    AIJobBuilder,
)

from Engine.factory.orchestrator.factory_orchestrator import (
    FactoryOrchestrator,
)

from Engine.factory.orchestrator.orchestration_result import (
    OrchestrationResult,
)

class QuestionGenerator:
    VERSION = "2.1.0"
    COMPONENT_NAME = "Question Generator"


    """
    Coordinates question generation.

    The QuestionGenerator performs no AI execution.

    Workflow
    --------
        Production Node
                │
                ▼
          AIJobBuilder
                │
                ▼
             AIJob
                │
                ▼
      FactoryOrchestrator
                │
                ▼
        Generated Questions
    """

    def __init__(
        self,
        *,
        ai_job_builder: AIJobBuilder,
        orchestrator: FactoryOrchestrator,
    ) -> None:
        """
        Create a QuestionGenerator.

        Parameters
        ----------
        ai_job_builder
            Builds AIJob instances from production inputs.

        orchestrator
            Executes the complete AI generation pipeline.
        """

        self._logger = logging.getLogger(
            self.__class__.__name__,
        )

        self._ai_job_builder = ai_job_builder

        self._orchestrator = orchestrator

        self._logger.info(
            "QuestionGenerator initialized."
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def generate(
        self,
        *,
        node: ProductionNodeModel,
        blueprint: BlueprintModel,
        runtime: RuntimeModel,
    ) -> Any:
        """
        Generate one question batch.

        The QuestionGenerator builds an AIJob and
        delegates the complete execution to the
        FactoryOrchestrator.
        """
        self._logger.info(
            "Starting question generation."
        )

        #
        # Build the strongly typed AIJob.
        #

        job = self._ai_job_builder.build(
            node=node,
            blueprint=blueprint,
            runtime=runtime,
        )

        self.before_generation(
            job,
        )

        #
        # Execute the manufacturing pipeline.
        #

        orchestration_result = (
            self._orchestrator.orchestrate(
                job,
            )
        )

        self.after_generation(
            job,
            orchestration_result,
        )

        self._logger.info(
            "Question generation completed."
        )

        return orchestration_result

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_generation(
        self,
        job: Any,
    ) -> None:
        """
        Hook executed immediately before the
        orchestration pipeline starts.
        """

        return

    
    def after_generation(
        self,
        job: Any,
        orchestration_result: OrchestrationResult,
    ) -> None:
        """
        Hook executed after the orchestration
        pipeline completes.
        """

        return
    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
        *,
        node: ProductionNodeModel,
        questions: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Return a concise generation summary.
        """

        return {
            "unit": node.location.unit,
            "chapter": node.location.chapter,
            "subtopic": node.location.subtopic,
            "set": node.location.set_number,
            "batch": node.location.batch_number,
            "requested_questions": node.question_count,
            "generated_questions": len(
                questions,
            ),
        }

    def diagnostics(
        self,
        *,
        node: ProductionNodeModel,
        questions: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Return generator diagnostics.
        """

        return {
            "component": (
                self.component_name
            ),
            "version": (
                self.version
            ),
            "summary": self.summary(
                node=node,
                questions=questions,
            ),
            "orchestrator": (
                self._orchestrator.__class__.__name__
            ),
            "ai_job_builder": (
                self._ai_job_builder.__class__.__name__
            ),
        }

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def generation_statistics(
        self,
        questions: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Return generation statistics.
        """

        generated = len(
            questions,
        )

        return {
            "generated_questions": generated,
            "empty_result": generated == 0,
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return component health.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
            "orchestrator": (
                self._orchestrator.__class__.__name__
            ),
            "ai_job_builder": (
                self._ai_job_builder.__class__.__name__
            ),
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(
        self,
    ) -> dict[str, bool]:
        """
        Return supported capabilities.
        """

        return {
            "ai_job_generation": True,
            "factory_orchestration": True,
            "provider_independent": True,
            "diagnostics": True,
            "health_reporting": True,
            "lifecycle_hooks": True,
        }
    # ---------------------------------------------------------
    # Component Information
    # ---------------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Component version.
        """

        return self.VERSION

    @property
    def component_name(
        self,
    ) -> str:
        """
        Human-readable component name.
        """

        return self.COMPONENT_NAME

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def configuration(
        self,
    ) -> dict[str, Any]:
        """
        Return the current component configuration.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "ai_job_builder": (
                self._ai_job_builder.__class__.__name__
            ),
            "orchestrator": (
                self._orchestrator.__class__.__name__
            ),
        }

    # ---------------------------------------------------------
    # Runtime Summary
    # ---------------------------------------------------------

    def runtime_summary(
        self,
    ) -> dict[str, Any]:
        """
        Return a concise runtime summary.
        """

        return {
            "component": self.component_name,
            "status": "READY",
            "version": self.version,
        }

    # ---------------------------------------------------------
    # Supported Operations
    # ---------------------------------------------------------

    def supports_generation(
        self,
    ) -> bool:
        """
        Return True when generation is supported.
        """

        return True

    def supports_orchestration(
        self,
    ) -> bool:
        """
        Return True when orchestration is available.
        """

        return True
   
    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return (
            "QuestionGenerator("
            f"version='{self.version}')"
        )

    def __str__(
        self,
    ) -> str:
        """
        Human-readable representation.
        """

        return (
            f"{self.component_name} "
            f"[v{self.version}]"
        )


# ---------------------------------------------------------
# Module Exports
# ---------------------------------------------------------

__all__ = [
    "QuestionGenerator",
]

