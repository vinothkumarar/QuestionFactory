"""
Question Factory OS v2.3

Validator Registry
"""

from __future__ import annotations

from collections.abc import Iterable

from Engine.factory.validation.validators.base_validator import BaseValidator


class ValidatorRegistry:
    """
    Maintains the ordered collection of validators.
    """

    def __init__(self) -> None:
        self._validators: list[BaseValidator] = []

    def register(
        self,
        validator: BaseValidator,
    ) -> None:
        """
        Register a validator.
        """
        self._validators.append(validator)

    def register_many(
        self,
        validators: Iterable[BaseValidator],
    ) -> None:
        """
        Register multiple validators.
        """
        self._validators.extend(validators)

    def clear(self) -> None:
        """
        Remove all validators.
        """
        self._validators.clear()

    @property
    def validators(self) -> tuple[BaseValidator, ...]:
        """
        Ordered validators.
        """
        return tuple(self._validators)

    def __len__(self) -> int:
        return len(self._validators)