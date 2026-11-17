from __future__ import annotations

import csv
import json
from pathlib import Path


class ArchetypeCatalogCSVExporter:
    """
    Export the complete validated Archetype catalogue contract to CSV.
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
        "assessment_mechanism",
        "reasoning_path",
        "exam_fit",
        "difficulty_potential",
        "variation_capacity",
        "variation_dimensions",
        "approval_status",
        "manufacturing_enabled",
    ]

    LIST_FIELDS = {
        "exam_fit",
        "difficulty_potential",
        "variation_dimensions",
    }

    def export(
        self,
        *,
        json_file: Path,
        csv_file: Path,
    ) -> None:
        data = json.loads(
            json_file.read_text(encoding="utf-8")
        )

        if not isinstance(data, list):
            raise ValueError(
                "Archetype catalogue JSON must contain a flat list."
            )

        with csv_file.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as fp:
            writer = csv.DictWriter(
                fp,
                fieldnames=self.HEADERS,
                extrasaction="raise",
            )
            writer.writeheader()

            for index, row in enumerate(data, start=1):
                if not isinstance(row, dict):
                    raise ValueError(
                        f"Archetype record #{index} must be an object."
                    )

                missing = [
                    field for field in self.HEADERS
                    if field not in row
                ]
                if missing:
                    raise ValueError(
                        f"Archetype record #{index} is missing CSV fields: "
                        + ", ".join(missing)
                    )

                output = dict(row)
                output["approval_status"] = (
                    "DRAFT_CORE_REQUIRES_ACADEMIC_REVIEW"
                )
                output["manufacturing_enabled"] = "FALSE"

                for field in self.LIST_FIELDS:
                    value = output[field]
                    if not isinstance(value, list):
                        raise ValueError(
                            f"Archetype record #{index} field "
                            f"'{field}' must be a list."
                        )
                    output[field] = " | ".join(
                        str(item) for item in value
                    )

                writer.writerow(output)


__all__ = ["ArchetypeCatalogCSVExporter"]
