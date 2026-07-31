"""
Question Factory OS v3.0

Validation Result

Represents the outcome produced by a single
quality validator.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from Engine.factory.quality.models.quality_issue import (
    QualityIssue,
)

from Engine.factory.quality.models.validation_rule import (
    ValidationRule,
)


@dataclass(slots=True)
class ValidationResult:
    """
    Result returned by a single validator.

    A successful validation may still contain
    informational or warning issues.
    """

    rule: ValidationRule

    passed: bool

    issues: list[QualityIssue] = field(
        default_factory=list
    )

    execution_time_ms: float = 0.0

    metadata: dict[str, object] = field(
        default_factory=dict
    )

    @property
    def has_issues(self) -> bool:
        """
        Returns True if one or more issues
        were produced.
        """

        return bool(self.issues)

    @property
    def issue_count(self) -> int:
        """
        Number of issues produced.
        """

        return len(self.issues)

    @property
    def repair_required(self) -> bool:
        """
        Returns True if at least one issue
        is repairable.
        """

        return any(
            issue.repairable
            for issue in self.issues
        )

    @property
    def blocking(self) -> bool:
        """
        Returns True if any issue is blocking.
        """

        return any(
            issue.is_blocking
            for issue in self.issues
        )

    def add_issue(
        self,
        issue: QualityIssue,
    ) -> None:
        """
        Add a quality issue to this result.
        """

        self.issues.append(issue)

        if issue.is_blocking:
            self.passed = False


__all__ = [
    "ValidationResult",
]
