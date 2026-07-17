"""
Question Factory OS
Merge Processor

Milestone : M4
Sprint    : S5
Release   : R1
"""

from __future__ import annotations

from Engine.builders.question_merger import QuestionMerger
from Engine.models.pipeline_context_model import PipelineContextModel

from .pipeline_processor import PipelineProcessor


class MergeProcessor(PipelineProcessor):
    """
    Pipeline stage responsible for merging the structured
    AI response into the question skeleton.

    This stage produces the complete Question model by
    combining the factory-generated metadata with the
    AI-generated educational content.
    """

    stage_id: str = "MERGE"

    name: str = "Merge Processor"

    description: str = "Creates the final Question object."

    def __init__(self) -> None:
        self._merger = QuestionMerger()

    def execute(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:
        """
        Merge the parsed AI response into the existing
        question skeleton.
        """

        
        if context.question is None:
            raise RuntimeError(
                "Question skeleton has not been generated."
            )

        if context.parsed_response is None:
            raise RuntimeError(
                "Parsed AI response is unavailable."
            )

        context.question = self._merger.merge(
            context.question,
            context.parsed_response,
        )

        return context