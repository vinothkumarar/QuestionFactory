"""
Question Factory OS
CSV Writer

Purpose:
Create CSV files for generated question batches.
"""

import csv
from pathlib import Path


CSV_HEADER = [
    "question_code",
    "unit_code",
    "chapter_code",
    "subtopic_code",
    "set_no",
    "difficulty",
    "question_text",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "correct_option",
    "answer",
    "explanation"
]


class CSVWriter:

    def create_batch_file(self, folder: Path, filename: str):

        file_path = folder / filename

        if file_path.exists():
            return file_path

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(CSV_HEADER)

        return file_path
