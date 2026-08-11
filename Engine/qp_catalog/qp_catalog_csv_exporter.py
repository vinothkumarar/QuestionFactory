from __future__ import annotations

import csv
import json
from pathlib import Path


class QPCatalogCSVExporter:
    """
    Export QP Catalog JSON to CSV.
    """

    def export(
        self,
        *,
        json_file: Path,
        csv_file: Path,
    ) -> None:

        data = json.loads(
            json_file.read_text(
                encoding="utf-8"
            )
        )

        fieldnames = [
            "subject",
            "unit",
            "chapter",
            "subtopic",
            "qp_id",
            "concept",
            "question_possibility",
            "archetype_id",
            "archetype",
        ]

        with open(
            csv_file,
            "w",
            newline="",
            encoding="utf-8",
        ) as fp:

            writer = csv.DictWriter(
                fp,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            archetype_counter = 1

            for row in data:

                output_row = {
                    "subject": row.get(
                        "subject",
                        "",
                    ),
                    "unit": row.get(
                        "unit",
                        "",
                    ),
                    "chapter": row.get(
                        "chapter",
                        "",
                    ),
                    "subtopic": row.get(
                        "subtopic",
                        "",
                    ),
                    "qp_id": row.get(
                        "qp_id",
                        "",
                    ),
                    "concept": row.get(
                        "concept",
                        "",
                    ),
                    "question_possibility": row.get(
                        "question_possibility",
                        "",
                    ),
                    "archetype_id": (
                        f"A{archetype_counter:03d}"
                    ),
                    "archetype": row.get(
                        "archetype",
                        "",
                    ),
                }

                writer.writerow(
                    output_row
                )

                archetype_counter += 1