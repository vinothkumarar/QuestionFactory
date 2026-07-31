"""
Question Factory OS v3.0

Validation Error

Represents a single schema validation error produced by the
SchemaValidator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class ValidationError:
    """
    Represents a single validation error.
    """

    code: str

    field: str

    message: str

    value: Any = None

    severity: str = "ERROR"

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the validation error into a dictionary.
        """

        return {
            "code": self.code,
            "field": self.field,
            "message": self.message,
            "value": self.value,
            "severity": self.severity,
        }

    def __repr__(self) -> str:
        return (
            "ValidationError("
            f"code='{self.code}', "
            f"field='{self.field}', "
            f"severity='{self.severity}')"
        )
        