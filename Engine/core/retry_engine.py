"""
Question Factory OS
Retry Engine
"""

from Engine.ai.provider_factory import ProviderFactory
from Engine.ai.repair_prompt_builder import RepairPromptBuilder
from Engine.ai.response_parser import ResponseParser


class RetryEngine:
    def __init__(self) -> None:
        self.builder = RepairPromptBuilder()
        self.provider = ProviderFactory.create()
        self.parser = ResponseParser()

    def repair(self, question, validation):
        prompt = self.builder.build(question, validation)

        response = self.provider.generate(prompt)

        return self.parser.parse(response)
        