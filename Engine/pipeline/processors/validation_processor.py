"""
Question Factory OS
Validation Processor

Milestone : M12
Sprint    : S3
Release   : R1
"""

from builders.boolean_normalizer import BooleanNormalizer

from core.validation_engine import ValidationEngine

from models.pipeline_context_model import PipelineContextModel

from pipeline.processors.pipeline_processor import PipelineProcessor


class ValidationProcessor(PipelineProcessor):
    """
    Stage 6

    Performs final data normalization
    followed by complete validation.
    """

    stage_id = "VALIDATE"

    name = "Validation Processor"

    description = "Normalizes and validates Question."

    def __init__(self):

        self.boolean_normalizer = BooleanNormalizer()

        self.validator = ValidationEngine()

    def execute(
        self,
        context: PipelineContextModel
    ) -> PipelineContextModel:

        #
        # Boolean Normalization
        #

        context.question = self.boolean_normalizer.normalize(

            context.question

        )

        #
        # Validation
        #

        context.validation = self.validator.validate(

            context.question

        )

        return context
        