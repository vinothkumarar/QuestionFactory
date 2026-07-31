"""
Question Factory OS v3.0

Quality Report

Aggregated report produced by the Quality Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from Engine.factory.quality.models.quality_issue import (
    QualityIssue,
)

from Engine.factory.quality.models.quality_score import (
    QualityScore,
)

from Engine.factory.quality.models.validation_result import (
    ValidationResult,
)


@dataclass(slots=True)
class QualityReport:
    """
    Complete quality assessment for a manufactured
    question batch.
    """

    validation_results: list[ValidationResult] = field(
        default_factory=list
    )

    issues: list[QualityIssue] = field(
        default_factory=list
    )

    score: QualityScore = field(
        default_factory=QualityScore
    )

    execution_time_ms: float = 0.0

    metadata: dict[str, object] = field(
        default_factory=dict
    )

    @property
    def passed(self) -> bool:
        """
        Overall validation result.
        """

        return self.score.passed

    @property
    def repair_required(self) -> bool:
        """
        Returns True if at least one issue is
        repairable.
        """

        return any(
            issue.repairable
            for issue in self.issues
        )

    @property
    def issue_count(self) -> int:
        """
        Total number of detected issues.
        """

        return len(self.issues)

    @property
    def validation_count(self) -> int:
        """
        Number of executed validators.
        """

        return len(self.validation_results)

    def add_result(
        self,
        result: ValidationResult,
    ) -> None:
        """
        Add a validator result to the report.
        """

        self.validation_results.append(result)
        self.issues.extend(result.issues)


__all__ = [
    "QualityReport",
]