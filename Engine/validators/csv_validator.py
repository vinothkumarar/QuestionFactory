"""
Question Factory OS
CSV Validator

Milestone : M7
Sprint    : S3
Release   : R1
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from Engine.models.csv_validation_result_model import CSVValidationResultModel
from Engine.schema.question_schema import EXPORT_COLUMNS


class CSVValidator:
    REQUIRED_FIELDS = [
        "question_code",
        "question_text",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_option",
    ]

    VALID_OPTIONS = {"A", "B", "C", "D"}

    def validate(
        self,
        csv_file: str | Path,
    ) -> CSVValidationResultModel:
        result = CSVValidationResultModel()

        codes: set[str] = set()
        questions: set[str] = set()

        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            #
            # Header validation
            #

            if reader.fieldnames != EXPORT_COLUMNS:
                result.passed = False
                result.errors.append(
                    "CSV header does not match QUESTION_SCHEMA."
                )

            for row_number, row in enumerate(reader, start=2):
                result.total_rows += 1

                #
                # Required fields
                #

                for field in self.REQUIRED_FIELDS:
                    if not row.get(field, "").strip():
                        result.errors.append(
                            f"Row {row_number}: Missing {field}"
                        )

                #
                # Duplicate question_code
                #

                code = row["question_code"]

                if code in codes:
                    result.errors.append(
                        f"Row {row_number}: Duplicate question_code {code}"
                    )

                codes.add(code)

                #
                # Duplicate question_text
                #

                text = row["question_text"]

                if text in questions:
                    result.errors.append(
                        f"Row {row_number}: Duplicate question_text"
                    )

                questions.add(text)

                #
                # Correct option
                #

                if row["correct_option"] not in self.VALID_OPTIONS:
                    result.errors.append(
                        f"Row {row_number}: Invalid correct_option"
                    )

        result.total_errors = len(result.errors)
        result.passed = result.total_errors == 0

        return result
        