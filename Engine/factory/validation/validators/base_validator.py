"""
Question Factory OS v2.3

Base Validator
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from Engine.factory.validation.models.validation_result import ValidationResult
from Engine.factory.validation.validation_context import ValidationContext


class BaseValidator(ABC):
    """
    Base class for every validator.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Validator name.
        """
        raise NotImplementedError

    @abstractmethod
    def validate(
        self,
        context: ValidationContext,
    ) -> ValidationResult:
        """
        Validate a question.
        """
        raise NotImplementedError
        