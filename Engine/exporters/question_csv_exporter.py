"""
Question Factory OS
Question CSV Exporter

Milestone : M13
Sprint    : S3
Release   : R1
"""

import csv
import os
from pathlib import Path

from schema.question_schema import EXPORT_COLUMNS


class QuestionCSVExporter:
    """
    Exports BatchResultModel to a uniquely
    named production CSV.
    """

    def export(self, batch_result, production_order):

        #
        # First Question
        #

        first_question = batch_result.worker_results[0].question

        unit = first_question["unit_id"]
        chapter = first_question["chapter_id"]
        subtopic = first_question["subtopic_id"]
        set_no = first_question["set_no"]

        question_start = production_order.question_start

        question_end = question_start + production_order.question_count - 1

        #
        # Output Folder
        #

        output_folder = Path("output") / unit / chapter / subtopic

        output_folder.mkdir(parents=True, exist_ok=True)

        #
        # File Name
        #

        file_name = (
            f"{unit}_"
            f"{chapter}_"
            f"{subtopic}_"
            f"{set_no}_"
            f"Q{question_start:03d}"
            f"_Q{question_end:03d}.csv"
        )

        output_file = output_folder / file_name

        with open(output_file, "w", newline="", encoding="utf-8") as csv_file:

            writer = csv.DictWriter(
                csv_file, fieldnames=EXPORT_COLUMNS, extrasaction="ignore"
            )

            writer.writeheader()

            for result in batch_result.worker_results:

                question = result.question.copy()

                #
                # Convert Tags
                #

                if isinstance(question.get("tags"), list):

                    question["tags"] = ",".join(question["tags"])

                writer.writerow(question)

        return str(output_file)
