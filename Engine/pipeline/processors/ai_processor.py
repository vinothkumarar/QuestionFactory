"""
Question Factory OS
AI Processor

Milestone : M4
Sprint    : S3
Release   : R1
"""

from __future__ import annotations

from time import perf_counter

from Engine.ai.provider_factory import ProviderFactory
from Engine.models.pipeline_context_model import PipelineContextModel

from .pipeline_processor import PipelineProcessor


class AIProcessor(PipelineProcessor):
    """
    Pipeline stage responsible for sending the generated
    prompt to the configured AI provider and storing the
    returned response in the pipeline context.
    """

    stage_id: str = "AI"

    name: str = "AI Processor"

    description: str = "Generates the AI response."

    def __init__(self) -> None:
        self._provider = ProviderFactory().create()

    def execute(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:
        """
        Execute the configured AI provider and record
        execution metadata.
        """

        start_time = perf_counter()

        context.raw_response = self._provider.generate(context.prompt)

        context.provider = type(self._provider).__name__

        context.execution_time_ms = int(
            (perf_counter() - start_time) * 1000
        )

        return context