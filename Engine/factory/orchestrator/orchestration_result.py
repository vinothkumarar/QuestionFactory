"""
Question Factory OS v2.1

Orchestration Result

Represents the immutable outcome of one
complete manufacturing orchestration cycle.

Pipeline
--------
AI Generation
    ↓
Batch Construction
    ↓
Validation
    ↓
Repair
    ↓
Statistics
    ↓
Orchestration Result
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from typing import Any

from Engine.factory.orchestrator.generation_statistics import (
    GenerationStatistics,
)
from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


# ---------------------------------------------------------------------
# Primary Result
# ---------------------------------------------------------------------


@dataclass(slots=True, frozen=True)
class OrchestrationResult:
    """
    Immutable result returned by FactoryOrchestrator.

    This object represents the final outcome of one
    autonomous manufacturing cycle.

    It contains the generated batch together with
    validation, repair and runtime statistics.
    """

    # -------------------------------------------------------------
    # Overall Status
    # -------------------------------------------------------------

    success: bool

    # -------------------------------------------------------------
    # Generation Output
    # -------------------------------------------------------------

    parsed_response: Any | None = None

    batch: QuestionBatchModel | None = None

    # -------------------------------------------------------------
    # Runtime Information
    # -------------------------------------------------------------

    statistics: GenerationStatistics | None = None

    message: str = ""

    # -------------------------------------------------------------
    # Validation / Repair
    # -------------------------------------------------------------

    validation_results: list[Any] = field(
        default_factory=list,
    )

    repair_results: list[Any] = field(
        default_factory=list,
    )
    # -------------------------------------------------------------
    # Additional Information
    # -------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    warnings: list[str] = field(
        default_factory=list,
    )

    errors: list[str] = field(
        default_factory=list,
    )

    # -------------------------------------------------------------
    # Convenience Properties
    # -------------------------------------------------------------

    @property
    def has_batch(
        self,
    ) -> bool:
        """
        Return True if a question batch is available.
        """

        return self.batch is not None

    @property
    def has_statistics(
        self,
    ) -> bool:
        """
        Return True if runtime statistics are available.
        """

        return self.statistics is not None

    @property
    def has_warnings(
        self,
    ) -> bool:
        """
        Return True if warnings were recorded.
        """

        return bool(self.warnings)

    @property
    def has_errors(
        self,
    ) -> bool:
        """
        Return True if errors were recorded.
        """

        return bool(self.errors)

    @property
    def validation_count(
        self,
    ) -> int:
        """
        Number of validation results.
        """

        return len(self.validation_results)

    @property
    def repair_count(
        self,
    ) -> int:
        """
        Number of repair results.
        """

        return len(self.repair_results)

    # -------------------------------------------------------------
    # Serialization
    # -------------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Return a serializable representation of the
        orchestration result.
        """

        return {
            "success": self.success,
            "message": self.message,
            "batch": self.batch,
            "parsed_response": self.parsed_response,
            "statistics": (
                self.statistics.to_dict()
                if self.statistics is not None
                else None
            ),
            "validation_results": self.validation_results,
            "repair_results": self.repair_results,
            "metadata": self.metadata,
            "warnings": self.warnings,
            "errors": self.errors,
        }
# ---------------------------------------------------------------------
# Summary Model
# ---------------------------------------------------------------------


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

    message: str


def create_summary(
    result: OrchestrationResult,
) -> OrchestrationSummary:
    """
    Create a compact orchestration summary.
    """

    return OrchestrationSummary(
        success=result.success,
        validation_count=result.validation_count,
        repair_count=result.repair_count,
        warning_count=len(result.warnings),
        error_count=len(result.errors),
        message=result.message,
    )


# ---------------------------------------------------------------------
# Convenience Factory Functions
# ---------------------------------------------------------------------


def result_ok(
    *,
    parsed_response: Any | None = None,
    batch: QuestionBatchModel | None = None,
    statistics: GenerationStatistics | None = None,
    validation_results: list[Any] | None = None,
    repair_results: list[Any] | None = None,
    metadata: dict[str, Any] | None = None,
    warnings: list[str] | None = None,
    message: str = "Manufacturing completed successfully.",
) -> OrchestrationResult:
    """
    Create a successful orchestration result.
    """

    return OrchestrationResult(
        success=True,
        parsed_response=parsed_response,
        batch=batch,
        statistics=statistics,
        message=message,
        validation_results=validation_results or [],
        repair_results=repair_results or [],
        metadata=metadata or {},
        warnings=warnings or [],
        errors=[],
    )


def result_failed(
    *,
    parsed_response: Any | None = None,
    batch: QuestionBatchModel | None = None,
    statistics: GenerationStatistics | None = None,
    errors: list[str] | None = None,
    warnings: list[str] | None = None,
    message: str = "Manufacturing failed.",
) -> OrchestrationResult:
    """
    Create a failed orchestration result.
    """

    return OrchestrationResult(
        success=False,
        parsed_response=parsed_response,
        batch=batch,
        statistics=statistics,
        message=message,
        validation_results=[],
        repair_results=[],
        metadata={},
        warnings=warnings or [],
        errors=errors or [],
    )


# ---------------------------------------------------------------------
# Public Exports
# ---------------------------------------------------------------------

__all__ = [
    "OrchestrationResult",
    "OrchestrationSummary",
    "create_summary",
    "result_ok",
    "result_failed",
]