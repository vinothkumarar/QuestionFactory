"""
Question Factory OS v2.1
------------------------

Provider-Agnostic AI Client Interface.

This module defines the abstract contract implemented by every
AI provider supported by Question Factory OS.

Responsibilities
----------------
• Provider-independent AI interface
• Capability discovery
• Health checks
• Request execution
• Streaming support
• Model enumeration
• Token estimation
• Retry contract

This module MUST NOT import provider SDKs.

Supported Providers
-------------------
- OpenAI
- Anthropic
- Google Gemini
- Azure OpenAI
- Ollama
- Local LLMs
- Future providers

Author:
Question Factory OS
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass
from dataclasses import field

from enum import Enum

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from factory.ai.models.ai_job import AIJob

# ----------------------------------------------------------------------
# Provider Types
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

    LOCAL = "local"

    CUSTOM = "custom"


# ----------------------------------------------------------------------
# Capability Types
# ----------------------------------------------------------------------


class AICapability(str, Enum):
    """
    Provider capabilities.
    """

    CHAT = "chat"

    COMPLETION = "completion"

    STREAMING = "streaming"

    JSON_MODE = "json_mode"

    FUNCTION_CALLING = "function_calling"

    VISION = "vision"

    EMBEDDINGS = "embeddings"

    TOKEN_ESTIMATION = "token_estimation"

    SYSTEM_PROMPTS = "system_prompts"

    TEMPERATURE = "temperature"


# ----------------------------------------------------------------------
# Client Status
# ----------------------------------------------------------------------


class AIClientStatus(str, Enum):

    UNKNOWN = "unknown"

    READY = "ready"

    DEGRADED = "degraded"

    UNAVAILABLE = "unavailable"


# ----------------------------------------------------------------------
# Health Result
# ----------------------------------------------------------------------


@dataclass(slots=True)
class AIHealthResult:
    """
    Provider health information.
    """

    healthy: bool

    provider: AIProvider

    status: AIClientStatus

    latency_ms: Optional[float] = None

    message: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# ----------------------------------------------------------------------
# Model Information
# ----------------------------------------------------------------------


@dataclass(slots=True)
class AIModelInfo:
    """
    Information describing a supported model.
    """

    provider: AIProvider

    model_name: str

    context_window: Optional[int] = None

    max_output_tokens: Optional[int] = None

    supports_streaming: bool = False

    supports_json: bool = False

    supports_vision: bool = False

    supports_functions: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)


# ----------------------------------------------------------------------
# Request Object
# ----------------------------------------------------------------------


@dataclass(slots=True)
class AIRequest:
    """
    Normalized request sent to providers.
    """

    job: AIJob

    prompt: str

    system_prompt: Optional[str] = None

    model: Optional[str] = None

    temperature: float = 0.2

    max_tokens: Optional[int] = None

    stream: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)


# ----------------------------------------------------------------------
# Response Object
# ----------------------------------------------------------------------


@dataclass(slots=True)
class AIResponse:
    """
    Normalized provider response.
    """

    success: bool

    provider: AIProvider

    model: str

    content: str

    finish_reason: Optional[str] = None

    prompt_tokens: Optional[int] = None

    completion_tokens: Optional[int] = None

    total_tokens: Optional[int] = None

    raw_response: Optional[Any] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# ----------------------------------------------------------------------
# Abstract AI Client
# ----------------------------------------------------------------------


class AIClient(ABC):
    """
    Provider-agnostic AI client interface.

    Every provider implementation (OpenAI, Anthropic, Gemini,
    Ollama, Azure OpenAI, etc.) must inherit from this class.

    The AIEngine interacts exclusively with this interface and
    never with provider SDKs directly.
    """

    def __init__(
        self,
        provider: AIProvider,
    ) -> None:
        self._provider = provider

    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------

    @property
    def provider(self) -> AIProvider:
        """
        Return the provider represented by this client.
        """
        return self._provider

    @property
    def provider_name(self) -> str:
        """
        Human-readable provider name.
        """
        return self._provider.value

    # ------------------------------------------------------------------
    # Core Execution
    # ------------------------------------------------------------------

    @abstractmethod
    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute a non-streaming AI request.

        Parameters
        ----------
        request:
            Normalized AI request.

        Returns
        -------
        AIResponse
            Normalized provider response.
        """
        raise NotImplementedError

    @abstractmethod
    def stream(
        self,
        request: AIRequest,
    ):
        """
        Execute a streaming request.

        Implementations should return an iterator/generator
        yielding provider-independent response chunks.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Health & Availability
    # ------------------------------------------------------------------

    @abstractmethod
    def health_check(self) -> AIHealthResult:
        """
        Perform a lightweight provider health check.
        """
        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> bool:
        """
        Return True if the provider is currently usable.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Model Discovery
    # ------------------------------------------------------------------

    @abstractmethod
    def list_models(
        self,
    ) -> List[AIModelInfo]:
        """
        Return supported models.
        """
        raise NotImplementedError

    @abstractmethod
    def default_model(self) -> str:
        """
        Return the provider's default model.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Capability Discovery
    # ------------------------------------------------------------------

    @abstractmethod
    def capabilities(
        self,
    ) -> List[AICapability]:
        """
        Return supported provider capabilities.
        """
        raise NotImplementedError

    def supports(
        self,
        capability: AICapability,
    ) -> bool:
        """
        Determine whether a capability is supported.
        """

        return capability in self.capabilities()

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

        Providers may implement an exact tokenizer or an
        approximate estimation strategy.
        """
        raise NotImplementedError

    @abstractmethod
    def max_context_window(
        self,
        model: Optional[str] = None,
    ) -> Optional[int]:
        """
        Return maximum supported context window.
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
        Validate a normalized AI request.

        Concrete providers may override this method to enforce
        provider-specific constraints, but should normally call
        super().validate_request().
        """

        if request is None:
            raise ValueError("request cannot be None.")

        if request.job is None:
            raise ValueError("request.job cannot be None.")

        if not request.prompt:
            raise ValueError("request.prompt cannot be empty.")

        if request.temperature < 0:
            raise ValueError("temperature cannot be negative.")

        if request.max_tokens is not None and request.max_tokens <= 0:
            raise ValueError("max_tokens must be greater than zero.")

    # ------------------------------------------------------------------
    # Request Normalization
    # ------------------------------------------------------------------

    def normalize_request(
        self,
        request: AIRequest,
    ) -> AIRequest:
        """
        Normalize a request before execution.

        Providers may override this method if additional
        normalization is required.
        """

        self.validate_request(request)

        if request.model is None:
            request.model = self.default_model()

        if request.system_prompt is not None:
            request.system_prompt = request.system_prompt.strip()

        request.prompt = request.prompt.strip()

        return request

    # ------------------------------------------------------------------
    # Lifecycle Hooks
    # ------------------------------------------------------------------

    def before_request(
        self,
        request: AIRequest,
    ) -> AIRequest:
        """
        Hook executed immediately before a request is sent.

        Default behavior performs normalization only.
        """

        return self.normalize_request(request)

    def after_response(
        self,
        response: AIResponse,
    ) -> AIResponse:
        """
        Hook executed immediately after a provider response
        has been received.

        Providers may override this for metrics, auditing,
        response cleanup, etc.
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
        Determine whether a failed request should be retried.

        Default implementation performs no retries.
        Provider implementations may override this method with
        provider-specific retry policies.
        """

        return False

    def max_retry_attempts(self) -> int:
        """
        Maximum retry attempts supported by this client.

        AIEngine should respect this value when coordinating
        retries.
        """

        return 0

    # ------------------------------------------------------------------
    # Request Metadata
    # ------------------------------------------------------------------

    def enrich_metadata(
        self,
        request: AIRequest,
    ) -> Dict[str, Any]:
        """
        Produce provider-independent request metadata.

        This metadata can be attached to logs, telemetry,
        audit records, or execution traces.
        """

        metadata = dict(request.metadata)

        metadata.setdefault("provider", self.provider.value)
        metadata.setdefault("model", request.model)
        metadata.setdefault("stream", request.stream)
        metadata.setdefault("temperature", request.temperature)
        metadata.setdefault("max_tokens", request.max_tokens)

        return metadata

    # ------------------------------------------------------------------
    # Response Utilities
    # ------------------------------------------------------------------

    def response_usage(
        self,
        response: AIResponse,
    ) -> Dict[str, Optional[int]]:
        """
        Return normalized token usage statistics.
        """

        return {
            "prompt_tokens": response.prompt_tokens,
            "completion_tokens": response.completion_tokens,
            "total_tokens": response.total_tokens,
        }

    def response_successful(
        self,
        response: AIResponse,
    ) -> bool:
        """
        Determine whether a normalized response represents
        a successful completion.
        """

        return response.success

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(self) -> Dict[str, Any]:
        """
        Return provider-independent diagnostic information.

        This method is intended for operational dashboards,
        monitoring endpoints, and runtime health reporting.
        """

        return {
            "provider": self.provider.value,
            "provider_name": self.provider_name,
            "default_model": self.default_model(),
            "capabilities": [capability.value for capability in self.capabilities()],
            "max_retry_attempts": self.max_retry_attempts(),
        }

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """
        Initialize the client.

        Most providers override this method to establish
        SDK clients, authenticate, or prepare caches.
        """

    def shutdown(self) -> None:
        """
        Gracefully release any provider resources.

        Default implementation performs no action.
        """

    def reset(self) -> None:
        """
        Reset transient provider state.

        Default implementation simply performs a
        shutdown followed by initialization.
        """

        self.shutdown()
        self.initialize()

    # ------------------------------------------------------------------
    # Context Manager Support
    # ------------------------------------------------------------------

    def __enter__(self):
        """
        Allow:

            with client:
                ...
        """

        self.initialize()
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        traceback,
    ) -> None:
        """
        Ensure resources are released.
        """

        self.shutdown()

    # ------------------------------------------------------------------
    # Identity Helpers
    # ------------------------------------------------------------------

    def __eq__(
        self,
        other: object,
    ) -> bool:

        if not isinstance(other, AIClient):
            return False

        return (
            self.provider == other.provider
            and self.default_model() == other.default_model()
        )

    def __hash__(self) -> int:

        return hash(
            (
                self.provider,
                self.default_model(),
            )
        )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"provider='{self.provider.value}', "
            f"model='{self.default_model()}')"
        )

    __str__ = __repr__

    # ------------------------------------------------------------------
    # Provider Information
    # ------------------------------------------------------------------

    def provider_summary(self) -> Dict[str, Any]:
        """
        Return a concise summary describing this provider.
        """

        return {
            "provider": self.provider.value,
            "default_model": self.default_model(),
            "available": self.is_available(),
            "capabilities": [capability.value for capability in self.capabilities()],
        }

    # ------------------------------------------------------------------
    # Capability Validation
    # ------------------------------------------------------------------

    def require_capability(
        self,
        capability: AICapability,
    ) -> None:
        """
        Raise an exception if the provider does not
        support the requested capability.
        """

        if not self.supports(capability):
            raise NotImplementedError(
                f"{self.provider.value} does not support " f"'{capability.value}'."
            )

    # ------------------------------------------------------------------
    # Execution Wrapper
    # ------------------------------------------------------------------

    def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Standard execution pipeline.

        Concrete providers normally should not override
        this method. Instead they implement generate().
        """

        normalized = self.before_request(request)

        response = self.generate(normalized)

        return self.after_response(response)

    # ------------------------------------------------------------------
    # Feature Helpers
    # ------------------------------------------------------------------

    def supports_streaming(self) -> bool:
        """
        Return True if streaming responses are supported.
        """

        return self.supports(AICapability.STREAMING)

    def supports_json_mode(self) -> bool:
        """
        Return True if structured JSON generation is supported.
        """

        return self.supports(AICapability.JSON_MODE)

    def supports_function_calling(self) -> bool:
        """
        Return True if function/tool calling is supported.
        """

        return self.supports(AICapability.FUNCTION_CALLING)

    def supports_vision(self) -> bool:
        """
        Return True if multimodal vision is supported.
        """

        return self.supports(AICapability.VISION)

    # ------------------------------------------------------------------
    # Convenience Methods
    # ------------------------------------------------------------------

    def create_request(
        self,
        *,
        job: AIJob,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AIRequest:
        """
        Convenience factory for creating normalized requests.
        """

        return AIRequest(
            job=job,
            prompt=prompt,
            system_prompt=system_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            metadata=dict(metadata or {}),
        )

    # ------------------------------------------------------------------
    # Client Information
    # ------------------------------------------------------------------

    def info(self) -> Dict[str, Any]:
        """
        Return a comprehensive description of this client.
        """

        return {
            "provider": self.provider.value,
            "provider_name": self.provider_name,
            "default_model": self.default_model(),
            "available": self.is_available(),
            "health": self.health_check().status.value,
            "capabilities": [capability.value for capability in self.capabilities()],
            "diagnostics": self.diagnostics(),
        }


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    "AIClient",
    "AIProvider",
    "AICapability",
    "AIClientStatus",
    "AIHealthResult",
    "AIModelInfo",
    "AIRequest",
    "AIResponse",
]
