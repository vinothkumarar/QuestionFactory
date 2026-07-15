"""
Question Factory OS
Generation Engine

Coordinates prompt building and AI generation.
"""

from ai.prompt_builder import PromptBuilder
from ai.mock_provider import MockProvider


class GenerationEngine:

    def __init__(self):

        self.prompt_builder = PromptBuilder()

        # Temporary provider
        self.provider = MockProvider()

    def generate(self, question: dict):

        prompt = self.prompt_builder.build(question)

        response = self.provider.generate(prompt)

        return response
