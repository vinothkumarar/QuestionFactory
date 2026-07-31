"""
Question Factory OS v3.0

Validation Result

Represents the aggregated outcome of schema validation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from Engine.validation.validation_error import ValidationError


@dataclass(slots=True)
class ValidationResult:
    """
    Aggregated validation result.
    """

    errors: list[ValidationError] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        """
        True when no validation errors exist.
        """

        return len(self.errors) == 0

    def add_error(self, error: ValidationError) -> None:
        """
        Add a validation error.
        """

        self.errors.append(error)

    def add_warning(self, warning: str) -> None:
        """
        Add a validation warning.
        """

        self.warnings.append(warning)

    @property
    def error_count(self) -> int:
        """
        Number of validation errors.
        """

        return len(self.errors)

    @property
    def warning_count(self) -> int:
        """
        Number of validation warnings.
        """

        return len(self.warnings)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the result into a serializable dictionary.
        """

        return {
            "valid": self.valid,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "errors": [error.to_dict() for error in self.errors],
            "warnings": list(self.warnings),
        }

    def summary(self) -> dict[str, Any]:
        """
        Return a concise validation summary.
        """

        return {
            "valid": self.valid,
            "errors": self.error_count,
            "warnings": self.warning_count,
        }

    def __repr__(self) -> str:
        return (
            "ValidationResult("
            f"valid={self.valid}, "
            f"errors={self.error_count}, "
            f"warnings={self.warning_count})"
        )
        