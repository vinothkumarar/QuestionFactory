"""
Question Factory OS
Validation Processor

Milestone : M12
Sprint    : S3
Release   : R1
"""

from __future__ import annotations

from Engine.builders.boolean_normalizer import BooleanNormalizer
from Engine.core.validation_engine import ValidationEngine
from Engine.models.pipeline_context_model import PipelineContextModel

from .pipeline_processor import PipelineProcessor


class ValidationProcessor(PipelineProcessor):
    """
    Final pipeline stage responsible for normalizing the
    completed Question model and performing comprehensive
    validation.

    This stage ensures the generated question satisfies all
    Question Factory quality, schema, and business rules
    before leaving the execution pipeline.
    """

    stage_id: str = "VALIDATE"

    name: str = "Validation Processor"

    description: str = "Normalizes and validates Question."

    def __init__(self) -> None:
        self._boolean_normalizer = BooleanNormalizer()
        self._validator = ValidationEngine()

    def execute(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:
        """
        Normalize the generated question and execute the
        complete validation workflow.
        """

        #
        # Boolean normalization
        #

        if context.question is None:
            raise RuntimeError(
                "Question has not been created."
            )

        context.question = self._boolean_normalizer.normalize(
            context.question,
        )

        #
        # Validation
        #

        context.validation = self._validator.validate(
            context.question,
        )

        return context