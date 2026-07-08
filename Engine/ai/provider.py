"""
Question Factory OS
AI Provider

Base interface for all AI providers.
"""

from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate AI response.

        Returns:
            str
        """
        pass
        