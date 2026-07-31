"""
Question Factory OS v3.0

Quality Issue

Represents a single issue detected during
quality validation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from Engine.factory.quality.models.validation_severity import (
    ValidationSeverity,
)


@dataclass(slots=True)
class QualityIssue:
    """
    Represents one quality issue identified by
    a validator.

    Attributes
    ----------
    rule_id:
        Validation rule identifier.

    severity:
        Severity of the issue.

    message:
        Human-readable description.

    question_id:
        Optional question identifier.

    location:
        Optional location within the batch.

    repairable:
        Indicates whether the Repair Engine
        can attempt an automatic fix.

    details:
        Additional structured diagnostic
        information.
    """

    rule_id: str

    severity: ValidationSeverity

    message: str

    question_id: str | None = None

    location: str | None = None

    repairable: bool = True

    details: dict[str, object] = field(
        default_factory=dict
    )

    @property
    def is_blocking(self) -> bool:
        """
        Returns True when the issue prevents
        the batch from progressing.
        """

        return self.severity is ValidationSeverity.CRITICAL

    @property
    def has_question(self) -> bool:
        """
        Indicates whether the issue refers
        to a specific question.
        """

        return self.question_id is not None


__all__ = [
    "QualityIssue",
]