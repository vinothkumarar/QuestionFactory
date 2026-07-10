"""
Question Factory OS
Question CSV Exporter

Milestone : M7
Sprint    : S2
Release   : R1
"""

import csv
import os

from schema.question_schema import EXPORT_COLUMNS


class QuestionCSVExporter:
    """
    Exports BatchResultModel to CSV.
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

                question = result.question.copy()

                #
                # Convert tags list into CSV string
                #

                if isinstance(
                    question.get("tags"),
                    list
                ):

                    question["tags"] = ",".join(

                        question["tags"]

                    )

                writer.writerow(question)

        return output_file
        