"""
Question Factory OS
Schema Package
"""

from .question_schema import (
    EXPORT_COLUMNS,
    QUESTION_COLUMNS,
    SYSTEM_COLUMNS,
)

# Backward compatibility for legacy code
QUESTION_SCHEMA = EXPORT_COLUMNS