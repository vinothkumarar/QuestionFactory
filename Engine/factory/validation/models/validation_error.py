"""
Question Factory OS v2.3

Validation Error Model
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ValidationError:
    """
    Represents a single validation error.
    """

    validator: str

    code: str

    field: str

    message: str

    severity: str = "ERROR"