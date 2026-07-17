"""
Question Factory OS
Pipeline Processor

Milestone : M4
Sprint    : S1
Release   : R1
"""

from __future__ import annotations

from abc import abstractmethod

from Engine.models.pipeline_context_model import (
    PipelineContextModel,
)
from Engine.pipeline.execution_pipeline import (
    PipelineStage,
)


class PipelineProcessor(PipelineStage):
    """
    Base class for every processor
    executed by the Execution Pipeline.
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
        Execute the processor.
        """
        raise NotImplementedError
        