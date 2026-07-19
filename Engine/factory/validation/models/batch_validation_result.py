"""
Question Factory OS v2.1

Batch Validation Result

Represents the outcome of validating an
entire QuestionBatchModel.

Produced by
-----------
ValidationEngine

Consumed by
-----------
FactoryOrchestrator
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from Engine.factory.validation.validation_result_model import (
    ValidationResultModel,
)
from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


@dataclass(slots=True)
class BatchValidationResult:
    """
    Represents the complete validation
    result for a question batch.
    """

    # ---------------------------------------------------------
    # Batch
    # ---------------------------------------------------------

    batch: QuestionBatchModel

    # ---------------------------------------------------------
    # Overall Result
    # ---------------------------------------------------------

    is_valid: bool = True

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    total_questions: int = 0

    valid_question_count: int = 0

    invalid_question_count: int = 0

    error_count: int = 0

    warning_count: int = 0

    # ---------------------------------------------------------
    # Validator Results
    # ---------------------------------------------------------

    validator_results: list[
        ValidationResultModel
    ] = field(
        default_factory=list,
    )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
    # ---------------------------------------------------------
    # Result Management
    # ---------------------------------------------------------

    def add_result(
        self,
        result: ValidationResultModel,
    ) -> None:
        """
        Add a validator result and update
        aggregate statistics.
        """

        self.validator_results.append(result)

        self.update_statistics()

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add or update metadata.
        """

        self.metadata[key] = value

    def clear_metadata(
        self,
    ) -> None:
        """
        Remove all metadata.
        """

        self.metadata.clear()

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def update_statistics(
        self,
    ) -> None:
        """
        Recalculate aggregate statistics
        from validator results.
        """

        self.total_questions = (
            len(self.batch.questions)
        )

        self.error_count = sum(
            len(result.errors)
            for result in self.validator_results
        )

        self.warning_count = sum(
            len(result.warnings)
            for result in self.validator_results
        )

        self.is_valid = all(
            result.is_successful()
            for result in self.validator_results
        )

        if self.validator_results:

            self.valid_question_count = (
                self.total_questions
                if self.is_valid
                else 0
            )

            self.invalid_question_count = (
                self.total_questions
                - self.valid_question_count
            )

        else:

            self.valid_question_count = 0
            self.invalid_question_count = 0

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset validation results while
        preserving the batch.
        """

        self.is_valid = True

        self.total_questions = 0

        self.valid_question_count = 0
        self.invalid_question_count = 0

        self.error_count = 0
        self.warning_count = 0

        self.validator_results.clear()

        self.metadata.clear()

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict[str, object]:
        """
        Return a concise validation
        summary.
        """

        return {
            "is_valid": self.is_valid,
            "total_questions": self.total_questions,
            "valid_questions": (
                self.valid_question_count
            ),
            "invalid_questions": (
                self.invalid_question_count
            ),
            "validator_count": (
                len(self.validator_results)
            ),
            "errors": self.error_count,
            "warnings": self.warning_count,
        }
    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return detailed diagnostic information.
        """

        return {
            "component": self.__class__.__name__,
            "batch_id": self.batch.batch_id,
            "summary": self.summary(),
            "metadata": dict(self.metadata),
            "validator_results": (
                len(self.validator_results)
            ),
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return validation health information.
        """

        return {
            "component": self.__class__.__name__,
            "status": (
                "READY"
                if self.is_valid
                else "FAILED"
            ),
            "batch_id": self.batch.batch_id,
            "validator_count": (
                len(self.validator_results)
            ),
            "error_count": self.error_count,
            "warning_count": self.warning_count,
        }

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, object]:
        """
        Convert the result into a serializable
        dictionary.
        """

        return {
            "batch_id": self.batch.batch_id,
            "is_valid": self.is_valid,
            "total_questions": self.total_questions,
            "valid_question_count": (
                self.valid_question_count
            ),
            "invalid_question_count": (
                self.invalid_question_count
            ),
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "validator_results": [
                result.to_dict()
                for result in self.validator_results
            ],
            "metadata": dict(self.metadata),
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
            "BatchValidationResult("
            f"is_valid={self.is_valid}, "
            f"questions={self.total_questions}, "
            f"errors={self.error_count}, "
            f"warnings={self.warning_count})"
        )

    def __str__(
        self,
    ) -> str:
        """
        Human-readable representation.
        """

        status = (
            "PASSED"
            if self.is_valid
            else "FAILED"
        )

        return (
            f"Batch Validation "
            f"[{status}] "
            f"({self.valid_question_count}/"
            f"{self.total_questions})"
        )
