"""
Question Factory OS
Merge Processor

Milestone : M4
Sprint    : S5
Release   : R1
"""

from builders.question_merger import QuestionMerger

from models.pipeline_context_model import PipelineContextModel

from pipeline.processors.pipeline_processor import PipelineProcessor


class MergeProcessor(PipelineProcessor):
    """
    Merges the AI-generated educational
    content into the factory question
    skeleton.
    """

    stage_id = "MERGE"

    name = "Merge Processor"

    description = "Creates the final Question object."

    def __init__(self):

        self.merger = QuestionMerger()

    def execute(
        self,
        context: PipelineContextModel
    ) -> PipelineContextModel:

        context.question = self.merger.merge(

            context.question,

            context.parsed_response

        )

        return context
        