"""
Question Factory OS v2.1

Validator Base

Defines the abstract interface implemented by every
validation module.

All validation rules (R01, R02, R03, QuestionValidator,
future validators, etc.) must inherit from this class.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from Engine.factory.validation.validation_result_model import (
    ValidationResultModel,
)


class ValidationModule(ABC):
    """
    Base interface implemented by every
    validation module.
    """

    # ---------------------------------------------------------
    # Identification
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable validator name.
        """

    @property
    @abstractmethod
    def validation_code(self) -> str:
        """
        Unique validation rule identifier.

        Examples
        --------
        R01
        R02
        R03
        SCHEMA
        METADATA
        """
    
    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    @abstractmethod
    def validate(
        self,
        question: Any,
    ) -> ValidationResultModel:
        """
        Validate a single question.

        Parameters
        ----------
        question:
            Question object or dictionary.

        Returns
        -------
        ValidationResultModel
        """

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def before_validation(
        self,
        question: Any,
    ) -> None:
        """
        Executed immediately before validation.

        Subclasses may override.
        """
        return

    def after_validation(
        self,
        question: Any,
        result: ValidationResultModel,
    ) -> None:
        """
        Executed immediately after validation.

        Subclasses may override.
        """
        return

    # ---------------------------------------------------------
    # Execution Wrapper
    # ---------------------------------------------------------

    def execute(
        self,
        question: Any,
    ) -> ValidationResultModel:
        """
        Execute the complete validation lifecycle.
        """

        self.before_validation(question)

        result = self.validate(question)

        self.after_validation(
            question,
            result,
        )

        return result

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def validate_configuration(
        self,
    ) -> None:
        """
        Validate validator configuration.
        """

        if not self.name.strip():
            raise ValueError(
                "Validator name cannot be empty."
            )

        if not self.validation_code.strip():
            raise ValueError(
                "Validation code cannot be empty."
            )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
        result: ValidationResultModel | None = None,
    ) -> dict[str, object]:
        """
        Return validator diagnostics.
        """

        diagnostics: dict[str, object] = {
            "component": self.__class__.__name__,
            "name": self.name,
            "validation_code": self.validation_code,
        }

        if result is not None:
            diagnostics["result"] = result.summary()

        return diagnostics

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return validator health.
        """

        return {
            "component": self.__class__.__name__,
            "status": "READY",
            "validation_code": self.validation_code,
        }

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    def capabilities(
        self,
    ) -> dict[str, object]:
        """
        Supported validator capabilities.
        """

        return {
            "single_question_validation": True,
            "lifecycle_hooks": True,
            "configuration_validation": True,
            "diagnostics": True,
            "health_reporting": True,
        }

    # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset validator runtime state.

        Reserved for future implementations.
        """

        return

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            "("
            f"name='{self.name}', "
            f"code='{self.validation_code}'"
            ")"
        )

    __str__ = __repr__


__all__ = [
    "ValidationModule",
]