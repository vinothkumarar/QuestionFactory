"""
Question Factory OS
Pipeline Processor

Milestone : M4
Sprint    : S1
Release   : R1
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from Engine.models.pipeline_context_model import PipelineContextModel
from Engine.pipeline.execution_pipeline import PipelineStage


class PipelineProcessor(PipelineStage, ABC):
    """
    Abstract base class for every processor executed by the
    Question Factory execution pipeline.

    A processor represents a single logical unit of work within
    the execution pipeline. Each processor receives the shared
    PipelineContextModel, performs its work, and returns the
    updated context for downstream stages.

    Implementations should avoid mutating unrelated portions of
    the context and should remain deterministic whenever possible.
    """

    stage_id: str = "BASE"

    name: str = "Base Processor"

    description: str = ""

    @abstractmethod
    def execute(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:
        """
        Execute this processor.

        Parameters
        ----------
        context:
            Shared pipeline execution context.

        Returns
        -------
        PipelineContextModel
            Updated execution context.
        """
        raise NotImplementedError  