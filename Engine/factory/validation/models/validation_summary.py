"""
Question Factory OS v2.3

Validation Summary Model
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .validation_result import ValidationResult


@dataclass(slots=True)
class ValidationSummary:
    """
    Aggregated validation results.
    """

    results: list[ValidationResult] = field(default_factory=list)

    @property
    def total_validators(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(result.passed for result in self.results)

    @property
    def failed(self) -> int:
        return self.total_validators - self.passed

    @property
    def repair_required(self) -> bool:
        return any(result.repairable for result in self.results)

    @property
    def total_errors(self) -> int:
        return sum(result.error_count for result in self.results)

    @property
    def total_warnings(self) -> int:
        return sum(result.warning_count for result in self.results)

    @property
    def success(self) -> bool:
        return self.failed == 0
        