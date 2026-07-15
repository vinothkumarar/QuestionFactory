"""
Question Factory OS v2.0

Validator Base

Provides the common implementation shared by
all validation rules.

Concrete validators should inherit from this
class and implement only the validation logic.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from Engine.factory.validation.validation_result_model import (
    ValidationResultModel,
)

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


class ValidatorBase(ABC):
    """
    Base class for all validators.
    """

    def __init__(self):

        self.logger = logging.getLogger(self.__class__.__name__)

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Validator name.
        """

    @property
    @abstractmethod
    def rule_code(self) -> str:
        """
        Validation rule identifier.
        """

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    @abstractmethod
    def validate(
        self,
        batch: QuestionBatchModel,
    ) -> ValidationResultModel:
        """
        Execute validation.
        """

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_validation(
        self,
        batch: QuestionBatchModel,
    ) -> None:
        """
        Executed immediately before validation.

        Override in derived validators when
        custom preprocessing is required.
        """

        return

    def after_validation(
        self,
        batch: QuestionBatchModel,
        result: ValidationResultModel,
    ) -> None:
        """
        Executed immediately after validation.

        Override for reporting, telemetry or
        custom post-processing.
        """

        return

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        batch: QuestionBatchModel,
    ) -> ValidationResultModel:
        """
        Execute the complete validation workflow.
        """

        self.logger.info(
            "Executing validator: %s",
            self.name,
        )

        self.before_validation(batch)

        result = self.validate(batch)

        self.after_validation(
            batch,
            result,
        )

        self.logger.info(
            "Validator '%s' completed.",
            self.name,
        )

        return result

    # ---------------------------------------------------------
    # Result Helpers
    # ---------------------------------------------------------

    def create_success_result(
        self,
    ) -> ValidationResultModel:
        """
        Create a successful validation result.
        """

        result = ValidationResultModel(
            validator_name=self.name,
            rule_code=self.rule_code,
        )

        result.mark_success()

        return result

    def create_failure_result(
        self,
    ) -> ValidationResultModel:
        """
        Create a failed validation result.
        """

        result = ValidationResultModel(
            validator_name=self.name,
            rule_code=self.rule_code,
        )

        result.mark_failure()

        return result

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(
        self,
        result: ValidationResultModel,
    ) -> dict:
        """
        Return a concise validation summary.
        """

        return {
            "validator": self.name,
            "rule_code": self.rule_code,
            "success": result.is_successful(),
            "errors": result.error_count,
            "warnings": result.warning_count,
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
        result: ValidationResultModel,
    ) -> dict:
        """
        Return validator diagnostics.
        """

        return {
            "component": self.__class__.__name__,
            "summary": self.summary(result),
            "statistics": result.statistics(),
        }

    # ---------------------------------------------------------
    # Component Information
    # ---------------------------------------------------------

    @property
    def version(self) -> str:
        """
        Validator framework version.
        """

        return "2.0.0"

    @property
    def component_name(self) -> str:
        """
        Component name.
        """

        return "Validator Base"

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(self) -> dict:
        """
        Return validator health information.
        """

        return {
            "component": self.component_name,
            "validator": self.name,
            "rule_code": self.rule_code,
            "version": self.version,
            "status": "READY",
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(self) -> dict:
        """
        Describe validator capabilities.
        """

        return {
            "execution_pipeline": True,
            "lifecycle_hooks": True,
            "result_helpers": True,
            "diagnostics": True,
            "health_reporting": True,
            "summary": True,
        }

    # ---------------------------------------------------------
    # Execution Information
    # ---------------------------------------------------------

    def execution_information(
        self,
    ) -> dict:
        """
        Return validator execution information.
        """

        return {
            "validator": self.name,
            "rule_code": self.rule_code,
            "execution_mode": "SEQUENTIAL",
            "framework_version": self.version,
        }

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate the validator configuration.

        Raises
        ------
        ValueError
            If required properties are invalid.
        """

        if not self.name.strip():

            raise ValueError("Validator name cannot be empty.")

        if not self.rule_code.strip():

            raise ValueError("Rule code cannot be empty.")

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def create_metadata(
        self,
    ) -> dict:
        """
        Create the default validator metadata.
        """

        return {
            "validator": self.name,
            "rule_code": self.rule_code,
            "framework_version": self.version,
        }

    def reset_result(
        self,
        result: ValidationResultModel,
    ) -> None:
        """
        Reset a validation result.
        """

        result.reset()

        result.validator_name = self.name
        result.rule_code = self.rule_code

    def supports_batch_validation(
        self,
    ) -> bool:
        """
        Indicates whether this validator operates
        on complete batches.

        Override in derived validators if a rule
        validates individual questions instead.
        """

        return True

    # ---------------------------------------------------------
    # Validator Information
    # ---------------------------------------------------------

    def validator_information(
        self,
    ) -> dict:
        """
        Return validator information.
        """

        return {
            "name": self.name,
            "rule_code": self.rule_code,
            "component": self.component_name,
            "version": self.version,
            "execution": (self.execution_information()),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return "ValidatorBase(" f"name='{self.name}', " f"rule='{self.rule_code}')"

    def __str__(
        self,
    ) -> str:

        return f"{self.rule_code} - " f"{self.name}"
