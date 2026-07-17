"""
Question Factory OS v2.1

Service Container

Application composition root.

Responsible for constructing and wiring the
complete Question Factory dependency graph.
"""

from __future__ import annotations

from Engine.factory.ai.ai_client import AIClient
from Engine.factory.ai.ai_engine import AIEngine
from Engine.factory.ai.prompt_builder import PromptBuilder
from Engine.factory.ai.response_parser import ResponseParser

from Engine.factory.generation.ai_job_builder import AIJobBuilder

from Engine.factory.orchestrator.factory_orchestrator import (
    FactoryOrchestrator,
)

import logging

LOGGER = logging.getLogger(__name__)


class ServiceContainer:
    """
    Application composition root.

    Owns creation of all shared services.
    """

    def __init__(self) -> None:

        self._logger = LOGGER

        self._logger.info(
            "Initializing ServiceContainer."
        )
            # Core AI Services
            #

        self._ai_client: AIClient | None = None
        self._prompt_builder: PromptBuilder | None = None
        self._response_parser: ResponseParser | None = None
        self._ai_engine: AIEngine | None = None

        #
        # Manufacturing Services
        #

        self._ai_job_builder: AIJobBuilder | None = None
        self._factory_orchestrator: FactoryOrchestrator | None = None
       
    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register_ai_client(
        self,
        ai_client: AIClient,
    ) -> None:
        """
        Register the AI provider implementation.
        """

        self._ai_client = ai_client

    def register_prompt_builder(
        self,
        prompt_builder: PromptBuilder,
    ) -> None:
        """
        Register the PromptBuilder.
        """

        self._prompt_builder = prompt_builder

    def register_response_parser(
        self,
        response_parser: ResponseParser,
    ) -> None:
        """
        Register the ResponseParser.
        """

        self._response_parser = response_parser

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    @property
    def ai_client(self) -> AIClient:
        """
        Return the configured AI client.
        """

        if self._ai_client is None:
            raise RuntimeError(
                "AIClient has not been registered."
            )

        return self._ai_client

    @property
    def prompt_builder(self) -> PromptBuilder:
        """
        Return the configured PromptBuilder.
        """

        if self._prompt_builder is None:
            raise RuntimeError(
                "PromptBuilder has not been registered."
            )

        return self._prompt_builder

    @property
    def response_parser(self) -> ResponseParser:
        """
        Return the configured ResponseParser.
        """

        if self._response_parser is None:
            raise RuntimeError(
                "ResponseParser has not been registered."
            )

        return self._response_parser

    # ---------------------------------------------------------
    # Health & Diagnostics
    # ---------------------------------------------------------

    def health(self) -> dict[str, bool]:
        """
        Return the registration status of core services.
        """

        return {
            "ai_client": self._ai_client is not None,
            "prompt_builder": self._prompt_builder is not None,
            "response_parser": self._response_parser is not None,
            "ai_engine": self._ai_engine is not None,
            "ai_job_builder": self._ai_job_builder is not None,
            "factory_orchestrator": (
                self._factory_orchestrator is not None
            ),
        }

    def diagnostics(self) -> dict[str, object]:
        """
        Return ServiceContainer diagnostics.
        """

        return {
            "component": "ServiceContainer",
            "health": self.health(),
        }

    def __repr__(self) -> str:
        return "ServiceContainer()"

    def __str__(self) -> str:
        return "Question Factory ServiceContainer"


__all__ = [
    "ServiceContainer",
]
