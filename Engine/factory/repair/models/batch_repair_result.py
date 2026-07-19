"""
Question Factory OS v2.1

Batch Repair Result

Aggregated result returned by the
Repair Engine after executing every
registered repair module.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from Engine.factory.repair.repair_result_model import (
    RepairResultModel,
)
from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


@dataclass(slots=True)
class BatchRepairResult:
    """
    Represents the complete repair
    outcome for a question batch.
    """

    batch: QuestionBatchModel

    success: bool = True

    repair_executed: bool = False

    repaired_question_count: int = 0

    failed_question_count: int = 0

    warning_count: int = 0

    module_results: list[
        RepairResultModel
    ] = field(default_factory=list)

    metadata: dict[
        str,
        Any,
    ] = field(default_factory=dict)
    # ---------------------------------------------------------
    # Result Management
    # ---------------------------------------------------------

    def add_result(
        self,
        result: RepairResultModel,
    ) -> None:
        """
        Add a repair result and refresh
        aggregate statistics.
        """

        self.module_results.append(
            result,
        )

        self.update_statistics()

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def update_statistics(
        self,
    ) -> None:
        """
        Recalculate aggregate repair
        statistics.
        """

        self.repaired_question_count = sum(
            result.repaired_count
            for result in self.module_results
        )

        self.failed_question_count = sum(
            result.failed_count
            for result in self.module_results
        )

        self.warning_count = sum(
            result.warning_count
            for result in self.module_results
        )

        self.repair_executed = (
            len(self.module_results) > 0
        )

        self.success = all(
            result.repaired
            for result in self.module_results
        )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict[str, int | bool]:
        """
        Return a concise repair summary.
        """

        return {
            "success": self.success,
            "repair_executed": self.repair_executed,
            "module_count": len(
                self.module_results,
            ),
            "repaired_questions": (
                self.repaired_question_count
            ),
            "failed_questions": (
                self.failed_question_count
            ),
            "warnings": self.warning_count,
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return repair diagnostics.
        """

        return {
            "summary": self.summary(),
            "metadata": dict(
                self.metadata,
            ),
            "module_results": len(
                self.module_results,
            ),
        }
    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return overall repair health.
        """

        return {
            "component": self.__class__.__name__,
            "status": (
                "SUCCESS"
                if self.success
                else "FAILED"
            ),
            "repair_executed": self.repair_executed,
            "module_count": len(
                self.module_results,
            ),
            "repaired_questions": (
                self.repaired_question_count
            ),
            "failed_questions": (
                self.failed_question_count
            ),
            "warnings": self.warning_count,
        }

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, object]:
        """
        Return a serializable
        representation.
        """

        return {
            "success": self.success,
            "repair_executed": self.repair_executed,
            "repaired_question_count": (
                self.repaired_question_count
            ),
            "failed_question_count": (
                self.failed_question_count
            ),
            "warning_count": self.warning_count,
            "module_count": len(
                self.module_results,
            ),
            "metadata": dict(
                self.metadata,
            ),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"success={self.success}, "
            f"modules={len(self.module_results)}, "
            f"repaired={self.repaired_question_count}, "
            f"failed={self.failed_question_count}, "
            f"warnings={self.warning_count}"
            f")"
        )

    __str__ = __repr__
