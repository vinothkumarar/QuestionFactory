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

from functools import cached_property

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
        

        #
        # Manufacturing Services
        #

        
        
       
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
            "ai_engine": "ai_engine" in self.__dict__,
            "ai_job_builder": "ai_job_builder" in self.__dict__,
            "factory_orchestrator": (
                "factory_orchestrator" in self.__dict__
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

    # ---------------------------------------------------------
    # Lazy Construction
    # ---------------------------------------------------------

    @cached_property
    def ai_job_builder(self) -> AIJobBuilder:
        """
        Lazily construct the shared AIJobBuilder.
        """

        self._logger.info(
            "Creating AIJobBuilder."
        )

        return AIJobBuilder()

    @cached_property
    def ai_engine(self) -> AIEngine:
        """
        Lazily construct the shared AIEngine.
        """

        self._logger.info(
            "Creating AIEngine."
        )

        return AIEngine(
            ai_client=self.ai_client,
            prompt_builder=self.prompt_builder,
            response_parser=self.response_parser,
        )

    @cached_property
    def factory_orchestrator(self) -> FactoryOrchestrator:
        """
        Lazily construct the shared FactoryOrchestrator.
        """

        self._logger.info(
            "Creating FactoryOrchestrator."
        )

        return FactoryOrchestrator(
            ai_engine=self.ai_engine,
            prompt_builder=self.prompt_builder,
            response_parser=self.response_parser,
        )


__all__ = [
    "ServiceContainer",
]

    

