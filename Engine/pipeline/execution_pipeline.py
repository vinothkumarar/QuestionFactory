"""
Question Factory OS v2.1

Execution Pipeline

Responsible for executing manufacturing stages.

The pipeline itself contains no business logic.

Each stage is responsible for exactly one
manufacturing responsibility.
"""

from __future__ import annotations

import logging
from abc import ABC
from abc import abstractmethod
from typing import Any

from Engine.models.pipeline_context_model import (
    PipelineContextModel,
)


# ==========================================================
# Pipeline Stage
# ==========================================================


class PipelineStage(ABC):
    """
    Base class for every execution stage.
    """

    #
    # Metadata
    #

    stage_id: str = "BASE"

    name: str = "Pipeline Stage"

    description: str = ""

    #
    # Execution
    #

    @abstractmethod
    def execute(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:
        """
        Execute the stage.
        """
        raise NotImplementedError


# ==========================================================
# Execution Pipeline
# ==========================================================


class ExecutionPipeline:
    """
    Sequential execution pipeline.

    Stages are executed in the order
    they are registered.
    """

    VERSION = "2.1.0"

    COMPONENT_NAME = "Execution Pipeline"

    def __init__(self) -> None:

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self._stages: list[PipelineStage] = []

    # ------------------------------------------------------
    # Registration
    # ------------------------------------------------------

    def add_stage(
        self,
        stage: PipelineStage,
    ) -> None:
        """
        Register a stage.
        """

        self._stages.append(stage)

        self.logger.info(
            "Registered stage: %s",
            stage.name,
        )

    #
    # Backward compatibility
    #

    def add_processor(
        self,
        processor: PipelineStage,
    ) -> None:
        """
        Legacy wrapper.
        """

        self.add_stage(processor)

    def remove_stage(
        self,
        stage_name: str,
    ) -> bool:
        """
        Remove a registered stage.
        """

        for stage in list(self._stages):

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
        Remove every stage.
        """

        self._stages.clear()

        self.logger.info(
            "Pipeline cleared."
        )

    # ------------------------------------------------------
    # Information
    # ------------------------------------------------------

    @property
    def stage_count(
        self,
    ) -> int:

        return len(self._stages)

    def size(
        self,
    ) -> int:
        """
        Legacy API.
        """

        return self.stage_count

    def is_empty(
        self,
    ) -> bool:

        return self.stage_count == 0

    def stage_names(
        self,
    ) -> list[str]:

        return [
            stage.name
            for stage in self._stages
        ]

    def has_stage(
        self,
        stage_name: str,
    ) -> bool:

        return stage_name in self.stage_names()
    # ------------------------------------------------------
    # Execution
    # ------------------------------------------------------

    def run(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:
        """
        Execute every registered stage.
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

                context = stage.execute(context)

            except Exception:

                self.logger.exception(
                    "Pipeline stage '%s' failed.",
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

    # ------------------------------------------------------
    # Lifecycle Hooks
    # ------------------------------------------------------

    def before_pipeline(
        self,
        context: PipelineContextModel,
    ) -> None:
        """
        Executed immediately before the
        pipeline starts.

        Override in derived classes if required.
        """

        return

    def after_pipeline(
        self,
        context: PipelineContextModel,
    ) -> None:
        """
        Executed immediately after the
        pipeline completes.
        """

        return

    def before_stage(
        self,
        stage: PipelineStage,
        context: PipelineContextModel,
    ) -> None:
        """
        Hook executed before every stage.
        """

        return

    def after_stage(
        self,
        stage: PipelineStage,
        context: PipelineContextModel,
    ) -> None:
        """
        Hook executed after every stage.
        """

        return

    # ------------------------------------------------------
    # Stage Lookup
    # ------------------------------------------------------

    def get_stage(
        self,
        stage_name: str,
    ) -> PipelineStage | None:
        """
        Return a registered stage by name.
        """

        for stage in self._stages:

            if stage.name == stage_name:
                return stage

        return None

    def stages(
        self,
    ) -> list[PipelineStage]:
        """
        Return a copy of the registered stages.
        """

        return list(self._stages)

    def contains(
        self,
        stage_name: str,
    ) -> bool:
        """
        Backward-compatible convenience wrapper.
        """

        return self.has_stage(stage_name)
    # ------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------

    def summary(
        self,
    ) -> dict[str, Any]:
        """
        Return a concise pipeline summary.
        """

        return {
            "stage_count": self.stage_count,
            "stages": self.stage_names(),
        }

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return detailed diagnostic information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "summary": self.summary(),
            "health": self.health(),
        }

    # ------------------------------------------------------
    # Version Information
    # ------------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Pipeline version.
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

    # ------------------------------------------------------
    # Health
    # ------------------------------------------------------

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return pipeline health information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "registered_stages": self.stage_count,
            "status": "READY",
        }

    # ------------------------------------------------------
    # Validation
    # ------------------------------------------------------

    def validate(
        self,
    ) -> None:
        """
        Validate the pipeline configuration.

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
    # ------------------------------------------------------
    # Capabilities
    # ------------------------------------------------------

    def supported_execution_model(
        self,
    ) -> str:
        """
        Return the execution model used by the pipeline.
        """

        return "SEQUENTIAL"

    def capabilities(
        self,
    ) -> dict[str, Any]:
        """
        Return the capabilities supported by this pipeline.
        """

        return {
            "sequential_execution": True,
            "stage_registration": True,
            "stage_removal": True,
            "stage_lookup": True,
            "pipeline_lifecycle": True,
            "stage_lifecycle": True,
            "validation": True,
            "diagnostics": True,
            "health_reporting": True,
            "backward_compatible": True,
        }

    # ------------------------------------------------------
    # Export
    # ------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Export pipeline metadata.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "execution_model": self.supported_execution_model(),
            "stage_count": self.stage_count,
            "stages": self.stage_names(),
            "health": self.health(),
            "capabilities": self.capabilities(),
        }

    # ------------------------------------------------------
    # Debug
    # ------------------------------------------------------

    def dump(
        self,
    ) -> dict[str, Any]:
        """
        Backward-compatible diagnostic dump.
        """

        return self.to_dict()

    # ------------------------------------------------------
    # Representation
    # ------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        return (
            "ExecutionPipeline("
            f"stages={self.stage_count}, "
            f"version='{self.version}')"
        )

    def __str__(
        self,
    ) -> str:
        return (
            f"{self.component_name} "
            f"[{self.stage_count} stage(s)]"
        )
#
# ==========================================================================
# End of File
# ==========================================================================

# The implementation intentionally preserves the original public API
# while modernizing the internal typing for Question Factory OS v2.1.
#
# Public API preserved:
#
#   • add_stage()
#   • add_processor()
#   • remove_stage()
#   • clear()
#   • run()
#   • stage_count
#   • size()
#   • stage_names()
#   • has_stage()
#   • contains()
#   • get_stage()
#   • stages()
#   • before_pipeline()
#   • after_pipeline()
#   • before_stage()
#   • after_stage()
#   • validate()
#   • health()
#   • summary()
#   • diagnostics()
#   • capabilities()
#   • dump()
#   • to_dict()
#
# Design Notes
# ------------
#
# PipelineStage now exposes metadata
#
#     stage_id
#     name
#     description
#
# as normal class attributes instead of abstract properties.
#
# This aligns with every existing processor implementation
# (BuildProcessor, PromptProcessor, AIProcessor,
# ParseProcessor, MergeProcessor, ValidationProcessor),
# eliminating the previous mypy inheritance conflict while
# preserving backward compatibility.
#
# No business logic has been changed.
#
# ==========================================================================
