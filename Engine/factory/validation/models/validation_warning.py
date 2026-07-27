"""
Question Factory OS v2.3

Validation Warning Model
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ValidationWarning:
    """
    Represents a non-fatal validation warning.
    """

    validator: str

    code: str

    field: str

    message: str
    