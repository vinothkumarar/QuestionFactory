from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


class ArchetypeCatalogCSVExporter:
    """Export archetypes and QP dispositions into separate audit-friendly CSVs."""

    HEADERS = [
        "subject", "unit", "chapter", "subtopic", "concept_id", "concept",
        "qp_id", "question_possibility", "archetype_id", "archetype",
        "assessment_mechanism", "reasoning_path", "exam_fit",
        "difficulty_potential", "variation_capacity", "variation_dimensions",
        "approval_status", "manufacturing_enabled",
    ]
    DISPOSITION_HEADERS = [
        "subject", "unit", "chapter", "subtopic", "concept_id", "concept",
        "qp_id", "question_possibility", "disposition", "rationale",
    ]
    LIST_FIELDS = {
        "exam_fit", "difficulty_potential", "variation_dimensions",
    }

    def _load_catalog(self, json_file: Path) -> dict[str, list[dict[str, Any]]]:
        data = json.loads(json_file.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or set(data) != {
            "qp_dispositions", "archetypes",
        }:
            raise ValueError(
                "Expected disposition-aware catalogue JSON object. "
                "Legacy flat-list catalogues require explicit migration."
            )
        if not isinstance(data["qp_dispositions"], list) or not isinstance(
            data["archetypes"], list
        ):
            raise ValueError("Catalogue arrays are malformed.")
        return data

    def export(self, *, json_file: Path, csv_file: Path) -> None:
        data = self._load_catalog(json_file)
        with csv_file.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.DictWriter(
                fp, fieldnames=self.HEADERS, extrasaction="raise",
            )
            writer.writeheader()
            for index, row in enumerate(data["archetypes"], start=1):
                if not isinstance(row, dict):
                    raise ValueError(f"Archetype record #{index} must be an object.")
                missing = [
                    field for field in self.HEADERS
                    if field not in row and field not in {
                        "approval_status", "manufacturing_enabled",
                    }
                ]
                if missing:
                    raise ValueError(
                        f"Archetype record #{index} is missing CSV fields: "
                        + ", ".join(missing)
                    )
                output = dict(row)
                output["approval_status"] = "DRAFT_CORE_REQUIRES_ACADEMIC_REVIEW"
                output["manufacturing_enabled"] = "FALSE"
                for field in self.LIST_FIELDS:
                    value = output[field]
                    if not isinstance(value, list):
                        raise ValueError(
                            f"Archetype record #{index} field '{field}' must be a list."
                        )
                    output[field] = " | ".join(str(item) for item in value)
                writer.writerow(output)

    def export_dispositions(
        self,
        *,
        json_file: Path,
        csv_file: Path,
        source_qps: list[dict[str, Any]],
    ) -> None:
        data = self._load_catalog(json_file)
        source_by_key = {
            (row["concept_id"], row["qp_id"]): row for row in source_qps
        }
        with csv_file.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.DictWriter(
                fp, fieldnames=self.DISPOSITION_HEADERS, extrasaction="raise",
            )
            writer.writeheader()
            for item in data["qp_dispositions"]:
                key = (item["concept_id"], item["qp_id"])
                source = source_by_key.get(key)
                if source is None:
                    raise ValueError(
                        f"Disposition references unknown source QP: {key}."
                    )
                writer.writerow({
                    **{field: source.get(field, "") for field in (
                        "subject", "unit", "chapter", "subtopic",
                        "concept_id", "concept", "qp_id",
                        "question_possibility",
                    )},
                    "disposition": item["disposition"],
                    "rationale": item["rationale"],
                })


__all__ = ["ArchetypeCatalogCSVExporter"]
