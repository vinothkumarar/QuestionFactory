"""
Question Factory OS
Pipeline Processor

Milestone : M4
Sprint    : S1
Release   : R1
"""

from abc import ABC
from abc import abstractmethod

from models.pipeline_context_model import PipelineContextModel


class PipelineProcessor(ABC):
    """
    Base class for every processor
    executed by the Execution Pipeline.
    """

    stage_id = "BASE"

    name = "Base Processor"

    description = ""

    @abstractmethod
    def execute(
        self,
        context: PipelineContextModel
    ) -> PipelineContextModel:
        """
        Execute the processor.

        Parameters
        ----------
        context : PipelineContextModel

        Returns
        -------
        PipelineContextModel
        """
        pass