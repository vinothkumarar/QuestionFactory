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
        batch_source = source[:325]
        catalogue = read_json(ARCHETYPE_CATALOGS / "U2_CH8_ST1.json")
        validate_catalog_response(
            response=catalogue,
            input_qps=batch_source,
        )
        self.assertEqual(len(catalogue["qp_dispositions"]), 325)
        self.assertEqual(len(catalogue["archetypes"]), 119)

        csv_path = ARCHETYPE_CATALOGS / "U2_CH8_ST1.csv"
        rows = csv_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(rows), 120)
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
                "U2_CH8_ST1_AR00054",
                "U2_CH8_ST1_AR00055",
                "U2_CH8_ST1_AR00056",
                "U2_CH8_ST1_AR00057",
                "U2_CH8_ST1_AR00058",
                "U2_CH8_ST1_AR00059",
                "U2_CH8_ST1_AR00060",
                "U2_CH8_ST1_AR00061",
                "U2_CH8_ST1_AR00062",
                "U2_CH8_ST1_AR00063",
                "U2_CH8_ST1_AR00064",
                "U2_CH8_ST1_AR00065",
                "U2_CH8_ST1_AR00066",
                "U2_CH8_ST1_AR00067",
                "U2_CH8_ST1_AR00068",
                "U2_CH8_ST1_AR00069",
                "U2_CH8_ST1_AR00070",
                "U2_CH8_ST1_AR00071",
                "U2_CH8_ST1_AR00072",
                "U2_CH8_ST1_AR00073",
                "U2_CH8_ST1_AR00074",
                "U2_CH8_ST1_AR00075",
                "U2_CH8_ST1_AR00076",
                "U2_CH8_ST1_AR00077",
                "U2_CH8_ST1_AR00078",
                "U2_CH8_ST1_AR00079",
                "U2_CH8_ST1_AR00080",
                "U2_CH8_ST1_AR00081",
                "U2_CH8_ST1_AR00082",
                "U2_CH8_ST1_AR00083",
                "U2_CH8_ST1_AR00084",
                "U2_CH8_ST1_AR00085",
                "U2_CH8_ST1_AR00086",
                "U2_CH8_ST1_AR00087",
                "U2_CH8_ST1_AR00088",
                "U2_CH8_ST1_AR00089",
                "U2_CH8_ST1_AR00090",
                "U2_CH8_ST1_AR00091",
                "U2_CH8_ST1_AR00092",
                "U2_CH8_ST1_AR00093",
                "U2_CH8_ST1_AR00094",
                "U2_CH8_ST1_AR00095",
                "U2_CH8_ST1_AR00096",
                "U2_CH8_ST1_AR00097",
                "U2_CH8_ST1_AR00098",
                "U2_CH8_ST1_AR00099",
                "U2_CH8_ST1_AR00100",
                "U2_CH8_ST1_AR00101",
                "U2_CH8_ST1_AR00102",
                "U2_CH8_ST1_AR00103",
                "U2_CH8_ST1_AR00104",
                "U2_CH8_ST1_AR00105",
                "U2_CH8_ST1_AR00106",
                "U2_CH8_ST1_AR00107",
                "U2_CH8_ST1_AR00108",
                "U2_CH8_ST1_AR00109",
                "U2_CH8_ST1_AR00110",
                "U2_CH8_ST1_AR00111",
                "U2_CH8_ST1_AR00112",
                "U2_CH8_ST1_AR00113",
                "U2_CH8_ST1_AR00114",
                "U2_CH8_ST1_AR00115",
                "U2_CH8_ST1_AR00116",
                "U2_CH8_ST1_AR00117",
                "U2_CH8_ST1_AR00118",
                "U2_CH8_ST1_AR00119",
            ],
        )


if __name__ == "__main__":
    unittest.main()
