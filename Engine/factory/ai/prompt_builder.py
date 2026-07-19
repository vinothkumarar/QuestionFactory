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
• Manufacturing instruction generation
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
import textwrap
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
    PromptRenderResult,
    PromptTemplate,
)

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Prompt Builder
# ----------------------------------------------------------------------


class PromptBuilder:
    """
    Builds PromptPackage instances from AIJob.

    The PromptBuilder is responsible for:

    • Selecting the correct prompt template.
    • Building the manufacturing instruction.
    • Constructing template variables.
    • Rendering the prompt.
    • Producing a PromptPackage.

    The PromptRegistry owns templates.

    PromptBuilder owns prompt composition.
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

        #
        # Build manufacturing instruction.
        #

        variables["instruction"] = (
            self._build_instruction(
                job=job,
                category=category,
                variables=variables,
            )
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
            system_prompt=variables.get(
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
    # Instruction Builder
    # ------------------------------------------------------------------

    def _build_instruction(
        self,
        *,
        job: AIJob,
        category: PromptCategory,
        variables: Dict[str, Any],
    ) -> str:
        """
        Build the manufacturing instruction
        consumed by PromptRegistry.

        This converts an AIJob into a single
        provider-independent prompt.
        """

        existing_prompt = (
            getattr(job, "prompt", "") or ""
        ).strip()

        #
        # Respect explicitly supplied prompts.
        #

        if existing_prompt:
            return existing_prompt

        if (
            category
            != PromptCategory.QUESTION_GENERATION
        ):
            return ""

        blueprint = variables.get(
            "blueprint",
            "",
        )

        metadata = variables.get(
            "metadata",
            {},
        )

        return textwrap.dedent(
            f"""
            You are an expert examination
            question setter.

            Generate exactly
            {variables.get("question_count", 1)}
            multiple-choice questions.

            Subject:
            {variables.get("subject", "")}

            Unit:
            {variables.get("unit", "")}

            Chapter:
            {variables.get("chapter", "")}

            Subtopic:
            {variables.get("subtopic", "")}

            Difficulty:
            {variables.get("difficulty", "")}

            Blueprint:
            {blueprint}

            Metadata:
            {metadata}

            Requirements

            - Follow the supplied blueprint.
            - Produce original questions.
            - Provide four options.
            - Exactly one correct answer.
            - Include explanation.
            - Return valid JSON only.
            """
        ).strip()

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
        Build template variables.

        Variables originate from the AIJob and
        may be overridden by caller supplied
        values.
        """

        variables = self._base_variables(
            job
        )

        if additional_variables:
            variables.update(
                additional_variables
            )

        #
        # Ensure mandatory prompt variables
        # always exist.
        #

        variables.setdefault(
            "instruction",
            "",
        )

        variables.setdefault(
            "system_prompt",
            "",
        )

        variables.setdefault(
            "prompt",
            "",
        )

        return variables

    def _base_variables(
        self,
        job: AIJob,
    ) -> Dict[str, Any]:
        """
        Build the provider-independent
        variable dictionary from AIJob.
        """

        variables: Dict[str, Any] = {

            #
            # Runtime identifiers
            #

            "job_id": getattr(
                job,
                "job_id",
                "",
            ),

            "request_id": getattr(
                job,
                "request_id",
                "",
            ),

            "project": getattr(
                job,
                "project",
                "",
            ),

            #
            # Existing prompts
            #

            "prompt": getattr(
                job,
                "prompt",
                "",
            ),

            "system_prompt": getattr(
                job,
                "system_prompt",
                "",
            ),

            #
            # Manufacturing context
            #

            "subject": getattr(
                job,
                "subject",
                "",
            ),

            "unit": getattr(
                job,
                "unit",
                "",
            ),

            "chapter": getattr(
                job,
                "chapter",
                "",
            ),

            "subtopic": getattr(
                job,
                "subtopic",
                "",
            ),

            "difficulty": getattr(
                job,
                "difficulty",
                "",
            ),

            "difficulty_level": getattr(
                job,
                "difficulty_level",
                "",
            ),

            "batch": getattr(
                job,
                "batch",
                "",
            ),

            "question_count": getattr(
                job,
                "question_count",
                1,
            ),

            #
            # Blueprint
            #

            "blueprint": getattr(
                job,
                "blueprint",
                "",
            ),

            #
            # Optional identifiers
            #

            "chapter_code": getattr(
                job,
                "chapter_code",
                "",
            ),

            "subtopic_code": getattr(
                job,
                "subtopic_code",
                "",
            ),

            "exam": getattr(
                job,
                "exam",
                "",
            ),

            "language": getattr(
                job,
                "language",
                "en",
            ),

            "tags": getattr(
                job,
                "tags",
                [],
            ),

            "metadata": getattr(
                job,
                "metadata",
                {},
            ),
        }

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

        Metadata is intentionally provider
        independent and useful for diagnostics.
        """

        metadata: Dict[str, Any] = {

            #
            # Builder
            #

            "builder": self.__class__.__name__,

            #
            # Template
            #

            "template_id": template.id,
            "template_name": template.name,
            "template_version": template.version,
            "template_category": (
                template.category.value
            ),

            #
            # Rendering
            #

            "render_duration_ms": (
                render_result.render_duration_ms
            ),

            #
            # Prompt statistics
            #

            "prompt_length": len(
                render_result.rendered_prompt
            ),

            "estimated_tokens": (
                self._estimate_tokens(
                    render_result.rendered_prompt
                )
            ),
        }

        #
        # Merge renderer metadata.
        #

        metadata.update(
            render_result.metadata
        )

        #
        # Runtime identifiers.
        #

        for field in (
            "job_id",
            "request_id",
            "project",
            "subject",
            "unit",
            "chapter",
            "subtopic",
            "difficulty",
            "batch",
            "question_count",
        ):

            value = getattr(
                job,
                field,
                None,
            )

            if value not in (
                None,
                "",
            ):
                metadata[field] = value

        #
        # Merge custom metadata supplied
        # by the AIJob.
        #

        job_metadata = getattr(
            job,
            "metadata",
            None,
        )

        if isinstance(
            job_metadata,
            dict,
        ):
            metadata.update(
                job_metadata
            )

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
            "registered_templates": (
                self._registry.size()
            ),
            "registry_valid": (
                self._registry.validate()
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
            "healthy": self.healthy(),
            "templates": self._registry.size(),
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
        Return a validated template.
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
        Return True if template exists.
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
        Return registered categories.
        """

        return self._registry.categories()

    # ------------------------------------------------------------------
    # Token Helpers
    # ------------------------------------------------------------------

    def estimate_prompt_tokens(
        self,
        prompt: str,
    ) -> int:
        """
        Estimate prompt tokens.
        """

        return self._estimate_tokens(
            prompt
        )

    def estimate_package_tokens(
        self,
        package: PromptPackage,
    ) -> int:
        """
        Estimate PromptPackage tokens.
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
        Return builder health.
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
        Number of registered templates.
        """

        return self._registry.size()

    def registry_statistics(
        self,
    ) -> Dict[str, Any]:
        """
        Return registry statistics.
        """

        return self._registry.statistics()

    def registry_description(
        self,
    ) -> Dict[str, Any]:
        """
        Return registry description.
        """

        return self._registry.describe()


# ----------------------------------------------------------------------
# Factory Helper
# ----------------------------------------------------------------------


def create_prompt_builder(
    registry: PromptRegistry,
) -> PromptBuilder:
    """
    Create a production PromptBuilder.
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
