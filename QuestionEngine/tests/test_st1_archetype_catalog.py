"""Integrity tests for the Mathematics U1/CH1/ST1 archetype catalogue."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARCHETYPE_PATH = ROOT / "QuestionEngine" / "catalogs" / "maths_u1_ch1_st1_archetypes.csv"
QPC_PATH = ROOT / "Engine" / "qpc" / "mathematics" / "U1_CH1.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class ST1ArchetypeCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.archetypes = read_csv(ARCHETYPE_PATH)
        cls.qpc = [
            row
            for row in read_csv(QPC_PATH)
            if row["subtopic_code"] == "U1_CH1_ST1"
        ]

    def test_catalog_has_unique_archetype_ids(self) -> None:
        ids = [row["archetype_id"] for row in self.archetypes]
        self.assertTrue(ids)
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_existing_qpc_has_archetype_coverage(self) -> None:
        qpc_ids = {row["qp_id"] for row in self.qpc}
        archetype_qp_ids = {row["qp_id"] for row in self.archetypes}
        self.assertEqual(qpc_ids, archetype_qp_ids)

    def test_archetype_qpc_descriptions_match_source_catalog(self) -> None:
        descriptions = {row["qp_id"]: row["question_possibility"] for row in self.qpc}
        for row in self.archetypes:
            self.assertEqual(
                row["question_possibility"],
                descriptions[row["qp_id"]],
                msg=f"QPC description drift for {row['qp_id']}",
            )

    def test_each_archetype_has_required_design_fields(self) -> None:
        required = (
            "archetype_id",
            "qp_id",
            "subtopic_code",
            "archetype_name",
            "construction_pattern",
            "target_skill",
            "suggested_format",
            "difficulty_band",
            "variation_dimensions",
            "distractor_strategy",
            "independent_verification_route",
            "scope_status",
        )
        for row in self.archetypes:
            for field in required:
                self.assertTrue(row[field].strip(), msg=f"{row['archetype_id']} missing {field}")

    def test_corrupted_qp016_is_blocked_not_interpreted(self) -> None:
        blocked = [
            row
            for row in self.archetypes
            if row["qp_id"] == "U1_CH1_ST1_QP016"
        ]
        self.assertTrue(blocked)
        self.assertTrue(all(row["scope_status"] == "BLOCKED_SOURCE_TEXT" for row in blocked))
        self.assertTrue(
            all("unknown" in row["notes"].lower() for row in blocked)
        )

    def test_other_qpcs_are_not_blocked_by_the_qp016_source_defect(self) -> None:
        incorrectly_blocked = [
            row
            for row in self.archetypes
            if row["qp_id"] != "U1_CH1_ST1_QP016"
            and row["scope_status"] == "BLOCKED_SOURCE_TEXT"
        ]
        self.assertEqual(incorrectly_blocked, [])


if __name__ == "__main__":
    unittest.main()
