"""
Question Factory OS
Generation Engine

Coordinates prompt building and AI generation.
"""

from Engine.ai.mock_provider import MockProvider
from Engine.ai.prompt_builder import PromptBuilder


class GenerationEngine:
    def __init__(self) -> None:
        self.prompt_builder = PromptBuilder()

        # Temporary provider
        self.provider = MockProvider()

    def generate(self, question: dict):
        prompt = self.prompt_builder.build(question)

        response = self.provider.generate(prompt)

        return response
        