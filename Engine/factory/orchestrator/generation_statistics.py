"""
Question Factory OS v2.1

Generation Statistics

Collects runtime statistics for a complete
manufacturing cycle.

Responsibilities
----------------
• Generation statistics
• Validation statistics
• Repair statistics
• AI execution statistics
• Timing metrics
• Runtime diagnostics

This class is purely informational and
contains no orchestration logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class GenerationStatistics:
    """
    Runtime statistics for one generation cycle.
    """

    VERSION = "2.1.0"

    COMPONENT_NAME = "Generation Statistics"

    # ---------------------------------------------------------
    # Batch Information
    # ---------------------------------------------------------

    batch_id: str = ""

    unit_code: str = ""

    chapter_code: str = ""

    subtopic_code: str = ""

    # ---------------------------------------------------------
    # Question Statistics
    # ---------------------------------------------------------

    requested_questions: int = 0

    generated_questions: int = 0

    validated_questions: int = 0

    repaired_questions: int = 0

    failed_questions: int = 0

    # ---------------------------------------------------------
    # Timing
    # ---------------------------------------------------------

    started_at: datetime | None = None

    completed_at: datetime | None = None

    duration_seconds: float = 0.0

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def start(
        self,
    ) -> None:
        """
        Mark generation start.
        """

        self.started_at = datetime.utcnow()

    def finish(
        self,
    ) -> None:
        """
        Mark generation completion.
        """

        self.completed_at = datetime.utcnow()

        if self.started_at is not None:

            self.duration_seconds = (
                self.completed_at
                - self.started_at
            ).total_seconds()
    # ---------------------------------------------------------
    # Question Counters
    # ---------------------------------------------------------

    def increment_generated(
        self,
        count: int = 1,
    ) -> None:
        """
        Increment generated question count.
        """

        self.generated_questions += count

    def increment_validated(
        self,
        count: int = 1,
    ) -> None:
        """
        Increment validated question count.
        """

        self.validated_questions += count

    def increment_repaired(
        self,
        count: int = 1,
    ) -> None:
        """
        Increment repaired question count.
        """

        self.repaired_questions += count

    def increment_failed(
        self,
        count: int = 1,
    ) -> None:
        """
        Increment failed question count.
        """

        self.failed_questions += count

    # ---------------------------------------------------------
    # Derived Statistics
    # ---------------------------------------------------------

    @property
    def success_rate(
        self,
    ) -> float:
        """
        Return generation success rate.
        """

        if self.requested_questions <= 0:

            return 0.0

        return (
            self.generated_questions
            / self.requested_questions
        ) * 100.0

    @property
    def validation_rate(
        self,
    ) -> float:
        """
        Return validation success rate.
        """

        if self.generated_questions <= 0:

            return 0.0

        return (
            self.validated_questions
            / self.generated_questions
        ) * 100.0

    @property
    def repair_rate(
        self,
    ) -> float:
        """
        Return repair percentage.
        """

        if self.generated_questions <= 0:

            return 0.0

        return (
            self.repaired_questions
            / self.generated_questions
        ) * 100.0
    # ---------------------------------------------------------
    # Export
    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Export statistics as a dictionary.
        """

        return {
            "component": self.COMPONENT_NAME,
            "version": self.VERSION,
            "batch_id": self.batch_id,
            "unit_code": self.unit_code,
            "chapter_code": self.chapter_code,
            "subtopic_code": self.subtopic_code,
            "requested_questions": self.requested_questions,
            "generated_questions": self.generated_questions,
            "validated_questions": self.validated_questions,
            "repaired_questions": self.repaired_questions,
            "failed_questions": self.failed_questions,
            "success_rate": round(
                self.success_rate,
                2,
            ),
            "validation_rate": round(
                self.validation_rate,
                2,
            ),
            "repair_rate": round(
                self.repair_rate,
                2,
            ),
            "duration_seconds": round(
                self.duration_seconds,
                3,
            ),
            "started_at": (
                self.started_at.isoformat()
                if self.started_at
                else None
            ),
            "completed_at": (
                self.completed_at.isoformat()
                if self.completed_at
                else None
            ),
            "metadata": dict(
                self.metadata,
            ),
        }

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add or update a metadata value.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a metadata value.
        """

        return self.metadata.get(
            key,
            default,
        )

    def clear_metadata(
        self,
    ) -> None:
        """
        Remove all metadata entries.
        """

        self.metadata.clear()
    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset all runtime statistics.
        """

        self.generated_questions = 0
        self.validated_questions = 0
        self.repaired_questions = 0
        self.failed_questions = 0

        self.started_at = None
        self.completed_at = None
        self.duration_seconds = 0.0

        self.metadata.clear()

    # ---------------------------------------------------------
    # Runtime Information
    # ---------------------------------------------------------

    @property
    def component_name(
        self,
    ) -> str:
        """
        Human-readable component name.
        """

        return self.COMPONENT_NAME

    @property
    def version(
        self,
    ) -> str:
        """
        Component version.
        """

        return self.VERSION

    def runtime_summary(
        self,
    ) -> dict[str, Any]:
        """
        Return a concise runtime summary.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "batch_id": self.batch_id,
            "generated": self.generated_questions,
            "validated": self.validated_questions,
            "repaired": self.repaired_questions,
            "failed": self.failed_questions,
            "duration_seconds": round(
                self.duration_seconds,
                3,
            ),
            "status": (
                "COMPLETED"
                if self.completed_at is not None
                else "RUNNING"
            ),
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return component health.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "healthy": True,
            "tracking": True,
            "timing": True,
            "metadata": True,
        }
    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.COMPONENT_NAME}"
            f"(version='{self.VERSION}', "
            f"batch_id='{self.batch_id}', "
            f"generated={self.generated_questions}, "
            f"validated={self.validated_questions})"
        )

    def __str__(
        self,
    ) -> str:
        """
        Human-readable representation.
        """

        return (
            f"{self.COMPONENT_NAME} "
            f"[Batch={self.batch_id}, "
            f"Generated={self.generated_questions}, "
            f"Validated={self.validated_questions}, "
            f"Duration={self.duration_seconds:.3f}s]"
        )

    # ---------------------------------------------------------
    # Convenience Helpers
    # ---------------------------------------------------------

    @property
    def is_running(
        self,
    ) -> bool:
        """
        True while a generation cycle is active.
        """

        return (
            self.started_at is not None
            and self.completed_at is None
        )

    @property
    def is_completed(
        self,
    ) -> bool:
        """
        True when the generation cycle has finished.
        """

        return self.completed_at is not None

    @property
    def total_processed(
        self,
    ) -> int:
        """
        Total processed questions.
        """

        return (
            self.validated_questions
            + self.failed_questions
        )

    @property
    def completion_rate(
        self,
    ) -> float:
        """
        Percentage of requested questions processed.
        """

        if self.requested_questions <= 0:
            return 0.0

        return (
            self.total_processed
            / self.requested_questions
        ) * 100.0
    