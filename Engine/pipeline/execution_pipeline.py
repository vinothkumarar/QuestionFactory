"""
Question Factory OS v2.0

Execution Pipeline

Responsible for executing manufacturing stages.

The pipeline itself contains no business logic.

Each stage is responsible for exactly one
manufacturing responsibility.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import List

from Engine.models.pipeline_context_model import (
    PipelineContextModel,
)


# ---------------------------------------------------------
# Pipeline Stage
# ---------------------------------------------------------

class PipelineStage(ABC):
    """
    Base class for every manufacturing stage.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Stage name.
        """

    @abstractmethod
    def execute(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:
        """
        Execute one pipeline stage.
        """


# ---------------------------------------------------------
# Execution Pipeline
# ---------------------------------------------------------

class ExecutionPipeline:
    """
    Executes manufacturing stages sequentially.
    """

    def __init__(self):

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self._stages: List[
            PipelineStage
        ] = []
            # ---------------------------------------------------------
    # Stage Management
    # ---------------------------------------------------------

    def add_stage(
        self,
        stage: PipelineStage,
    ) -> None:
        """
        Register a pipeline stage.
        """

        self._stages.append(stage)

        self.logger.info(
            "Registered stage: %s",
            stage.name,
        )

    # ---------------------------------------------------------
    # Backward Compatibility
    # ---------------------------------------------------------

    def add_processor(
        self,
        processor: PipelineStage,
    ) -> None:
        """
        Backward-compatible wrapper.

        Legacy code using add_processor() will continue
        to work without modification.
        """

        self.add_stage(processor)

    def remove_stage(
        self,
        stage_name: str,
    ) -> bool:
        """
        Remove a stage by name.

        Returns
        -------
        bool
            True if removed.
        """

        for stage in self._stages:

            if stage.name == stage_name:

                self._stages.remove(stage)

                self.logger.info(
                    "Removed stage: %s",
                    stage_name,
                )

                return True

        return False

    def clear(self) -> None:
        """
        Remove every registered stage.
        """

        self._stages.clear()

        self.logger.info(
            "Pipeline cleared."
        )

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    @property
    def stage_count(self) -> int:
        """
        Number of registered stages.
        """

        return len(self._stages)

    #
    # Backward compatibility
    #

    def size(self) -> int:
        """
        Legacy API.

        Equivalent to stage_count.
        """

        return self.stage_count

    def stage_names(self) -> List[str]:
        """
        Return registered stage names.
        """

        return [
            stage.name
            for stage in self._stages
        ]

    def has_stage(
        self,
        stage_name: str,
    ) -> bool:
        """
        Determine whether a stage exists.
        """

        return stage_name in self.stage_names()
            # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def run(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:
        """
        Execute every registered pipeline stage.

        Stages are executed sequentially in the order they
        were registered.
        """

        self.logger.info(
            "Pipeline execution started."
        )

        self.before_pipeline(context)

        for stage in self._stages:

            self.before_stage(
                stage,
                context,
            )

            self.logger.info(
                "Executing stage: %s",
                stage.name,
            )

            try:

                context = stage.execute(
                    context
                )

            except Exception:

                self.logger.exception(
                    "Stage '%s' failed.",
                    stage.name,
                )

                raise

            self.after_stage(
                stage,
                context,
            )

        self.after_pipeline(context)

        self.logger.info(
            "Pipeline execution completed."
        )

        return context

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_pipeline(
        self,
        context: PipelineContextModel,
    ) -> None:
        """
        Executed before pipeline execution begins.

        Override in derived implementations to perform
        initialization, metrics collection or checkpointing.
        """

        return

    def after_pipeline(
        self,
        context: PipelineContextModel,
    ) -> None:
        """
        Executed after pipeline execution completes.

        Override for reporting or cleanup.
        """

        return

    def before_stage(
        self,
        stage: PipelineStage,
        context: PipelineContextModel,
    ) -> None:
        """
        Executed immediately before a stage runs.
        """

        return

    def after_stage(
        self,
        stage: PipelineStage,
        context: PipelineContextModel,
    ) -> None:
        """
        Executed immediately after a stage completes.
        """

        return
            # ---------------------------------------------------------
    # Stage Lookup
    # ---------------------------------------------------------

    def get_stage(
        self,
        stage_name: str,
    ) -> PipelineStage | None:
        """
        Return a registered stage by name.

        Parameters
        ----------
        stage_name
            Name of the stage.

        Returns
        -------
        PipelineStage | None
        """

        for stage in self._stages:

            if stage.name == stage_name:
                return stage

        return None

    def stages(self) -> List[PipelineStage]:
        """
        Return all registered stages.

        A shallow copy is returned to prevent callers from
        modifying the internal stage collection.
        """

        return list(self._stages)

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(self) -> dict:
        """
        Return a concise pipeline summary.
        """

        return {
            "stage_count": self.stage_count,
            "stages": self.stage_names(),
        }

    def diagnostics(self) -> dict:
        """
        Return detailed pipeline diagnostics.
        """

        return {
            "component": self.__class__.__name__,
            "summary": self.summary(),
            "health": self.health(),
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    @property
    def version(self) -> str:
        """
        Pipeline version.
        """

        return "2.0.0"

    @property
    def component_name(self) -> str:
        """
        Pipeline component name.
        """

        return "Execution Pipeline"

    def health(self) -> dict:
        """
        Return pipeline health information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "registered_stages": self.stage_count,
            "status": "READY",
        }

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def is_empty(self) -> bool:
        """
        Determine whether the pipeline has any stages.
        """

        return self.stage_count == 0

    def contains(
        self,
        stage_name: str,
    ) -> bool:
        """
        Determine whether a stage exists.

        Backward-compatible convenience wrapper.
        """

        return self.has_stage(stage_name)
            # ---------------------------------------------------------
    # Pipeline Information
    # ---------------------------------------------------------

    def supported_execution_model(self) -> str:
        """
        Return the execution model used by the pipeline.
        """

        return "SEQUENTIAL"

    def capabilities(self) -> dict:
        """
        Describe the capabilities supported by this pipeline.
        """

        return {
            "sequential_execution": True,
            "stage_registration": True,
            "stage_removal": True,
            "stage_lookup": True,
            "pipeline_lifecycle": True,
            "stage_lifecycle": True,
            "diagnostics": True,
            "health_reporting": True,
            "backward_compatible": True,
        }

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(self) -> None:
        """
        Validate pipeline configuration.

        Raises
        ------
        ValueError
            If duplicate stage names are detected.
        """

        stage_names = self.stage_names()

        duplicates = {
            name
            for name in stage_names
            if stage_names.count(name) > 1
        }

        if duplicates:

            duplicate_list = ", ".join(
                sorted(duplicates)
            )

            raise ValueError(
                "Duplicate pipeline stages detected: "
                f"{duplicate_list}"
            )

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            "ExecutionPipeline("
            f"stages={self.stage_count}, "
            f"version='{self.version}')"
        )

    def __str__(self) -> str:
        return (
            f"{self.component_name} "
            f"[{self.stage_count} stage(s)]"
        )
        