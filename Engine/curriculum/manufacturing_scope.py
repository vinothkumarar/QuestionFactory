"""
Question Factory OS v2.4
Manufacturing Scope

Milestone : M14
Sprint    : S1
Release   : R1

Defines the supported curriculum manufacturing scopes.
"""

from __future__ import annotations

from enum import Enum


class ManufacturingScope(str, Enum):
    """
    Supported manufacturing scopes.

    Every curriculum manufacturing request begins
    with one of these scopes.
    """

    ONE_BATCH = "ONE_BATCH"

    SUBTOPIC = "SUBTOPIC"

    CHAPTER = "CHAPTER"

    UNIT = "UNIT"

    SUBJECT = "SUBJECT"

    COMPLETE_CURRICULUM = "COMPLETE_CURRICULUM"

    def __str__(self) -> str:
        return self.value


__all__ = [
    "ManufacturingScope",
]