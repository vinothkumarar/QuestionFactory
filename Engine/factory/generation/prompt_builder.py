"""
Question Factory OS v2.0

Prompt Builder

Responsible for converting a provider-independent
generation request into a provider-ready prompt.

The PromptBuilder contains no AI provider logic.
"""

from __future__ import annotations

import logging
from typing import Dict, List


class PromptBuilder:
    """
    Builds structured prompts for AI generation.
    """

    def __init__(self):

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def build(
        self,
        request: Dict,
    ) -> str:
        """
        Build the complete generation prompt.
        """

        self.logger.info(
            "Building generation prompt."
        )

        sections: List[str] = []

        sections.append(
            self._factory_context(
                request
            )
        )

        sections.append(
            self._production_context(
                request
            )
        )

        sections.append(
            self._blueprint_rules(
                request
            )
        )

        sections.append(
            self._runtime_context(
                request
            )
        )

        sections.append(
            self._output_requirements(
                request
            )
        )

        prompt = "\n\n".join(sections)

        self.logger.info(
            "Prompt successfully built."
        )

        return prompt
            # ---------------------------------------------------------
    # Factory Context
    # ---------------------------------------------------------

    def _factory_context(
        self,
        request: Dict,
    ) -> str:
        """
        Build the factory context section.
        """

        factory = request["factory"]

        return "\n".join(
            [
                "### FACTORY CONTEXT",
                f"Factory Name : {factory['name']}",
                f"Factory Version : {factory['version']}",
                (
                    "Blueprint Version : "
                    f"{factory['blueprint_version']}"
                ),
                "",
                (
                    "You are the manufacturing engine of "
                    "Question Factory OS."
                ),
                (
                    "Generate questions strictly according "
                    "to the supplied production request."
                ),
            ]
        )

    # ---------------------------------------------------------
    # Production Context
    # ---------------------------------------------------------

    def _production_context(
        self,
        request: Dict,
    ) -> str:
        """
        Build the production context section.
        """

        production = request["production"]

        lines = [
            "### PRODUCTION CONTEXT",
            f"Unit : {production['unit_code']}",
            f"Chapter : {production['chapter_code']}",
            f"Subtopic : {production['subtopic_code']}",
            f"Set : {production['set_number']}",
            f"Batch : {production['batch_number']}",
            (
                "Question Range : "
                f"{production['question_start']} - "
                f"{production['question_end']}"
            ),
            (
                "Questions Required : "
                f"{production['question_count']}"
            ),
        ]

        return "\n".join(lines)

    # ---------------------------------------------------------
    # Blueprint Rules
    # ---------------------------------------------------------

    def _blueprint_rules(
        self,
        request: Dict,
    ) -> str:
        """
        Build the blueprint rules section.
        """

        generation = request["generation"]

        rules = generation.get(
            "rules",
            {},
        )

        archetypes = generation.get(
            "archetypes",
            {},
        )

        lines = [
            "### BLUEPRINT RULES",
        ]

        if not rules:

            lines.append(
                "No explicit manufacturing rules supplied."
            )

        else:

            for section, value in rules.items():

                lines.append("")
                lines.append(f"[{section}]")
                lines.append(str(value))

        if archetypes:

            lines.append("")
            lines.append(
                "Available Archetype Sections:"
            )

            for name in sorted(archetypes.keys()):

                lines.append(f"- {name}")

        return "\n".join(lines)
            # ---------------------------------------------------------
    # Runtime Context
    # ---------------------------------------------------------

    def _runtime_context(
        self,
        request: Dict,
    ) -> str:
        """
        Build the runtime context section.
        """

        runtime = request["runtime"]

        lines = [
            "### RUNTIME CONTEXT",
            (
                f"Run ID : "
                f"{runtime.get('run_id', 'UNKNOWN')}"
            ),
            (
                "Repair Before Expand : "
                f"{runtime.get('repair_before_expand', False)}"
            ),
            (
                "Checkpoint Enabled : "
                f"{runtime.get('checkpoint_enabled', False)}"
            ),
            "",
            (
                "Follow the active runtime behaviour "
                "during manufacturing."
            ),
        ]

        return "\n".join(lines)

    # ---------------------------------------------------------
    # Output Requirements
    # ---------------------------------------------------------

    def _output_requirements(
        self,
        request: Dict,
    ) -> str:
        """
        Build the required output specification.
        """

        generation = request["generation"]

        lines = [
            "### OUTPUT REQUIREMENTS",
            "",
            (
                "Return ONLY the generated questions."
            ),
            (
                "Do not include explanations unless "
                "explicitly requested."
            ),
            (
                "Produce structured output that can be "
                "parsed automatically."
            ),
            (
                "Follow the configured schema version: "
                f"{generation.get('schema_version')}"
            ),
        ]

        return "\n".join(lines)

    # ---------------------------------------------------------
    # Final Instructions
    # ---------------------------------------------------------

    def _final_instructions(
        self,
        request: Dict,
    ) -> str:
        """
        Build the final manufacturing instructions.
        """

        production = request["production"]

        return "\n".join(
            [
                "### FINAL INSTRUCTIONS",
                "",
                (
                    "Manufacture exactly "
                    f"{production['question_count']} "
                    "high-quality questions."
                ),
                (
                    "Maintain consistent difficulty for "
                    "the requested set."
                ),
                (
                    "Ensure every question is unique."
                ),
                (
                    "Avoid duplicate concepts unless "
                    "explicitly required."
                ),
                (
                    "Return only the final manufactured "
                    "question batch."
                ),
            ]
        )
            # ---------------------------------------------------------
    # Prompt Validation
    # ---------------------------------------------------------

    def validate_prompt(
        self,
        prompt: str,
    ) -> None:
        """
        Validate the generated prompt.

        Raises
        ------
        ValueError
            If the prompt is invalid.
        """

        if not prompt.strip():

            raise ValueError(
                "Generated prompt is empty."
            )

        required_sections = [
            "FACTORY CONTEXT",
            "PRODUCTION CONTEXT",
            "BLUEPRINT RULES",
            "RUNTIME CONTEXT",
            "OUTPUT REQUIREMENTS",
            "FINAL INSTRUCTIONS",
        ]

        for section in required_sections:

            if section not in prompt:

                raise ValueError(
                    f"Missing prompt section: {section}"
                )

        self.logger.info(
            "Prompt validation successful."
        )

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_build(
        self,
        request: Dict,
    ) -> None:
        """
        Hook executed immediately before prompt
        construction.
        """

        return

    def after_build(
        self,
        request: Dict,
        prompt: str,
    ) -> None:
        """
        Hook executed after prompt construction.
        """

        return

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def statistics(
        self,
        prompt: str,
    ) -> Dict:
        """
        Return prompt statistics.
        """

        lines = prompt.splitlines()

        words = prompt.split()

        return {
            "characters": len(prompt),
            "lines": len(lines),
            "words": len(words),
        }

    def summary(
        self,
        prompt: str,
    ) -> Dict:
        """
        Return a concise prompt summary.
        """

        stats = self.statistics(prompt)

        return {
            "characters": stats["characters"],
            "lines": stats["lines"],
            "words": stats["words"],
        }

    def diagnostics(
        self,
        prompt: str,
    ) -> Dict:
        """
        Return detailed prompt diagnostics.
        """

        return {
            "component": self.__class__.__name__,
            "summary": self.summary(prompt),
            "statistics": self.statistics(prompt),
        }
            # ---------------------------------------------------------
    # Component Information
    # ---------------------------------------------------------

    @property
    def version(self) -> str:
        """
        Prompt Builder version.
        """

        return "2.0.0"

    @property
    def component_name(self) -> str:
        """
        Component name.
        """

        return "Prompt Builder"

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(self) -> Dict:
        """
        Return component health information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(self) -> Dict:
        """
        Describe Prompt Builder capabilities.
        """

        return {
            "structured_prompt": True,
            "provider_independent": True,
            "blueprint_aware": True,
            "runtime_aware": True,
            "validation": True,
            "diagnostics": True,
            "statistics": True,
            "lifecycle_hooks": True,
        }

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def create_empty_prompt(self) -> str:
        """
        Return an empty prompt.

        Useful for testing and fallback scenarios.
        """

        return ""

    def supported_sections(self) -> List[str]:
        """
        Return the prompt sections produced by this builder.
        """

        return [
            "FACTORY CONTEXT",
            "PRODUCTION CONTEXT",
            "BLUEPRINT RULES",
            "RUNTIME CONTEXT",
            "OUTPUT REQUIREMENTS",
            "FINAL INSTRUCTIONS",
        ]

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            "PromptBuilder("
            f"version='{self.version}')"
        )

    def __str__(self) -> str:
        return (
            f"{self.component_name} "
            f"[v{self.version}]"
        )
        