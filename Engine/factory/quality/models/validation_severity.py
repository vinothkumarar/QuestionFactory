"""
Question Factory OS v3.0

Validation Severity

Defines the severity level of a validation result.
"""

from __future__ import annotations

from enum import Enum


class ValidationSeverity(str, Enum):
    """
    Severity assigned to a validation outcome.

    INFO:
        Informational only.

    WARNING:
        Non-blocking issue.

    ERROR:
        Validation failure that should normally
        be repaired before export.

    CRITICAL:
        Blocking failure. The batch must not
        proceed until resolved.
    """

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


__all__ = [
    "ValidationSeverity",
]