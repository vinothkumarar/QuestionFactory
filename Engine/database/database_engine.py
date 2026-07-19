"""
Question Factory OS
Database Engine

Current Architecture:
AI -> Validation -> Repair -> CSV Export -> Manual Upload

This class is intentionally kept as a placeholder.
The Question Factory does not write directly to any database.
"""

from __future__ import annotations

from typing import Any


class DatabaseEngine:
    """
    Placeholder database engine.

    The Question Factory generates validated CSV output.
    Uploading questions into Supabase (or any other database)
    is performed manually outside the manufacturing pipeline.
    """

    def __init__(self) -> None:
        pass

    def save_question(self, question: dict[str, Any]) -> bool:
        """
        No-op.

        Questions are exported to CSV instead of being written
        directly to a database.
        """
        return True

    def save_batch(self, report: Any) -> dict[str, int]:
        """
        Simulate a successful save for compatibility with older code.
        """
        inserted = len(getattr(report, "results", []))

        return {
            "inserted": inserted,
            "skipped": 0,
        }