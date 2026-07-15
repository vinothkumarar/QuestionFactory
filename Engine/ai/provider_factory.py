"""
Question Factory OS
Provider Factory
"""

from core.config_manager import ConfigManager
from ai.mock_provider import MockProvider


class ProviderFactory:

    @staticmethod
    def create():

        config = ConfigManager().load()

        provider = config["provider"]

        if provider == "mock":
            return MockProvider()

        if provider == "openai":
            from ai.openai_provider import OpenAIProvider

            return OpenAIProvider()

        raise ValueError(f"Unsupported provider: {provider}")
