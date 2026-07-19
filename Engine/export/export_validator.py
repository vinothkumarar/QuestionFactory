"""
Question Factory OS v2.2

Export Validator

Validates CSV rows before export.
"""

from __future__ import annotations

from Engine.export.constants import (
    REQUIRED_COLUMNS,
    SUPABASE_COLUMNS,
    VALID_DIFFICULTIES,
    VALID_QUESTION_TYPES,
)
from Engine.export.interfaces.validator import Validator
from Engine.export.models.csv_row import CSVRow
from Engine.export.models.export_summary import ExportSummary


class ExportValidator(Validator):
    """
    Validates CSV export rows.
    """

    def validate_row(
        self,
        row: CSVRow,
    ) -> list[str]:
        """
        Validate a single CSV row.

        Returns a list of validation errors.
        """

        errors: list[str] = []

        values = row.to_dict()

        #
        # Required columns
        #
        for column in REQUIRED_COLUMNS:

            if column not in values:
                errors.append(
                    f"Missing required column: {column}"
                )
                continue

            value = values[column]

            if value is None:
                errors.append(
                    f"Column '{column}' cannot be None."
                )
                continue

            if isinstance(value, str) and not value.strip():
                errors.append(
                    f"Column '{column}' cannot be empty."
                )

        #
        # Difficulty
        #
        difficulty = values.get("difficulty")

        if (
            difficulty
            and difficulty not in VALID_DIFFICULTIES
        ):
            errors.append(
                f"Invalid difficulty: {difficulty}"
            )

        #
        # Question Type
        #
        question_type = values.get("question_type")

        if (
            question_type
            and question_type not in VALID_QUESTION_TYPES
        ):
            errors.append(
                f"Invalid question type: {question_type}"
            )

        #
        # Answer
        #
        answer = values.get("correct_answer")

        if answer is None or str(answer).strip() == "":
            errors.append(
                "Correct answer is missing."
            )

        return errors

    def validate(
        self,
        rows: list[CSVRow],
    ) -> ExportSummary:
        """
        Validate the complete export.
        """

        summary = ExportSummary()

        summary.total_rows = len(rows)

        seen_ids: set[str] = set()

        for row in rows:

            row_errors = self.validate_row(row)

            values = row.to_dict()

            question_id = str(
                values.get("question_id", "")
            )

            if question_id:

                if question_id in seen_ids:
                    row_errors.append(
                        f"Duplicate question_id: {question_id}"
                    )
                else:
                    seen_ids.add(question_id)

            if row_errors:
                summary.failed_rows += 1
                summary.errors.extend(row_errors)
            else:
                summary.successful_rows += 1

        #
        # Schema verification
        #
        if rows:

            exported_columns = tuple(
                rows[0].columns
            )

            if exported_columns != SUPABASE_COLUMNS:

                summary.errors.append(
                    "CSV column ordering does not match "
                    "SUPABASE_COLUMNS."
                )

        return summary