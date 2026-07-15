"""
Question Factory OS v2.1
------------------------

Prompt Templates

Central registry for all prompt templates used by
the AI subsystem.

Responsibilities
----------------
• Register templates
• Locate templates
• Render templates
• Validate variables
• Manage template versions

Provider agnostic.

Author:
Question Factory OS
"""

from __future__ import annotations

import logging
import re
import time

from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from string import Formatter
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

    EXPLANATION = "explanation"

    DISTRACTOR = "distractor"

    BLUEPRINT = "blueprint"

    REPORT = "report"


# ----------------------------------------------------------------------
# Prompt Template
# ----------------------------------------------------------------------


@dataclass(slots=True, frozen=True)
class PromptTemplate:
    """
    Immutable prompt template.
    """

    id: str

    name: str

    version: str

    category: PromptCategory

    description: str

    template: str

    variables: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def variable_count(
        self,
    ) -> int:
        """
        Number of declared variables.
        """

        return len(self.variables)

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Serialize template.
        """

        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "category": self.category.value,
            "description": self.description,
            "template": self.template,
            "variables": list(self.variables),
            "metadata": dict(self.metadata),
        }

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Lightweight description.
        """

        return {
            "id": self.id,
            "version": self.version,
            "category": self.category.value,
            "variables": self.variable_count,
        }


# ----------------------------------------------------------------------
# Prompt Render Result
# ----------------------------------------------------------------------


@dataclass(slots=True, frozen=True)
class PromptRenderResult:
    """
    Result returned after rendering.
    """

    success: bool

    rendered_prompt: str

    missing_variables: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    render_duration_ms: float = 0.0

    @property
    def has_missing_variables(
        self,
    ) -> bool:
        """
        True if rendering failed because of
        missing variables.
        """

        return bool(
            self.missing_variables
        )

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Serialize result.
        """

        return {
            "success": self.success,
            "rendered_prompt": self.rendered_prompt,
            "missing_variables": list(
                self.missing_variables
            ),
            "metadata": dict(
                self.metadata
            ),
            "render_duration_ms": (
                self.render_duration_ms
            ),
        }

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Lightweight render summary.
        """

        return {
            "success": self.success,
            "missing": len(
                self.missing_variables
            ),
            "duration_ms": (
                self.render_duration_ms
            ),
        }


# ----------------------------------------------------------------------
# Prompt Registry
# ----------------------------------------------------------------------


class PromptRegistry:
    """
    Central template registry.

    Responsible for:

    • Registration
    • Lookup
    • Rendering
    • Validation
    • Statistics
    """

    def __init__(
        self,
    ) -> None:

        self._templates: Dict[
            str,
            PromptTemplate,
        ] = {}

        logger.info(
            "PromptRegistry initialized."
        )
    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    def _version_key(
        self,
        version: str,
    ) -> tuple[int, ...]:
        """
        Convert dotted version into a sortable tuple.

        Example
        -------
        2.10 -> (2, 10)
        """

        try:
            return tuple(
                int(part)
                for part in version.split(".")
            )

        except ValueError:

            logger.warning(
                "Invalid version '%s'.",
                version,
            )

            return (0,)

    def _extract_variables(
        self,
        template: str,
    ) -> List[str]:
        """
        Extract placeholder names from
        a format string.
        """

        formatter = Formatter()

        variables: List[str] = []

        for (
            _,
            field_name,
            _,
            _,
        ) in formatter.parse(template):

            if (
                field_name
                and field_name not in variables
            ):
                variables.append(field_name)

        return variables

    def _validate_template(
        self,
        template: PromptTemplate,
    ) -> None:
        """
        Validate template integrity.
        """

        if not template.id.strip():
            raise ValueError(
                "Template id cannot be empty."
            )

        if not template.name.strip():
            raise ValueError(
                "Template name cannot be empty."
            )

        if not template.version.strip():
            raise ValueError(
                "Template version cannot be empty."
            )

        if not template.template.strip():
            raise ValueError(
                "Template body cannot be empty."
            )

        discovered = self._extract_variables(
            template.template
        )

        missing = [
            variable
            for variable in discovered
            if variable not in template.variables
        ]

        if missing:

            raise ValueError(
                "Template '%s' is missing "
                "variable declarations: %s"
                % (
                    template.id,
                    ", ".join(missing),
                )
            )

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        template: PromptTemplate,
    ) -> None:
        """
        Register a prompt template.
        """

        self._validate_template(
            template
        )

        self._templates[
            template.id
        ] = template

        logger.info(
            "Registered prompt template '%s'.",
            template.id,
        )

    def unregister(
        self,
        template_id: str,
    ) -> bool:
        """
        Remove a template.
        """

        if template_id not in self._templates:
            return False

        del self._templates[
            template_id
        ]

        logger.info(
            "Removed template '%s'.",
            template_id,
        )

        return True

    def clear(
        self,
    ) -> None:
        """
        Remove every template.
        """

        self._templates.clear()

        logger.info(
            "Prompt registry cleared."
        )

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def exists(
        self,
        template_id: str,
    ) -> bool:
        """
        Return True if template exists.
        """

        return (
            template_id
            in self._templates
        )

    def get(
        self,
        template_id: str,
    ) -> PromptTemplate:
        """
        Return template by id.

        Raises
        ------
        KeyError
        """

        try:
            return self._templates[
                template_id
            ]

        except KeyError as ex:

            raise KeyError(
                f"Unknown template "
                f"'{template_id}'."
            ) from ex

    def find(
        self,
        *,
        category: PromptCategory,
        version: Optional[str] = None,
    ) -> Optional[
        PromptTemplate
    ]:
        """
        Locate a template.

        When version is omitted,
        the newest version is returned.
        """

        matches = [

            template

            for template
            in self._templates.values()

            if template.category
            == category

        ]

        if not matches:
            return None

        if version is not None:

            for template in matches:

                if (
                    template.version
                    == version
                ):
                    return template

            return None

        return sorted(
            matches,
            key=lambda item:
            self._version_key(
                item.version
            ),
        )[-1]
    # ------------------------------------------------------------------
    # Rendering Helpers
    # ------------------------------------------------------------------

    def _missing_variables(
        self,
        template: PromptTemplate,
        values: Dict[str, Any],
    ) -> List[str]:
        """
        Return the list of variables required by the
        template but not supplied by the caller.
        """

        missing: List[str] = []

        for variable in template.variables:

            if variable not in values:
                missing.append(variable)

        return missing

    def _render(
        self,
        template: PromptTemplate,
        values: Dict[str, Any],
    ) -> PromptRenderResult:
        """
        Render a template.
        """

        start = time.perf_counter()

        missing = self._missing_variables(
            template,
            values,
        )

        if missing:

            duration = (
                time.perf_counter() - start
            ) * 1000.0

            return PromptRenderResult(
                success=False,
                rendered_prompt="",
                missing_variables=missing,
                metadata={
                    "template_id": template.id,
                    "template_name": template.name,
                    "template_version": template.version,
                },
                render_duration_ms=duration,
            )

        rendered = template.template.format(
            **values
        )

        duration = (
            time.perf_counter() - start
        ) * 1000.0

        return PromptRenderResult(
            success=True,
            rendered_prompt=rendered,
            missing_variables=[],
            metadata={
                "template_id": template.id,
                "template_name": template.name,
                "template_version": template.version,
            },
            render_duration_ms=duration,
        )

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render_template(
        self,
        *,
        category: PromptCategory,
        values: Dict[str, Any],
        version: Optional[str] = None,
    ) -> PromptRenderResult:
        """
        Render a template by category.
        """

        template = self.find(
            category=category,
            version=version,
        )

        if template is None:

            raise ValueError(
                "No prompt template found for "
                f"category '{category.value}'."
            )

        logger.debug(
            "Rendering template '%s'.",
            template.id,
        )

        return self._render(
            template,
            values,
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
    ) -> bool:
        """
        Validate every registered template.
        """

        for template in self._templates.values():

            self._validate_template(
                template
            )

        return True

    # ------------------------------------------------------------------
    # Registry Inspection
    # ------------------------------------------------------------------

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
                self._version_key(
                    item.version
                ),
                item.id,
            ),
        )

    def categories(
        self,
    ) -> List[PromptCategory]:
        """
        Return registered categories.
        """

        categories = {

            template.category

            for template
            in self._templates.values()

        }

        return sorted(
            categories,
            key=lambda item: item.value,
        )

    def size(
        self,
    ) -> int:
        """
        Number of registered templates.
        """

        return len(
            self._templates
        )

    def is_empty(
        self,
    ) -> bool:
        """
        True if the registry contains
        no templates.
        """

        return (
            self.size() == 0
        )
    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, Any]:
        """
        Return registry statistics.
        """

        category_counts: Dict[str, int] = {}

        latest_versions: Dict[str, str] = {}

        for template in self._templates.values():

            category = template.category.value

            category_counts[category] = (
                category_counts.get(category, 0)
                + 1
            )

            current = latest_versions.get(category)

            if (
                current is None
                or self._version_key(
                    template.version
                )
                > self._version_key(current)
            ):
                latest_versions[
                    category
                ] = template.version

        return {
            "template_count": len(
                self._templates
            ),
            "category_count": len(
                category_counts
            ),
            "categories": category_counts,
            "latest_versions": latest_versions,
        }

    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------

    def describe(
        self,
    ) -> Dict[str, Any]:
        """
        Return a descriptive summary of the registry.
        """

        return {
            "component": "PromptRegistry",
            "statistics": self.statistics(),
            "categories": [
                category.value
                for category in self.categories()
            ],
            "templates": [
                template.summary()
                for template in self.templates()
            ],
        }

    # ------------------------------------------------------------------
    # Built-in Templates
    # ------------------------------------------------------------------

    def register_builtin_templates(
        self,
    ) -> None:
        """
        Register the default Question Factory
        prompt templates.

        Safe to call multiple times.
        """

        builtin_templates = [

            PromptTemplate(
                id="question_generation_v2_1",
                name="Question Generation",
                version="2.1",
                category=PromptCategory.QUESTION_GENERATION,
                description=(
                    "Generate examination-quality "
                    "questions."
                ),
                template="{instruction}",
                variables=[
                    "instruction",
                ],
            ),

            PromptTemplate(
                id="question_repair_v2_1",
                name="Question Repair",
                version="2.1",
                category=PromptCategory.QUESTION_REPAIR,
                description=(
                    "Repair existing questions."
                ),
                template="{instruction}",
                variables=[
                    "instruction",
                ],
            ),

            PromptTemplate(
                id="validation_v2_1",
                name="Validation",
                version="2.1",
                category=PromptCategory.VALIDATION,
                description=(
                    "Validate generated content."
                ),
                template="{instruction}",
                variables=[
                    "instruction",
                ],
            ),

            PromptTemplate(
                id="explanation_v2_1",
                name="Explanation",
                version="2.1",
                category=PromptCategory.EXPLANATION,
                description=(
                    "Generate explanations."
                ),
                template="{instruction}",
                variables=[
                    "instruction",
                ],
            ),

            PromptTemplate(
                id="distractor_v2_1",
                name="Distractor Generation",
                version="2.1",
                category=PromptCategory.DISTRACTOR,
                description=(
                    "Generate distractors."
                ),
                template="{instruction}",
                variables=[
                    "instruction",
                ],
            ),

            PromptTemplate(
                id="blueprint_v2_1",
                name="Blueprint",
                version="2.1",
                category=PromptCategory.BLUEPRINT,
                description=(
                    "Blueprint analysis."
                ),
                template="{instruction}",
                variables=[
                    "instruction",
                ],
            ),

            PromptTemplate(
                id="report_v2_1",
                name="Report",
                version="2.1",
                category=PromptCategory.REPORT,
                description=(
                    "Generate reports."
                ),
                template="{instruction}",
                variables=[
                    "instruction",
                ],
            ),

        ]

        for template in builtin_templates:

            if not self.exists(
                template.id
            ):
                self.register(
                    template
                )

        logger.info(
            "%d built-in prompt templates "
            "registered.",
            len(builtin_templates),
        )
    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def health(
        self,
    ) -> Dict[str, Any]:
        """
        Return registry health information.
        """

        return {
            "component": "PromptRegistry",
            "status": "READY",
            "registered_templates": self.size(),
            "categories": len(
                self.categories()
            ),
            "valid": self.validate(),
        }

    # ------------------------------------------------------------------
    # Capabilities
    # ------------------------------------------------------------------

    def capabilities(
        self,
    ) -> Dict[str, bool]:
        """
        Return supported registry capabilities.
        """

        return {
            "registration": True,
            "lookup": True,
            "rendering": True,
            "validation": True,
            "statistics": True,
            "builtin_templates": True,
            "versioning": True,
        }


# ----------------------------------------------------------------------
# Factory Helper
# ----------------------------------------------------------------------

def create_prompt_registry(
    *,
    register_builtin: bool = True,
) -> PromptRegistry:
    """
    Create a production-ready prompt registry.

    Parameters
    ----------
    register_builtin:
        Register the built-in Question Factory
        prompt templates.

    Returns
    -------
    PromptRegistry
    """

    registry = PromptRegistry()

    if register_builtin:

        registry.register_builtin_templates()

    logger.info(
        "Prompt registry created."
    )

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
