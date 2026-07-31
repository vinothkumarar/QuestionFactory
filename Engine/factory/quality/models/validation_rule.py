"""
Question Factory OS v3.0

Validation Rule

Immutable metadata describing a Quality Assurance rule.
"""

from __future__ import annotations

from dataclasses import dataclass

from Engine.factory.quality.models.validation_severity import (
    ValidationSeverity,
)


@dataclass(frozen=True, slots=True)
class ValidationRule:
    """
    Immutable definition of a validation rule.

    Attributes
    ----------
    rule_id:
        Unique rule identifier
        (e.g. QA001).

    name:
        Short human-readable name.

    description:
        Detailed description of the rule.

    severity:
        Severity assigned when the rule fails.

    repairable:
        Indicates whether the Repair Engine
        may attempt an automatic correction.
    """

    rule_id: str

    name: str

    description: str

    severity: ValidationSeverity

    repairable: bool = True

    @property
    def is_blocking(self) -> bool:
        """
        Returns True when failure of this rule
        blocks production.
        """

        return self.severity is ValidationSeverity.CRITICAL


__all__ = [
    "ValidationRule",
]