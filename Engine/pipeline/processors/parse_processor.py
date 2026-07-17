"""
Question Factory OS
Parse Processor

Milestone : M4
Sprint    : S4
Release   : R1
"""

from __future__ import annotations

from Engine.ai.response_parser import ResponseParser
from Engine.models.pipeline_context_model import PipelineContextModel

from .pipeline_processor import PipelineProcessor


class ParseProcessor(PipelineProcessor):
    """
    Pipeline stage responsible for converting the raw AI
    response into a structured Python object suitable for
    downstream processing.

    The parsed response is stored in the shared pipeline
    context for subsequent merge and validation stages.
    """

    stage_id: str = "PARSE"

    name: str = "Parse Processor"

    description: str = "Parses AI JSON response."

    def __init__(self) -> None:
        self._parser = ResponseParser()

    def execute(
        self,
        context: PipelineContextModel,
    ) -> PipelineContextModel:
        """
        Parse the raw AI response into a structured
        representation.
        """

        
        if context.raw_response is None:
            raise RuntimeError(
                "AI response has not been generated."
            )

        context.parsed_response = self._parser.parse(
            context.raw_response,
        )

        return context