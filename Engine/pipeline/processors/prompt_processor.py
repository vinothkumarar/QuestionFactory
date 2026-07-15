"""
Question Factory OS
Prompt Processor

Milestone : M4
Sprint    : S2
Release   : R1
"""

from ai.prompt_builder import PromptBuilder

from models.pipeline_context_model import PipelineContextModel

from pipeline.processors.pipeline_processor import PipelineProcessor


class PromptProcessor(PipelineProcessor):
    """
    Builds the AI prompt from the
    Question Skeleton.
    """

    stage_id = "PROMPT"

    name = "Prompt Processor"

    description = "Creates the AI prompt."

    def __init__(self):

        self.builder = PromptBuilder()

    def execute(self, context: PipelineContextModel) -> PipelineContextModel:

        context.prompt = self.builder.build(context.question)

        return context
