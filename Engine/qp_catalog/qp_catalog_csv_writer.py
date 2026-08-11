from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class QPCatalogCSVWriter:
    """
    Writes Question Possibility Catalog
    to CSV.
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
        "archetype_id",
        "archetype",
    ]

    def write(
        self,
        *,
        rows: list[dict[str, Any]],
        output_file: str,
    ) -> Path:

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            mode="w",
            newline="",
            encoding="utf-8",
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=self.HEADERS,
            )

            writer.writeheader()

            for row in rows:

                writer.writerow(
                    {
                        "qp_id": row.get(
                            "qp_id",
                            "",
                        ),
                        "question_possibility": row.get(
                            "question_possibility",
                            "",
                        ),
                        "concept": row.get(
                            "concept",
                            "",
                        ),
                        "archetype": row.get(
                            "archetype",
                            "",
                        ),
                    }
                )

        return output_path