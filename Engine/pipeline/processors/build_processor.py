"""
Question Factory OS
Build Processor

Milestone : M10
Sprint    : S3
Release   : R1
"""

from __future__ import annotations

from typing import Any

from Engine.builders.question_builder import QuestionBuilder
from Engine.models.pipeline_context_model import PipelineContextModel

from .pipeline_processor import PipelineProcessor


class BuildProcessor(PipelineProcessor):
    """
    Pipeline stage responsible for constructing the initial
    Question Factory skeleton.

    The generated skeleton contains all production metadata
    required by downstream AI and validation stages.
    """

    stage_id: str = "BUILD"

    name: str = "Build Processor"

    description: str = "Creates the Question Skeleton."

    def __init__(self) -> None:
        self._builder = QuestionBuilder()

    def execute(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:
        """
        Build the initial question skeleton from the
        production order.
        """

        production_order = context.production_order

        runtime: dict[str, Any] = {
            #
            # Project Information
            #
            "current_project": production_order.unit,
            "current_subject": production_order.subject,
            "current_unit": production_order.unit,
            "current_chapter": production_order.chapter,
            "current_subtopic": production_order.subtopic,
            "current_set": production_order.set_no,
            "current_batch": production_order.batch_no,
            #
            # Manufacturing Information
            #
            "question_number": production_order.question_start,
            "difficulty": "Blueprint",
        }

        context.question = self._builder.build(
            runtime=runtime,
            question_number=production_order.question_start,
        )

        return context