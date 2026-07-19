"""
Question Factory OS v2.0

R02 Validator

Academic integrity validation.

Verifies the internal academic consistency of
generated questions after structural validation.
"""

from __future__ import annotations

from Engine.factory.validation.validator_base import (
    ValidationModule,
)

from Engine.factory.validation.validation_result_model import (
    ValidationResultModel,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


class R02Validator(ValidationModule):
    """
    Academic integrity validator.
    """

    @property
    def name(self) -> str:

        return "R02 Academic Validator"

    @property
    def validation_code(self) -> str:

        return "R02"

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        batch: QuestionBatchModel,
    ) -> ValidationResultModel:
        """
        Execute academic validation.
        """

        result = ValidationResultModel(
            validator_name=self.name,
            rule_code=self.validation_code,
            success=True,
        )

        self._validate_answers(
            batch,
            result,
        )

        self._validate_explanations(
            batch,
            result,
        )

        self._validate_question_integrity(
            batch,
            result,
        )

        if result.has_errors():

            result.mark_failure()

        else:

            result.mark_success()

        return result

    # ---------------------------------------------------------
    # Answer Validation
    # ---------------------------------------------------------

    def _validate_answers(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate answer options and the
        correct answer.
        """

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            self._validate_question_answers(
                index,
                question,
                result,
            )

    def _validate_question_answers(
        self,
        index: int,
        question,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate one question's answer set.
        """

        #
        # Empty options
        #

        for option_index, option in enumerate(
            question.options,
            start=1,
        ):

            if not option.strip():

                result.add_error(
                    f"Question {index}: " f"Option {option_index} " "is empty."
                )

        #
        # Duplicate options
        #

        normalized = [option.strip().lower() for option in question.options]

        unique = {option for option in normalized if option}

        if len(unique) != len(normalized):

            result.add_error(f"Question {index}: " "Duplicate options detected.")

        #
        # Correct option
        #

        if question.correct_option not in {"A", "B", "C", "D"}:

            result.add_error(f"Question {index}: " "Invalid correct option.")

        option_map = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
        }

        if question.correct_option in option_map:

            option_index = option_map[question.correct_option]

            if option_index >= len(question.options):

                result.add_error(
                    f"Question {index}: " "Correct option does not " "exist."
                )

            elif not question.options[option_index].strip():

                result.add_error(
                    f"Question {index}: " "Correct option refers to " "an empty choice."
                )

    # ---------------------------------------------------------
    # Explanation Validation
    # ---------------------------------------------------------

    def _validate_explanations(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate explanations for every question.
        """

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            explanation = question.explanation.strip()

            if not explanation:

                result.add_warning(f"Question {index}: " "Explanation is empty.")

                continue

            if len(explanation) < 20:

                result.add_warning(
                    f"Question {index}: " "Explanation appears too short."
                )

    # ---------------------------------------------------------
    # Question Integrity
    # ---------------------------------------------------------

    def _validate_question_integrity(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate internal question consistency.
        """

        for index, question in enumerate(
            batch.questions,
            start=1,
        ):

            self._validate_single_question(
                index,
                question,
                result,
            )

    def _validate_single_question(
        self,
        index: int,
        question,
        result: ValidationResultModel,
    ) -> None:
        """
        Validate one question.
        """

        question_text = question.question_text.strip().lower()

        #
        # Question identical to an option
        #

        for option_number, option in enumerate(
            question.options,
            start=1,
        ):

            normalized_option = option.strip().lower()

            if question_text and question_text == normalized_option:

                result.add_error(
                    f"Question {index}: "
                    f"Question text matches "
                    f"Option {option_number}."
                )

        #
        # Very short question
        #

        if len(question_text) < 10:

            result.add_warning(
                f"Question {index}: " "Question text appears " "too short."
            )

        #
        # Basic ambiguity indicators
        #

        ambiguous_terms = {
            "maybe",
            "possibly",
            "approximately",
            "around",
        }

        lowered = question_text

        for term in ambiguous_terms:

            if term in lowered:

                result.add_warning(
                    f"Question {index}: "
                    f"Potential ambiguity "
                    f"('{term}') detected."
                )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> dict[str, object]:
        """
        Return R02 validation statistics.
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
        Return a concise R02 validation summary.
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
        Describe R02 validator capabilities.
        """

        return {
            "answer_validation": True,
            "option_validation": True,
            "explanation_validation": True,
            "question_integrity": True,
            "ambiguity_detection": True,
            "diagnostics": True,
            "statistics": True,
            "health_reporting": True,
        }

    # ---------------------------------------------------------
    # Execution Information
    # ---------------------------------------------------------

    def execution_information(
        self,
    ) -> dict[str, object]:
        """
        Return validator execution information.
        """

        return {
            "validator": self.name,
            "rule_code": self.validation_code,
            "execution_mode": "SEQUENTIAL",
            "validation_scope": "ACADEMIC",
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
            "validation_scope": "ACADEMIC",
            "version": "2.1.0",
            "execution": (self.execution_information()),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return "R02Validator(" f"rule='{self.validation_code}')"

    def __str__(
        self,
    ) -> str:

        return f"{self.validation_code} - " "Academic Validation"
