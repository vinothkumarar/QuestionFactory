"""
Question Factory OS
Smart CSV Exporter
"""

import csv
from pathlib import Path

from core.folder_manager import FolderManager
from core.file_name_generator import FileNameGenerator


class CSVExporter:

    def __init__(self):

        self.folder_manager = FolderManager()
        self.file_name_generator = FileNameGenerator()

    def export(self, report, runtime: dict):

        if not report.results:

            print("No questions to export.")
            return

        # ----------------------------------------
        # Create output folder
        # ----------------------------------------

        first_question = report.results[0]["question"]

        output_folder = self.folder_manager.create_output_folder(first_question)

        # ----------------------------------------
        # Generate filename
        # ----------------------------------------

        file_name = self.file_name_generator.generate(runtime)

        output_file = output_folder / file_name

        # ----------------------------------------
        # Prepare rows
        # ----------------------------------------

        rows = []

        for result in report.results:

            rows.append(result["question"])

        fieldnames = list(rows[0].keys())

        # ----------------------------------------
        # Write CSV
        # ----------------------------------------

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:

            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, extrasaction="ignore"
            )

            writer.writeheader()

            writer.writerows(rows)

        print()
        print("=" * 80)
        print("SMART CSV EXPORT COMPLETE")
        print("=" * 80)
        print(output_file.resolve())

        return output_file
