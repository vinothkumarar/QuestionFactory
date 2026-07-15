"""
Question Factory OS v2.1
------------------------

Prompt Package

Represents a fully rendered prompt ready for execution
by the AI Engine.

Responsibilities
----------------
• Hold rendered prompt text
• Hold system prompt
• Track template metadata
• Store rendering variables
• Carry manufacturing metadata
• Provide prompt diagnostics

This object is immutable once created and forms the
contract between PromptBuilder and AIEngine.

Author:
Question Factory OS
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from typing import Any
from typing import Dict
from typing import Optional

# ----------------------------------------------------------------------
# Prompt Package
# ----------------------------------------------------------------------


@dataclass(slots=True, frozen=True)
class PromptPackage:
    """
    Fully rendered prompt package.

    This object is produced by PromptBuilder and consumed
    by AIEngine.
    """

    # ------------------------------------------------------------------
    # Prompt Content
    # ------------------------------------------------------------------

    prompt: str

    system_prompt: Optional[str] = None

    # ------------------------------------------------------------------
    # Template Information
    # ------------------------------------------------------------------

    template_id: str = ""

    template_version: str = ""

    template_category: str = ""

    # ------------------------------------------------------------------
    # Rendering Context
    # ------------------------------------------------------------------

    variables: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Runtime Information
    # ------------------------------------------------------------------

    estimated_tokens: Optional[int] = None

    checksum: Optional[str] = None

    render_duration_ms: Optional[float] = None
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    @property
    def is_valid(self) -> bool:
        """
        Return True if the package contains a usable prompt.
        """

        return bool(self.prompt.strip())

    @property
    def has_system_prompt(self) -> bool:
        """
        Return True if a system prompt is present.
        """

        return bool(self.system_prompt and self.system_prompt.strip())

    @property
    def has_metadata(self) -> bool:
        """
        Return True if metadata exists.
        """

        return bool(self.metadata)

    @property
    def has_variables(self) -> bool:
        """
        Return True if rendering variables exist.
        """

        return bool(self.variables)

    @property
    def has_checksum(self) -> bool:
        """
        Return True if a checksum has been assigned.
        """

        return self.checksum is not None

    # ------------------------------------------------------------------
    # Information
    # ------------------------------------------------------------------

    @property
    def prompt_length(self) -> int:
        """
        Return the prompt length in characters.
        """

        return len(self.prompt)

    @property
    def variable_count(self) -> int:
        """
        Number of rendering variables.
        """

        return len(self.variables)

    @property
    def metadata_count(self) -> int:
        """
        Number of metadata entries.
        """

        return len(self.metadata)

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Export the package as a serializable dictionary.
        """

        return {
            "prompt": self.prompt,
            "system_prompt": self.system_prompt,
            "template_id": self.template_id,
            "template_version": self.template_version,
            "template_category": self.template_category,
            "variables": dict(self.variables),
            "metadata": dict(self.metadata),
            "estimated_tokens": self.estimated_tokens,
            "checksum": self.checksum,
            "render_duration_ms": self.render_duration_ms,
        }

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(self) -> Dict[str, Any]:
        """
        Return package diagnostics.

        Suitable for runtime monitoring and debugging.
        """

        return {
            "valid": self.is_valid,
            "prompt_length": self.prompt_length,
            "has_system_prompt": self.has_system_prompt,
            "variable_count": self.variable_count,
            "metadata_count": self.metadata_count,
            "estimated_tokens": self.estimated_tokens,
            "checksum_present": self.has_checksum,
        }

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_json_dict(self) -> Dict[str, Any]:
        """
        Return a JSON-serializable representation.

        This is equivalent to to_dict() and exists to make
        serialization intent explicit for callers.
        """

        return self.to_dict()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        """
        Return a concise package summary.

        Suitable for logging and runtime dashboards without
        exposing the full prompt contents.
        """

        return {
            "template_id": self.template_id,
            "template_version": self.template_version,
            "template_category": self.template_category,
            "prompt_length": self.prompt_length,
            "estimated_tokens": self.estimated_tokens,
            "variable_count": self.variable_count,
            "metadata_count": self.metadata_count,
        }

    # ------------------------------------------------------------------
    # Convenience Helpers
    # ------------------------------------------------------------------

    def variable(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a rendering variable.
        """

        return self.variables.get(name, default)

    def metadata_value(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a metadata value.
        """

        return self.metadata.get(name, default)

    # ------------------------------------------------------------------
    # Prompt Preview
    # ------------------------------------------------------------------

    def preview(
        self,
        *,
        max_length: int = 120,
    ) -> str:
        """
        Return a shortened preview of the rendered prompt.

        Useful for logs and diagnostics.
        """

        text = self.prompt.strip()

        if len(text) <= max_length:
            return text

        return text[: max_length - 3] + "..."

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"template_id='{self.template_id}', "
            f"version='{self.template_version}', "
            f"category='{self.template_category}', "
            f"tokens={self.estimated_tokens})"
        )

    __str__ = __repr__


# ----------------------------------------------------------------------
# Factory Helper
# ----------------------------------------------------------------------


def create_prompt_package(
    *,
    prompt: str,
    system_prompt: Optional[str] = None,
    template_id: str = "",
    template_version: str = "",
    template_category: str = "",
    variables: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    estimated_tokens: Optional[int] = None,
    checksum: Optional[str] = None,
    render_duration_ms: Optional[float] = None,
) -> PromptPackage:
    """
    Create a PromptPackage.

    This helper provides a stable construction point and avoids
    callers having to create mutable default dictionaries.
    """

    return PromptPackage(
        prompt=prompt,
        system_prompt=system_prompt,
        template_id=template_id,
        template_version=template_version,
        template_category=template_category,
        variables=dict(variables or {}),
        metadata=dict(metadata or {}),
        estimated_tokens=estimated_tokens,
        checksum=checksum,
        render_duration_ms=render_duration_ms,
    )


# ----------------------------------------------------------------------
# Module Exports
# ----------------------------------------------------------------------

__all__ = [
    "PromptPackage",
    "create_prompt_package",
]
