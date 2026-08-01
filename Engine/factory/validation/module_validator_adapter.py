"""
Question Factory OS v3.0

Module Validator Adapter

Adapts ValidationModule to the legacy Validator interface.
"""

from __future__ import annotations

from Engine.factory.validation.question_validator import (
    Validator,
)
from Engine.factory.validation.validator_base import (
    ValidationModule,
)
from Engine.models.question_batch_model import (
    QuestionBatchModel,
)
from Engine.factory.validation.validation_result_model import (
    ValidationResultModel,
)


class ModuleValidatorAdapter(Validator):
    """
    Adapts ValidationModule to Validator.
    """

    def __init__(
        self,
        module: ValidationModule,
    ) -> None:
        self._module = module

    @property
    def name(self) -> str:
        return self._module.name

    def validate(
        self,
        batch: QuestionBatchModel,
    ) -> ValidationResultModel:
        return self._module.validate(batch)


__all__ = [
    "ModuleValidatorAdapter",
]