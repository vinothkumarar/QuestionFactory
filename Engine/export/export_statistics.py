"""
Question Factory OS v2.2

Export Statistics

Generates statistics for exported CSV rows.

This component performs reporting only.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from Engine.export.models.csv_row import CSVRow


class ExportStatistics:
    """
    Generates export statistics.
    """

    def generate(
        self,
        rows: list[CSVRow],
    ) -> dict[str, Any]:
        """
        Generate statistics for exported rows.
        """

        statistics: dict[str, Any] = {}

        statistics["total_rows"] = len(rows)

        if not rows:
            statistics["difficulty_distribution"] = {}
            statistics["question_type_distribution"] = {}
            statistics["subject_distribution"] = {}
            statistics["chapter_distribution"] = {}
            statistics["pyq_questions"] = 0
            statistics["non_pyq_questions"] = 0
            return statistics

        statistics["difficulty_distribution"] = (
            self._difficulty_distribution(rows)
        )

        statistics["question_type_distribution"] = (
            self._question_type_distribution(rows)
        )

        statistics["subject_distribution"] = (
            self._subject_distribution(rows)
        )

        statistics["chapter_distribution"] = (
            self._chapter_distribution(rows)
        )

        statistics["pyq_questions"] = (
            self._count_pyq(rows)
        )

        statistics["non_pyq_questions"] = (
            len(rows) - statistics["pyq_questions"]
        )

        return statistics

    ####################################################################
    # Distribution Helpers
    ####################################################################

    def _difficulty_distribution(
        self,
        rows: list[CSVRow],
    ) -> dict[str, int]:

        counter: Counter[str] = Counter()

        for row in rows:
            difficulty = str(
                row.get("difficulty", "")
            )

            if difficulty:
                counter[difficulty] += 1

        return dict(counter)

    def _question_type_distribution(
        self,
        rows: list[CSVRow],
    ) -> dict[str, int]:

        counter: Counter[str] = Counter()

        for row in rows:
            question_type = str(
                row.get("question_type", "")
            )

            if question_type:
                counter[question_type] += 1

        return dict(counter)

    def _subject_distribution(
        self,
        rows: list[CSVRow],
    ) -> dict[str, int]:

        counter: Counter[str] = Counter()

        for row in rows:
            subject = str(
                row.get("subject_code", "")
            )

            if subject:
                counter[subject] += 1

        return dict(counter)

    def _chapter_distribution(
        self,
        rows: list[CSVRow],
    ) -> dict[str, int]:

        counter: Counter[str] = Counter()

        for row in rows:
            chapter = str(
                row.get("chapter_code", "")
            )

            if chapter:
                counter[chapter] += 1

        return dict(counter)

    ####################################################################
    # PYQ
    ####################################################################

    def _count_pyq(
        self,
        rows: list[CSVRow],
    ) -> int:

        count = 0

        for row in rows:

            if bool(row.get("pyq_inspired", False)):
                count += 1

        return count