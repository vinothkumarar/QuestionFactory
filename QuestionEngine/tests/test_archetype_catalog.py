"""Tests for the validated ST1 archetype catalogue loader."""

from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from question_engine.archetype_catalog import (
    ArchetypeCatalog,
    ArchetypeCatalogError,
)


ROOT = Path(__file__).resolve().parents[2]
ARCHETYPE_PATH = ROOT / "QuestionEngine" / "catalogs" / "maths_u1_ch1_st1_archetypes.csv"
QPC_PATH = ROOT / "Engine" / "qpc" / "mathematics" / "U1_CH1.csv"


class ArchetypeCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = ArchetypeCatalog.load(ARCHETYPE_PATH, QPC_PATH)

    def test_loads_all_st1_archetypes_and_qpc_entries(self) -> None:
        entries = self.catalog.for_subtopic("U1_CH1_ST1")
        self.assertEqual(len(entries), 40)
        self.assertEqual(
            len({entry.archetype_id for entry in entries}),
            len(entries),
        )
        self.assertEqual(
            len({entry.qp_id for entry in entries}),
            20,
        )

    def test_qp016_is_blocked_and_other_recipes_remain_available(self) -> None:
        qp016 = self.catalog.for_qp("U1_CH1_ST1_QP016")
        self.assertEqual(len(qp016), 2)
        self.assertTrue(all(entry.blocked_for_generation for entry in qp016))

        available = self.catalog.available_for_internal_draft_design("U1_CH1_ST1")
        self.assertEqual(len(available), 38)
        self.assertFalse(any(entry.qp_id.endswith("QP016") for entry in available))

    def test_rejects_qpc_description_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            altered_qpc = Path(directory) / "U1_CH1.csv"
            with QPC_PATH.open("r", encoding="utf-8-sig", newline="") as source:
                reader = csv.DictReader(source)
                rows = list(reader)
                fieldnames = reader.fieldnames or []
            for row in rows:
                if row["qp_id"] == "U1_CH1_ST1_QP001":
                    row["question_possibility"] = "Changed source text"
                    break
            with altered_qpc.open("w", encoding="utf-8", newline="") as target:
                writer = csv.DictWriter(target, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            with self.assertRaisesRegex(
                ArchetypeCatalogError, "Question possibility text mismatch"
            ):
                ArchetypeCatalog.load(ARCHETYPE_PATH, altered_qpc)

    def test_rejects_duplicate_archetype_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            duplicate_catalog = Path(directory) / "archetypes.csv"
            with ARCHETYPE_PATH.open("r", encoding="utf-8-sig", newline="") as source:
                reader = csv.DictReader(source)
                rows = list(reader)
                fieldnames = reader.fieldnames or []
            rows.append(dict(rows[0]))
            with duplicate_catalog.open("w", encoding="utf-8", newline="") as target:
                writer = csv.DictWriter(target, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            with self.assertRaisesRegex(
                ArchetypeCatalogError, "Duplicate archetype_id"
            ):
                ArchetypeCatalog.load(duplicate_catalog, QPC_PATH)


if __name__ == "__main__":
    unittest.main()
