"""
Question Factory OS v2.2

CSV Export Constants

Defines the canonical CSV schema for manual upload into the
Supabase questions table.

All CSV exports must use this exact column ordering.
"""

from __future__ import annotations

from typing import Final

###############################################################################
# Encoding
###############################################################################

DEFAULT_ENCODING: Final[str] = "utf-8"

DEFAULT_NEWLINE: Final[str] = ""

###############################################################################
# CSV Dialect
###############################################################################

CSV_DELIMITER: Final[str] = ","

CSV_QUOTECHAR: Final[str] = '"'

###############################################################################
# Supported Difficulties
###############################################################################

VALID_DIFFICULTIES: Final[frozenset[str]] = frozenset(
    {
        "Foundation",
        "Easy",
        "Easy+",
        "Medium",
        "Hard",
        "Elite",
    }
)

###############################################################################
# Supported Question Types
###############################################################################

VALID_QUESTION_TYPES: Final[frozenset[str]] = frozenset(
    {
        "MCQ",
        "MSQ",
        "NAT",
        "INTEGER",
        "ASSERTION_REASON",
    }
)

###############################################################################
# Canonical Supabase Column Order
###############################################################################

SUPABASE_COLUMNS: Final[tuple[str, ...]] = (
    "question_id",
    "subject_code",
    "unit_code",
    "chapter_code",
    "subtopic_code",
    "set_code",
    "batch_code",
    "question_number",
    "question_type",
    "difficulty",
    "question_text",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "correct_answer",
    "explanation",
    "pyq_inspired",
    "pyq_year",
    "marks",
    "negative_marks",
    "time_seconds",
    "status",
    "created_by",
    "created_at",
)

###############################################################################
# Required Columns
###############################################################################

REQUIRED_COLUMNS: Final[frozenset[str]] = frozenset(
    {
        "question_id",
        "question_text",
        "question_type",
        "difficulty",
        "correct_answer",
    }
)