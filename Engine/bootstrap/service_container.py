"""
Question Factory OS v2.1

Service Container

Application composition root.

Responsible for constructing and wiring the
complete Question Factory dependency graph.
"""

from __future__ import annotations

import logging
import os

from functools import cached_property

from Engine.factory.ai.ai_client import AIClient
from Engine.factory.ai.ai_engine import AIEngine

from Engine.factory.ai.clients.openai_client import (
    OpenAIClient,
)

from Engine.factory.ai.prompt_builder import (
    PromptBuilder,
)

from Engine.factory.ai.prompt_templates import (
    create_prompt_registry,
)

from Engine.factory.ai.response_parser import (
    ResponseParser,
    create_response_parser,
)

from Engine.factory.generation.ai_job_builder import (
    AIJobBuilder,
)

from Engine.factory.generation.question_generator import (
    QuestionGenerator,
)

from Engine.factory.orchestrator.factory_orchestrator import (
    FactoryOrchestrator,
)

from Engine.factory.repair.repair_engine import (
    RepairEngine,
)

from Engine.factory.validation.question_validator import (
    QuestionValidator,
)

from Engine.factory.orchestrator.batch_adapter import (
    BatchAdapter,
)

from Engine.factory.validation.validation_engine import (
    ValidationEngine,
)

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

        #
        # -----------------------------------------------------
        # Core AI Services
        # -----------------------------------------------------
        #

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:

            raise RuntimeError(
                "OPENAI_API_KEY environment "
                "variable is not configured."
            )

        model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5.5",
        )

        registry = create_prompt_registry()

        self._ai_client: AIClient = OpenAIClient(
            api_key=api_key,
            model=model,
        )

        self._prompt_builder: PromptBuilder = (
            PromptBuilder(
                registry=registry,
            )
        )

        self._response_parser: ResponseParser = (
            create_response_parser()
        )

        self._logger.info(
            "AI subsystem initialized."
        )

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
        Override the default AI client.
        """

        self._ai_client = ai_client

    def register_prompt_builder(
        self,
        prompt_builder: PromptBuilder,
    ) -> None:
        """
        Override the PromptBuilder.
        """

        self._prompt_builder = prompt_builder

    def register_response_parser(
        self,
        response_parser: ResponseParser,
    ) -> None:
        """
        Override the ResponseParser.
        """

        self._response_parser = response_parser

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    @property
    def ai_client(
        self,
    ) -> AIClient:

        return self._ai_client

    @property
    def prompt_builder(
        self,
    ) -> PromptBuilder:

        return self._prompt_builder

    @property
    def response_parser(
        self,
    ) -> ResponseParser:

        return self._response_parser
    # ---------------------------------------------------------
    # Health & Diagnostics
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, bool]:
        """
        Return the health of the container.
        """

        return {
            "ai_client": self._ai_client is not None,
            "prompt_builder": (
                self._prompt_builder is not None
            ),
            "response_parser": (
                self._response_parser is not None
            ),
            "ai_engine": (
                "ai_engine" in self.__dict__
            ),
            "ai_job_builder": (
                "ai_job_builder" in self.__dict__
            ),
            "factory_orchestrator": (
                "factory_orchestrator"
                in self.__dict__
            ),
            "question_generator": (
                "question_generator"
                in self.__dict__
            ),
        }

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Container diagnostics.
        """

        return {
            "component": "ServiceContainer",
            "health": self.health(),
        }

    def __repr__(
        self,
    ) -> str:

        return "ServiceContainer()"

    def __str__(
        self,
    ) -> str:

        return (
            "Question Factory "
            "ServiceContainer"
        )

    # ---------------------------------------------------------
    # Lazy Construction
    # ---------------------------------------------------------

    @cached_property
    def ai_job_builder(
        self,
    ) -> AIJobBuilder:
        """
        Shared AIJobBuilder.
        """

        self._logger.info(
            "Creating AIJobBuilder."
        )

        return AIJobBuilder()

    @cached_property
    def ai_engine(
        self,
    ) -> AIEngine:
        """
        Shared AIEngine.
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
    def factory_orchestrator(
        self,
    ) -> FactoryOrchestrator:
        """
        Shared FactoryOrchestrator.
        """

        self._logger.info(
            "Creating FactoryOrchestrator."
        )

        validation_engine = ValidationEngine(
            validator=QuestionValidator(),
        )

        repair_engine = RepairEngine()

        batch_adapter = BatchAdapter()

        return FactoryOrchestrator(
            ai_engine=self.ai_engine,
            validation_engine=validation_engine,
            repair_engine=repair_engine,
            batch_adapter=batch_adapter,
        )

    @cached_property
    def question_generator(
        self,
    ) -> QuestionGenerator:
        """
        Shared QuestionGenerator.
        """

        self._logger.info(
            "Creating QuestionGenerator."
        )

        return QuestionGenerator(
            ai_job_builder=self.ai_job_builder,
            orchestrator=self.factory_orchestrator,
        )


__all__ = [
    "ServiceContainer",
]