"""
Question Factory OS
Prompt Processor

Milestone : M4
Sprint    : S2
Release   : R1
"""

from __future__ import annotations

from Engine.ai.prompt_builder import PromptBuilder
from Engine.models.pipeline_context_model import PipelineContextModel

from .pipeline_processor import PipelineProcessor


class PromptProcessor(PipelineProcessor):
    """
    Pipeline stage responsible for generating the AI prompt
    from the question skeleton produced by the Build stage.

    The generated prompt is stored in the shared pipeline
    context for consumption by the AI processor.
    """

    stage_id: str = "PROMPT"

    name: str = "Prompt Processor"

    description: str = "Creates the AI prompt."

    def __init__(self) -> None:
        self._builder = PromptBuilder()

    def execute(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:
        """
        Generate the AI prompt from the current question
        skeleton.
        """

        
        if context.question is None:
            raise RuntimeError(
                "Question skeleton has not been generated."
            )

        context.prompt = self._builder.build(context.question)

        return context