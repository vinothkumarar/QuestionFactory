"""
Question Factory OS
Build Processor

Milestone : M4
Sprint    : S1
Release   : R1
"""

from builders.question_builder import QuestionBuilder

from models.pipeline_context_model import PipelineContextModel

from pipeline.processors.pipeline_processor import PipelineProcessor


class BuildProcessor(PipelineProcessor):
    """
    Builds the Question Skeleton using
    the QuestionBuilder.
    """

    stage_id = "BUILD"

    name = "Build Processor"

    description = "Creates the Question Skeleton."

    def __init__(self):

        self.builder = QuestionBuilder()

    def execute(
        self,
        context: PipelineContextModel
    ) -> PipelineContextModel:

        runtime = {

            "current_project": context.production_order.unit,

            "current_chapter": context.production_order.chapter,

            "current_subtopic": context.production_order.subtopic,

            "current_set": context.production_order.set_no,

            "current_batch": context.production_order.batch_no

        }

        context.question = self.builder.build(

            runtime,

            context.production_order.question_start

        )

        return context
        