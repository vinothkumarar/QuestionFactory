"""
Question Factory OS v2.1
------------------------

AI Client Factory

Responsibilities
----------------
• Create AI provider clients.
• Maintain provider registry.
• Support runtime registration.
• Support dependency injection.
• Keep AIEngine provider-independent.

The factory never imports provider SDKs directly.
Concrete provider implementations register themselves.

Author:
Question Factory OS
"""

from __future__ import annotations

import logging

from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Type

from Engine.factory.ai.ai_client import AIClient
from Engine.factory.ai.ai_client import AIProvider

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Type Definitions
# ----------------------------------------------------------------------

ClientClass = Type[AIClient]

ClientBuilder = Callable[..., AIClient]


# ----------------------------------------------------------------------
# Client Factory
# ----------------------------------------------------------------------


class ClientFactory:
    """
    Enterprise AI client factory.

    Features
    --------
    • Provider registry
    • Runtime registration
    • Lazy client creation
    • Dependency Injection friendly
    • Plugin friendly
    • Thread-safe read operations

    Provider implementations register themselves during
    application startup.
    """

    def __init__(self) -> None:

        self._client_classes: Dict[
            AIProvider,
            ClientClass,
        ] = {}

        self._builders: Dict[
            AIProvider,
            ClientBuilder,
        ] = {}

        logger.info("ClientFactory initialized.")

    # ------------------------------------------------------------------
    # Registration API
    # ------------------------------------------------------------------

    def register_client(
        self,
        provider: AIProvider,
        client_class: ClientClass,
        *,
        replace: bool = False,
    ) -> None:
        """
        Register an AI client implementation.

        Parameters
        ----------
        provider:
            Provider identifier.

        client_class:
            Concrete subclass of AIClient.

        replace:
            Replace an existing registration if True.
        """

        if not issubclass(client_class, AIClient):
            raise TypeError(f"{client_class!r} must inherit from AIClient.")

        if provider in self._client_classes and not replace:
            raise ValueError(f"Provider '{provider.value}' is already registered.")

        self._client_classes[provider] = client_class

        logger.info(
            "Registered client '%s' for provider '%s'.",
            client_class.__name__,
            provider.value,
        )

    def register_builder(
        self,
        provider: AIProvider,
        builder: ClientBuilder,
        *,
        replace: bool = False,
    ) -> None:
        """
        Register a custom client builder.

        Builders are useful when provider construction
        requires dependency injection or complex setup.
        """

        if provider in self._builders and not replace:
            raise ValueError(f"Builder already registered for '{provider.value}'.")

        self._builders[provider] = builder

        logger.info(
            "Registered builder for provider '%s'.",
            provider.value,
        )

    # ------------------------------------------------------------------
    # Unregistration
    # ------------------------------------------------------------------

    def unregister(
        self,
        provider: AIProvider,
    ) -> bool:
        """
        Remove all registrations associated with a provider.

        Returns
        -------
        bool
            True if anything was removed.
        """

        removed = False

        if provider in self._client_classes:
            del self._client_classes[provider]
            removed = True

        if provider in self._builders:
            del self._builders[provider]
            removed = True

        if removed:
            logger.info(
                "Unregistered provider '%s'.",
                provider.value,
            )

        return removed

    def clear(self) -> None:
        """
        Remove every registered provider.

        Primarily intended for testing.
        """

        self._client_classes.clear()
        self._builders.clear()

        logger.info("ClientFactory registry cleared.")

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def is_registered(
        self,
        provider: AIProvider,
    ) -> bool:
        """
        Return True if a provider has either a client class
        or a builder registered.
        """

        return provider in self._client_classes or provider in self._builders

    def registered_providers(
        self,
    ) -> list[AIProvider]:
        """
        Return all registered providers.
        """

        providers = set(self._client_classes.keys()) | set(self._builders.keys())

        return sorted(
            providers,
            key=lambda item: item.value,
        )

    def registered_client_class(
        self,
        provider: AIProvider,
    ) -> Optional[ClientClass]:
        """
        Return the registered client class, if any.
        """

        return self._client_classes.get(provider)

    def registered_builder(
        self,
        provider: AIProvider,
    ) -> Optional[ClientBuilder]:
        """
        Return the registered builder, if any.
        """

        return self._builders.get(provider)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> bool:
        """
        Validate the internal registry.

        Returns
        -------
        bool
            True if the registry is valid.
        """

        for provider, client_class in self._client_classes.items():

            if not issubclass(client_class, AIClient):
                logger.error(
                    "Invalid client registered for '%s'.",
                    provider.value,
                )
                return False

        for provider, builder in self._builders.items():

            if not callable(builder):
                logger.error(
                    "Builder for '%s' is not callable.",
                    provider.value,
                )
                return False

        return True

    # ------------------------------------------------------------------
    # Client Creation
    # ------------------------------------------------------------------

    def create(
        self,
        provider: AIProvider,
        *args: Any,
        **kwargs: Any,
    ) -> AIClient:
        """
        Create a client instance for the requested provider.

        Resolution order
        ----------------
        1. Registered builder
        2. Registered client class

        Parameters
        ----------
        provider:
            Provider to instantiate.

        Returns
        -------
        AIClient
            Newly constructed client instance.

        Raises
        ------
        ValueError
            If the provider is not registered.

        TypeError
            If the constructed object is not an AIClient.
        """

        logger.debug(
            "Creating AI client for provider '%s'.",
            provider.value,
        )

        builder = self._builders.get(provider)

        if builder is not None:
            client = builder(*args, **kwargs)

            self._validate_client_instance(
                provider,
                client,
            )

            logger.debug("Client created using registered builder.")

            return client

        client_class = self._client_classes.get(provider)

        if client_class is None:
            raise ValueError(
                f"No client registered for provider " f"'{provider.value}'."
            )

        client = client_class(*args, **kwargs)

        self._validate_client_instance(
            provider,
            client,
        )

        logger.debug("Client created using registered class.")

        return client

    # ------------------------------------------------------------------
    # Internal Validation
    # ------------------------------------------------------------------

    def _validate_client_instance(
        self,
        provider: AIProvider,
        client: AIClient,
    ) -> None:
        """
        Ensure the returned object is a valid AIClient.
        """

        if not isinstance(client, AIClient):
            raise TypeError(
                f"Factory returned invalid client for " f"'{provider.value}'."
            )

    # ------------------------------------------------------------------
    # Safe Creation
    # ------------------------------------------------------------------

    def try_create(
        self,
        provider: AIProvider,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[AIClient]:
        """
        Attempt to create a client.

        Returns None instead of raising an exception.
        """

        try:
            return self.create(
                provider,
                *args,
                **kwargs,
            )

        except Exception:
            logger.exception(
                "Unable to create client '%s'.",
                provider.value,
            )

            return None

    # ------------------------------------------------------------------
    # Batch Creation
    # ------------------------------------------------------------------

    def create_all(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Dict[AIProvider, AIClient]:
        """
        Create one client for every registered provider.

        Providers that fail to construct are skipped.
        """

        clients: Dict[
            AIProvider,
            AIClient,
        ] = {}

        for provider in self.registered_providers():

            client = self.try_create(
                provider,
                *args,
                **kwargs,
            )

            if client is not None:
                clients[provider] = client

        return clients

    # ------------------------------------------------------------------
    # Availability
    # ------------------------------------------------------------------

    def available_providers(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> list[AIProvider]:
        """
        Return providers that are currently available.

        Providers that cannot be created or fail their
        availability check are excluded.
        """

        available: list[AIProvider] = []

        for provider in self.registered_providers():

            client = self.try_create(
                provider,
                *args,
                **kwargs,
            )

            if client is None:
                continue

            try:
                if client.is_available():
                    available.append(provider)
            except Exception:
                logger.exception(
                    "Availability check failed for '%s'.",
                    provider.value,
                )

        return available

    # ------------------------------------------------------------------
    # Default Provider Resolution
    # ------------------------------------------------------------------

    def default_provider(self) -> Optional[AIProvider]:
        """
        Return the default provider.

        Current implementation returns the first registered
        provider in deterministic order.

        Future versions may load this value from configuration.
        """

        providers = self.registered_providers()

        if not providers:
            return None

        return providers[0]

    # ------------------------------------------------------------------
    # Health & Diagnostics
    # ------------------------------------------------------------------

    def health(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Return health information for all registered providers.

        Providers that fail construction or health checks are
        reported individually without affecting the overall result.
        """

        providers: Dict[str, Dict[str, Any]] = {}

        healthy = 0
        unhealthy = 0

        for provider in self.registered_providers():

            try:
                client = self.create(
                    provider,
                    *args,
                    **kwargs,
                )

                result = client.health_check()

                providers[provider.value] = {
                    "healthy": result.healthy,
                    "status": result.status.value,
                    "latency_ms": result.latency_ms,
                    "message": result.message,
                }

                if result.healthy:
                    healthy += 1
                else:
                    unhealthy += 1

            except Exception as ex:

                providers[provider.value] = {
                    "healthy": False,
                    "status": "error",
                    "message": str(ex),
                }

                unhealthy += 1

                logger.exception(
                    "Health check failed for '%s'.",
                    provider.value,
                )

        return {
            "healthy": unhealthy == 0,
            "registered_providers": len(self.registered_providers()),
            "healthy_providers": healthy,
            "unhealthy_providers": unhealthy,
            "providers": providers,
        }

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def statistics(self) -> Dict[str, Any]:
        """
        Return registry statistics.
        """

        return {
            "registered_clients": len(self._client_classes),
            "registered_builders": len(self._builders),
            "registered_providers": len(self.registered_providers()),
            "valid": self.validate(),
        }

    # ------------------------------------------------------------------
    # Registry Export
    # ------------------------------------------------------------------

    def describe(self) -> Dict[str, Dict[str, Optional[str]]]:
        """
        Return a serializable description of the registry.

        This method intentionally exports names only and
        does not expose implementation details.
        """

        result: Dict[str, Dict[str, Optional[str]]] = {}

        for provider in self.registered_providers():

            client_class = self._client_classes.get(provider)
            builder = self._builders.get(provider)

            result[provider.value] = {
                "client_class": (client_class.__name__ if client_class else None),
                "builder": (
                    getattr(
                        builder,
                        "__name__",
                        builder.__class__.__name__,
                    )
                    if builder
                    else None
                ),
            }

        return result

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def supports(
        self,
        provider: AIProvider,
    ) -> bool:
        """
        Return True if the provider is registered.
        """

        return self.is_registered(provider)

    def __contains__(
        self,
        provider: AIProvider,
    ) -> bool:
        """
        Enable:

            if AIProvider.OPENAI in factory:
                ...
        """

        return self.supports(provider)

    def __len__(self) -> int:
        """
        Return the number of registered providers.
        """

        return len(self.registered_providers())

    def __iter__(self):
        """
        Iterate over registered providers.
        """

        return iter(self.registered_providers())

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"providers={len(self)}, "
            f"clients={len(self._client_classes)}, "
            f"builders={len(self._builders)})"
        )

    __str__ = __repr__


# ----------------------------------------------------------------------
# Factory Helper
# ----------------------------------------------------------------------


def create_client_factory() -> ClientFactory:
    """
    Create a production-ready ClientFactory.

    This helper centralizes construction and provides a single
    extension point for future startup initialization such as:

    - Plugin discovery
    - Built-in provider registration
    - Configuration loading
    - Dependency injection integration

    No providers are automatically registered. Provider modules
    should register themselves during application startup.
    """

    factory = ClientFactory()

    logger.info("Production ClientFactory created.")

    return factory


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    "ClientFactory",
    "ClientBuilder",
    "ClientClass",
    "create_client_factory",
]
