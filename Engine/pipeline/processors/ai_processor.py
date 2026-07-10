"""
Question Factory OS
AI Processor

Milestone : M4
Sprint    : S3
Release   : R1
"""

import time

from ai.provider_factory import ProviderFactory

from models.pipeline_context_model import PipelineContextModel

from pipeline.processors.pipeline_processor import PipelineProcessor


class AIProcessor(PipelineProcessor):
    """
    Sends the generated prompt to the configured
    AI provider and stores the raw response.
    """

    stage_id = "AI"

    name = "AI Processor"

    description = "Generates the AI response."

    def __init__(self):

        self.provider = ProviderFactory().create()

    def execute(
        self,
        context: PipelineContextModel
    ) -> PipelineContextModel:

        start_time = time.time()

        context.raw_response = self.provider.generate(
            context.prompt
        )

        context.provider = type(self.provider).__name__

        context.execution_time_ms = int(
            (time.time() - start_time) * 1000
        )

        return context
        