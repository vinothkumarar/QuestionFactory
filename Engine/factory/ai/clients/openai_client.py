"""
Question Factory OS v2.1
------------------------

OpenAI Client

Enterprise implementation of the provider-agnostic
AIClient using the OpenAI Responses API.

Responsibilities
----------------
• Request normalization
• OpenAI SDK interaction
• Response normalization
• Streaming support
• Health monitoring
• Model discovery
• Token estimation
• Diagnostics
• Telemetry

Author
------
Question Factory OS Team
"""

from __future__ import annotations

import logging
import time

from collections.abc import Iterator
from typing import Any
from typing import Optional
from typing import cast

from openai import OpenAI

from factory.ai.ai_client import (
    AICapability,
    AIClient,
    AIClientStatus,
    AIHealthResult,
    AIModelInfo,
    AIProvider,
    AIRequest,
    AIResponse,
)

logger = logging.getLogger(__name__)


class OpenAIClient(AIClient):
    """
    OpenAI implementation of AIClient.

    This class encapsulates all OpenAI SDK
    interactions. The remainder of Question
    Factory OS communicates only with the
    provider-independent AIClient interface.
    """

    DEFAULT_MODEL = "gpt-5.5"

    def __init__(
        self,
        api_key: str,
        *,
        model: str = DEFAULT_MODEL,
        base_url: Optional[str] = None,
        organization: Optional[str] = None,
        timeout: float = 120.0,
    ) -> None:
        """
        Parameters
        ----------
        api_key:
            OpenAI API key.

        model:
            Default model.

        base_url:
            Optional compatible endpoint.

        organization:
            Optional organization id.

        timeout:
            HTTP timeout.
        """

        super().__init__(
            AIProvider.OPENAI
        )

        self._default_model = model

        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            organization=organization,
            timeout=timeout,
        )

        logger.info(
            "OpenAIClient initialized "
            "(model=%s).",
            model,
        )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def initialize(
        self,
    ) -> None:
        """
        Initialize provider resources.
        """

        logger.debug(
            "OpenAI provider initialized."
        )

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown provider resources.
        """

        logger.debug(
            "OpenAI provider shutdown."
        )

    # ---------------------------------------------------------
    # Provider Information
    # ---------------------------------------------------------

    def default_model(
        self,
    ) -> str:
        """
        Return configured default model.
        """

        return self._default_model

    @property
    def client(
        self,
    ) -> OpenAI:
        """
        Return underlying SDK client.
        """

        return self._client

    @property
    def configured_model(
        self,
    ) -> str:
        """
        Return configured default model.
        """

        return self._default_model

    def set_default_model(
        self,
        model: str,
    ) -> None:
        """
        Update default model.
        """

        model = model.strip()

        if not model:

            raise ValueError(
                "Model name cannot be empty."
            )

        logger.info(
            "Changing model '%s' -> '%s'.",
            self._default_model,
            model,
        )

        self._default_model = model
    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(
        self,
    ) -> list[AICapability]:
        """
        Return provider capabilities.
        """

        return [
            AICapability.CHAT,
            AICapability.STREAMING,
            AICapability.JSON_MODE,
            AICapability.FUNCTION_CALLING,
            AICapability.SYSTEM_PROMPTS,
            AICapability.TEMPERATURE,
            AICapability.TOKEN_ESTIMATION,
            AICapability.VISION,
            AICapability.REASONING,
            AICapability.STRUCTURED_OUTPUT,
        ]

    # ---------------------------------------------------------
    # Model Discovery
    # ---------------------------------------------------------

    def list_models(
        self,
    ) -> list[AIModelInfo]:
        """
        Return available OpenAI models.

        If discovery fails, gracefully fall
        back to the configured default model.
        """

        models: list[AIModelInfo] = []

        try:

            response = self._client.models.list()

            for model in response.data:

                models.append(
                    AIModelInfo(
                        provider=AIProvider.OPENAI,
                        model_name=model.id,
                        supports_streaming=True,
                        supports_json=True,
                        supports_functions=True,
                        supports_vision=True,
                        metadata={},
                    )
                )

        except Exception:

            logger.exception(
                "Unable to retrieve model list."
            )

            models.append(
                AIModelInfo(
                    provider=AIProvider.OPENAI,
                    model_name=self.default_model(),
                    supports_streaming=True,
                    supports_json=True,
                    supports_functions=True,
                    supports_vision=True,
                    metadata={
                        "fallback": True,
                    },
                )
            )

        return models

    def supports_model(
        self,
        model: str,
    ) -> bool:
        """
        Determine whether a model is
        available.
        """

        try:

            return any(
                item.model_name == model
                for item in self.list_models()
            )

        except Exception:

            logger.exception(
                "Unable to verify model '%s'.",
                model,
            )

            return False

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health_check(
        self,
    ) -> AIHealthResult:
        """
        Perform a lightweight provider
        health check.
        """

        started = time.perf_counter()

        try:

            self._client.models.list()

            latency = (
                time.perf_counter()
                - started
            ) * 1000

            return AIHealthResult(
                healthy=True,
                provider=AIProvider.OPENAI,
                status=AIClientStatus.READY,
                latency_ms=round(
                    latency,
                    2,
                ),
                message="Provider reachable.",
            )

        except Exception as ex:

            latency = (
                time.perf_counter()
                - started
            ) * 1000

            logger.exception(
                "Health check failed."
            )

            return AIHealthResult(
                healthy=False,
                provider=AIProvider.OPENAI,
                status=AIClientStatus.UNAVAILABLE,
                latency_ms=round(
                    latency,
                    2,
                ),
                message=str(ex),
            )

    # ---------------------------------------------------------
    # Token Utilities
    # ---------------------------------------------------------

    def estimate_tokens(
        self,
        text: str,
    ) -> int:
        """
        Estimate token count.

        This provides a lightweight
        approximation. Future versions may
        integrate tiktoken.
        """

        if not text:
            return 0

        return max(
            1,
            len(text) // 4,
        )

    def max_context_window(
        self,
        model: Optional[str] = None,
    ) -> Optional[int]:
        """
        Return the supported context
        window.
        """

        _ = model

        return 128_000
    # ---------------------------------------------------------
    # Core Generation
    # ---------------------------------------------------------

    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute a non-streaming request.
        """

        request = self.before_request(
            request
        )

        self.log_request(
            request
        )

        started = time.perf_counter()

        try:

            response = self._execute_response_request(
                request
            )

            result = self._map_response(
                response=response,
                request=request,
            )

            result.response_time_ms = round(
                (
                    time.perf_counter()
                    - started
                )
                * 1000,
                2,
            )

            self.log_response(
                result
            )

            return self.after_response(
                result
            )

        except Exception as ex:

            logger.exception(
                "OpenAI request execution failed."
            )

            raise self.map_exception(
                ex
            ) from ex

    # ---------------------------------------------------------
    # Streaming
    # ---------------------------------------------------------

    def stream(
        self,
        request: AIRequest,
    ) -> Iterator[Any]:
        """
        Execute a streaming request.

        Yields provider SDK events.
        """

        request = self.before_request(
            request
        )

        self.log_request(
            request
        )

        input_payload = self._build_input(
            request
        )

        with self._client.responses.stream(
            model=self.normalize_model(
                request.model
            ),
            input=cast(
                Any,
                input_payload,
            ),
            temperature=self.normalize_temperature(
                request.temperature
            ),
            max_output_tokens=self.normalize_max_tokens(
                request.max_tokens
            ),
        ) as stream:

            for event in stream:

                yield event

    # ---------------------------------------------------------
    # Internal Execution
    # ---------------------------------------------------------

    def _execute_response_request(
        self,
        request: AIRequest,
    ) -> Any:
        """
        Execute a Responses API request.
        """

        input_payload = self._build_input(
            request
        )

        return self._client.responses.create(
            model=self.normalize_model(
                request.model
            ),
            input=cast(
                Any,
                input_payload,
            ),
            temperature=self.normalize_temperature(
                request.temperature
            ),
            max_output_tokens=self.normalize_max_tokens(
                request.max_tokens
            ),
        )

    # ---------------------------------------------------------
    # Request Validation
    # ---------------------------------------------------------

    def validate_request(
        self,
        request: AIRequest,
    ) -> None:
        """
        Validate an OpenAI request.
        """

        super().validate_request(
            request
        )

        if (
            request.model is not None
            and not request.model.strip()
        ):
            raise ValueError(
                "Model name cannot be empty."
            )

        if (
            request.temperature
            > 2.0
        ):
            raise ValueError(
                "Temperature cannot exceed 2.0."
            )

        if (
            request.temperature
            < 0.0
        ):
            raise ValueError(
                "Temperature cannot be negative."
            )

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_request(
        self,
        request: AIRequest,
    ) -> AIRequest:
        """
        Provider-specific preprocessing.
        """

        request = super().before_request(
            request
        )

        return request

    def after_response(
        self,
        response: AIResponse,
    ) -> AIResponse:
        """
        Provider-specific postprocessing.
        """

        return super().after_response(
            response
        )
    # ---------------------------------------------------------
    # Request Builder
    # ---------------------------------------------------------

    def _build_input(
        self,
        request: AIRequest,
    ) -> list[dict[str, Any]]:
        """
        Build an OpenAI Responses API input payload.
        """

        messages: list[dict[str, Any]] = []

        if request.has_system_prompt:

            messages.append(
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": request.system_prompt,
                        }
                    ],
                }
            )

        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": request.prompt,
                    }
                ],
            }
        )

        return messages

    # ---------------------------------------------------------
    # Response Mapping
    # ---------------------------------------------------------

    def _map_response(
        self,
        *,
        response: Any,
        request: AIRequest,
    ) -> AIResponse:
        """
        Convert an OpenAI Responses API response
        into a provider-independent AIResponse.
        """

        content = self._extract_text(
            response
        )

        usage = getattr(
            response,
            "usage",
            None,
        )

        prompt_tokens: Optional[int] = None
        completion_tokens: Optional[int] = None
        total_tokens: Optional[int] = None

        if usage is not None:

            prompt_tokens = getattr(
                usage,
                "input_tokens",
                None,
            )

            completion_tokens = getattr(
                usage,
                "output_tokens",
                None,
            )

            total_tokens = getattr(
                usage,
                "total_tokens",
                None,
            )

        finish_reason = getattr(
            response,
            "status",
            None,
        )

        return AIResponse(
            success=True,
            provider=AIProvider.OPENAI,
            model=self.normalize_model(
                request.model
            ),
            content=content,
            finish_reason=finish_reason,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            raw_response=response,
            metadata={
                "response_id": getattr(
                    response,
                    "id",
                    None,
                ),
            },
        )

    # ---------------------------------------------------------
    # Response Extraction
    # ---------------------------------------------------------

    def _extract_text(
        self,
        response: Any,
    ) -> str:
        """
        Extract the generated text from the
        OpenAI Responses API response.
        """

        text = getattr(
            response,
            "output_text",
            None,
        )

        if isinstance(
            text,
            str,
        ):
            return text

        if text is not None:
            return str(text)

        output = getattr(
            response,
            "output",
            None,
        )

        if not output:
            return ""

        fragments: list[str] = []

        for item in output:

            contents = getattr(
                item,
                "content",
                [],
            )

            for content in contents:

                value = getattr(
                    content,
                    "text",
                    None,
                )

                if value:
                    fragments.append(
                        value
                    )

        return "\n".join(
            fragments
        )

    # ---------------------------------------------------------
    # Response Validation
    # ---------------------------------------------------------

    def _validate_response(
        self,
        response: Any,
    ) -> None:
        """
        Validate the provider response.
        """

        if response is None:

            raise RuntimeError(
                "OpenAI returned no response."
            )

        if not hasattr(
            response,
            "output",
        ) and not hasattr(
            response,
            "output_text",
        ):
            raise RuntimeError(
                "Invalid OpenAI response."
            )
    # ---------------------------------------------------------
    # Retry Policy
    # ---------------------------------------------------------

    def should_retry(
        self,
        exception: Exception,
        attempt: int,
    ) -> bool:
        """
        Determine whether a failed request should
        be retried.

        Conservative retry policy:

        • Maximum three attempts
        • Retry transient failures only
        """

        if attempt >= self.max_retry_attempts():
            return False

        retryable = (
            TimeoutError,
            ConnectionError,
        )

        return isinstance(
            exception,
            retryable,
        )

    def max_retry_attempts(
        self,
    ) -> int:
        """
        Maximum retry attempts.
        """

        return 3

    # ---------------------------------------------------------
    # Configuration Validation
    # ---------------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate provider configuration.
        """

        if not self._default_model.strip():

            raise ValueError(
                "Default model cannot be empty."
            )

        self.ensure_available()

    # ---------------------------------------------------------
    # Exception Mapping
    # ---------------------------------------------------------

    def map_exception(
        self,
        exception: Exception,
    ) -> RuntimeError:
        """
        Convert provider-specific exceptions
        into provider-independent exceptions.
        """

        logger.exception(
            "OpenAI provider exception."
        )

        return RuntimeError(
            f"OpenAI request failed: "
            f"{exception}"
        )

    # ---------------------------------------------------------
    # Logging Helpers
    # ---------------------------------------------------------

    def log_request(
        self,
        request: AIRequest,
    ) -> None:
        """
        Log request metadata.

        Prompt contents are intentionally
        excluded from logs.
        """

        logger.debug(
            "OpenAI request "
            "(model=%s, stream=%s, "
            "temperature=%s, "
            "max_tokens=%s)",
            self.normalize_model(
                request.model
            ),
            request.stream,
            request.temperature,
            request.max_tokens,
        )

    def log_response(
        self,
        response: AIResponse,
    ) -> None:
        """
        Log response metadata.
        """

        logger.debug(
            "OpenAI response "
            "(success=%s, "
            "tokens=%s, "
            "finish_reason=%s)",
            response.success,
            response.total_tokens,
            response.finish_reason,
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return provider diagnostics.
        """

        diagnostics = super().diagnostics()

        diagnostics.update(
            {
                "configured_model":
                    self._default_model,
                "sdk_client":
                    self._client.__class__.__name__,
                "responses_api": True,
            }
        )

        return diagnostics

    # ---------------------------------------------------------
    # Provider Summary
    # ---------------------------------------------------------

    def provider_summary(
        self,
    ) -> dict[str, Any]:
        """
        Return an OpenAI-specific summary.
        """

        summary = super().provider_summary()

        summary.update(
            {
                "configured_model":
                    self._default_model,
                "responses_api": True,
            }
        )

        return summary

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    def info(
        self,
    ) -> dict[str, Any]:
        """
        Return detailed provider information.
        """

        information = super().info()

        information.update(
            {
                "configured_model":
                    self._default_model,
                "sdk":
                    self._client.__class__.__name__,
                "responses_api": True,
            }
        )

        return information
    # ---------------------------------------------------------
    # Usage Helpers
    # ---------------------------------------------------------

    def extract_text(
        self,
        response: AIResponse,
    ) -> str:
        """
        Return the normalized response text.
        """

        return response.content

    def usage_summary(
        self,
        response: AIResponse,
    ) -> dict[str, Optional[int]]:
        """
        Return normalized token usage information.
        """

        return {
            "prompt_tokens": response.prompt_tokens,
            "completion_tokens": response.completion_tokens,
            "total_tokens": response.total_tokens,
        }

    # ---------------------------------------------------------
    # SDK Information
    # ---------------------------------------------------------

    def sdk_version(
        self,
    ) -> Optional[str]:
        """
        Return the installed OpenAI SDK version.

        Returns
        -------
        Optional[str]
            Installed version or None.
        """

        try:

            from importlib.metadata import version

            return version("openai")

        except Exception:

            logger.debug(
                "Unable to determine OpenAI SDK version."
            )

            return None

    # ---------------------------------------------------------
    # Model Utilities
    # ---------------------------------------------------------

    

    def reset_default_model(
        self,
    ) -> None:
        """
        Reset to the library default model.
        """

        self._default_model = self.DEFAULT_MODEL

    # ---------------------------------------------------------
    # Provider Utilities
    # ---------------------------------------------------------

    def supports_streaming(
        self,
    ) -> bool:
        """
        Return True if streaming is supported.
        """

        return True

    def supports_json_mode(
        self,
    ) -> bool:
        """
        Return True if structured JSON output
        is supported.
        """

        return True

    def supports_function_calling(
        self,
    ) -> bool:
        """
        Return True if function calling
        is supported.
        """

        return True

    def supports_reasoning(
        self,
    ) -> bool:
        """
        Return True if reasoning models
        are supported.
        """

        return True

    def supports_vision(
        self,
    ) -> bool:
        """
        Return True if vision models
        are supported.
        """

        return True

    # ---------------------------------------------------------
    # Telemetry
    # ---------------------------------------------------------

    def telemetry(
        self,
        request: AIRequest,
        response: AIResponse,
    ) -> dict[str, Any]:
        """
        Produce provider-independent telemetry.
        """

        telemetry = super().telemetry(
            request,
            response,
        )

        telemetry.update(
            {
                "sdk_version": self.sdk_version(),
                "configured_model": self._default_model,
            }
        )

        return telemetry

    # ---------------------------------------------------------
    # Readiness
    # ---------------------------------------------------------

    @property
    def ready(
        self,
    ) -> bool:
        """
        Return True if the provider is
        operational.
        """

        try:

            return self.health_check().healthy

        except Exception:

            return False
    # ---------------------------------------------------------
    # Operational Helpers
    # ---------------------------------------------------------

    def ping(
        self,
    ) -> bool:
        """
        Lightweight connectivity check.

        Returns
        -------
        bool
            True if the provider is reachable.
        """

        try:

            return self.health_check().healthy

        except Exception:

            logger.exception(
                "Provider ping failed."
            )

            return False

    def refresh_models(
        self,
    ) -> list[AIModelInfo]:
        """
        Refresh and return the current model list.

        Future implementations may introduce
        caching. For now this delegates directly
        to model discovery.
        """

        return self.list_models()

    # ---------------------------------------------------------
    # Health Summary
    # ---------------------------------------------------------

    def health_summary(
        self,
    ) -> dict[str, Any]:
        """
        Return a concise health summary.
        """

        health = self.health_check()

        return {
            "provider": self.provider.value,
            "healthy": health.healthy,
            "status": health.status.value,
            "latency_ms": health.latency_ms,
            "message": health.message,
        }

    # ---------------------------------------------------------
    # Configuration Summary
    # ---------------------------------------------------------

    def configuration(
        self,
    ) -> dict[str, Any]:
        """
        Return provider configuration.
        """

        return {
            "provider": self.provider.value,
            "default_model": self._default_model,
            "sdk_version": self.sdk_version(),
            "responses_api": True,
        }

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return provider statistics.

        Reserved for future runtime metrics.
        """

        return {
            "provider": self.provider.value,
            "configured_model": self._default_model,
            "available": self.ready,
            "supports_streaming": True,
            "supports_reasoning": True,
            "supports_vision": True,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"provider='{self.provider.value}', "
            f"model='{self._default_model}')"
        )

    __str__ = __repr__

    # ---------------------------------------------------------
    # Equality
    # ---------------------------------------------------------

    def __eq__(
        self,
        other: object,
    ) -> bool:

        if not isinstance(
            other,
            OpenAIClient,
        ):
            return NotImplemented

        return (
            self._default_model
            == other._default_model
        )

    def __hash__(
        self,
    ) -> int:

        return hash(
            (
                self.provider,
                self._default_model,
            )
        )
    # ---------------------------------------------------------
    # Factory Helpers
    # ---------------------------------------------------------

    @classmethod
    def create(
        cls,
        api_key: str,
        *,
        model: str = DEFAULT_MODEL,
        base_url: Optional[str] = None,
        organization: Optional[str] = None,
        timeout: float = 120.0,
    ) -> "OpenAIClient":
        """
        Factory helper for constructing an
        OpenAIClient.
        """

        return cls(
            api_key=api_key,
            model=model,
            base_url=base_url,
            organization=organization,
            timeout=timeout,
        )

    # ---------------------------------------------------------
    # Close
    # ---------------------------------------------------------

    def close(
        self,
    ) -> None:
        """
        Close the underlying SDK client if
        supported by the installed version.
        """

        close = getattr(
            self._client,
            "close",
            None,
        )

        if callable(close):

            try:

                close()

            except Exception:

                logger.exception(
                    "Failed to close OpenAI client."
                )

    # ---------------------------------------------------------
    # Context Manager Support
    # ---------------------------------------------------------

    def __enter__(
        self,
    ) -> "OpenAIClient":

        self.initialize()

        return self

    def __exit__(
        self,
        exc_type,
        exc,
        traceback,
    ) -> None:

        self.shutdown()

        self.close()


# ---------------------------------------------------------
# Module Exports
# ---------------------------------------------------------

__all__ = [
    "OpenAIClient",
]
