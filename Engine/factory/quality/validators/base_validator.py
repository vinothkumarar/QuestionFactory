"""
Question Factory OS v3.0

Base Validator

Abstract base class for all quality validators.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from Engine.factory.quality.models.validation_context import (
    ValidationContext,
)

from Engine.factory.quality.models.validation_result import (
    ValidationResult,
)


class BaseValidator(ABC):
    """
    Base class for every quality validator.
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
        Validate a manufactured question batch.
        """
        raise NotImplementedError


__all__ = [
    "BaseValidator",
]