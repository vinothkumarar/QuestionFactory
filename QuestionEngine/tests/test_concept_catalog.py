from pathlib import Path
import tempfile
import unittest

from question_engine.concept_catalog import ConceptCatalog, ConceptCatalogError


REPO_ROOT = Path(__file__).resolve().parents[2]


class ConceptCatalogTests(unittest.TestCase):
    def test_provisional_pilot_concepts_are_not_released_for_generation(self):
        catalog = ConceptCatalog.load(
            REPO_ROOT / "catalogs" / "maths_u1_ch1_st1_concepts.csv"
        )
        self.assertEqual(len(catalog.for_subtopic("U1_CH1_ST1")), 7)
        self.assertEqual(catalog.approved_for_generation("U1_CH1_ST1"), ())

    def test_only_explicitly_approved_concepts_are_released(self):
        from question_engine.concept_catalog import ConceptEntry

        catalog = ConceptCatalog([
            ConceptEntry(
                concept_id="C-1",
                subtopic_code="U1_CH1_ST1",
                concept_name="Integer membership",
                learning_outcome="Classify integers.",
                review_status="APPROVED",
            ),
            ConceptEntry(
                concept_id="C-2",
                subtopic_code="U1_CH1_ST1",
                concept_name="Ordering",
                learning_outcome="Order integers.",
                review_status="PROVISIONAL_REVIEW_REQUIRED",
            ),
        ])
        self.assertEqual(
            [entry.concept_id for entry in catalog.approved_for_generation("U1_CH1_ST1")],
            ["C-1"],
        )

    def test_duplicate_concept_ids_are_rejected(self):
        from question_engine.concept_catalog import ConceptEntry

        row = ConceptEntry("C-1", "U1_CH1_ST1", "Name", "Outcome", "APPROVED")
        with self.assertRaisesRegex(ConceptCatalogError, "Duplicate concept_id"):
            ConceptCatalog([row, row])

    def test_unknown_review_status_is_rejected(self):
        from question_engine.concept_catalog import ConceptEntry

        row = ConceptEntry("C-1", "U1_CH1_ST1", "Name", "Outcome", "READY")
        with self.assertRaisesRegex(ConceptCatalogError, "Unsupported review status"):
            ConceptCatalog([row])


if __name__ == "__main__":
    unittest.main()
