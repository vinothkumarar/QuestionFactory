"""
Question Factory OS
Parse Processor

Milestone : M4
Sprint    : S4
Release   : R1
"""

from ai.response_parser import ResponseParser

from models.pipeline_context_model import PipelineContextModel

from pipeline.processors.pipeline_processor import PipelineProcessor


class ParseProcessor(PipelineProcessor):
    """
    Converts the raw AI response into
    a Python dictionary.
    """

    stage_id = "PARSE"

    name = "Parse Processor"

    description = "Parses AI JSON response."

    def __init__(self):

        self.parser = ResponseParser()

    def execute(self, context: PipelineContextModel) -> PipelineContextModel:

        context.parsed_response = self.parser.parse(context.raw_response)

        return context
