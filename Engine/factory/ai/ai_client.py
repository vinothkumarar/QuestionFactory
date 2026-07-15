"""
Question Factory OS v2.1
------------------------

Provider Agnostic AI Client

This module defines the common abstractions shared by every
AI provider supported by Question Factory OS.

The AIClient is the enterprise foundation for:

    • OpenAI
    • Anthropic
    • Google Gemini
    • Ollama
    • Azure OpenAI
    • Future providers

Responsibilities
----------------
• Standard request/response contracts
• Provider capabilities
• Health monitoring
• Lifecycle management
• Diagnostics
• Retry policy
• Telemetry
• Provider-independent validation

Author
------
Question Factory OS Team
"""

from __future__ import annotations

import logging

from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass
from dataclasses import field

from enum import Enum

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# AI Provider
# ----------------------------------------------------------------------


class AIProvider(str, Enum):
    """
    Supported AI providers.
    """

    OPENAI = "openai"

    ANTHROPIC = "anthropic"

    GEMINI = "gemini"

    AZURE_OPENAI = "azure_openai"

    OLLAMA = "ollama"

    CUSTOM = "custom"


# ----------------------------------------------------------------------
# AI Client Status
# ----------------------------------------------------------------------


class AIClientStatus(str, Enum):
    """
    Runtime provider status.
    """

    UNKNOWN = "unknown"

    INITIALIZING = "initializing"

    READY = "ready"

    DEGRADED = "degraded"

    UNAVAILABLE = "unavailable"

    FAILED = "failed"

    SHUTDOWN = "shutdown"


# ----------------------------------------------------------------------
# Provider Capabilities
# ----------------------------------------------------------------------


class AICapability(str, Enum):
    """
    Provider capabilities.
    """

    CHAT = "chat"

    STREAMING = "streaming"

    JSON_MODE = "json_mode"

    FUNCTION_CALLING = "function_calling"

    SYSTEM_PROMPTS = "system_prompts"

    TEMPERATURE = "temperature"

    TOKEN_ESTIMATION = "token_estimation"

    IMAGE_INPUT = "image_input"

    IMAGE_OUTPUT = "image_output"

    AUDIO_INPUT = "audio_input"

    AUDIO_OUTPUT = "audio_output"

    VISION = "vision"

    EMBEDDINGS = "embeddings"

    REASONING = "reasoning"

    TOOLS = "tools"

    STRUCTURED_OUTPUT = "structured_output"

    MULTIMODAL = "multimodal"


# ----------------------------------------------------------------------
# Finish Reasons
# ----------------------------------------------------------------------


class AIFinishReason(str, Enum):
    """
    Standardized completion reasons.
    """

    STOP = "stop"

    LENGTH = "length"

    TOOL_CALL = "tool_call"

    CONTENT_FILTER = "content_filter"

    ERROR = "error"

    UNKNOWN = "unknown"
# ----------------------------------------------------------------------
# AI Request
# ----------------------------------------------------------------------


@dataclass(slots=True)
class AIRequest:
    """
    Provider-independent AI request.
    """

    prompt: str

    system_prompt: Optional[str] = None

    model: Optional[str] = None

    temperature: float = 0.7

    max_tokens: Optional[int] = None

    stream: bool = False

    response_format: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    user: Optional[str] = None

    conversation_id: Optional[str] = None

    request_id: Optional[str] = None

    timeout: Optional[float] = None

    tags: List[str] = field(
        default_factory=list
    )

    extra: Dict[str, Any] = field(
        default_factory=dict
    )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def has_system_prompt(
        self,
    ) -> bool:
        """
        Return True if a system prompt exists.
        """

        return bool(
            self.system_prompt
            and self.system_prompt.strip()
        )

    @property
    def has_model(
        self,
    ) -> bool:
        """
        Return True if a model is specified.
        """

        return bool(
            self.model
            and self.model.strip()
        )

    @property
    def has_max_tokens(
        self,
    ) -> bool:
        """
        Return True if max_tokens is configured.
        """

        return self.max_tokens is not None

    @property
    def has_metadata(
        self,
    ) -> bool:
        """
        Return True if metadata exists.
        """

        return bool(self.metadata)

    @property
    def has_tags(
        self,
    ) -> bool:
        """
        Return True if tags are present.
        """

        return bool(self.tags)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
    ) -> None:
        """
        Validate request fields.
        """

        if not self.prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        if self.temperature < 0.0:
            raise ValueError(
                "Temperature cannot be negative."
            )

        if self.temperature > 2.0:
            raise ValueError(
                "Temperature cannot exceed 2.0."
            )

        if (
            self.max_tokens is not None
            and self.max_tokens <= 0
        ):
            raise ValueError(
                "max_tokens must be greater than zero."
            )

        if (
            self.timeout is not None
            and self.timeout <= 0
        ):
            raise ValueError(
                "timeout must be greater than zero."
            )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Serialize request.
        """

        return {
            "prompt": self.prompt,
            "system_prompt": self.system_prompt,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": self.stream,
            "response_format": self.response_format,
            "metadata": dict(
                self.metadata
            ),
            "user": self.user,
            "conversation_id": (
                self.conversation_id
            ),
            "request_id": self.request_id,
            "timeout": self.timeout,
            "tags": list(self.tags),
            "extra": dict(self.extra),
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "AIRequest":
        """
        Create an AIRequest from a dictionary.
        """

        return cls(
            prompt=data["prompt"],
            system_prompt=data.get(
                "system_prompt"
            ),
            model=data.get(
                "model"
            ),
            temperature=data.get(
                "temperature",
                0.7,
            ),
            max_tokens=data.get(
                "max_tokens"
            ),
            stream=data.get(
                "stream",
                False,
            ),
            response_format=data.get(
                "response_format"
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
            user=data.get("user"),
            conversation_id=data.get(
                "conversation_id"
            ),
            request_id=data.get(
                "request_id"
            ),
            timeout=data.get(
                "timeout"
            ),
            tags=list(
                data.get(
                    "tags",
                    [],
                )
            ),
            extra=dict(
                data.get(
                    "extra",
                    {},
                )
            ),
        )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Return a lightweight request summary.
        """

        return {
            "model": self.model,
            "stream": self.stream,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "has_system_prompt": (
                self.has_system_prompt
            ),
            "response_format": (
                self.response_format
            ),
        }
# ----------------------------------------------------------------------
# AI Response
# ----------------------------------------------------------------------


@dataclass(slots=True)
class AIResponse:
    """
    Provider-independent AI response.
    """

    success: bool

    provider: AIProvider

    model: str

    content: str

    finish_reason: Optional[str] = None

    prompt_tokens: Optional[int] = None

    completion_tokens: Optional[int] = None

    total_tokens: Optional[int] = None

    raw_response: Any = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    error_message: Optional[str] = None

    response_time_ms: Optional[float] = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def has_usage(
        self,
    ) -> bool:
        """
        True if token usage is available.
        """

        return self.total_tokens is not None

    @property
    def has_error(
        self,
    ) -> bool:
        """
        True if an error message exists.
        """

        return bool(
            self.error_message
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        """
        True if metadata exists.
        """

        return bool(
            self.metadata
        )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Serialize response.
        """

        return {
            "success": self.success,
            "provider": self.provider.value,
            "model": self.model,
            "content": self.content,
            "finish_reason": (
                self.finish_reason
            ),
            "prompt_tokens": (
                self.prompt_tokens
            ),
            "completion_tokens": (
                self.completion_tokens
            ),
            "total_tokens": (
                self.total_tokens
            ),
            "metadata": dict(
                self.metadata
            ),
            "error_message": (
                self.error_message
            ),
            "response_time_ms": (
                self.response_time_ms
            ),
        }

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Lightweight response summary.
        """

        return {
            "provider": (
                self.provider.value
            ),
            "model": self.model,
            "success": self.success,
            "tokens": self.total_tokens,
            "finish_reason": (
                self.finish_reason
            ),
        }


# ----------------------------------------------------------------------
# AI Health Result
# ----------------------------------------------------------------------


@dataclass(slots=True)
class AIHealthResult:
    """
    Health check result.
    """

    healthy: bool

    provider: AIProvider

    status: AIClientStatus

    latency_ms: Optional[
        float
    ] = None

    message: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Serialize health result.
        """

        return {
            "healthy": self.healthy,
            "provider": (
                self.provider.value
            ),
            "status": (
                self.status.value
            ),
            "latency_ms": (
                self.latency_ms
            ),
            "message": self.message,
            "metadata": dict(
                self.metadata
            ),
        }


# ----------------------------------------------------------------------
# AI Model Information
# ----------------------------------------------------------------------


@dataclass(slots=True)
class AIModelInfo:
    """
    Information describing a
    provider model.
    """

    provider: AIProvider

    model_name: str

    supports_streaming: bool = False

    supports_json: bool = False

    supports_functions: bool = False

    supports_vision: bool = False

    context_window: Optional[
        int
    ] = None

    max_output_tokens: Optional[
        int
    ] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Serialize model information.
        """

        return {
            "provider": (
                self.provider.value
            ),
            "model_name": (
                self.model_name
            ),
            "supports_streaming": (
                self.supports_streaming
            ),
            "supports_json": (
                self.supports_json
            ),
            "supports_functions": (
                self.supports_functions
            ),
            "supports_vision": (
                self.supports_vision
            ),
            "context_window": (
                self.context_window
            ),
            "max_output_tokens": (
                self.max_output_tokens
            ),
            "metadata": dict(
                self.metadata
            ),
        }

    @property
    def supports_multimodal(
        self,
    ) -> bool:
        """
        True if the model supports
        multimodal inputs.
        """

        return self.supports_vision
# ----------------------------------------------------------------------
# AI Client
# ----------------------------------------------------------------------


class AIClient(ABC):
    """
    Provider-agnostic AI client.

    All provider implementations inherit from this class.

    Examples
    --------
    - OpenAIClient
    - AnthropicClient
    - GeminiClient
    - OllamaClient
    """

    def __init__(
        self,
        provider: AIProvider,
    ) -> None:
        """
        Initialize the AI provider.
        """

        self._provider = provider

        logger.info(
            "%s initialized.",
            provider.value,
        )

    # ------------------------------------------------------------------
    # Provider Information
    # ------------------------------------------------------------------

    @property
    def provider(
        self,
    ) -> AIProvider:
        """
        Return the provider.
        """

        return self._provider

    @property
    def provider_name(
        self,
    ) -> str:
        """
        Human-readable provider name.
        """

        return self._provider.value

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    def initialize(
        self,
    ) -> None:
        """
        Initialize the provider.

        Called once before the provider
        is used.
        """

        raise NotImplementedError

    @abstractmethod
    def shutdown(
        self,
    ) -> None:
        """
        Shutdown the provider.

        Release provider resources.
        """

        raise NotImplementedError

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    @abstractmethod
    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute a non-streaming request.
        """

        raise NotImplementedError

    @abstractmethod
    def stream(
        self,
        request: AIRequest,
    ):
        """
        Execute a streaming request.

        Provider implementations may
        yield provider-specific events.
        """

        raise NotImplementedError

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    @abstractmethod
    def health_check(
        self,
    ) -> AIHealthResult:
        """
        Perform a provider health check.
        """

        raise NotImplementedError

    def is_available(
        self,
    ) -> bool:
        """
        Return True if the provider
        is operational.
        """

        return self.health_check().healthy

    # ------------------------------------------------------------------
    # Models
    # ------------------------------------------------------------------

    @abstractmethod
    def list_models(
        self,
    ) -> List[AIModelInfo]:
        """
        Return available models.
        """

        raise NotImplementedError

    @abstractmethod
    def default_model(
        self,
    ) -> str:
        """
        Return the configured default
        model.
        """

        raise NotImplementedError

    # ------------------------------------------------------------------
    # Capabilities
    # ------------------------------------------------------------------

    @abstractmethod
    def capabilities(
        self,
    ) -> List[AICapability]:
        """
        Return supported provider
        capabilities.
        """

        raise NotImplementedError

    # ------------------------------------------------------------------
    # Token Utilities
    # ------------------------------------------------------------------

    @abstractmethod
    def estimate_tokens(
        self,
        text: str,
    ) -> int:
        """
        Estimate token count.
        """

        raise NotImplementedError

    @abstractmethod
    def max_context_window(
        self,
        model: Optional[str] = None,
    ) -> Optional[int]:
        """
        Return the maximum supported
        context window.
        """

        raise NotImplementedError

    # ------------------------------------------------------------------
    # Request Validation
    # ------------------------------------------------------------------

    def validate_request(
        self,
        request: AIRequest,
    ) -> None:
        """
        Validate a provider-independent
        request.
        """

        request.validate()

    # ------------------------------------------------------------------
    # Lifecycle Hooks
    # ------------------------------------------------------------------

    def before_request(
        self,
        request: AIRequest,
    ) -> AIRequest:
        """
        Hook executed immediately before
        provider execution.

        Providers may override this
        method.
        """

        return request

    def after_response(
        self,
        response: AIResponse,
    ) -> AIResponse:
        """
        Hook executed immediately after
        provider execution.

        Providers may override this
        method.
        """

        return response
    # ------------------------------------------------------------------
    # Retry Policy
    # ------------------------------------------------------------------

    def should_retry(
        self,
        exception: Exception,
        attempt: int,
    ) -> bool:
        """
        Determine whether a failed request
        should be retried.

        Provider implementations may
        override this policy.
        """

        _ = exception

        return (
            attempt
            < self.max_retry_attempts()
        )

    def max_retry_attempts(
        self,
    ) -> int:
        """
        Maximum retry attempts.
        """

        return 3

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(
        self,
    ) -> Dict[str, Any]:
        """
        Return provider diagnostics.
        """

        health = self.health_check()

        return {
            "provider": self.provider.value,
            "provider_name": self.provider_name,
            "status": health.status.value,
            "healthy": health.healthy,
            "latency_ms": health.latency_ms,
            "default_model": (
                self.default_model()
            ),
            "capabilities": [
                capability.value
                for capability
                in self.capabilities()
            ],
        }

    # ------------------------------------------------------------------
    # Provider Summary
    # ------------------------------------------------------------------

    def provider_summary(
        self,
    ) -> Dict[str, Any]:
        """
        Return a concise provider summary.
        """

        return {
            "provider": (
                self.provider.value
            ),
            "model": (
                self.default_model()
            ),
            "available": (
                self.is_available()
            ),
        }

    # ------------------------------------------------------------------
    # Provider Information
    # ------------------------------------------------------------------

    def info(
        self,
    ) -> Dict[str, Any]:
        """
        Return detailed provider
        information.
        """

        return {
            "provider": (
                self.provider.value
            ),
            "provider_name": (
                self.provider_name
            ),
            "default_model": (
                self.default_model()
            ),
            "capabilities": [
                capability.value
                for capability
                in self.capabilities()
            ],
            "models": [
                model.to_dict()
                for model
                in self.list_models()
            ],
            "health": (
                self.health_check()
                .to_dict()
            ),
        }

    # ------------------------------------------------------------------
    # Telemetry
    # ------------------------------------------------------------------

    def telemetry(
        self,
        request: AIRequest,
        response: AIResponse,
    ) -> Dict[str, Any]:
        """
        Return provider-independent
        telemetry.
        """

        return {
            "provider": (
                self.provider.value
            ),
            "model": (
                response.model
            ),
            "stream": (
                request.stream
            ),
            "temperature": (
                request.temperature
            ),
            "prompt_tokens": (
                response.prompt_tokens
            ),
            "completion_tokens": (
                response.completion_tokens
            ),
            "total_tokens": (
                response.total_tokens
            ),
            "finish_reason": (
                response.finish_reason
            ),
            "response_time_ms": (
                response.response_time_ms
            ),
        }

    # ------------------------------------------------------------------
    # Exception Mapping
    # ------------------------------------------------------------------

    def map_exception(
        self,
        exception: Exception,
    ) -> RuntimeError:
        """
        Convert provider-specific
        exceptions into a provider-
        independent RuntimeError.

        Provider implementations may
        override this method.
        """

        logger.exception(
            "%s provider exception.",
            self.provider_name,
        )

        return RuntimeError(
            str(exception)
        )
    # ------------------------------------------------------------------
    # Shared Utility Helpers
    # ------------------------------------------------------------------

    def normalize_model(
        self,
        model: Optional[str],
    ) -> str:
        """
        Normalize the requested model.

        If the caller does not specify a model,
        the provider default model is returned.
        """

        if model is None:
            return self.default_model()

        model = model.strip()

        if not model:
            return self.default_model()

        return model

    def normalize_temperature(
        self,
        temperature: float,
    ) -> float:
        """
        Normalize temperature into the
        provider supported range.

        Default implementation follows the
        OpenAI-compatible range [0.0, 2.0].
        """

        if temperature < 0.0:
            return 0.0

        if temperature > 2.0:
            return 2.0

        return temperature

    def normalize_max_tokens(
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
    # Convenience Helpers
    # ------------------------------------------------------------------

    def supports(
        self,
        capability: AICapability,
    ) -> bool:
        """
        Determine whether the provider
        supports a capability.
        """

        return (
            capability
            in self.capabilities()
        )

    def supports_streaming(
        self,
    ) -> bool:
        """
        True if streaming is supported.
        """

        return self.supports(
            AICapability.STREAMING
        )

    def supports_json_mode(
        self,
    ) -> bool:
        """
        True if JSON mode is supported.
        """

        return self.supports(
            AICapability.JSON_MODE
        )

    def supports_function_calling(
        self,
    ) -> bool:
        """
        True if function calling is supported.
        """

        return self.supports(
            AICapability.FUNCTION_CALLING
        )

    def supports_vision(
        self,
    ) -> bool:
        """
        True if vision is supported.
        """

        return self.supports(
            AICapability.VISION
        )

    def supports_reasoning(
        self,
    ) -> bool:
        """
        True if reasoning models are supported.
        """

        return self.supports(
            AICapability.REASONING
        )

    # ------------------------------------------------------------------
    # Request Execution
    # ------------------------------------------------------------------

    def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute a provider-independent
        request.

        This is the standard entry point used
        by the rest of Question Factory OS.
        """

        self.validate_request(
            request
        )

        request = self.before_request(
            request
        )

        response = self.generate(
            request
        )

        response = self.after_response(
            response
        )

        return response

    # ------------------------------------------------------------------
    # Readiness
    # ------------------------------------------------------------------

    @property
    def ready(
        self,
    ) -> bool:
        """
        Return True if the provider is ready.
        """

        try:

            return self.is_available()

        except Exception:

            logger.exception(
                "Provider readiness check failed."
            )

            return False

    @property
    def status(
        self,
    ) -> AIClientStatus:
        """
        Current provider status.
        """

        return (
            self.health_check()
            .status
        )
    # ------------------------------------------------------------------
    # Model Helpers
    # ------------------------------------------------------------------

    def supports_model(
        self,
        model: str,
    ) -> bool:
        """
        Determine whether the specified model
        is supported by this provider.
        """

        model = model.strip()

        if not model:
            return False

        try:

            available_models = self.list_models()

        except Exception:

            logger.exception(
                "Unable to retrieve provider models."
            )

            return False

        return any(
            item.model_name == model
            for item in available_models
        )

    def model_information(
        self,
        model: str,
    ) -> Optional[AIModelInfo]:
        """
        Return information for the requested
        model.

        Returns
        -------
        AIModelInfo | None
        """

        for item in self.list_models():

            if item.model_name == model:
                return item

        return None

    # ------------------------------------------------------------------
    # Health Helpers
    # ------------------------------------------------------------------

    def ensure_available(
        self,
    ) -> None:
        """
        Ensure the provider is available.

        Raises
        ------
        RuntimeError
            If the provider is unavailable.
        """

        health = self.health_check()

        if not health.healthy:

            raise RuntimeError(
                health.message
                or (
                    f"{self.provider_name} "
                    "is unavailable."
                )
            )

    # ------------------------------------------------------------------
    # Logging Helpers
    # ------------------------------------------------------------------

    def log_request(
        self,
        request: AIRequest,
    ) -> None:
        """
        Log request metadata.

        Prompt contents are intentionally
        excluded.
        """

        logger.debug(
            "%s request "
            "(model=%s, stream=%s)",
            self.provider_name,
            self.normalize_model(
                request.model
            ),
            request.stream,
        )

    def log_response(
        self,
        response: AIResponse,
    ) -> None:
        """
        Log response metadata.
        """

        logger.debug(
            "%s response "
            "(success=%s, tokens=%s)",
            self.provider_name,
            response.success,
            response.total_tokens,
        )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Return a concise provider summary.
        """

        health = self.health_check()

        return {
            "provider": self.provider.value,
            "provider_name": self.provider_name,
            "status": health.status.value,
            "healthy": health.healthy,
            "default_model": (
                self.default_model()
            ),
            "ready": self.ready,
        }

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"provider='{self.provider.value}', "
            f"model='{self.default_model()}')"
        )

    __str__ = __repr__
    # ------------------------------------------------------------------
    # Configuration Validation
    # ------------------------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate provider configuration.

        The default implementation simply verifies
        that the provider is available.

        Provider implementations may extend this
        validation with API-key, endpoint or
        authentication specific checks.
        """

        self.ensure_available()

    # ------------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------------

    @property
    def healthy(
        self,
    ) -> bool:
        """
        Return True if the provider passes
        the health check.
        """

        return self.health_check().healthy

    @property
    def latency_ms(
        self,
    ) -> Optional[float]:
        """
        Return the latest measured provider
        latency.
        """

        return self.health_check().latency_ms

    # ------------------------------------------------------------------
    # Equality
    # ------------------------------------------------------------------

    def __eq__(
        self,
        other: object,
    ) -> bool:

        if not isinstance(
            other,
            AIClient,
        ):
            return NotImplemented

        return (
            self.provider
            == other.provider
        )

    def __hash__(
        self,
    ) -> int:

        return hash(
            self.provider
        )


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    # Enums
    "AIProvider",
    "AIClientStatus",
    "AICapability",
    "AIFinishReason",

    # Models
    "AIRequest",
    "AIResponse",
    "AIHealthResult",
    "AIModelInfo",

    # Base Client
    "AIClient",
]
