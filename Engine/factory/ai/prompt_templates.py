"""
Question Factory OS v2.1
------------------------

Prompt Template Registry

Responsibilities
----------------
• Store prompt templates
• Version prompt assets
• Register templates
• Retrieve templates
• Support future external template loading

PromptBuilder consumes this module to render prompts.

Author:
Question Factory OS
"""

from __future__ import annotations

import logging

from dataclasses import dataclass
from dataclasses import field

from enum import Enum

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Prompt Categories
# ----------------------------------------------------------------------


class PromptCategory(str, Enum):
    """
    Supported prompt categories.
    """

    QUESTION_GENERATION = "question_generation"

    QUESTION_REPAIR = "question_repair"

    VALIDATION = "validation"

    QUALITY_AUDIT = "quality_audit"

    CSV_EXPORT = "csv_export"

    EXPLANATION = "explanation"

    CUSTOM = "custom"


# ----------------------------------------------------------------------
# Prompt Template
# ----------------------------------------------------------------------


@dataclass(slots=True)
class PromptTemplate:
    """
    Immutable prompt definition.
    """

    id: str

    name: str

    category: PromptCategory

    version: str

    description: str

    template: str

    variables: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


# ----------------------------------------------------------------------
# Prompt Registry
# ----------------------------------------------------------------------


class PromptRegistry:
    """
    Registry of prompt templates.

    Templates are versioned assets that may later be loaded
    from Markdown, YAML, or a database.
    """

    def __init__(self) -> None:

        self._templates: Dict[
            str,
            PromptTemplate,
        ] = {}

        logger.info("PromptRegistry initialized.")

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        template: PromptTemplate,
        *,
        replace: bool = False,
    ) -> None:
        """
        Register a prompt template.
        """

        if not replace and template.id in self._templates:
            raise ValueError(
                f"Prompt template '{template.id}' " f"is already registered."
            )

        self._templates[template.id] = template

        logger.debug(
            "Registered prompt template '%s'.",
            template.id,
        )

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(
        self,
        template_id: str,
    ) -> PromptTemplate:
        """
        Retrieve a template by its identifier.
        """

        try:
            return self._templates[template_id]

        except KeyError as ex:
            raise KeyError(f"Unknown prompt template '{template_id}'.") from ex

    # ------------------------------------------------------------------
    # Version Helpers
    # ------------------------------------------------------------------

    def _version_key(
        self,
        version: str,
    ) -> tuple[int, ...]:
        """
        Convert a dotted version string into a sortable tuple.

        Examples
        --------
        "2.1"   -> (2, 1)
        "2.10"  -> (2, 10)
        "10.0"  -> (10, 0)

        Invalid versions sort before valid semantic versions.
        """

        try:
            return tuple(int(part) for part in version.split("."))

        except ValueError:

            logger.warning(
                "Invalid template version '%s'.",
                version,
            )

            return (0,)

    def find(
        self,
        *,
        category: PromptCategory,
        version: Optional[str] = None,
    ) -> Optional[PromptTemplate]:
        """
        Locate a template by category and optional version.

        If a version is supplied, an exact match is returned.

        If version is omitted, the latest semantic version
        is returned.
        """

        matches = [
            template
            for template in self._templates.values()
            if template.category == category
        ]

        if not matches:
            return None

        if version is not None:

            for template in matches:

                if template.version == version:
                    return template

            return None

        return sorted(
            matches,
            key=lambda item: self._version_key(item.version),
        )[-1]

    # ------------------------------------------------------------------
    # Removal
    # ------------------------------------------------------------------

    def unregister(
        self,
        template_id: str,
    ) -> bool:
        """
        Remove a registered template.
        """

        if template_id not in self._templates:
            return False

        del self._templates[template_id]

        logger.info(
            "Removed prompt template '%s'.",
            template_id,
        )

        return True

    def clear(self) -> None:
        """
        Remove every registered template.

        Primarily intended for testing.
        """

        self._templates.clear()

        logger.info("Prompt registry cleared.")

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def contains(
        self,
        template_id: str,
    ) -> bool:
        """
        Return True if the template exists.
        """

        return template_id in self._templates

    def templates(
        self,
    ) -> List[PromptTemplate]:
        """
        Return every registered template.
        """

        return sorted(
            self._templates.values(),
            key=lambda item: (
                item.category.value,
                self._version_key(item.version),
                item.id,
            ),
        )

    def categories(
        self,
    ) -> List[PromptCategory]:
        """
        Return all categories currently represented in the
        registry.
        """

        return sorted(
            {template.category for template in self._templates.values()},
            key=lambda item: item.value,
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> bool:
        """
        Validate the registry contents.
        """

        for template in self._templates.values():

            if not template.id.strip():
                return False

            if not template.name.strip():
                return False

            if not template.template.strip():
                return False

        return True


# ----------------------------------------------------------------------
# Render Result
# ----------------------------------------------------------------------


@dataclass(slots=True)
class PromptRenderResult:
    """
    Result of rendering a prompt template.
    """

    success: bool

    rendered_prompt: str

    missing_variables: List[str] = field(default_factory=list)

    unused_variables: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ----------------------------------------------------------------------
    # Rendering
    # ----------------------------------------------------------------------

    def render(
        self,
        template_id: str,
        variables: Dict[str, Any],
    ) -> PromptRenderResult:
        """
        Render a registered prompt template.
        """

        template = self.get(template_id)

        missing = self._missing_variables(
            template,
            variables,
        )

        unused = self._unused_variables(
            template,
            variables,
        )

        if missing:

            return PromptRenderResult(
                success=False,
                rendered_prompt="",
                missing_variables=missing,
                unused_variables=unused,
                metadata={
                    "template": template.id,
                },
            )

        rendered = template.template.format(**variables)

        return PromptRenderResult(
            success=True,
            rendered_prompt=rendered,
            unused_variables=unused,
            metadata={
                "template": template.id,
                "version": template.version,
                "category": template.category.value,
            },
        )

    # ------------------------------------------------------------------
    # Variable Validation
    # ------------------------------------------------------------------

    def _missing_variables(
        self,
        template: PromptTemplate,
        variables: Dict[str, Any],
    ) -> List[str]:
        """
        Return required variables that are absent.
        """

        missing: List[str] = []

        for variable in template.variables:

            if variable not in variables:

                missing.append(variable)

        return sorted(missing)

    def _unused_variables(
        self,
        template: PromptTemplate,
        variables: Dict[str, Any],
    ) -> List[str]:
        """
        Return supplied variables that are not referenced
        by the template definition.
        """

        unused = []

        allowed = set(template.variables)

        for variable in variables.keys():

            if variable not in allowed:

                unused.append(variable)

        return sorted(unused)

    # ------------------------------------------------------------------
    # Template Inspection
    # ------------------------------------------------------------------

    def variables(
        self,
        template_id: str,
    ) -> List[str]:
        """
        Return the variables required by a template.
        """

        return list(self.get(template_id).variables)

    def description(
        self,
        template_id: str,
    ) -> str:
        """
        Return the template description.
        """

        return self.get(template_id).description

    def version(
        self,
        template_id: str,
    ) -> str:
        """
        Return the template version.
        """

        return self.get(template_id).version

    # ------------------------------------------------------------------
    # Direct Template Rendering
    # ------------------------------------------------------------------

    def render_template(
        self,
        template: PromptTemplate,
        variables: Dict[str, Any],
    ) -> PromptRenderResult:
        """
        Render a PromptTemplate instance directly.

        This avoids a second registry lookup when the caller
        already has a template instance.
        """

        missing = self._missing_variables(
            template,
            variables,
        )

        unused = self._unused_variables(
            template,
            variables,
        )

        if missing:

            return PromptRenderResult(
                success=False,
                rendered_prompt="",
                missing_variables=missing,
                unused_variables=unused,
                metadata={
                    "template": template.id,
                    "version": template.version,
                },
            )

        rendered = template.template.format(**variables)

        return PromptRenderResult(
            success=True,
            rendered_prompt=rendered,
            unused_variables=unused,
            metadata={
                "template": template.id,
                "category": template.category.value,
                "version": template.version,
            },
        )

    # ------------------------------------------------------------------
    # Category Helpers
    # ------------------------------------------------------------------

    def templates_by_category(
        self,
        category: PromptCategory,
    ) -> List[PromptTemplate]:
        """
        Return all templates belonging to a category.
        """

        return sorted(
            [
                template
                for template in self._templates.values()
                if template.category == category
            ],
            key=lambda item: (
                item.version,
                item.id,
            ),
        )

    def latest(
        self,
        category: PromptCategory,
    ) -> Optional[PromptTemplate]:
        """
        Return the latest template for a category.
        """

        return self.find(
            category=category,
        )

    # ------------------------------------------------------------------
    # Registry Information
    # ------------------------------------------------------------------

    def size(self) -> int:
        """
        Return the number of registered templates.
        """

        return len(self._templates)

    def empty(self) -> bool:
        """
        Return True if no templates are registered.
        """

        return self.size() == 0

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(self) -> Dict[str, Any]:
        """
        Return registry diagnostics.
        """

        return {
            "template_count": self.size(),
            "category_count": len(self.categories()),
            "valid": self.validate(),
        }

    def statistics(self) -> Dict[str, Any]:
        """
        Return template statistics grouped by category.
        """

        stats: Dict[str, int] = {}

        for category in self.categories():

            stats[category.value] = len(self.templates_by_category(category))

        return stats

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def describe(
        self,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Return a serializable description of the registry.
        """

        description: Dict[str, Dict[str, Any]] = {}

        for template in self.templates():

            description[template.id] = {
                "name": template.name,
                "category": template.category.value,
                "version": template.version,
                "variables": list(template.variables),
            }

        return description

    # ------------------------------------------------------------------
    # Built-in Templates
    # ------------------------------------------------------------------

    def register_builtin_templates(self) -> None:
        """
        Register all built-in prompt templates.

        Safe to call multiple times. Existing templates are
        replaced with the current built-in versions.
        """

        templates = [
            # ----------------------------------------------------------
            # Question Generation
            # ----------------------------------------------------------
            PromptTemplate(
                id="question_generation_v2_1",
                name="Question Generation",
                category=PromptCategory.QUESTION_GENERATION,
                version="2.1",
                description="Generate questions from the manufacturing blueprint.",
                variables=[
                    "subject",
                    "chapter",
                    "subtopic",
                    "difficulty",
                    "blueprint",
                    "batch",
                    "question_count",
                ],
                template="""
You are Question Factory OS.

Generate {question_count} high-quality questions.

Subject:
{subject}

Chapter:
{chapter}

Subtopic:
{subtopic}

Difficulty:
{difficulty}

Blueprint:
{blueprint}

Batch:
{batch}

Return ONLY valid JSON.
""".strip(),
            ),
            # ----------------------------------------------------------
            # Question Repair
            # ----------------------------------------------------------
            PromptTemplate(
                id="question_repair_v2_1",
                name="Question Repair",
                category=PromptCategory.QUESTION_REPAIR,
                version="2.1",
                description="Repair invalid generated questions.",
                variables=[
                    "question_json",
                    "validation_errors",
                ],
                template="""
Repair the supplied question.

Question:
{question_json}

Validation Errors:
{validation_errors}

Return ONLY corrected JSON.
""".strip(),
            ),
            # ----------------------------------------------------------
            # Validation
            # ----------------------------------------------------------
            PromptTemplate(
                id="validation_v2_1",
                name="Validation",
                category=PromptCategory.VALIDATION,
                version="2.1",
                description="Validate generated question data.",
                variables=[
                    "question_json",
                ],
                template="""
Validate the following question.

{question_json}

Return validation results as JSON.
""".strip(),
            ),
            # ----------------------------------------------------------
            # Quality Audit
            # ----------------------------------------------------------
            PromptTemplate(
                id="quality_audit_v2_1",
                name="Quality Audit",
                category=PromptCategory.QUALITY_AUDIT,
                version="2.1",
                description="Audit overall question quality.",
                variables=[
                    "question_json",
                    "blueprint",
                ],
                template="""
Audit this question.

Blueprint:
{blueprint}

Question:
{question_json}

Return an audit report in JSON.
""".strip(),
            ),
            # ----------------------------------------------------------
            # CSV Export
            # ----------------------------------------------------------
            PromptTemplate(
                id="csv_export_v2_1",
                name="CSV Export",
                category=PromptCategory.CSV_EXPORT,
                version="2.1",
                description="Prepare question for CSV export.",
                variables=[
                    "question_json",
                ],
                template="""
Transform the following question into the required
CSV-compatible structure.

{question_json}

Return JSON only.
""".strip(),
            ),
            # ----------------------------------------------------------
            # Explanation
            # ----------------------------------------------------------
            PromptTemplate(
                id="explanation_v2_1",
                name="Explanation",
                category=PromptCategory.EXPLANATION,
                version="2.1",
                description="Generate a detailed explanation.",
                variables=[
                    "question_json",
                ],
                template="""
Generate a complete solution and explanation.

Question:
{question_json}

Return JSON.
""".strip(),
            ),
        ]

        for template in templates:

            self.register(
                template,
                replace=True,
            )

        logger.info(
            "Registered %d built-in prompt templates.",
            len(templates),
        )


# ----------------------------------------------------------------------
# Factory Helper
# ----------------------------------------------------------------------


def create_prompt_registry(
    *,
    register_builtin: bool = True,
) -> PromptRegistry:
    """
    Create a production-ready PromptRegistry.

    Parameters
    ----------
    register_builtin:
        Automatically register the built-in Question Factory
        templates.

    Returns
    -------
    PromptRegistry
    """

    registry = PromptRegistry()

    if register_builtin:
        registry.register_builtin_templates()

    logger.info("Production PromptRegistry created.")

    return registry


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    "PromptCategory",
    "PromptTemplate",
    "PromptRenderResult",
    "PromptRegistry",
    "create_prompt_registry",
]
