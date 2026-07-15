"""
Question Factory OS v2.1

Orchestration Result

Represents the complete result of one
manufacturing orchestration cycle.

This object is intentionally immutable and
contains only orchestration state.

It does not perform validation,
generation or repair itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from typing import Any


@dataclass(slots=True, frozen=True)
class OrchestrationResult:
    """
    Result returned by FactoryOrchestrator.
    """

    success: bool

    parsed_response: Any

    question_batch: Any | None = None

    validation_results: list[Any] = field(
        default_factory=list
    )

    repair_results: list[Any] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )
@dataclass(slots=True, frozen=True)
class OrchestrationSummary:
    """
    Lightweight orchestration summary.
    """

    success: bool

    validation_count: int

    repair_count: int

    warning_count: int

    error_count: int


def create_summary(
    result: OrchestrationResult,
) -> OrchestrationSummary:
    """
    Create a compact orchestration summary.
    """

    return OrchestrationSummary(
        success=result.success,
        validation_count=len(
            result.validation_results
        ),
        repair_count=len(
            result.repair_results
        ),
        warning_count=len(
            result.warnings
        ),
        error_count=len(
            result.errors
        ),
    )
def result_ok(
    parsed_response: Any,
    *,
    question_batch: Any | None = None,
    validation_results: list[Any] | None = None,
    repair_results: list[Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> OrchestrationResult:
    """
    Convenience factory for successful
    orchestration.
    """

    return OrchestrationResult(
        success=True,
        parsed_response=parsed_response,
        question_batch=question_batch,
        validation_results=(
            validation_results or []
        ),
        repair_results=(
            repair_results or []
        ),
        metadata=metadata or {},
    )


def result_failed(
    *,
    parsed_response: Any = None,
    errors: list[str] | None = None,
    warnings: list[str] | None = None,
) -> OrchestrationResult:
    """
    Convenience factory for failed
    orchestration.
    """

    return OrchestrationResult(
        success=False,
        parsed_response=parsed_response,
        errors=errors or [],
        warnings=warnings or [],
    )


__all__ = [
    "OrchestrationResult",
    "OrchestrationSummary",
    "create_summary",
    "result_ok",
    "result_failed",
]
