from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from Engine.catalog.archetype_catalog.archetype_catalog_csv_exporter import (
    ArchetypeCatalogCSVExporter,
)
from Engine.catalog.archetype_catalog.run_all_archetype_catalogs import (
    assign_archetype_ids,
    load_existing_catalog,
    persist_catalog,
    select_qp_files,
)


class ArchetypeRunnerContractTests(unittest.TestCase):
    def test_factory_assigns_sequential_ids_without_rewriting_existing(self) -> None:
        existing = [
            {"archetype_id": "U2_CH8_ST1_AR00003"},
        ]
        generated = [
            {"archetype_id": ""},
            {"archetype_id": ""},
        ]
        assign_archetype_ids(
            archetypes=generated,
            scope_id="U2_CH8_ST1",
            existing_archetypes=existing,
        )
        self.assertEqual(
            [row["archetype_id"] for row in generated],
            ["U2_CH8_ST1_AR00004", "U2_CH8_ST1_AR00005"],
        )
        self.assertEqual(
            existing[0]["archetype_id"],
            "U2_CH8_ST1_AR00003",
        )

    def test_legacy_flat_list_is_not_silently_resumed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy.json"
            path.write_text(json.dumps([]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Legacy flat-list"):
                load_existing_catalog(path)

    def test_runner_can_select_only_requested_catalogue_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "U1_CH1_ST1.json").write_text("[]", encoding="utf-8")
            (root / "U2_CH8_ST1.json").write_text("[]", encoding="utf-8")
            selected = select_qp_files(
                qp_dir=root,
                scopes=["U1_CH1_ST1"],
            )
        self.assertEqual([path.stem for path in selected], ["U1_CH1_ST1"])

    def test_runner_rejects_unknown_catalogue_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "not found"):
                select_qp_files(
                    qp_dir=Path(directory),
                    scopes=["U1_CH1_ST99"],
                )

    def test_persistence_keeps_zero_archetype_disposition(self) -> None:
        source: dict[str, Any] = {
            "subject": "Mathematics",
            "unit": "U1",
            "chapter": "CH1",
            "subtopic": "Sets",
            "concept_id": "C001",
            "concept": "Basic set concepts",
            "qp_id": "QP001",
            "question_possibility": "Recognize a set",
        }
        catalog = {
            "qp_dispositions": [{
                "concept_id": "C001",
                "qp_id": "QP001",
                "disposition": "FOUNDATION_ONLY",
                "rationale": "Prerequisite knowledge only.",
            }],
            "archetypes": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_file = root / "catalog.json"
            archetype_csv = root / "archetypes.csv"
            disposition_csv = root / "dispositions.csv"
            persist_catalog(
                json_file=json_file,
                archetype_csv=archetype_csv,
                disposition_csv=disposition_csv,
                catalog=catalog,
                source_qps=[source],
                exporter=ArchetypeCatalogCSVExporter(),
            )
            saved = json.loads(json_file.read_text(encoding="utf-8"))
            disposition_rows = disposition_csv.read_text(encoding="utf-8")

        self.assertEqual(saved["archetypes"], [])
        self.assertEqual(
            saved["qp_dispositions"][0]["disposition"],
            "FOUNDATION_ONLY",
        )
        self.assertIn("FOUNDATION_ONLY", disposition_rows)


if __name__ == "__main__":
    unittest.main()
