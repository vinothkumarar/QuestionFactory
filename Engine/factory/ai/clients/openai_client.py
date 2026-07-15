"""
Question Factory OS v2.1
------------------------

OpenAI Client

Concrete implementation of the provider-agnostic AIClient
interface for OpenAI-compatible APIs.

Responsibilities
----------------
• Request normalization
• OpenAI SDK interaction
• Response normalization
• Health checks
• Model discovery
• Token estimation
• Capability reporting

The rest of Question Factory OS communicates only with the
AIClient abstraction and is unaware of OpenAI SDK details.
"""

from __future__ import annotations

import logging
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from openai import OpenAI

from factory.ai.ai_client import (
    AIClient,
    AIHealthResult,
    AIClientStatus,
    AIModelInfo,
    AIProvider,
    AICapability,
    AIRequest,
    AIResponse,
)

logger = logging.getLogger(__name__)


class OpenAIClient(AIClient):
    """
    OpenAI implementation of AIClient.
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
            Optional OpenAI-compatible endpoint.

        organization:
            Optional organization identifier.

        timeout:
            HTTP timeout in seconds.
        """

        super().__init__(AIProvider.OPENAI)

        self._default_model = model

        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            organization=organization,
            timeout=timeout,
        )

        logger.info(
            "OpenAIClient initialized with model '%s'.",
            model,
        )

    # ------------------------------------------------------------------
    # Provider Information
    # ------------------------------------------------------------------

    def default_model(self) -> str:
        """
        Return the configured default model.
        """

        return self._default_model

    def is_available(self) -> bool:
        """
        Return True if the provider is reachable.

        This method delegates to the lightweight health check.
        """

        return self.health_check().healthy

    # ------------------------------------------------------------------
    # Capability Discovery
    # ------------------------------------------------------------------

    def capabilities(
        self,
    ) -> List[AICapability]:
        """
        Return the capabilities supported by this client.
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
        ]

    # ------------------------------------------------------------------
    # Model Discovery
    # ------------------------------------------------------------------

    def list_models(
        self,
    ) -> List[AIModelInfo]:
        """
        Return available models.

        The implementation attempts to query the provider. If that
        fails (permissions, network, etc.), it gracefully falls back
        to the configured default model.
        """

        models: List[AIModelInfo] = []

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
                    )
                )

        except Exception:

            logger.exception("Unable to retrieve OpenAI model list.")

            models.append(
                AIModelInfo(
                    provider=AIProvider.OPENAI,
                    model_name=self.default_model(),
                    supports_streaming=True,
                    supports_json=True,
                    supports_functions=True,
                    supports_vision=True,
                )
            )

        return models

    # ------------------------------------------------------------------
    # Health Check
    # ------------------------------------------------------------------

    def health_check(
        self,
    ) -> AIHealthResult:
        """
        Perform a lightweight connectivity test.

        The model listing endpoint is intentionally used because it
        is inexpensive and verifies authentication.
        """

        started = time.perf_counter()

        try:

            self._client.models.list()

            latency = (time.perf_counter() - started) * 1000

            return AIHealthResult(
                healthy=True,
                provider=AIProvider.OPENAI,
                status=AIClientStatus.READY,
                latency_ms=round(latency, 2),
                message="Provider reachable.",
            )

        except Exception as ex:

            latency = (time.perf_counter() - started) * 1000

            logger.exception("OpenAI health check failed.")

            return AIHealthResult(
                healthy=False,
                provider=AIProvider.OPENAI,
                status=AIClientStatus.UNAVAILABLE,
                latency_ms=round(latency, 2),
                message=str(ex),
            )

    # ------------------------------------------------------------------
    # Token Utilities
    # ------------------------------------------------------------------

    def estimate_tokens(
        self,
        text: str,
    ) -> int:
        """
        Estimate token count.

        This implementation intentionally provides a lightweight
        approximation. Future versions may integrate tiktoken for
        model-specific tokenization.
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
        Return the supported context window.

        Future releases may maintain a provider-specific registry.
        """

        _ = model

        return 128_000

    # ------------------------------------------------------------------
    # Core Generation
    # ------------------------------------------------------------------

    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute a non-streaming generation request.
        """

        request = self.before_request(request)

        try:

            response = self._execute_response_request(request)

            result = self._map_response(
                response=response,
                request=request,
            )

            return self.after_response(result)

        except Exception:

            logger.exception("OpenAI request execution failed.")

            raise

    # ------------------------------------------------------------------
    # Streaming
    # ------------------------------------------------------------------

    def stream(
        self,
        request: AIRequest,
    ):
        """
        Execute a streaming request.

        Yields provider SDK events directly for now.
        Future versions may normalize streaming events into
        provider-independent stream objects.
        """

        request = self.before_request(request)

        input_payload = self._build_input(request)

        with self._client.responses.stream(
            model=request.model,
            input=input_payload,
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
        ) as stream:

            for event in stream:
                yield event

    # ------------------------------------------------------------------
    # Internal Request Execution
    # ------------------------------------------------------------------

    def _execute_response_request(
        self,
        request: AIRequest,
    ):
        """
        Execute a Responses API request.
        """

        input_payload = self._build_input(request)

        return self._client.responses.create(
            model=self._safe_model_name(request.model),
            input=input_payload,
            temperature=self._safe_temperature(request.temperature),
            max_output_tokens=self._safe_max_tokens(request.max_tokens),
        )

    # ------------------------------------------------------------------
    # Input Builder
    # ------------------------------------------------------------------

    def _build_input(
        self,
        request: AIRequest,
    ) -> list[dict]:
        """
        Build the Responses API input payload.
        """

        input_items: list[dict] = []

        if request.system_prompt:

            input_items.append(
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

        input_items.append(
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

        return input_items

    # ------------------------------------------------------------------
    # Response Mapping
    # ------------------------------------------------------------------

    def _map_response(
        self,
        response: Any,
        request: AIRequest,
    ) -> AIResponse:
        """
        Convert an OpenAI Responses API object into the
        provider-independent AIResponse.
        """

        output_text = getattr(
            response,
            "output_text",
            "",
        )

        usage = getattr(
            response,
            "usage",
            None,
        )

        prompt_tokens = None
        completion_tokens = None
        total_tokens = None

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

        return AIResponse(
            success=True,
            provider=AIProvider.OPENAI,
            model=request.model or self.default_model(),
            content=output_text,
            finish_reason=getattr(
                response,
                "status",
                None,
            ),
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            raw_response=response,
        )

    # ------------------------------------------------------------------
    # Request Validation
    # ------------------------------------------------------------------

    def validate_request(
        self,
        request: AIRequest,
    ) -> None:
        """
        Validate an OpenAI request.

        Extends the base validation with provider-specific checks.
        """

        super().validate_request(request)

        if request.model is None:
            return

        if not request.model.strip():
            raise ValueError("Model name cannot be empty.")

        if request.temperature > 2.0:
            raise ValueError("OpenAI temperature cannot exceed 2.0.")

    # ------------------------------------------------------------------
    # Lifecycle Hooks
    # ------------------------------------------------------------------

    def before_request(
        self,
        request: AIRequest,
    ) -> AIRequest:
        """
        Execute provider-specific preprocessing.
        """

        request = super().before_request(request)

        logger.debug(
            "Executing OpenAI request " "(model=%s, stream=%s)",
            request.model,
            request.stream,
        )

        return request

    def after_response(
        self,
        response: AIResponse,
    ) -> AIResponse:
        """
        Execute provider-specific postprocessing.
        """

        logger.debug(
            "OpenAI request completed " "(tokens=%s)",
            response.total_tokens,
        )

        return super().after_response(response)

    # ------------------------------------------------------------------
    # Retry Policy
    # ------------------------------------------------------------------

    def should_retry(
        self,
        exception: Exception,
        attempt: int,
    ) -> bool:
        """
        Determine whether the failed request should
        be retried.

        Conservative retry policy:
        - Maximum three attempts.
        - Retry only transient failures.
        """

        if attempt >= self.max_retry_attempts():
            return False

        retryable = (
            TimeoutError,
            ConnectionError,
        )

        return isinstance(exception, retryable)

    def max_retry_attempts(self) -> int:
        """
        Maximum retry attempts supported by this client.
        """

        return 3

    # ------------------------------------------------------------------
    # Exception Mapping
    # ------------------------------------------------------------------

    def _map_exception(
        self,
        exception: Exception,
    ) -> RuntimeError:
        """
        Convert provider-specific exceptions into a
        provider-neutral runtime exception.

        Future versions can introduce dedicated
        Question Factory exception types without
        changing callers.
        """

        logger.exception("OpenAI provider exception.")

        return RuntimeError(f"OpenAI request failed: {exception}")

    # ------------------------------------------------------------------
    # Logging Helpers
    # ------------------------------------------------------------------

    def _log_request(
        self,
        request: AIRequest,
    ) -> None:
        """
        Log request metadata.

        Prompt contents are intentionally excluded to
        avoid logging potentially sensitive information.
        """

        logger.debug(
            "OpenAI request " "(model=%s, temperature=%s, " "max_tokens=%s, stream=%s)",
            request.model,
            request.temperature,
            request.max_tokens,
            request.stream,
        )

    def _log_response(
        self,
        response: AIResponse,
    ) -> None:
        """
        Log normalized response metadata.
        """

        logger.debug(
            "OpenAI response " "(success=%s, total_tokens=%s)",
            response.success,
            response.total_tokens,
        )

    # ------------------------------------------------------------------
    # Telemetry
    # ------------------------------------------------------------------

    def telemetry(
        self,
        request: AIRequest,
        response: AIResponse,
    ) -> Dict[str, Any]:
        """
        Produce provider-independent telemetry data.

        This information is suitable for runtime
        metrics, dashboards, and audit logs.
        """

        return {
            "provider": self.provider.value,
            "model": response.model,
            "stream": request.stream,
            "temperature": request.temperature,
            "prompt_tokens": response.prompt_tokens,
            "completion_tokens": response.completion_tokens,
            "total_tokens": response.total_tokens,
            "finish_reason": response.finish_reason,
        }

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @property
    def client(self) -> OpenAI:
        """
        Return the underlying OpenAI SDK client.

        This property exists primarily for advanced scenarios
        and integration testing. The rest of Question Factory OS
        should interact through the AIClient interface instead.
        """

        return self._client

    @property
    def configured_model(self) -> str:
        """
        Return the configured default model.
        """

        return self._default_model

    def set_default_model(
        self,
        model: str,
    ) -> None:
        """
        Update the default model used for requests that do not
        explicitly specify one.
        """

        if not model.strip():
            raise ValueError("Model name cannot be empty.")

        logger.info(
            "Changing default model from '%s' to '%s'.",
            self._default_model,
            model,
        )

        self._default_model = model

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(self) -> Dict[str, Any]:
        """
        Return provider diagnostics.

        Extends the base AIClient diagnostics with OpenAI-
        specific information.
        """

        diagnostics = super().diagnostics()

        diagnostics.update(
            {
                "configured_model": self._default_model,
                "supports_responses_api": True,
                "sdk_client": self._client.__class__.__name__,
            }
        )

        return diagnostics

    # ------------------------------------------------------------------
    # Model Helpers
    # ------------------------------------------------------------------

    def supports_model(
        self,
        model: str,
    ) -> bool:
        """
        Determine whether the specified model is available.

        If model discovery cannot be performed, False is returned.
        """

        try:

            models = self.list_models()

            return any(item.model_name == model for item in models)

        except Exception:

            logger.exception(
                "Unable to verify model '%s'.",
                model,
            )

            return False

    # ------------------------------------------------------------------
    # Response Helpers
    # ------------------------------------------------------------------

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
    ) -> Dict[str, Optional[int]]:
        """
        Return a normalized usage summary.
        """

        return {
            "prompt_tokens": response.prompt_tokens,
            "completion_tokens": response.completion_tokens,
            "total_tokens": response.total_tokens,
        }

    # ------------------------------------------------------------------
    # SDK Compatibility Helpers
    # ------------------------------------------------------------------

    def sdk_version(self) -> Optional[str]:
        """
        Attempt to determine the installed OpenAI SDK version.

        Returns None if the version cannot be determined.
        """

        try:

            from importlib.metadata import version

            return version("openai")

        except Exception:

            logger.debug("Unable to determine OpenAI SDK version.")

            return None

    # ------------------------------------------------------------------
    # Provider Summary
    # ------------------------------------------------------------------

    def provider_summary(self) -> Dict[str, Any]:
        """
        Return an OpenAI-specific provider summary.
        """

        summary = super().provider_summary()

        summary.update(
            {
                "sdk_version": self.sdk_version(),
                "responses_api": True,
                "default_model": self._default_model,
            }
        )

        return summary

    # ------------------------------------------------------------------
    # Operational Information
    # ------------------------------------------------------------------

    def info(self) -> Dict[str, Any]:
        """
        Return a comprehensive provider description.
        """

        info = super().info()

        info.update(
            {
                "configured_model": self._default_model,
                "sdk_version": self.sdk_version(),
                "responses_api": True,
            }
        )

        return info

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """
        Initialize the provider client.

        The OpenAI SDK is initialized during construction, so this
        method currently performs no additional work. It exists to
        satisfy the AIClient lifecycle contract and to support future
        initialization logic.
        """

        logger.debug("OpenAIClient initialized.")

    def shutdown(self) -> None:
        """
        Release provider resources.

        The OpenAI SDK manages its own HTTP resources internally.
        Future SDK versions may expose explicit cleanup methods.
        """

        logger.debug("OpenAIClient shutdown.")

    # ------------------------------------------------------------------
    # Internal Utilities
    # ------------------------------------------------------------------

    def _safe_model_name(
        self,
        model: Optional[str],
    ) -> str:
        """
        Return a valid model name.
        """

        if model and model.strip():
            return model

        return self._default_model

    def _safe_temperature(
        self,
        temperature: float,
    ) -> float:
        """
        Normalize temperature into the supported range.
        """

        return max(
            0.0,
            min(
                2.0,
                temperature,
            ),
        )

    def _safe_max_tokens(
        self,
        max_tokens: Optional[int],
    ) -> Optional[int]:
        """
        Normalize max output tokens.
        """

        if max_tokens is None:
            return None

        return max(
            1,
            max_tokens,
        )

    # ------------------------------------------------------------------
    # Readiness
    # ------------------------------------------------------------------

    @property
    def ready(self) -> bool:
        """
        Return True if the client is operational.
        """

        try:
            return self.is_available()
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"model='{self._default_model}', "
            f"provider='{self.provider.value}')"
        )

    __str__ = __repr__


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    "OpenAIClient",
]
