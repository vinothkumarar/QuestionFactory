"""
Question Factory OS
CSV Writer

Purpose:
Create CSV files for generated question batches.
"""

import csv
from pathlib import Path

from Engine.schema import EXPORT_COLUMNS


class CSVWriter:
    def create_batch_file(
        self,
        folder: Path,
        filename: str,
    ) -> Path:
        file_path = folder / filename

        if file_path.exists():
            return file_path

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(EXPORT_COLUMNS)

        return file_path
