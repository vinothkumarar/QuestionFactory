"""
Question Factory OS v2.2

Export Summary
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ExportSummary:
    """
    Summary of an export operation.
    """

    total_rows: int = 0

    successful_rows: int = 0

    failed_rows: int = 0

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    duration_seconds: float = 0.0

    @property
    def success(self) -> bool:
        return not self.errors

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    @property
    def error_count(self) -> int:
        return len(self.errors)