"""
Question Factory OS
Validation Processor

Milestone : M4
Sprint    : S6
Release   : R1
"""

from core.validation_engine import ValidationEngine

from models.pipeline_context_model import PipelineContextModel

from pipeline.processors.pipeline_processor import PipelineProcessor


class ValidationProcessor(PipelineProcessor):
    """
    Validates the merged Question object.
    """

    stage_id = "VALIDATE"

    name = "Validation Processor"

    description = "Runs Validation Engine."

    def __init__(self):

        self.validator = ValidationEngine()

    def execute(
        self,
        context: PipelineContextModel
    ) -> PipelineContextModel:

        context.validation = self.validator.validate(

            context.question

        )

        return context
        