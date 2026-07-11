"""
Question Factory OS
Question CSV Exporter

Milestone : M10
Sprint    : S2
Release   : R1
"""

import csv
import os

from schema.question_schema import EXPORT_COLUMNS


class QuestionCSVExporter:
    """
    CSV Exporter

    Supports

    • Full Export
    • Incremental Append
    """

    def export(
        self,
        batch_result,
        output_file
    ):

        os.makedirs(

            os.path.dirname(output_file),

            exist_ok=True

        )

        with open(

            output_file,

            "w",

            newline="",

            encoding="utf-8"

        ) as csv_file:

            writer = csv.DictWriter(

                csv_file,

                fieldnames=EXPORT_COLUMNS,

                extrasaction="ignore"

            )

            writer.writeheader()

            for result in batch_result.worker_results:

                self._write_question(

                    writer,

                    result.question

                )

        return output_file

    def append(
        self,
        question: dict,
        output_file: str
    ):

        os.makedirs(

            os.path.dirname(output_file),

            exist_ok=True

        )

        file_exists = os.path.exists(
            output_file
        )

        write_header = (

            not file_exists

            or

            os.path.getsize(output_file) == 0

        )

        with open(

            output_file,

            "a",

            newline="",

            encoding="utf-8"

        ) as csv_file:

            writer = csv.DictWriter(

                csv_file,

                fieldnames=EXPORT_COLUMNS,

                extrasaction="ignore"

            )

            if write_header:

                writer.writeheader()

            self._write_question(

                writer,

                question

            )

    #
    # Internal
    #

    def _write_question(

        self,

        writer,

        question

    ):

        question = question.copy()

        if isinstance(

            question.get("tags"),

            list

        ):

            question["tags"] = ",".join(

                question["tags"]

            )

        writer.writerow(question)