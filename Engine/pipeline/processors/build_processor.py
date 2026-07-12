"""
Question Factory OS
Build Processor

Milestone : M10
Sprint    : S3
Release   : R1
"""

from builders.question_builder import QuestionBuilder

from models.pipeline_context_model import PipelineContextModel

from pipeline.processors.pipeline_processor import PipelineProcessor


class BuildProcessor(PipelineProcessor):
    """
    Stage 1

    Builds the Question Skeleton.

    The generated skeleton contains all
    production metadata required by the
    downstream AI pipeline.
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

            #
            # Project Information
            #

            "current_project":
                context.production_order.unit,

            "current_subject":
                context.production_order.subject,

            "current_unit":
                context.production_order.unit,

            "current_chapter":
                context.production_order.chapter,

            "current_subtopic":
                context.production_order.subtopic,

            "current_set":
                context.production_order.set_no,

            "current_batch":
                context.production_order.batch_no,

            #
            # Manufacturing Information
            #

            "question_number":
                context.production_order.question_start,

            "difficulty":
                "Blueprint"

        }

        context.question = self.builder.build(

            runtime,

            context.production_order.question_start

        )

        return context
        