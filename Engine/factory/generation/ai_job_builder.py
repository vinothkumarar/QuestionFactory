"""
Question Factory OS v2.1

AI Job Builder

Responsible for converting the manufacturing
context into a strongly typed AIJob.

Pipeline
--------
ProductionNode
      +
Blueprint
      +
Runtime
      ↓
 AIJobBuilder
      ↓
    AIJob

This class contains no AI logic.
It only constructs AIJob instances.
"""

from __future__ import annotations

import logging
from typing import Any

from Engine.blueprint.blueprint_model import BlueprintModel
from Engine.factory.ai.models.ai_job import AIJob
from Engine.models.production_node_model import ProductionNodeModel
from Engine.models.runtime_model import RuntimeModel


LOGGER = logging.getLogger(__name__)


class AIJobBuilder:
    """
    Builds AIJob instances from the
    current manufacturing context.
    """

    VERSION = "2.1.0"

    COMPONENT_NAME = "AI Job Builder"

    def __init__(self) -> None:

        self._logger = LOGGER

        self._logger.info(
            "%s initialized.",
            self.COMPONENT_NAME,
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def build(
        self,
        *,
        node: ProductionNodeModel,
        blueprint: BlueprintModel,
        runtime: RuntimeModel,
    ) -> AIJob:
        """
        Build a fully configured AIJob.
        """

        self.validate(
            node=node,
            blueprint=blueprint,
            runtime=runtime,
        )

        metadata = self._build_metadata(
            node=node,
            blueprint=blueprint,
            runtime=runtime,
        )

        payload = self._build_generation_payload(
            node=node,
            blueprint=blueprint,
            runtime=runtime,
        )

        job = AIJob(
            project=getattr(runtime, "project", ""),
            job_type="QUESTION_GENERATION",

            subject=node.location.unit,
            chapter=node.location.chapter,
            subtopic=node.location.subtopic,
            batch=str(node.location.batch_number),
            question_count=node.question_count,

            blueprint=blueprint.blueprint_version,

            metadata={
                "builder_metadata": metadata,
                "generation_payload": payload,
            },
        )

        self._logger.info(
            "AIJob successfully created."
        )

        return job
    # ---------------------------------------------------------
    # Metadata Construction
    # ---------------------------------------------------------

    def _build_metadata(
        self,
        *,
        node: ProductionNodeModel,
        blueprint: BlueprintModel,
        runtime: RuntimeModel,
    ) -> dict[str, Any]:
        """
        Build AI job metadata.

        Metadata identifies the manufacturing
        context but does not contain the
        generation payload.
        """

        return {
            "factory": blueprint.factory.name,
            "factory_version": blueprint.factory.version,
            "blueprint_version": blueprint.blueprint_version,
            "runtime_node": runtime.current_node,
            "unit": node.location.unit,
            "chapter": node.location.chapter,
            "subtopic": node.location.subtopic,
            "set": node.location.set_number,
            "batch": node.location.batch_number,
        }

    # ---------------------------------------------------------
    # Generation Payload
    # ---------------------------------------------------------

    def _build_generation_payload(
        self,
        *,
        node: ProductionNodeModel,
        blueprint: BlueprintModel,
        runtime: RuntimeModel,
    ) -> dict[str, Any]:
        """
        Build the payload consumed by
        the AI subsystem.
        """

        return {
            "production": {
                "question_from": node.question_range.question_from,
                "question_to": node.question_range.question_to,
                "question_count": node.question_count,
            },
            "runtime": {
                "current_node": runtime.current_node,
                "current_batch": runtime.current_batch,
                "checkpoint_enabled": runtime.is_recovery_required,
            },
            "generation": {
                "rules": blueprint.rules.rules,
                "archetypes": blueprint.archetypes.archetypes,
                "schema_version": blueprint.schema_version,
            },
        }
    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        *,
        node: ProductionNodeModel,
        blueprint: BlueprintModel,
        runtime: RuntimeModel,
    ) -> None:
        """
        Validate the manufacturing context before
        constructing an AIJob.
        """

        if node is None:
            raise ValueError(
                "ProductionNodeModel cannot be None."
            )

        if blueprint is None:
            raise ValueError(
                "BlueprintModel cannot be None."
            )

        if runtime is None:
            raise ValueError(
                "RuntimeModel cannot be None."
            )

        self._logger.debug(
            "AIJobBuilder validation successful."
        )

    # ---------------------------------------------------------
    # Component Information
    # ---------------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Builder version.
        """

        return self.VERSION

    @property
    def component_name(
        self,
    ) -> str:
        """
        Human-readable component name.
        """

        return self.COMPONENT_NAME
    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return component health.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(
        self,
    ) -> dict[str, bool]:
        """
        Return supported capabilities.
        """

        return {
            "ai_job_construction": True,
            "metadata_generation": True,
            "payload_generation": True,
            "validation": True,
            "diagnostics": True,
            "provider_independent": True,
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return diagnostic information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "health": self.health(),
            "capabilities": self.capabilities(),
        }
    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        return (
            "AIJobBuilder("
            f"version='{self.version}')"
        )

    def __str__(
        self,
    ) -> str:
        return (
            f"{self.component_name} "
            f"[v{self.version}]"
        )


__all__ = [
    "AIJobBuilder",
]
