"""
Question Factory OS
Provider Factory
"""

from Engine.ai.mock_provider import MockProvider
from Engine.core.config_manager import ConfigManager


class ProviderFactory:
    @staticmethod
    def create():
        config = ConfigManager().load()

        provider = config["provider"]

        if provider == "mock":
            return MockProvider()

        if provider == "openai":
            from Engine.ai.openai_provider import OpenAIProvider

            return OpenAIProvider()

        raise ValueError(f"Unsupported provider: {provider}")
        