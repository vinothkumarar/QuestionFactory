"""
Question Factory OS v2.1

Validation Engine

Coordinates execution of the Factory
Validation subsystem.

Pipeline
--------
QuestionBatchModel
        │
        ▼
QuestionValidator
        │
        ├── R01
        ├── R02
        └── R03
        │
        ▼
BatchValidationResult
"""

from __future__ import annotations

import logging

from Engine.factory.validation.models.batch_validation_result import (
    BatchValidationResult,
)
from Engine.factory.validation.question_validator import (
    QuestionValidator,
)
from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


class ValidationEngine:
    """
    Factory Validation Engine.

    Acts as the bridge between the
    FactoryOrchestrator and the
    QuestionValidator.
    """

    VERSION = "2.1.0"

    COMPONENT_NAME = "Validation Engine"

    def __init__(
        self,
        validator: QuestionValidator | None = None,
    ) -> None:
        """
        Initialize the validation engine.
        """

        self._logger = logging.getLogger(
            self.__class__.__name__,
        )

        self._validator = (
            validator
            if validator is not None
            else QuestionValidator()
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def validate(
        self,
        batch: QuestionBatchModel,
    ) -> BatchValidationResult:
        """
        Execute validation for the supplied
        question batch.
        """

        self._logger.info(
            "Starting batch validation."
        )

        result = BatchValidationResult(
            batch=batch,
        )
        validator_results = (
            self._validator.execute(
                batch,
            )
        )

        for validator_result in validator_results:

            result.add_result(
                validator_result,
            )

        result.update_statistics()

        self._logger.info(
            (
                "Validation completed. "
                "Validators=%d "
                "Errors=%d "
                "Warnings=%d"
            ),
            len(result.validator_results),
            result.error_count,
            result.warning_count,
        )

        return result

    # ---------------------------------------------------------
    # Validator Management
    # ---------------------------------------------------------

    def add_validator(
        self,
        validator,
    ) -> None:
        """
        Register a validation module.
        """

        self._validator.add_validator(
            validator,
        )

    def remove_validator(
        self,
        validator_name: str,
    ) -> bool:
        """
        Remove a registered validator.
        """

        return self._validator.remove_validator(
            validator_name,
        )

    def clear_validators(
        self,
    ) -> None:
        """
        Remove every registered validator.
        """

        self._validator.clear()
    # ---------------------------------------------------------
    # Validator Information
    # ---------------------------------------------------------

    @property
    def validator_count(
        self,
    ) -> int:
        """
        Return the number of registered
        validators.
        """

        return self._validator.validator_count

    def validator_names(
        self,
    ) -> list[str]:
        """
        Return registered validator names.
        """

        return self._validator.validator_names()

    def has_validator(
        self,
        validator_name: str,
    ) -> bool:
        """
        Determine whether a validator
        is registered.
        """

        return self._validator.has_validator(
            validator_name,
        )

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate the validator
        configuration.
        """

        self._validator.validate_configuration()

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset the validation engine.
        """

        self._validator.clear()

        self._logger.info(
            "Validation engine reset."
        )

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
    # ---------------------------------------------------------
    # Runtime Information
    # ---------------------------------------------------------

    def runtime_summary(
        self,
    ) -> dict[str, object]:
        """
        Return a concise runtime summary.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
            "validator_count": self.validator_count,
            "validators": self.validator_names(),
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return validation engine health
        information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "healthy": True,
            "validator_count": self.validator_count,
            "registered_validators": (
                self.validator_names()
            ),
            "status": "READY",
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return detailed diagnostics for
        the validation engine.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "validator_count": self.validator_count,
            "validators": self.validator_names(),
            "runtime": self.runtime_summary(),
            "health": self.health(),
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(
        self,
    ) -> dict[str, bool]:
        """
        Describe validation engine
        capabilities.
        """

        return {
            "batch_validation": True,
            "validator_registration": True,
            "validator_removal": True,
            "configuration_validation": True,
            "runtime_summary": True,
            "health_reporting": True,
            "diagnostics": True,
        }
    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    def execution_information(
        self,
    ) -> dict[str, object]:
        """
        Return execution information.
        """

        return {
            "execution_model": "SEQUENTIAL",
            "component": self.component_name,
            "validator_count": self.validator_count,
            "validators": self.validator_names(),
        }

    def validator_information(
        self,
    ) -> dict[str, object]:
        """
        Return validator information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "validator_count": self.validator_count,
            "validators": self.validator_names(),
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
            f"{self.__class__.__name__}("
            f"validators={self.validator_count}, "
            f"version='{self.version}')"
        )

    def __str__(
        self,
    ) -> str:
        """
        Human-readable representation.
        """

        return (
            f"{self.component_name} "
            f"v{self.version} "
            f"({self.validator_count} validator(s))"
        )
        