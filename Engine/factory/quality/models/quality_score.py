"""
Question Factory OS v3.0

Quality Score

Aggregated quality metrics for a validation run.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class QualityScore:
    """
    Overall quality metrics for a validation report.
    """

    passed_rules: int = 0

    failed_rules: int = 0

    warnings: int = 0

    errors: int = 0

    critical_errors: int = 0

    @property
    def total_rules(self) -> int:
        """
        Total number of evaluated rules.
        """

        return self.passed_rules + self.failed_rules

    @property
    def percentage(self) -> float:
        """
        Overall validation percentage.
        """

        total = self.total_rules

        if total == 0:
            return 100.0

        return (
            self.passed_rules / total
        ) * 100.0

    @property
    def passed(self) -> bool:
        """
        Overall pass/fail status.
        """

        return (
            self.critical_errors == 0
            and self.errors == 0
        )


__all__ = [
    "QualityScore",
]
