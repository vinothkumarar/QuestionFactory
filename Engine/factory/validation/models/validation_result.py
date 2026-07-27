"""
Question Factory OS v2.3

Validation Result Model
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .validation_error import ValidationError
from .validation_warning import ValidationWarning


@dataclass(slots=True)
class ValidationResult:
    """
    Result produced by a validator.
    """

    validator_name: str

    passed: bool = True

    repairable: bool = False

    execution_time_ms: float = 0.0

    errors: list[ValidationError] = field(default_factory=list)

    warnings: list[ValidationWarning] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)