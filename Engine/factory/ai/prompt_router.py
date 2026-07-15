"""
Question Factory OS v2.1
------------------------

Prompt Router

Responsibilities
----------------
• Central routing point between PromptBuilder and AIEngine.
• Selects the appropriate prompt strategy.
• Keeps AIEngine provider-agnostic.
• Supports future prompt versions.
• Supports provider capability overrides.
• Supports fallback prompt strategies.

The router NEVER calls AI providers directly.

Pipeline

PromptBuilder
      │
      ▼
PromptRouter
      │
      ▼
AIEngine
      │
      ▼
Provider Adapter

Author:
Question Factory OS
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict
from typing import Optional
from typing import Any

from factory.ai.models.ai_job import AIJob

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Prompt Types
# ----------------------------------------------------------------------


class PromptType(str, Enum):
    """
    Supported prompt categories.
    """

    QUESTION_GENERATION = "question_generation"

    QUESTION_REPAIR = "question_repair"

    VALIDATION = "validation"

    QUALITY_REVIEW = "quality_review"

    CSV_EXPORT = "csv_export"

    EXPLANATION = "explanation"

    CUSTOM = "custom"


# ----------------------------------------------------------------------
# Prompt Version
# ----------------------------------------------------------------------


class PromptVersion(str, Enum):
    """
    Versioned prompt templates.
    """

    V1 = "v1"

    V2 = "v2"

    V2_1 = "v2.1"

    LATEST = "latest"


# ----------------------------------------------------------------------
# Routing Decision
# ----------------------------------------------------------------------


@dataclass(slots=True)
class PromptRoutingDecision:
    """
    Immutable routing result.
    """

    prompt_type: PromptType

    version: PromptVersion

    template_name: str

    provider_override: Optional[str]

    metadata: Dict[str, Any]


# ----------------------------------------------------------------------
# Prompt Router
# ----------------------------------------------------------------------


class PromptRouter:
    """
    Enterprise prompt routing component.

    Responsibilities
    ----------------
    • Determine prompt template.
    • Determine prompt version.
    • Select provider overrides.
    • Allow future feature flags.
    • Maintain backward compatibility.

    The router contains NO provider-specific SDK logic.
    """

    DEFAULT_TEMPLATE = "default"

    def __init__(self) -> None:

        self._routes: Dict[PromptType, Dict[PromptVersion, str]] = {}

        self._provider_overrides: Dict[PromptType, str] = {}

        self._register_default_routes()

        logger.info("PromptRouter initialized.")

    # ------------------------------------------------------------------
    # Route Registration
    # ------------------------------------------------------------------

    def _register_default_routes(self) -> None:
        """
        Register the built-in prompt templates.

        Additional templates may be registered by plugins or future
        factory modules without modifying the router itself.
        """

        self.register_route(
            PromptType.QUESTION_GENERATION,
            PromptVersion.V2_1,
            "question_generation_v2_1",
        )

        self.register_route(
            PromptType.QUESTION_GENERATION,
            PromptVersion.LATEST,
            "question_generation_v2_1",
        )

        self.register_route(
            PromptType.QUESTION_REPAIR,
            PromptVersion.V2_1,
            "question_repair_v2_1",
        )

        self.register_route(
            PromptType.QUESTION_REPAIR,
            PromptVersion.LATEST,
            "question_repair_v2_1",
        )

        self.register_route(
            PromptType.VALIDATION,
            PromptVersion.V2_1,
            "validation_v2_1",
        )

        self.register_route(
            PromptType.VALIDATION,
            PromptVersion.LATEST,
            "validation_v2_1",
        )

        self.register_route(
            PromptType.QUALITY_REVIEW,
            PromptVersion.V2_1,
            "quality_review_v2_1",
        )

        self.register_route(
            PromptType.QUALITY_REVIEW,
            PromptVersion.LATEST,
            "quality_review_v2_1",
        )

        self.register_route(
            PromptType.CSV_EXPORT,
            PromptVersion.V2_1,
            "csv_export_v2_1",
        )

        self.register_route(
            PromptType.CSV_EXPORT,
            PromptVersion.LATEST,
            "csv_export_v2_1",
        )

        self.register_route(
            PromptType.EXPLANATION,
            PromptVersion.V2_1,
            "explanation_v2_1",
        )

        self.register_route(
            PromptType.EXPLANATION,
            PromptVersion.LATEST,
            "explanation_v2_1",
        )

        self.register_route(
            PromptType.CUSTOM,
            PromptVersion.LATEST,
            self.DEFAULT_TEMPLATE,
        )

    # ------------------------------------------------------------------
    # Public Registration API
    # ------------------------------------------------------------------

    def register_route(
        self,
        prompt_type: PromptType,
        version: PromptVersion,
        template_name: str,
    ) -> None:
        """
        Register or replace a prompt template.

        This API allows future modules or plugins to extend routing
        behavior without modifying PromptRouter.
        """

        if prompt_type not in self._routes:
            self._routes[prompt_type] = {}

        self._routes[prompt_type][version] = template_name

        logger.debug(
            "Registered prompt route: %s -> %s (%s)",
            prompt_type.value,
            template_name,
            version.value,
        )

    def register_provider_override(
        self,
        prompt_type: PromptType,
        provider_name: str,
    ) -> None:
        """
        Register a preferred provider for a prompt category.

        This is advisory only. AIEngine may ignore the override if the
        requested provider is unavailable.
        """

        self._provider_overrides[prompt_type] = provider_name

        logger.info(
            "Registered provider override '%s' for '%s'",
            provider_name,
            prompt_type.value,
        )

    # ------------------------------------------------------------------
    # Lookup Helpers
    # ------------------------------------------------------------------

    def _resolve_version(
        self,
        version: Optional[PromptVersion],
    ) -> PromptVersion:
        """
        Resolve a version request.

        None always maps to the latest supported prompt version.
        """

        if version is None:
            return PromptVersion.LATEST

        return version

    def _resolve_template(
        self,
        prompt_type: PromptType,
        version: PromptVersion,
    ) -> str:
        """
        Resolve the template name.

        If the requested version does not exist but a LATEST mapping
        exists, the latest mapping is used as a safe fallback.
        """

        versions = self._routes.get(prompt_type)

        if versions is None:
            logger.warning(
                "Prompt type '%s' not registered. " "Using default template.",
                prompt_type.value,
            )
            return self.DEFAULT_TEMPLATE

        if version in versions:
            return versions[version]

        if PromptVersion.LATEST in versions:
            return versions[PromptVersion.LATEST]

        logger.warning(
            "No template registered for %s (%s). " "Using default template.",
            prompt_type.value,
            version.value,
        )

        return self.DEFAULT_TEMPLATE

    def _resolve_provider_override(
        self,
        prompt_type: PromptType,
    ) -> Optional[str]:
        """
        Return an optional provider preference.
        """

        return self._provider_overrides.get(prompt_type)

    # ------------------------------------------------------------------
    # Public Routing API
    # ------------------------------------------------------------------

    def route(
        self,
        prompt_type: PromptType,
        version: Optional[PromptVersion] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> PromptRoutingDecision:
        """
        Resolve a prompt routing decision.

        This method performs no provider calls. It simply determines
        which prompt template should be used and whether a provider
        preference exists.
        """

        resolved_version = self._resolve_version(version)

        template_name = self._resolve_template(
            prompt_type=prompt_type,
            version=resolved_version,
        )

        provider_override = self._resolve_provider_override(prompt_type)

        decision = PromptRoutingDecision(
            prompt_type=prompt_type,
            version=resolved_version,
            template_name=template_name,
            provider_override=provider_override,
            metadata=dict(metadata or {}),
        )

        logger.debug(
            "Prompt routed: type=%s version=%s template=%s provider=%s",
            prompt_type.value,
            resolved_version.value,
            template_name,
            provider_override,
        )

        return decision

    # ------------------------------------------------------------------
    # AIJob Routing
    # ------------------------------------------------------------------

    def route_job(
        self,
        job: AIJob,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> PromptRoutingDecision:
        """
        Build a routing decision directly from an AIJob.

        AIJob remains the authoritative source for the requested
        operation while PromptRouter maps it to a concrete template.
        """

        prompt_type = self._infer_prompt_type(job)

        merged_metadata = self._build_metadata(
            job=job,
            metadata=metadata,
        )

        return self.route(
            prompt_type=prompt_type,
            version=PromptVersion.LATEST,
            metadata=merged_metadata,
        )

    # ------------------------------------------------------------------
    # Metadata Builder
    # ------------------------------------------------------------------

    def _build_metadata(
        self,
        job: AIJob,
        metadata: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Construct routing metadata.

        The returned dictionary accompanies the routing decision and can
        be consumed by PromptBuilder, AIEngine, telemetry, or audit
        components.
        """

        result: Dict[str, Any] = {}

        if metadata:
            result.update(metadata)

        result.setdefault("job_id", getattr(job, "job_id", None))
        result.setdefault("job_type", getattr(job, "job_type", None))
        result.setdefault("priority", getattr(job, "priority", None))
        result.setdefault("provider", getattr(job, "provider", None))
        result.setdefault("model", getattr(job, "model", None))

        return result

    # ------------------------------------------------------------------
    # Prompt Type Inference
    # ------------------------------------------------------------------

    def _infer_prompt_type(
        self,
        job: AIJob,
    ) -> PromptType:
        """
        Infer the prompt category from the AIJob.

        Future AIJob versions may expose a native prompt_type field.
        Until then, inference is performed using common attributes.
        """

        operation = (
            getattr(job, "operation", None) or getattr(job, "job_type", None) or ""
        )

        operation = str(operation).strip().lower()

        mapping = {
            "generate": PromptType.QUESTION_GENERATION,
            "question_generation": PromptType.QUESTION_GENERATION,
            "repair": PromptType.QUESTION_REPAIR,
            "question_repair": PromptType.QUESTION_REPAIR,
            "validate": PromptType.VALIDATION,
            "validation": PromptType.VALIDATION,
            "quality_review": PromptType.QUALITY_REVIEW,
            "review": PromptType.QUALITY_REVIEW,
            "csv_export": PromptType.CSV_EXPORT,
            "export": PromptType.CSV_EXPORT,
            "explanation": PromptType.EXPLANATION,
        }

        prompt_type = mapping.get(operation)

        if prompt_type is not None:
            return prompt_type

        logger.debug(
            "Unknown AIJob operation '%s'; using CUSTOM prompt type.",
            operation,
        )

        return PromptType.CUSTOM

    # ------------------------------------------------------------------
    # Route Inspection
    # ------------------------------------------------------------------

    def has_route(
        self,
        prompt_type: PromptType,
        version: Optional[PromptVersion] = None,
    ) -> bool:
        """
        Returns True if a route exists.
        """

        resolved_version = self._resolve_version(version)

        versions = self._routes.get(prompt_type)

        if not versions:
            return False

        return resolved_version in versions or PromptVersion.LATEST in versions

    def get_registered_versions(
        self,
        prompt_type: PromptType,
    ) -> list[PromptVersion]:
        """
        Return all registered versions for a prompt type.
        """

        versions = self._routes.get(prompt_type)

        if not versions:
            return []

        return sorted(
            versions.keys(),
            key=lambda item: item.value,
        )

    def get_registered_prompt_types(
        self,
    ) -> list[PromptType]:
        """
        Return every registered prompt type.
        """

        return sorted(
            self._routes.keys(),
            key=lambda item: item.value,
        )

    # ------------------------------------------------------------------
    # Route Management
    # ------------------------------------------------------------------

    def unregister_route(
        self,
        prompt_type: PromptType,
        version: PromptVersion,
    ) -> bool:
        """
        Remove a registered route.

        Returns True if a route was removed.
        """

        versions = self._routes.get(prompt_type)

        if not versions:
            return False

        if version not in versions:
            return False

        del versions[version]

        logger.info(
            "Removed prompt route '%s' (%s)",
            prompt_type.value,
            version.value,
        )

        if not versions:
            del self._routes[prompt_type]

        return True

    def clear_provider_override(
        self,
        prompt_type: PromptType,
    ) -> bool:
        """
        Remove an existing provider override.
        """

        if prompt_type not in self._provider_overrides:
            return False

        del self._provider_overrides[prompt_type]

        logger.info(
            "Removed provider override for '%s'",
            prompt_type.value,
        )

        return True

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def validate(self) -> bool:
        """
        Validate internal router configuration.

        Returns
        -------
        bool
            True if the router configuration is valid.
        """

        for prompt_type, versions in self._routes.items():

            if not versions:
                logger.error(
                    "Prompt type '%s' has no registered templates.",
                    prompt_type.value,
                )
                return False

            for version, template in versions.items():

                if not template.strip():
                    logger.error(
                        "Empty template registered for %s (%s).",
                        prompt_type.value,
                        version.value,
                    )
                    return False

        return True

    def health(self) -> Dict[str, Any]:
        """
        Return diagnostic information suitable for
        runtime monitoring.
        """

        return {
            "healthy": self.validate(),
            "registered_prompt_types": len(self._routes),
            "registered_routes": sum(len(item) for item in self._routes.values()),
            "provider_overrides": len(self._provider_overrides),
        }

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def describe_routes(self) -> Dict[str, Dict[str, str]]:
        """
        Return a serializable representation of all routes.

        Useful for diagnostics, runtime dashboards,
        and future REST endpoints.
        """

        result: Dict[str, Dict[str, str]] = {}

        for prompt_type, versions in self._routes.items():

            result[prompt_type.value] = {
                version.value: template for version, template in versions.items()
            }

        return result

    def describe_provider_overrides(
        self,
    ) -> Dict[str, str]:
        """
        Return all registered provider preferences.
        """

        return {
            prompt_type.value: provider
            for prompt_type, provider in self._provider_overrides.items()
        }

    # ------------------------------------------------------------------
    # Convenience Methods
    # ------------------------------------------------------------------

    def supports(
        self,
        prompt_type: PromptType,
    ) -> bool:
        """
        Returns True if the prompt type is supported.
        """

        return prompt_type in self._routes

    def template_for(
        self,
        prompt_type: PromptType,
        version: Optional[PromptVersion] = None,
    ) -> str:
        """
        Return only the template name for callers that do
        not require a complete routing decision.
        """

        resolved_version = self._resolve_version(version)

        return self._resolve_template(
            prompt_type,
            resolved_version,
        )

    # ------------------------------------------------------------------
    # Configuration Import / Export
    # ------------------------------------------------------------------

    def export_configuration(self) -> Dict[str, Any]:
        """
        Export the current router configuration.

        Returns
        -------
        Dict[str, Any]
            Serializable configuration snapshot.
        """

        return {
            "routes": self.describe_routes(),
            "provider_overrides": self.describe_provider_overrides(),
        }

    def import_configuration(
        self,
        configuration: Dict[str, Any],
        *,
        replace: bool = False,
    ) -> None:
        """
        Import a router configuration.

        Parameters
        ----------
        configuration:
            Configuration previously produced by
            export_configuration().

        replace:
            If True, existing routes and provider overrides
            are cleared before importing.
        """

        if replace:
            self._routes.clear()
            self._provider_overrides.clear()

        routes = configuration.get("routes", {})

        for prompt_type_name, versions in routes.items():

            try:
                prompt_type = PromptType(prompt_type_name)
            except ValueError:
                logger.warning(
                    "Ignoring unknown prompt type '%s'.",
                    prompt_type_name,
                )
                continue

            for version_name, template_name in versions.items():

                try:
                    version = PromptVersion(version_name)
                except ValueError:
                    logger.warning(
                        "Ignoring unknown prompt version '%s'.",
                        version_name,
                    )
                    continue

                self.register_route(
                    prompt_type=prompt_type,
                    version=version,
                    template_name=template_name,
                )

        overrides = configuration.get(
            "provider_overrides",
            {},
        )

        for prompt_type_name, provider in overrides.items():

            try:
                prompt_type = PromptType(prompt_type_name)
            except ValueError:
                logger.warning(
                    "Ignoring provider override for " "unknown prompt type '%s'.",
                    prompt_type_name,
                )
                continue

            self.register_provider_override(
                prompt_type=prompt_type,
                provider_name=provider,
            )

    # ------------------------------------------------------------------
    # Object Helpers
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        """
        Return the total number of registered routes.
        """

        return sum(len(versions) for versions in self._routes.values())

    def __contains__(
        self,
        prompt_type: PromptType,
    ) -> bool:
        """
        Enable:
            if PromptType.VALIDATION in router:
                ...
        """

        return self.supports(prompt_type)

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"routes={len(self)}, "
            f"prompt_types={len(self._routes)}, "
            f"provider_overrides="
            f"{len(self._provider_overrides)})"
        )

    __str__ = __repr__


# ----------------------------------------------------------------------
# Factory Function
# ----------------------------------------------------------------------


def create_prompt_router() -> PromptRouter:
    """
    Create a production-ready PromptRouter instance.

    Centralizing construction allows future dependency injection,
    plugin registration, or configuration loading without changing
    callers.
    """

    router = PromptRouter()

    logger.info("Production PromptRouter created.")

    return router


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    "PromptRouter",
    "PromptRoutingDecision",
    "PromptType",
    "PromptVersion",
    "create_prompt_router",
]
