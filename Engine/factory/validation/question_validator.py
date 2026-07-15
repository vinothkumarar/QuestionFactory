"""
Question Factory OS v2.0

Question Validator

Coordinates execution of all registered
question validators.

The QuestionValidator does not contain
validation logic itself. It orchestrates
specialized validators such as R01, R02
and R03.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import List

from Engine.models.question_batch_model import (
    QuestionBatchModel,
)


# ---------------------------------------------------------
# Validator Interface
# ---------------------------------------------------------

class Validator(ABC):
    """
    Base interface for every validator.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Validator name.
        """

    @abstractmethod
    def validate(
        self,
        batch: QuestionBatchModel,
    ):
        """
        Validate the supplied batch.
        """


# ---------------------------------------------------------
# Question Validator
# ---------------------------------------------------------

class QuestionValidator:
    """
    Coordinates execution of all validators.
    """

    def __init__(self):

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self._validators: List[
            Validator
        ] = []

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def validate(
        self,
        batch: QuestionBatchModel,
    ):
        """
        Execute every registered validator.
        """

        self.logger.info(
            "Starting validation."
        )

        results = []

        for validator in self._validators:

            self.logger.info(
                "Executing validator: %s",
                validator.name,
            )

            result = validator.validate(
                batch
            )

            results.append(
                result
            )

        self.logger.info(
            "Validation completed."
        )

        return results
            # ---------------------------------------------------------
    # Validator Management
    # ---------------------------------------------------------

    def add_validator(
        self,
        validator: Validator,
    ) -> None:
        """
        Register a validator.
        """

        self._validators.append(
            validator
        )

        self.logger.info(
            "Registered validator: %s",
            validator.name,
        )

    def remove_validator(
        self,
        validator_name: str,
    ) -> bool:
        """
        Remove a validator by name.

        Returns
        -------
        bool
            True if the validator was removed.
        """

        for validator in self._validators:

            if validator.name == validator_name:

                self._validators.remove(
                    validator
                )

                self.logger.info(
                    "Removed validator: %s",
                    validator_name,
                )

                return True

        return False

    def get_validator(
        self,
        validator_name: str,
    ) -> Validator | None:
        """
        Return a validator by name.
        """

        for validator in self._validators:

            if validator.name == validator_name:

                return validator

        return None

    def validators(
        self,
    ) -> List[Validator]:
        """
        Return a copy of all registered validators.
        """

        return list(
            self._validators
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all registered validators.
        """

        self._validators.clear()

        self.logger.info(
            "Validator registry cleared."
        )

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    @property
    def validator_count(
        self,
    ) -> int:
        """
        Return the number of registered validators.
        """

        return len(
            self._validators
        )

    def validator_names(
        self,
    ) -> List[str]:
        """
        Return validator names.
        """

        return [
            validator.name
            for validator
            in self._validators
        ]

    def has_validator(
        self,
        validator_name: str,
    ) -> bool:
        """
        Determine whether a validator exists.
        """

        return (
            validator_name
            in self.validator_names()
        )
            # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_validation(
        self,
        batch: QuestionBatchModel,
    ) -> None:
        """
        Executed immediately before validation begins.

        Override in derived implementations for
        telemetry, auditing or preprocessing.
        """

        return

    def after_validation(
        self,
        batch: QuestionBatchModel,
        results: List,
    ) -> None:
        """
        Executed immediately after validation
        completes.

        Override for reporting or metrics.
        """

        return

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    def execute(
        self,
        batch: QuestionBatchModel,
    ) -> List:
        """
        Execute the complete validation workflow.
        """

        self.before_validation(
            batch
        )

        results = self.validate(
            batch
        )

        self.after_validation(
            batch,
            results,
        )

        return results

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(
        self,
        results: List,
    ) -> dict:
        """
        Return a concise validation summary.
        """

        return {
            "validator_count": (
                self.validator_count
            ),
            "result_count": len(
                results
            ),
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
        results: List,
    ) -> dict:
        """
        Return validation diagnostics.
        """

        return {
            "component": (
                self.__class__.__name__
            ),
            "validators": (
                self.validator_names()
            ),
            "summary": self.summary(
                results
            ),
        }
            # ---------------------------------------------------------
    # Component Information
    # ---------------------------------------------------------

    @property
    def version(self) -> str:
        """
        Validator version.
        """

        return "2.0.0"

    @property
    def component_name(self) -> str:
        """
        Component name.
        """

        return "Question Validator"

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(self) -> dict:
        """
        Return validator health information.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "registered_validators": (
                self.validator_count
            ),
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
            "validator_registration": True,
            "validator_lookup": True,
            "validator_removal": True,
            "lifecycle_hooks": True,
            "diagnostics": True,
            "health_reporting": True,
            "batch_validation": True,
            "plugin_architecture": True,
        }

    # ---------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------

    def is_empty(self) -> bool:
        """
        Determine whether any validators
        are registered.
        """

        return self.validator_count == 0

    def validate_configuration(self) -> None:
        """
        Validate the validator configuration.

        Raises
        ------
        ValueError
            If duplicate validator names are found.
        """

        names = self.validator_names()

        duplicates = {
            name
            for name in names
            if names.count(name) > 1
        }

        if duplicates:

            duplicate_list = ", ".join(
                sorted(duplicates)
            )

            raise ValueError(
                "Duplicate validators detected: "
                f"{duplicate_list}"
            )

    def execution_information(self) -> dict:
        """
        Return execution information.
        """

        return {
            "execution_model": "SEQUENTIAL",
            "validator_count": (
                self.validator_count
            ),
            "validators": (
                self.validator_names()
            ),
        }
            # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    def validator_information(
        self,
    ) -> dict:
        """
        Return validator information.
        """

        return {
            "name": self.component_name,
            "version": self.version,
            "validator_count": (
                self.validator_count
            ),
            "validators": (
                self.validator_names()
            ),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            "QuestionValidator("
            f"validators={self.validator_count}, "
            f"version='{self.version}')"
        )

    def __str__(
        self,
    ) -> str:

        return (
            f"{self.component_name} "
            f"[{self.validator_count} validator(s)]"
        )
        