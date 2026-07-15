"""
Question Factory OS v2.1
------------------------

Prompt Builder

Responsibilities
----------------
• Select prompt templates
• Build rendering variables
• Render prompts
• Assemble PromptPackage objects
• Attach manufacturing metadata
• Estimate prompt size

PromptBuilder is the bridge between the Manufacturing Layer
and the AI Layer.

Author:
Question Factory OS
"""

from __future__ import annotations

import logging
import time

from typing import Any
from typing import Dict
from typing import Optional

from factory.ai.ai_job import AIJob
from factory.ai.models.prompt_package import (
    PromptPackage,
    create_prompt_package,
)
from factory.ai.prompt_templates import (
    PromptCategory,
    PromptRegistry,
    PromptTemplate,
    PromptRenderResult,
)

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Prompt Builder
# ----------------------------------------------------------------------


class PromptBuilder:
    """
    Builds PromptPackage objects from AIJob instances.
    """

    def __init__(
        self,
        registry: PromptRegistry,
    ) -> None:
        """
        Parameters
        ----------
        registry:
            Prompt template registry.
        """

        self._registry = registry

        logger.info("PromptBuilder initialized.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(
        self,
        job: AIJob,
        *,
        category: PromptCategory = (PromptCategory.QUESTION_GENERATION),
        template_version: Optional[str] = None,
        additional_variables: Optional[Dict[str, Any]] = None,
    ) -> PromptPackage:
        """
        Build a PromptPackage from an AIJob.
        """

        started = time.perf_counter()

        template = self._select_template(
            category=category,
            version=template_version,
        )

        variables = self._build_variables(
            job=job,
            additional_variables=additional_variables,
        )

        render_result = self._render(
            template=template,
            variables=variables,
        )

        metadata = self._build_metadata(
            job=job,
            template=template,
            render_result=render_result,
        )

        elapsed_ms = (time.perf_counter() - started) * 1000.0

        return create_prompt_package(
            prompt=render_result.rendered_prompt,
            system_prompt=metadata.get("system_prompt"),
            template_id=template.id,
            template_version=template.version,
            template_category=template.category.value,
            variables=variables,
            metadata=metadata,
            estimated_tokens=self._estimate_tokens(render_result.rendered_prompt),
            render_duration_ms=round(
                elapsed_ms,
                2,
            ),
        )

    # ------------------------------------------------------------------
    # Template Selection
    # ------------------------------------------------------------------

    def _select_template(
        self,
        *,
        category: PromptCategory,
        version: Optional[str],
    ) -> PromptTemplate:
        """
        Select the appropriate prompt template.
        """

        template = self._registry.find(
            category=category,
            version=version,
        )

        if template is None:
            raise ValueError(
                "No prompt template found for " f"category '{category.value}'."
            )

        return template

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(
        self,
        *,
        template: PromptTemplate,
        variables: Dict[str, Any],
    ) -> PromptRenderResult:
        """
        Render the selected template.
        """

        result = self._registry.render_template(
            template=template,
            variables=variables,
        )

        if not result.success:

            missing = ", ".join(result.missing_variables)

            raise ValueError(
                "Prompt rendering failed. " f"Missing variables: {missing}"
            )

        return result

    # ------------------------------------------------------------------
    # Variable Construction
    # ------------------------------------------------------------------

    def _build_variables(
        self,
        *,
        job: AIJob,
        additional_variables: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Build the rendering variables.

        Standard variables are extracted from the AIJob.
        Caller-supplied variables override defaults.
        """

        variables = self._base_variables(job)

        if additional_variables:
            variables.update(additional_variables)

        return variables

    def _base_variables(
        self,
        job: AIJob,
    ) -> Dict[str, Any]:
        """
        Build the default variable dictionary from the AIJob.

        This method intentionally remains provider-independent.
        """

        variables: Dict[str, Any] = {}

        #
        # Common identifiers
        #

        variables["job_id"] = getattr(
            job,
            "job_id",
            "",
        )

        variables["request_id"] = getattr(
            job,
            "request_id",
            "",
        )

        variables["project"] = getattr(
            job,
            "project",
            "",
        )

        #
        # Prompt information
        #

        variables["prompt"] = getattr(
            job,
            "prompt",
            "",
        )

        variables["system_prompt"] = getattr(
            job,
            "system_prompt",
            "",
        )

        #
        # Manufacturing context
        #

        variables["subject"] = getattr(
            job,
            "subject",
            "",
        )

        variables["chapter"] = getattr(
            job,
            "chapter",
            "",
        )

        variables["subtopic"] = getattr(
            job,
            "subtopic",
            "",
        )

        variables["difficulty"] = getattr(
            job,
            "difficulty",
            "",
        )

        variables["batch"] = getattr(
            job,
            "batch",
            "",
        )

        variables["question_count"] = getattr(
            job,
            "question_count",
            1,
        )

        variables["blueprint"] = getattr(
            job,
            "blueprint",
            "",
        )

        return variables

    # ------------------------------------------------------------------
    # Metadata Construction
    # ------------------------------------------------------------------

    def _build_metadata(
        self,
        *,
        job: AIJob,
        template: PromptTemplate,
        render_result: PromptRenderResult,
    ) -> Dict[str, Any]:
        """
        Build PromptPackage metadata.
        """

        metadata: Dict[str, Any] = {
            "template_id": template.id,
            "template_version": template.version,
            "template_category": template.category.value,
            "builder": self.__class__.__name__,
        }

        metadata.update(render_result.metadata)

        #
        # Optional runtime identifiers
        #

        job_id = getattr(job, "job_id", None)

        if job_id:
            metadata["job_id"] = job_id

        request_id = getattr(
            job,
            "request_id",
            None,
        )

        if request_id:
            metadata["request_id"] = request_id

        return metadata

    # ------------------------------------------------------------------
    # Token Estimation
    # ------------------------------------------------------------------

    def _estimate_tokens(
        self,
        prompt: str,
    ) -> int:
        """
        Estimate prompt tokens.

        This is intentionally a lightweight approximation.
        A provider-specific tokenizer may replace this in
        future releases.
        """

        if not prompt:
            return 0

        return max(
            1,
            len(prompt) // 4,
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_template(
        self,
        template: PromptTemplate,
    ) -> None:
        """
        Validate a prompt template before rendering.
        """

        if not template.id.strip():
            raise ValueError("Template identifier cannot be empty.")

        if not template.template.strip():
            raise ValueError("Template content cannot be empty.")

    def validate_variables(
        self,
        template: PromptTemplate,
        variables: Dict[str, Any],
    ) -> None:
        """
        Validate rendering variables.

        Delegates variable verification to the registry.
        """

        result = self._registry.render_template(
            template=template,
            variables=variables,
        )

        if not result.success:

            missing = ", ".join(result.missing_variables)

            raise ValueError("Missing template variables: " f"{missing}")

    # ------------------------------------------------------------------
    # Convenience Builders
    # ------------------------------------------------------------------

    def build_generation_prompt(
        self,
        job: AIJob,
        *,
        template_version: Optional[str] = None,
        additional_variables: Optional[Dict[str, Any]] = None,
    ) -> PromptPackage:
        """
        Build a question-generation prompt.
        """

        return self.build(
            job=job,
            category=PromptCategory.QUESTION_GENERATION,
            template_version=template_version,
            additional_variables=additional_variables,
        )

    def build_repair_prompt(
        self,
        job: AIJob,
        *,
        template_version: Optional[str] = None,
        additional_variables: Optional[Dict[str, Any]] = None,
    ) -> PromptPackage:
        """
        Build a repair prompt.
        """

        return self.build(
            job=job,
            category=PromptCategory.QUESTION_REPAIR,
            template_version=template_version,
            additional_variables=additional_variables,
        )

    def build_validation_prompt(
        self,
        job: AIJob,
        *,
        template_version: Optional[str] = None,
        additional_variables: Optional[Dict[str, Any]] = None,
    ) -> PromptPackage:
        """
        Build a validation prompt.
        """

        return self.build(
            job=job,
            category=PromptCategory.VALIDATION,
            template_version=template_version,
            additional_variables=additional_variables,
        )

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(self) -> Dict[str, Any]:
        """
        Return PromptBuilder diagnostics.
        """

        return {
            "builder": self.__class__.__name__,
            "registry_valid": self._registry.validate(),
            "registered_templates": self._registry.size(),
            "categories": [category.value for category in self._registry.categories()],
        }

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        """
        Return a concise summary of the builder.
        """

        return {
            "registered_templates": self._registry.size(),
            "registry_valid": self._registry.validate(),
        }

    # ------------------------------------------------------------------
    # Registry Access
    # ------------------------------------------------------------------

    def template(
        self,
        *,
        category: PromptCategory,
        version: Optional[str] = None,
    ) -> PromptTemplate:
        """
        Return the selected prompt template.
        """

        template = self._select_template(
            category=category,
            version=version,
        )

        self.validate_template(template)

        return template

    def template_exists(
        self,
        *,
        category: PromptCategory,
        version: Optional[str] = None,
    ) -> bool:
        """
        Return True if a matching template exists.
        """

        return (
            self._registry.find(
                category=category,
                version=version,
            )
            is not None
        )

    def available_categories(
        self,
    ) -> list[PromptCategory]:
        """
        Return all registered template categories.
        """

        return self._registry.categories()

    # ------------------------------------------------------------------
    # Rendering Statistics
    # ------------------------------------------------------------------

    def estimate_prompt_tokens(
        self,
        prompt: str,
    ) -> int:
        """
        Public wrapper around the internal token estimator.
        """

        return self._estimate_tokens(prompt)

    def estimate_package_tokens(
        self,
        package: PromptPackage,
    ) -> int:
        """
        Estimate the token count for a PromptPackage.
        """

        return self._estimate_tokens(package.prompt)

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def healthy(self) -> bool:
        """
        Return True if the PromptBuilder is operational.
        """

        return self._registry.validate() and self._registry.size() > 0

    # ------------------------------------------------------------------
    # Registry Information
    # ------------------------------------------------------------------

    def template_count(self) -> int:
        """
        Return the number of registered templates.
        """

        return self._registry.size()

    def registry_statistics(
        self,
    ) -> Dict[str, Any]:
        """
        Return prompt registry statistics.
        """

        return self._registry.statistics()

    def registry_description(
        self,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Return a serializable description of all
        registered templates.
        """

        return self._registry.describe()


# ----------------------------------------------------------------------
# Factory Helper
# ----------------------------------------------------------------------


def create_prompt_builder(
    registry: PromptRegistry,
) -> PromptBuilder:
    """
    Create a production-ready PromptBuilder.

    Parameters
    ----------
    registry:
        Prompt template registry.

    Returns
    -------
    PromptBuilder
    """

    builder = PromptBuilder(
        registry=registry,
    )

    logger.info("Production PromptBuilder created.")

    return builder


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    "PromptBuilder",
    "create_prompt_builder",
]
