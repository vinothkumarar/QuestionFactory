"""
Question Factory OS
Retry Engine
"""

from ai.repair_prompt_builder import RepairPromptBuilder
from ai.provider_factory import ProviderFactory
from ai.response_parser import ResponseParser


class RetryEngine:

    def __init__(self):

        self.builder = RepairPromptBuilder()

        self.provider = ProviderFactory.create()

        self.parser = ResponseParser()

    def repair(
        self,
        question,
        validation
    ):

        prompt = self.builder.build(
            question,
            validation
        )

        response = self.provider.generate(
            prompt
        )

        return self.parser.parse(
            response
        )
        