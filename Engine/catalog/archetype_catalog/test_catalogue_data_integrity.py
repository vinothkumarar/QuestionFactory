from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

from Engine.catalog.archetype_catalog.qp_disposition_contract import (
    validate_catalog_response,
)


ROOT = Path(__file__).parent
QP_CATALOGS = ROOT.parent / "qp_catalog" / "catalogs"
ARCHETYPE_CATALOGS = ROOT / "catalogs"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


class CatalogueDataIntegrityTests(unittest.TestCase):
    def test_st1_foundation_dispositions_cover_all_normalized_qps(self) -> None:
        source = read_json(QP_CATALOGS / "U1_CH1_ST1.json")
        catalogue = read_json(ARCHETYPE_CATALOGS / "U1_CH1_ST1.json")
        validate_catalog_response(response=catalogue, input_qps=source)
        self.assertEqual(len(source), 19)
        self.assertEqual(len(catalogue["qp_dispositions"]), 19)
        self.assertEqual(catalogue["archetypes"], [])
        self.assertTrue(all(
            row["disposition"] == "FOUNDATION_ONLY"
            for row in catalogue["qp_dispositions"]
        ))

    def test_st2_foundation_dispositions_cover_all_normalized_qps(self) -> None:
        source = read_json(QP_CATALOGS / "U1_CH1_ST2.json")
        catalogue = read_json(ARCHETYPE_CATALOGS / "U1_CH1_ST2.json")
        validate_catalog_response(response=catalogue, input_qps=source)
        self.assertEqual(len(source), 10)
        self.assertEqual(len(catalogue["qp_dispositions"]), 10)
        self.assertEqual(catalogue["archetypes"], [])
        self.assertTrue(all(
            row["disposition"] == "FOUNDATION_ONLY"
            for row in catalogue["qp_dispositions"]
        ))

    def test_matrix_batch_one_matches_source_and_keeps_gates_closed(self) -> None:
        source = read_json(QP_CATALOGS / "U2_CH8_ST1.json")
        batch_source = source[:100]
        catalogue = read_json(ARCHETYPE_CATALOGS / "U2_CH8_ST1.json")
        validate_catalog_response(
            response=catalogue,
            input_qps=batch_source,
        )
        self.assertEqual(len(catalogue["qp_dispositions"]), 100)
        self.assertEqual(len(catalogue["archetypes"]), 17)

        csv_path = ARCHETYPE_CATALOGS / "U2_CH8_ST1.csv"
        rows = csv_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(rows), 18)
        for row in rows[1:]:
            self.assertIn("DRAFT_CORE_REQUIRES_ACADEMIC_REVIEW", row)
            self.assertIn("FALSE", row)

        ids = [row["archetype_id"] for row in catalogue["archetypes"]]
        self.assertEqual(
            ids,
            [
                "U2_CH8_ST1_AR00001",
                "U2_CH8_ST1_AR00002",
                "U2_CH8_ST1_AR00003",
                "U2_CH8_ST1_AR00004",
                "U2_CH8_ST1_AR00005",
                "U2_CH8_ST1_AR00006",
                "U2_CH8_ST1_AR00007",
                "U2_CH8_ST1_AR00008",
                "U2_CH8_ST1_AR00009",
                "U2_CH8_ST1_AR00010",
                "U2_CH8_ST1_AR00011",
                "U2_CH8_ST1_AR00012",
                "U2_CH8_ST1_AR00013",
                "U2_CH8_ST1_AR00014",
                "U2_CH8_ST1_AR00015",
                "U2_CH8_ST1_AR00016",
                "U2_CH8_ST1_AR00017",
            ],
        )


if __name__ == "__main__":
    unittest.main()
