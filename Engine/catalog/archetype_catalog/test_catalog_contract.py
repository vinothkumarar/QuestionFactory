from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from Engine.catalog.archetype_catalog.archetype_catalog_ai_client import (
    ArchetypeCatalogAIClient,
)
from Engine.catalog.archetype_catalog.archetype_catalog_csv_exporter import (
    ArchetypeCatalogCSVExporter,
)
from Engine.catalog.archetype_catalog.batch_archetype_catalog_generator import (
    BatchArchetypeCatalogGenerator,
)


def valid_record() -> dict[str, Any]:
    return {
        "subject": "Mathematics",
        "unit": "Number System",
        "chapter": "Basic Number System",
        "subtopic": "Number Set Classification",
        "concept_id": "C004",
        "concept": "Classification across the three sets",
        "qp_id": "QP010",
        "question_possibility": "Classify Given Number",
        "archetype_id": "",
        "archetype": "Constraint-based classification",
        "assessment_mechanism": "Infer membership from supplied constraints.",
        "reasoning_path": "Resolve constraints, identify sign and integrality, then classify.",
        "exam_fit": ["JEE_MAIN"],
        "difficulty_potential": ["MODERATE"],
        "variation_capacity": "MODERATE",
        "variation_dimensions": ["Constraint form", "Number representation"],
    }


class ArchetypeCatalogContractTests(unittest.TestCase):
    def test_ai_contract_accepts_blank_factory_owned_id(self) -> None:
        client = ArchetypeCatalogAIClient.__new__(ArchetypeCatalogAIClient)
        client._validate_records([valid_record()])

    def test_ai_contract_rejects_ai_assigned_id(self) -> None:
        client = ArchetypeCatalogAIClient.__new__(ArchetypeCatalogAIClient)
        record = valid_record()
        record["archetype_id"] = "U1_CH1_ST1_AR00001"
        with self.assertRaisesRegex(ValueError, "Factory assigns"):
            client._validate_records([record])

    def test_prompt_uses_disposition_aware_catalogue_contract(self) -> None:
        prompt = BatchArchetypeCatalogGenerator().load_prompt(
            qps=[
                {
                    "subject": "Mathematics",
                    "unit": "Number System",
                    "chapter": "Basic Number System",
                    "subtopic": "Number Set Classification",
                    "concept_id": "C004",
                    "concept": "Classification across the three sets",
                    "qp_id": "QP010",
                    "question_possibility": "Classify Given Number",
                }
            ]
        )
        self.assertIn("AUTHORITATIVE BATCH CONTRACT", prompt)
        self.assertIn('"qp_dispositions"', prompt)
        self.assertIn("FOUNDATION_ONLY", prompt)
        self.assertIn('"assessment_mechanism"', prompt)
        self.assertIn('"variation_dimensions"', prompt)
        self.assertIn('"archetype_id": ""', prompt)

    def test_csv_export_preserves_metadata_and_default_gate(self) -> None:
        record = valid_record()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_file = root / "catalog.json"
            csv_file = root / "catalog.csv"
            json_file.write_text(
                json.dumps({
                    "qp_dispositions": [{
                        "concept_id": record["concept_id"],
                        "qp_id": record["qp_id"],
                        "disposition": "ELIGIBLE",
                        "rationale": "A distinct JEE mechanism is supported.",
                    }],
                    "archetypes": [record],
                }),
                encoding="utf-8",
            )

            ArchetypeCatalogCSVExporter().export(
                json_file=json_file,
                csv_file=csv_file,
            )

            with csv_file.open(
                newline="",
                encoding="utf-8",
            ) as handle:
                row = next(csv.DictReader(handle))

        self.assertEqual(
            row["assessment_mechanism"],
            record["assessment_mechanism"],
        )
        self.assertEqual(
            row["variation_dimensions"],
            "Constraint form | Number representation",
        )
        self.assertEqual(
            row["approval_status"],
            "DRAFT_CORE_REQUIRES_ACADEMIC_REVIEW",
        )
        self.assertEqual(row["manufacturing_enabled"], "FALSE")


if __name__ == "__main__":
    unittest.main()
