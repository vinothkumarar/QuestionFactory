from __future__ import annotations

import csv
import json
from pathlib import Path


class QPCatalogCSVExporter:
    """
    Export QP catalog JSON to CSV.
    """

    HEADERS = [
        "subject",
        "unit",
        "chapter",
        "subtopic",
        "concept_id",
        "concept",
        "qp_id",
        "question_possibility",
    ]

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

        with csv_file.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as fp:

            writer = csv.DictWriter(
                fp,
                fieldnames=self.HEADERS,
            )

            writer.writeheader()

            for row in data:
                writer.writerow(
                    {
                        "subject":
                            row.get(
                                "subject",
                                "",
                            ),
                        "unit":
                            row.get(
                                "unit",
                                "",
                            ),
                        "chapter":
                            row.get(
                                "chapter",
                                "",
                            ),
                        "subtopic":
                            row.get(
                                "subtopic",
                                "",
                            ),
                        "concept_id":
                            row.get(
                                "concept_id",
                                "",
                            ),
                        "concept":
                            row.get(
                                "concept",
                                "",
                            ),
                        "qp_id":
                            row.get(
                                "qp_id",
                                "",
                            ),
                        "question_possibility":
                            row.get(
                                "question_possibility",
                                "",
                            ),
                    }
                )