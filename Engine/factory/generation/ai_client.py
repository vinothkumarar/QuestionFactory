"""
Question Factory OS v2.0

AI Client

Responsible for communicating with AI providers.

The AIClient provides a provider-independent interface
for prompt execution.

Business logic is intentionally excluded.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod


# ---------------------------------------------------------
# Provider Interface
# ---------------------------------------------------------

class AIProvider(ABC):
    """
    Base interface for every AI provider.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Provider name.
        """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Execute prompt generation.
        """


# ---------------------------------------------------------
# AI Client
# ---------------------------------------------------------

class AIClient:
    """
    Provider-independent AI client.
    """

    def __init__(
        self,
        provider: AIProvider,
    ):

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self.provider = provider

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Execute prompt generation using
        the configured provider.
        """

        self.logger.info(
            "Using AI provider: %s",
            self.provider.name,
        )

        response = self.provider.generate(
            prompt
        )

        self.logger.info(
            "AI response received."
        )

        return response
            # ---------------------------------------------------------
    # Provider Management
    # ---------------------------------------------------------

    def set_provider(
        self,
        provider: AIProvider,
    ) -> None:
        """
        Replace the active AI provider.
        """

        self.logger.info(
            "Switching AI provider: %s -> %s",
            self.provider.name,
            provider.name,
        )

        self.provider = provider

    def get_provider(self) -> AIProvider:
        """
        Return the active provider.
        """

        return self.provider

    @property
    def provider_name(self) -> str:
        """
        Return the active provider name.
        """

        return self.provider.name

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_prompt(
        self,
        prompt: str,
    ) -> None:
        """
        Validate a prompt before it is sent to
        the AI provider.
        """

        if not isinstance(prompt, str):

            raise TypeError(
                "Prompt must be a string."
            )

        if not prompt.strip():

            raise ValueError(
                "Prompt cannot be empty."
            )

        self.logger.info(
            "Prompt validation successful."
        )

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_generation(
        self,
        prompt: str,
    ) -> None:
        """
        Executed immediately before invoking
        the AI provider.

        Override in derived implementations for
        telemetry, auditing or preprocessing.
        """

        return

    def after_generation(
        self,
        prompt: str,
        response: str,
    ) -> None:
        """
        Executed immediately after receiving
        the AI response.

        Override for metrics, logging or
        downstream integrations.
        """

        return

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    def execute(
        self,
        prompt: str,
    ) -> str:
        """
        Convenience wrapper around generate().
        """

        self.validate_prompt(
            prompt
        )

        self.before_generation(
            prompt
        )

        response = self.generate(
            prompt
        )

        self.after_generation(
            prompt,
            response,
        )

        return response
            # ---------------------------------------------------------
    # Response Validation
    # ---------------------------------------------------------

    def validate_response(
        self,
        response: str,
    ) -> None:
        """
        Validate the AI response.
        """

        if not isinstance(response, str):

            raise TypeError(
                "AI response must be a string."
            )

        if not response.strip():

            raise ValueError(
                "AI response is empty."
            )

        self.logger.info(
            "AI response validation successful."
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        prompt: str,
        response: str,
    ) -> dict:
        """
        Return execution statistics.
        """

        return {
            "provider": self.provider_name,
            "prompt_characters": len(prompt),
            "prompt_words": len(prompt.split()),
            "response_characters": len(response),
            "response_words": len(response.split()),
        }

    def summary(
        self,
        prompt: str,
        response: str,
    ) -> dict:
        """
        Return a concise execution summary.
        """

        stats = self.statistics(
            prompt,
            response,
        )

        return {
            "provider": stats["provider"],
            "prompt_words": stats["prompt_words"],
            "response_words": stats["response_words"],
        }

    def diagnostics(
        self,
        prompt: str,
        response: str,
    ) -> dict:
        """
        Return detailed execution diagnostics.
        """

        return {
            "component": self.__class__.__name__,
            "provider": self.provider_name,
            "summary": self.summary(
                prompt,
                response,
            ),
            "statistics": self.statistics(
                prompt,
                response,
            ),
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    @property
    def version(self) -> str:
        """
        AI Client version.
        """

        return "2.0.0"

    @property
    def component_name(self) -> str:
        """
        Component name.
        """

        return "AI Client"

    def health(self) -> dict:
        """
        Return component health information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "provider": self.provider_name,
            "status": "READY",
        }
            # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(self) -> dict:
        """
        Describe AI Client capabilities.
        """

        return {
            "provider_abstraction": True,
            "provider_switching": True,
            "prompt_validation": True,
            "response_validation": True,
            "lifecycle_hooks": True,
            "diagnostics": True,
            "health_reporting": True,
        }

    def supported_execution_mode(self) -> str:
        """
        Return the execution mode supported by
        this client.
        """

        return "SYNCHRONOUS"

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def create_empty_response(self) -> str:
        """
        Create an empty AI response.

        Useful for testing and fallback scenarios.
        """

        return ""

    def provider_information(self) -> dict:
        """
        Return information about the active provider.
        """

        return {
            "name": self.provider_name,
            "class": self.provider.__class__.__name__,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            "AIClient("
            f"provider='{self.provider_name}', "
            f"version='{self.version}')"
        )

    def __str__(self) -> str:
        return (
            f"{self.component_name} "
            f"[{self.provider_name}]"
        )