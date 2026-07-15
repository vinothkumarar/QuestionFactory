"""
Question Factory OS
CSV Writer

Purpose:
Create CSV files for generated question batches.
"""

import csv
from pathlib import Path
from core.schema import QUESTION_SCHEMA


class CSVWriter:

    def create_batch_file(self, folder: Path, filename: str):

        file_path = folder / filename

        if file_path.exists():
            return file_path

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:

            writer = csv.writer(csvfile)
            writer.writerow(QUESTION_SCHEMA)

        return file_path
