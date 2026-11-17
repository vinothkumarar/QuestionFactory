from __future__ import annotations

import unittest
from typing import Any

from Engine.catalog.archetype_catalog.qp_disposition_contract import (
    validate_catalog_response,
)


def qp(qp_id: str = "QP001") -> dict[str, Any]:
    return {
        "subject": "Mathematics",
        "unit": "U1",
        "chapter": "CH1",
        "subtopic": "Sets",
        "concept_id": "C001",
        "concept": "Set inclusion",
        "qp_id": qp_id,
        "question_possibility": f"Possibility {qp_id}",
    }


def disposition(
    status: str,
    qp_id: str = "QP001",
) -> dict[str, Any]:
    return {
        "concept_id": "C001",
        "qp_id": qp_id,
        "disposition": status,
        "rationale": "Disposition justified by academic scope review.",
    }


def archetype(qp_id: str = "QP001") -> dict[str, Any]:
    return {
        **qp(qp_id),
        "archetype_id": "",
        "archetype": "Distinct assessment mechanism",
        "assessment_mechanism": "Infer a set relation from constraints.",
        "reasoning_path": "Translate constraints, then test inclusion.",
        "exam_fit": ["JEE_MAIN"],
        "difficulty_potential": ["MODERATE"],
        "variation_capacity": "MODERATE",
        "variation_dimensions": ["Set structure"],
    }


class QPDispositionContractTests(unittest.TestCase):
    def test_foundation_only_qp_can_complete_without_archetypes(self) -> None:
        result = validate_catalog_response(
            response={
                "qp_dispositions": [disposition("FOUNDATION_ONLY")],
                "archetypes": [],
            },
            input_qps=[qp()],
        )
        self.assertEqual(result["archetypes"], [])

    def test_eligible_qp_requires_an_archetype(self) -> None:
        with self.assertRaisesRegex(ValueError, "must have at least one"):
            validate_catalog_response(
                response={
                    "qp_dispositions": [disposition("ELIGIBLE")],
                    "archetypes": [],
                },
                input_qps=[qp()],
            )

    def test_non_eligible_qp_cannot_have_an_archetype(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-eligible QP"):
            validate_catalog_response(
                response={
                    "qp_dispositions": [disposition("OUT_OF_SCOPE")],
                    "archetypes": [archetype()],
                },
                input_qps=[qp()],
            )

    def test_every_input_qp_requires_a_disposition(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing QP dispositions"):
            validate_catalog_response(
                response={
                    "qp_dispositions": [disposition("FOUNDATION_ONLY")],
                    "archetypes": [],
                },
                input_qps=[qp(), qp("QP002")],
            )

    def test_duplicate_dispositions_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Duplicate QP disposition"):
            validate_catalog_response(
                response={
                    "qp_dispositions": [
                        disposition("FOUNDATION_ONLY"),
                        disposition("FOUNDATION_ONLY"),
                    ],
                    "archetypes": [],
                },
                input_qps=[qp()],
            )

    def test_unknown_archetype_qp_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown QP"):
            validate_catalog_response(
                response={
                    "qp_dispositions": [disposition("ELIGIBLE")],
                    "archetypes": [archetype("QP999")],
                },
                input_qps=[qp()],
            )

    def test_eligible_qp_with_archetype_is_accepted(self) -> None:
        result = validate_catalog_response(
            response={
                "qp_dispositions": [disposition("ELIGIBLE")],
                "archetypes": [archetype()],
            },
            input_qps=[qp()],
        )
        self.assertEqual(len(result["archetypes"]), 1)

    def test_archetype_cannot_change_copied_source_metadata(self) -> None:
        changed = archetype()
        changed["question_possibility"] = "Changed by AI"
        with self.assertRaisesRegex(ValueError, "does not exactly match"):
            validate_catalog_response(
                response={
                    "qp_dispositions": [disposition("ELIGIBLE")],
                    "archetypes": [changed],
                },
                input_qps=[qp()],
            )


if __name__ == "__main__":
    unittest.main()
