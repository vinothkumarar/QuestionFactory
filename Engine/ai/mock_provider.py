"""
Question Factory OS
Mock AI Provider

Used for local development and testing.
"""

from Engine.ai.provider import AIProvider


class MockProvider(AIProvider):
    def generate(self, prompt: str) -> str:
        return f"MOCK RESPONSE:\n\n{prompt}"
        