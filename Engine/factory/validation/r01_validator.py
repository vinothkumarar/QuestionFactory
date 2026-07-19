"""
Question Factory OS v2.0

R01 Validator

Structural validation.

Verifies that every generated question satisfies
the minimum structural requirements before
academic validation begins.
"""

from __future__ import annotations

from collections import Counter

from Engine.factory.validation.validator_base import (
    ValidationModule,
)

from Engine.factory.validation.validation_result_model import (
    ValidationResultModel,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


class R01Validator(ValidationModule):
    """
    Structural validator.
    """

    @property
    def name(self) -> str:

        return "R01 Structural Validator"

    @property
    def validation_code(self) -> str:

        return "R01"

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        batch: QuestionBatchModel,
    ) -> ValidationResultModel:
        """
        Execute structural validation.
        """
        
        result = ValidationResultModel(
            validator_name=self.name,
            rule_code=self.validation_code,
            success=True,
        )

        self._validate_batch(
            batch,
            result,
        )

        self._validate_questions(
            batch,
            result,
        )

        self._validate_duplicates(
            batch,
            result,
        )

        if result.has_errors():

            result.mark_failure()

        else:

            result.mark_success()

        return result

    # ---------------------------------------------------------
    # Batch Validation
    # ---------------------------------------------------------

    def _validate_batch(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate the overall batch structure.
        """

        if batch is None:

            result.add_error("Batch is None.")

            return

        if batch.is_empty():

            result.add_error("Batch contains no questions.")

            return

        if not batch.batch_id.strip():

            result.add_warning("Batch ID is empty.")

        if not batch.unit_code.strip():

            result.add_warning("Unit code is empty.")

        if not batch.chapter_code.strip():

            result.add_warning("Chapter code is empty.")

        if not batch.subtopic_code.strip():

            result.add_warning("Subtopic code is empty.")

    # ---------------------------------------------------------
    # Question Validation
    # ---------------------------------------------------------

    def _validate_questions(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate the structural integrity of every
        generated question.
        """

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            self._validate_question(
                index,
                question,
                result,
            )

    def _validate_question(
        self,
        index: int,
        question,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate one generated question.
        """

        if not question.question_code.strip():

            result.add_error(f"Question {index}: " "Missing question code.")

        if not question.question_text.strip():

            result.add_error(f"Question {index}: " "Question text is empty.")

        if len(question.options) < 4:

            result.add_error(f"Question {index}: " "Less than four options found.")

        if not question.correct_option.strip():

            result.add_error(f"Question {index}: " "Correct option not specified.")

        if question.correct_option and question.correct_option not in {
            "A",
            "B",
            "C",
            "D",
        }:

            result.add_error(
                f"Question {index}: " "Correct option must be " "A, B, C or D."
            )

        if not question.explanation.strip():

            result.add_warning(f"Question {index}: " "Explanation is empty.")

    # ---------------------------------------------------------
    # Duplicate Validation
    # ---------------------------------------------------------

    def _validate_duplicates(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate duplicate question codes.
        """

        question_codes = [
            question.question_code
            for question in batch.questions
            if question.question_code.strip()
        ]

        duplicates = [
            code for code, count in Counter(question_codes).items() if count > 1
        ]

        for code in duplicates:

            result.add_error(f"Duplicate question code: {code}")

    # ---------------------------------------------------------
    # Batch Consistency
    # ---------------------------------------------------------

    def _validate_consistency(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Ensure every question belongs to the
        expected production location.
        """

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            if question.unit_code and question.unit_code != batch.unit_code:

                result.add_error(f"Question {index}: " "Unit code mismatch.")

            if question.chapter_code and question.chapter_code != batch.chapter_code:

                result.add_error(f"Question {index}: " "Chapter code mismatch.")

            if question.subtopic_code and question.subtopic_code != batch.subtopic_code:

                result.add_error(f"Question {index}: " "Subtopic code mismatch.")

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> dict[str, object]:
        """
        Return R01 validation statistics.
        """

        return {
            "questions_checked": (batch.question_count),
            "errors": (result.error_count),
            "warnings": (result.warning_count),
            "passed": (result.is_successful()),
        }

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------
    
    def summary(
        self,
        result: ValidationResultModel,
    ) -> dict[str, object]:
        """
        Return a concise R01 validation summary.
        """

        return {
            "validator": self.name,
            "rule_code": self.validation_code,
            "success": (result.is_successful()),
            "errors": (result.error_count),
            "warnings": (result.warning_count),
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------
    
    def diagnostics(
        self,
        result: ValidationResultModel | None = None,
    ) -> dict[str, object]:
        """
        Return detailed R01 diagnostics.
        """

        diagnostics: dict[str, object] = {
            "component": self.__class__.__name__,
        }

        if result is not None:
            diagnostics.update(
                {
                    "summary": self.summary(result),
                    "statistics": result.statistics(),
                    "metadata": dict(result.metadata),
                }
            )

        return diagnostics
    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(self) -> dict[str, object]:
        """
        Return validator health information.
        """

        return {
            "validator": self.name,
            "rule_code": self.validation_code,
            "version": "2.1.0",
            "status": "READY",
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(self) -> dict[str, object]:
        """
        Describe R01 validator capabilities.
        """

        return {
            "batch_validation": True,
            "question_validation": True,
            "duplicate_detection": True,
            "consistency_validation": True,
            "diagnostics": True,
            "statistics": True,
            "health_reporting": True,
        }

    # ---------------------------------------------------------
    # Execution Information
    # ---------------------------------------------------------

    def execution_information(self) -> dict[str, object]:
        """
        Return execution information.
        """

        return {
            "validator": self.name,
            "rule_code": self.validation_code,
            "execution_mode": "SEQUENTIAL",
            "validation_scope": "STRUCTURAL",
            "framework_version": "2.1.0",
        }

    # ---------------------------------------------------------
    # Validator Information
    # ---------------------------------------------------------

    def validator_information(
        self,
    ) -> dict[str, object]:
        """
        Return validator information.
        """

        return {
            "name": self.name,
            "rule_code": self.validation_code,
            "validation_scope": "STRUCTURAL",
            "version": "2.1.0",
            "execution": (self.execution_information()),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "R01Validator("
            f"rule='{self.validation_code}')"
        )

    def __str__(
        self,
    ) -> str:

        return f"{self.validation_code} - " "Structural Validation"
