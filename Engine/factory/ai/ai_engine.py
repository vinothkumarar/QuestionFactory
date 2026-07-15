"""
Question Factory OS v2.1
------------------------

AI Engine

Central orchestration engine for all AI operations.

Responsibilities
----------------
• Accept AIJob requests
• Build PromptPackage objects
• Execute AI requests
• Parse AI responses
• Coordinate provider-agnostic execution

The AI Engine is the boundary between the
Manufacturing Layer and AI providers.

Author:
Question Factory OS
"""

from __future__ import annotations

import logging
from typing import Any
from typing import Optional

from factory.ai.ai_client import AIClient
from factory.ai.models.ai_job import AIJob
from factory.ai.models.prompt_package import PromptPackage
from factory.ai.prompt_builder import PromptBuilder
from factory.ai.response_parser import ResponseParser
from factory.ai.ai_client import AIRequest


logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# AI Engine
# ----------------------------------------------------------------------


class AIEngine:
    """
    Central AI orchestration engine.

    The engine coordinates prompt construction,
    provider execution and response parsing.
    """

    def __init__(
        self,
        *,
        ai_client: AIClient,
        prompt_builder: PromptBuilder,
        response_parser: ResponseParser,
    ) -> None:
        """
        Parameters
        ----------
        ai_client:
            Provider implementation.

        prompt_builder:
            Builds PromptPackage instances.

        response_parser:
            Parses provider responses.
        """

        self._client = ai_client

        self._prompt_builder = prompt_builder

        self._response_parser = response_parser

        logger.info(
            "AIEngine initialized."
        )
    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def execute(
        self,
        job: AIJob,
    ) -> Any:
        """
        Execute an AI job.

        Workflow
        --------
        AIJob
            ↓
        PromptBuilder
            ↓
        PromptPackage
            ↓
        AI Provider
            ↓
        ResponseParser
        """

        job.validate()

        package = self._prompt_builder.build(
            job=job,
        )

        return self.execute_package(package)

    def execute_package(
        self,
        package: PromptPackage,
    ) -> Any:
        """
        Execute an already prepared PromptPackage.

        This method enables prompt replay,
        retries and cached execution.
        """

        self._validate_package(package)

        logger.info(
            "Executing prompt package '%s'.",
            package.template_id,
        )

        raw_response = self._execute_provider(
            package,
        )

        return self._parse_response(
            package,
            raw_response,
        )

    # ------------------------------------------------------------------
    # Internal Execution
    # ------------------------------------------------------------------
                
    def _execute_provider(
        self,
        package: PromptPackage,
    ) -> Any:
        """
        Execute the request using the configured
        AI provider.
        """

        request = AIRequest(
            prompt=package.prompt,
            system_prompt=package.system_prompt,
     )

        return self._client.execute(
            request,
    )

    
    def _parse_response(
        self,
        package: PromptPackage,
        raw_response: Any,
    ) -> Any:
        """
        Parse the provider response.
        """

        _ = package

        return self._response_parser.parse(
            raw_response,
        )
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_package(
        self,
        package: PromptPackage,
    ) -> None:
        """
        Validate a PromptPackage before execution.
        """

        if not package.is_valid:
            raise ValueError(
                "PromptPackage is invalid."
            )

        if not package.prompt.strip():
            raise ValueError(
                "PromptPackage contains an empty prompt."
            )

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate AI Engine configuration.
        """

        if self._client is None:
            raise ValueError(
                "AI client has not been configured."
            )

        if self._prompt_builder is None:
            raise ValueError(
                "PromptBuilder has not been configured."
            )

        if self._response_parser is None:
            raise ValueError(
                "ResponseParser has not been configured."
            )

    @property
    def is_ready(
        self,
    ) -> bool:
        """
        Return True if the engine is correctly configured.
        """

        try:
            self.validate_configuration()
            return True

        except ValueError:
            return False

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return AI Engine health information.
        """

        return {
            "component": "AIEngine",
            "status": (
                "READY"
                if self.is_ready
                else "NOT_READY"
            ),
            "client": (
                self._client.__class__.__name__
            ),
            "prompt_builder": (
                self._prompt_builder.__class__.__name__
            ),
            "response_parser": (
                self._response_parser.__class__.__name__
            ),
        }

    # ------------------------------------------------------------------
    # Capabilities
    # ------------------------------------------------------------------

    def capabilities(
        self,
    ) -> dict[str, bool]:
        """
        Return supported engine capabilities.
        """

        return {
            "prompt_building": True,
            "provider_execution": True,
            "response_parsing": True,
            "configuration_validation": True,
            "prompt_package_execution": True,
        }

    # ------------------------------------------------------------------
    # Execution Information
    # ------------------------------------------------------------------

    def execution_information(
        self,
    ) -> dict[str, Any]:
        """
        Return engine execution information.
        """

        return {
            "component": "AIEngine",
            "execution_mode": "SYNCHRONOUS",
            "framework_version": "2.1.0",
            "provider": (
                self._client.__class__.__name__
            ),
        }
    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return AI Engine statistics.

        Runtime counters will be introduced in a future
        release. For now, this method reports the engine
        configuration and component status.
        """

        return {
            "provider": self._client.__class__.__name__,
            "prompt_builder": (
                self._prompt_builder.__class__.__name__
            ),
            "response_parser": (
                self._response_parser.__class__.__name__
            ),
            "ready": self.is_ready,
        }

    # ------------------------------------------------------------------
    # Provider Information
    # ------------------------------------------------------------------

    def provider_information(
        self,
    ) -> dict[str, Any]:
        """
        Return information about the configured AI provider.
        """

        return {
            "provider": (
                self._client.__class__.__name__
            ),
            "provider_type": (
                type(self._client).__name__
            ),
        }

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return comprehensive engine diagnostics.
        """

        return {
            "health": self.health(),
            "capabilities": self.capabilities(),
            "execution": (
                self.execution_information()
            ),
            "statistics": self.statistics(),
            "provider": (
                self.provider_information()
            ),
        }

    # ------------------------------------------------------------------
    # Runtime Summary
    # ------------------------------------------------------------------

    def summary(
        self,
    ) -> dict[str, Any]:
        """
        Return a concise summary suitable for
        runtime dashboards and logging.
        """

        return {
            "provider": (
                self._client.__class__.__name__
            ),
            "ready": self.is_ready,
            "execution_mode": "SYNCHRONOUS",
            "framework_version": "2.1.0",
        }

    # ------------------------------------------------------------------
    # Supported Operations
    # ------------------------------------------------------------------

    def supports_execution(
        self,
    ) -> bool:
        """
        Return True if the engine is capable of
        executing AI jobs.
        """

        return self.is_ready

    def supports_prompt_packages(
        self,
    ) -> bool:
        """
        Return True if PromptPackage execution
        is supported.
        """

        return True
    # ------------------------------------------------------------------
    # Runtime Configuration
    # ------------------------------------------------------------------

    def set_client(
        self,
        client: AIClient,
    ) -> None:
        """
        Replace the configured AI client.
        """

        self._client = client

        logger.info(
            "AI provider updated to '%s'.",
            client.__class__.__name__,
        )

    def set_prompt_builder(
        self,
        prompt_builder: PromptBuilder,
    ) -> None:
        """
        Replace the configured PromptBuilder.
        """

        self._prompt_builder = prompt_builder

        logger.info(
            "PromptBuilder updated."
        )

    def set_response_parser(
        self,
        response_parser: ResponseParser,
    ) -> None:
        """
        Replace the configured ResponseParser.
        """

        self._response_parser = response_parser

        logger.info(
            "ResponseParser updated."
        )

    # ------------------------------------------------------------------
    # Runtime Utilities
    # ------------------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset runtime state.

        Reserved for future execution statistics,
        retry queues and runtime metrics.
        """

        logger.info(
            "AIEngine runtime reset."
        )

    def configuration(
        self,
    ) -> dict[str, Any]:
        """
        Return the current runtime configuration.
        """

        return {
            "provider": (
                self._client.__class__.__name__
            ),
            "prompt_builder": (
                self._prompt_builder.__class__.__name__
            ),
            "response_parser": (
                self._response_parser.__class__.__name__
            ),
        }

    # ------------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------------

    @property
    def provider_name(
        self,
    ) -> str:
        """
        Return the configured provider name.
        """

        return self._client.__class__.__name__

    @property
    def builder_name(
        self,
    ) -> str:
        """
        Return the configured PromptBuilder name.
        """

        return (
            self._prompt_builder.__class__.__name__
        )

    @property
    def parser_name(
        self,
    ) -> str:
        """
        Return the configured ResponseParser name.
        """

        return (
            self._response_parser.__class__.__name__
        )

    # ------------------------------------------------------------------
    # Engine Summary
    # ------------------------------------------------------------------

    def engine_summary(
        self,
    ) -> dict[str, Any]:
        """
        Return a compact engine summary.
        """

        return {
            "provider": self.provider_name,
            "builder": self.builder_name,
            "parser": self.parser_name,
            "ready": self.is_ready,
        }
    

        