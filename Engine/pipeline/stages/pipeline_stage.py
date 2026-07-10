"""
Question Factory OS
Pipeline Stage Interface

Version : 2.3.7.1.2
"""

from abc import ABC
from abc import abstractmethod

from models.pipeline_context_model import PipelineContextModel


class PipelineStage(ABC):

    # -------------------------------------------------
    # Stage Metadata
    # -------------------------------------------------

    name = "Unnamed Stage"

    description = ""

    # -------------------------------------------------
    # Execution Contract
    # -------------------------------------------------

    @abstractmethod
    def execute(
        self,
        context: PipelineContextModel
    ) -> PipelineContextModel:
        """
        Execute one stage of the execution pipeline.

        Every stage receives the PipelineContextModel,
        modifies it if necessary,
        and returns it.
        """
        pass
        