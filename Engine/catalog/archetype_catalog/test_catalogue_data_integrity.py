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
        batch_source = source[:210]
        catalogue = read_json(ARCHETYPE_CATALOGS / "U2_CH8_ST1.json")
        validate_catalog_response(
            response=catalogue,
            input_qps=batch_source,
        )
        self.assertEqual(len(catalogue["qp_dispositions"]), 210)
        self.assertEqual(len(catalogue["archetypes"]), 53)

        csv_path = ARCHETYPE_CATALOGS / "U2_CH8_ST1.csv"
        rows = csv_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(rows), 54)
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
                "U2_CH8_ST1_AR00018",
                "U2_CH8_ST1_AR00019",
                "U2_CH8_ST1_AR00020",
                "U2_CH8_ST1_AR00021",
                "U2_CH8_ST1_AR00022",
                "U2_CH8_ST1_AR00023",
                "U2_CH8_ST1_AR00024",
                "U2_CH8_ST1_AR00025",
                "U2_CH8_ST1_AR00026",
                "U2_CH8_ST1_AR00027",
                "U2_CH8_ST1_AR00028",
                "U2_CH8_ST1_AR00029",
                "U2_CH8_ST1_AR00030",
                "U2_CH8_ST1_AR00031",
                "U2_CH8_ST1_AR00032",
                "U2_CH8_ST1_AR00033",
                "U2_CH8_ST1_AR00034",
                "U2_CH8_ST1_AR00035",
                "U2_CH8_ST1_AR00036",
                "U2_CH8_ST1_AR00037",
                "U2_CH8_ST1_AR00038",
                "U2_CH8_ST1_AR00039",
                "U2_CH8_ST1_AR00040",
                "U2_CH8_ST1_AR00041",
                "U2_CH8_ST1_AR00042",
                "U2_CH8_ST1_AR00043",
                "U2_CH8_ST1_AR00044",
                "U2_CH8_ST1_AR00045",
                "U2_CH8_ST1_AR00046",
                "U2_CH8_ST1_AR00047",
                "U2_CH8_ST1_AR00048",
                "U2_CH8_ST1_AR00049",
                "U2_CH8_ST1_AR00050",
                "U2_CH8_ST1_AR00051",
                "U2_CH8_ST1_AR00052",
                "U2_CH8_ST1_AR00053",
            ],
        )


if __name__ == "__main__":
    unittest.main()
