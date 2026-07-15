"""
Question Factory OS v2.1
------------------------

Prompt Builder

Responsible for constructing PromptPackage
instances from AIJob objects using the
PromptRegistry.

Responsibilities
----------------
• Template selection
• Variable construction
• Prompt rendering
• PromptPackage creation
• Metadata generation
• Token estimation

Provider agnostic.

Author:
Question Factory OS
"""

from __future__ import annotations

import logging
import time

from typing import Any
from typing import Dict
from typing import Optional

from Engine.factory.ai.models.ai_job import AIJob
from Engine.factory.ai.models.prompt_package import (
    PromptPackage,
    create_prompt_package,
)
from Engine.factory.ai.prompt_templates import (
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
    Builds PromptPackage objects from AIJob
    instances.

    PromptBuilder coordinates template lookup,
    rendering and PromptPackage construction,
    while PromptRegistry owns template storage
    and rendering.
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

        logger.info(
            "PromptBuilder initialized."
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def registry(
        self,
    ) -> PromptRegistry:
        """
        Return the underlying prompt registry.
        """

        return self._registry

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(
        self,
        job: AIJob,
        *,
        category: PromptCategory = (
            PromptCategory.QUESTION_GENERATION
        ),
        template_version: Optional[str] = None,
        additional_variables: Optional[
            Dict[str, Any]
        ] = None,
    ) -> PromptPackage:
        """
        Build a PromptPackage from an AIJob.
        """

        started = time.perf_counter()

        template = self._registry.find(
            category=category,
            version=template_version,
        )

        if template is None:

            raise ValueError(
                "No prompt template found "
                f"for category "
                f"'{category.value}'."
            )

        variables = self._build_variables(
            job=job,
            additional_variables=additional_variables,
        )
        render_result = (
            self._registry.render_template(
                category=category,
                values=variables,
                version=template_version,
            )
        )

        if not render_result.success:

            missing = ", ".join(
                render_result.missing_variables
            )

            raise ValueError(
                "Prompt rendering failed. "
                f"Missing variables: {missing}"
            )

        metadata = self._build_metadata(
            job=job,
            template=template,
            render_result=render_result,
        )

        elapsed_ms = (
            time.perf_counter() - started
        ) * 1000.0

        return create_prompt_package(
            prompt=render_result.rendered_prompt,
            system_prompt=metadata.get(
                "system_prompt"
            ),
            template_id=template.id,
            template_version=template.version,
            template_category=template.category.value,
            variables=variables,
            metadata=metadata,
            estimated_tokens=self._estimate_tokens(
                render_result.rendered_prompt
            ),
            render_duration_ms=round(
                elapsed_ms,
                2,
            ),
        )

    # ------------------------------------------------------------------
    # Variable Construction
    # ------------------------------------------------------------------

    def _build_variables(
        self,
        *,
        job: AIJob,
        additional_variables: Optional[
            Dict[str, Any]
        ],
    ) -> Dict[str, Any]:
        """
        Build the rendering variables.

        Standard variables are extracted
        from the AIJob.

        Caller supplied variables override
        defaults.
        """

        variables = self._base_variables(
            job
        )

        if additional_variables:

            variables.update(
                additional_variables
            )

        return variables

    def _base_variables(
        self,
        job: AIJob,
    ) -> Dict[str, Any]:
        """
        Build the provider-independent
        variable dictionary.
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

        #
        # Optional runtime information
        #

        variables["unit"] = getattr(
            job,
            "unit",
            "",
        )

        variables["chapter_code"] = getattr(
            job,
            "chapter_code",
            "",
        )

        variables["subtopic_code"] = getattr(
            job,
            "subtopic_code",
            "",
        )

        variables["difficulty_level"] = getattr(
            job,
            "difficulty_level",
            "",
        )

        variables["exam"] = getattr(
            job,
            "exam",
            "",
        )

        variables["language"] = getattr(
            job,
            "language",
            "en",
        )

        variables["tags"] = getattr(
            job,
            "tags",
            [],
        )

        variables["metadata"] = getattr(
            job,
            "metadata",
            {},
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
            "builder": self.__class__.__name__,
            "template_id": template.id,
            "template_name": template.name,
            "template_version": template.version,
            "template_category": template.category.value,
            "render_duration_ms": (
                render_result.render_duration_ms
            ),
        }

        metadata.update(
            render_result.metadata
        )

        #
        # Optional runtime identifiers
        #

        job_id = getattr(
            job,
            "job_id",
            None,
        )

        if job_id:

            metadata["job_id"] = job_id

        request_id = getattr(
            job,
            "request_id",
            None,
        )

        if request_id:

            metadata["request_id"] = request_id

        project = getattr(
            job,
            "project",
            None,
        )

        if project:

            metadata["project"] = project

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

        This is intentionally a lightweight
        approximation.

        Provider-specific tokenizers may
        replace this implementation in
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
        Validate a prompt template.
        """

        if not template.id.strip():

            raise ValueError(
                "Template identifier cannot be empty."
            )

        if not template.template.strip():

            raise ValueError(
                "Template content cannot be empty."
            )

    def validate_variables(
        self,
        *,
        category: PromptCategory,
        variables: Dict[str, Any],
        version: Optional[str] = None,
    ) -> None:
        """
        Validate rendering variables.

        Delegates validation to the
        PromptRegistry.
        """

        result = self._registry.render_template(
            category=category,
            values=variables,
            version=version,
        )

        if result.success:
            return

        missing = ", ".join(
            result.missing_variables
        )

        raise ValueError(
            "Missing template variables: "
            f"{missing}"
        )

    # ------------------------------------------------------------------
    # Convenience Builders
    # ------------------------------------------------------------------

    def build_generation_prompt(
        self,
        job: AIJob,
        *,
        template_version: Optional[str] = None,
        additional_variables: Optional[
            Dict[str, Any]
        ] = None,
    ) -> PromptPackage:
        """
        Build a question generation prompt.
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
        additional_variables: Optional[
            Dict[str, Any]
        ] = None,
    ) -> PromptPackage:
        """
        Build a question repair prompt.
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
        additional_variables: Optional[
            Dict[str, Any]
        ] = None,
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

    def diagnostics(
        self,
    ) -> Dict[str, Any]:
        """
        Return PromptBuilder diagnostics.
        """

        return {
            "component": self.__class__.__name__,
            "healthy": self.healthy(),
            "registry_valid": (
                self._registry.validate()
            ),
            "registered_templates": (
                self._registry.size()
            ),
            "categories": [
                category.value
                for category
                in self._registry.categories()
            ],
        }

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Return a concise PromptBuilder summary.
        """

        return {
            "builder": self.__class__.__name__,
            "registered_templates": (
                self._registry.size()
            ),
            "registry_valid": (
                self._registry.validate()
            ),
        }

    # ------------------------------------------------------------------
    # Template Access
    # ------------------------------------------------------------------

    def template(
        self,
        *,
        category: PromptCategory,
        version: Optional[str] = None,
    ) -> PromptTemplate:
        """
        Return the selected template.
        """

        template = self._registry.find(
            category=category,
            version=version,
        )

        if template is None:

            raise ValueError(
                "No prompt template found "
                f"for category "
                f"'{category.value}'."
            )

        self.validate_template(
            template
        )

        return template

    def template_exists(
        self,
        *,
        category: PromptCategory,
        version: Optional[str] = None,
    ) -> bool:
        """
        Return True if a matching template
        exists.
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
        Return all registered prompt
        categories.
        """

        return self._registry.categories()

    # ------------------------------------------------------------------
    # Token Estimation
    # ------------------------------------------------------------------

    def estimate_prompt_tokens(
        self,
        prompt: str,
    ) -> int:
        """
        Estimate the number of prompt tokens.
        """

        return self._estimate_tokens(
            prompt
        )

    def estimate_package_tokens(
        self,
        package: PromptPackage,
    ) -> int:
        """
        Estimate the token count for a
        PromptPackage.
        """

        return self._estimate_tokens(
            package.prompt
        )
    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def healthy(
        self,
    ) -> bool:
        """
        Return True if the PromptBuilder is
        operational.
        """

        return (
            self._registry.validate()
            and self._registry.size() > 0
        )

    # ------------------------------------------------------------------
    # Registry Information
    # ------------------------------------------------------------------

    def template_count(
        self,
    ) -> int:
        """
        Return the number of registered
        templates.
        """

        return self._registry.size()

    def registry_statistics(
        self,
    ) -> Dict[str, Any]:
        """
        Return PromptRegistry statistics.
        """

        return self._registry.statistics()

    def registry_description(
        self,
    ) -> Dict[str, Any]:
        """
        Return a serializable description of
        the PromptRegistry.
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
    """

    builder = PromptBuilder(
        registry=registry,
    )

    logger.info(
        "Production PromptBuilder created."
    )

    return builder


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    "PromptBuilder",
    "create_prompt_builder",
]
