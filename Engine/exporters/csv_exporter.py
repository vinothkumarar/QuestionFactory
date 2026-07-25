"""
Question Factory OS
Smart CSV Exporter
"""

import csv
from pathlib import Path

from Engine.core.file_name_generator import FileNameGenerator
from Engine.core.folder_manager import FolderManager


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

            print("\n========== AFTER MERGE ==========")
            if rows:
                first_question = rows[0]
                print(
                    {
                        "question_text": first_question.get("question_text"),
                        "subject_id": first_question.get("subject_id"),
                        "unit_id": first_question.get("unit_id"),
                        "chapter_id": first_question.get("chapter_id"),
                        "subtopic_id": first_question.get("subtopic_id"),
                        "question_code": first_question.get("question_code"),
                    }
                )
          
            writer.writerows(rows)

        print()
        print("=" * 80)
        print("SMART CSV EXPORT COMPLETE")
        print("=" * 80)
        print(output_file.resolve())

        return output_file
