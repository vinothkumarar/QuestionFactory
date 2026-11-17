from __future__ import annotations

import unittest
from typing import Any

from Engine.catalog.archetype_catalog.qp_disposition_contract import (
    validate_catalog_response,
)


def qp(qp_id: str = "QP001") -> dict[str, Any]:
    return {"concept_id": "C001", "qp_id": qp_id}


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
        "concept_id": "C001",
        "qp_id": qp_id,
        "archetype_id": "",
        "archetype": "Distinct assessment mechanism",
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

    def test_every_input_qp_requires_exactly_one_disposition(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
