import tempfile
import unittest
from pathlib import Path

from question_engine.exam_syllabus import (
    ExamSyllabusMapping,
    ExamSyllabusRegistry,
    ExamSyllabusRegistryError,
    ExamSyllabusSource,
    ExamVersionedQuestionScopeVerifier,
)


def source(**changes):
    values = dict(
        source_id="JEE-MAIN-2026", exam="JEE Main", syllabus_version="2026",
        official_source_title="Official JEE Main syllabus",
        official_source_url="https://example.org/jee-main-2026.pdf",
        publication_date="2025-10-01", effective_from="2026-01-01",
        effective_to="2026-12-31", retrieved_at="2026-11-16T10:00:00Z",
        document_sha256="a" * 64,
    )
    values.update(changes)
    return ExamSyllabusSource(**values)


def mapping(**changes):
    values = dict(
        mapping_id="MAP-001", source_id="JEE-MAIN-2026", exam="JEE Main",
        syllabus_version="2026", subject_id="MATHEMATICS",
        official_wording="Number systems",
        curriculum_subtopic_code="U1_CH1_ST1",
        review_status="PROVISIONAL_REVIEW_REQUIRED",
    )
    values.update(changes)
    return ExamSyllabusMapping(**values)


class ExamSyllabusRegistryTests(unittest.TestCase):
    def test_provisional_mapping_is_not_approved(self):
        registry = ExamSyllabusRegistry([source()], [mapping()])
        self.assertIsNone(registry.approved_mapping(
            "JEE Main", "2026", "MATHEMATICS", "U1_CH1_ST1"
        ))
        self.assertEqual(len(registry.pending_mappings()), 1)

    def test_exact_audited_approved_mapping_is_returned(self):
        approved = mapping(
            review_status="APPROVED", reviewer_id="reviewer-1",
            reviewed_at="2026-11-16T10:00:00Z",
            review_source="Official PDF page 3",
            approval_rationale="Wording and mapping manually checked against source.",
        )
        registry = ExamSyllabusRegistry([source()], [approved])
        self.assertEqual(
            registry.approved_mapping("JEE Main", "2026", "MATHEMATICS", "U1_CH1_ST1"),
            approved,
        )

    def test_rejects_mapping_with_unregistered_source(self):
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "unknown source_id"):
            ExamSyllabusRegistry([source()], [mapping(source_id="MISSING")])

    def test_rejects_exam_or_version_mismatch(self):
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "does not match"):
            ExamSyllabusRegistry([source()], [mapping(syllabus_version="2025")])


    def test_approved_mapping_requires_downloaded_fingerprinted_source(self):
        approved = mapping(
            review_status="APPROVED", reviewer_id="reviewer",
            reviewed_at="2026-11-16T10:00:00Z",
            review_source="Official syllabus PDF page 3",
            approval_rationale="Exact wording and mapping checked.",
        )
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "SHA-256-fingerprinted"):
            ExamSyllabusRegistry([source(document_sha256="")], [approved])
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "SHA-256-fingerprinted"):
            ExamSyllabusRegistry([source(retrieved_at="")], [approved])

    def test_approved_mapping_requires_explicit_source_effective_date(self):
        approved = mapping(
            review_status="APPROVED", reviewer_id="reviewer",
            reviewed_at="2026-11-16T10:00:00Z",
            review_source="Official syllabus PDF page 3",
            approval_rationale="Exact wording and mapping checked.",
        )
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "effective_from"):
            ExamSyllabusRegistry([source(effective_from="")], [approved])

    def test_rejects_approved_mapping_without_audit_evidence(self):
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "requires reviewer"):
            ExamSyllabusRegistry([source()], [mapping(review_status="APPROVED")])

    def test_rejects_timezone_free_review_timestamp(self):
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "timezone"):
            ExamSyllabusRegistry([source()], [mapping(
                review_status="REJECTED", reviewer_id="reviewer",
                reviewed_at="2026-11-16T10:00:00", review_source="PDF page 3",
                approval_rationale="Not in scope.",
            )])

    def test_rejects_invalid_hash_and_inverted_effective_dates(self):
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "document_sha256"):
            ExamSyllabusRegistry([source(document_sha256="bad")], [])
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "precedes"):
            ExamSyllabusRegistry([source(effective_to="2025-12-31")], [])


    def test_repository_registry_records_official_sources_without_approving_mappings(self):
        root = Path(__file__).resolve().parents[1]
        registry = ExamSyllabusRegistry.load_csv(
            root / "catalogs" / "exam_syllabus_sources.csv",
            root / "catalogs" / "exam_syllabus_mappings.csv",
        )
        self.assertEqual(len(registry.sources), 8)
        source_ids = {item.source_id for item in registry.sources}
        self.assertEqual(source_ids, {
            "NEET-UG-2026-NMC", "JEE-MAIN-2026-NTA",
            "JEE-MAIN-2027-NTA", "JEE-ADVANCED-2026-IITD",
            "JEE-ADVANCED-2027-IITD", "BITSAT-2026-BITS",
            "NEET-UG-2027-NTA", "BITSAT-2027-BITS",
        })
        jee_main_2026 = next(item for item in registry.sources if item.source_id == "JEE-MAIN-2026-NTA")
        self.assertEqual(jee_main_2026.publication_date, "2025-10-31")
        self.assertEqual(jee_main_2026.document_sha256, "")
        self.assertTrue(jee_main_2026.official_source_url.endswith("/202510311323551056.pdf"))
        jee_main_2027 = next(item for item in registry.sources if item.source_id == "JEE-MAIN-2027-NTA")
        self.assertEqual(jee_main_2027.publication_date, "")
        self.assertTrue(jee_main_2027.official_source_url.endswith("/20261024683680768.pdf"))
        jee_advanced_2026 = next(item for item in registry.sources if item.source_id == "JEE-ADVANCED-2026-IITD")
        self.assertTrue(jee_advanced_2026.official_source_url.endswith("/jee-advanced-2026-syllabus.pdf"))
        bitsat_2026 = next(item for item in registry.sources if item.source_id == "BITSAT-2026-BITS")
        self.assertTrue(bitsat_2026.official_source_url.endswith("/BITSAT-2026_brochure.pdf"))
        neet_2027 = next(item for item in registry.sources if item.source_id == "NEET-UG-2027-NTA")
        self.assertEqual(neet_2027.official_source_url, "https://neet.nta.nic.in/")
        bitsat_2027 = next(item for item in registry.sources if item.source_id == "BITSAT-2027-BITS")
        self.assertEqual(bitsat_2027.official_source_url, "https://admissions.bits-pilani.ac.in/FD/FD_brochure.html")
        self.assertEqual(registry.mappings, ())
        status_path = root / "catalogs" / "exam_syllabus_source_status.csv"
        with status_path.open("r", encoding="utf-8", newline="") as handle:
            status_rows = list(__import__("csv").DictReader(handle))
        self.assertEqual({row["source_id"] for row in status_rows}, source_ids)
        self.assertTrue(all(row["subtopic_mapping_status"] == "NO_MAPPINGS_APPROVED" for row in status_rows))


    def test_provisional_baseline_selects_latest_prior_year_without_approving_mapping(self):
        registry = ExamSyllabusRegistry(
            [
                source(),
                source(
                    source_id="JEE-MAIN-2025",
                    syllabus_version="2025",
                    official_source_title="Official JEE Main 2025 syllabus",
                    publication_date="2024-11-01",
                    effective_from="",
                    effective_to="",
                    retrieved_at="",
                    document_sha256="",
                ),
            ],
            [],
        )
        baseline = registry.provisional_baseline_source("JEE Main", "2027")
        self.assertIsNotNone(baseline)
        self.assertEqual(baseline.syllabus_version, "2026")
        self.assertIsNone(registry.approved_mapping(
            "JEE Main", "2027", "MATHEMATICS", "U1_CH1_ST1"
        ))

    def test_provisional_baseline_does_not_choose_future_or_ambiguous_sources(self):
        registry = ExamSyllabusRegistry([source()], [])
        self.assertIsNone(registry.provisional_baseline_source("JEE Advanced", "2027"))
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "four-digit year"):
            registry.provisional_baseline_source("JEE Main", "latest")
        duplicate_year_source = source(
            source_id="JEE-MAIN-2026-ALT",
            official_source_title="Alternate official JEE Main 2026 source",
        )
        ambiguous = ExamSyllabusRegistry([source(), duplicate_year_source], [])
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "Ambiguous prior-year"):
            ambiguous.provisional_baseline_source("JEE Main", "2027")

    def test_allows_unknown_publication_and_effective_dates_without_inventing_them(self):
        registry = ExamSyllabusRegistry(
            [source(publication_date="", effective_from="", effective_to="")], []
        )
        self.assertEqual(registry.sources[0].publication_date, "")
        with self.assertRaisesRegex(ExamSyllabusRegistryError, "effective_to requires"):
            ExamSyllabusRegistry(
                [source(publication_date="", effective_from="", effective_to="2026-12-31")], []
            )

    def test_csv_loader_requires_schema_and_loads_records(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources_path = root / "sources.csv"
            mappings_path = root / "mappings.csv"
            sources_path.write_text(
                "source_id,exam,syllabus_version,official_source_title,official_source_url,"
                "publication_date,effective_from,effective_to,retrieved_at,document_sha256\n"
                "JEE-MAIN-2026,JEE Main,2026,Official JEE Main syllabus,"
                "https://example.org/jee-main-2026.pdf,2025-10-01,2026-01-01,"
                "2026-12-31,2026-11-16T10:00:00Z," + "a" * 64 + "\n",
                encoding="utf-8",
            )
            mappings_path.write_text(
                "mapping_id,source_id,exam,syllabus_version,subject_id,official_wording,"
                "curriculum_subtopic_code,review_status,reviewer_id,reviewed_at,"
                "review_source,approval_rationale\n",
                encoding="utf-8",
            )
            registry = ExamSyllabusRegistry.load_csv(sources_path, mappings_path)
        self.assertEqual(len(registry.sources), 1)
        self.assertEqual(len(registry.mappings), 0)


class ExamVersionedScopeIntegrationTests(unittest.TestCase):
    def test_requires_approved_mapping_for_exam_target(self):
        from question_engine.curriculum import CurriculumSnapshot
        from question_engine.scope_verification import ScopeVerificationResult

        curriculum = CurriculumSnapshot(
            subjects=[{"id": "MATHEMATICS"}], units=[], chapters=[],
            subtopics=[{"id": "ST1", "code": "U1_CH1_ST1"}],
        )

        class PassingBaseVerifier:
            def verify(self, question):
                return ScopeVerificationResult(question.question_id, True, "base", "internal check passed")

        approved = mapping(
            review_status="APPROVED", reviewer_id="reviewer",
            reviewed_at="2026-11-16T10:00:00Z",
            review_source="Official syllabus PDF page 3",
            approval_rationale="Exact official wording manually mapped.",
        )
        registry = ExamSyllabusRegistry([source()], [approved])
        verifier = ExamVersionedQuestionScopeVerifier(
            curriculum, PassingBaseVerifier(), registry, {"JEE Main": "2026"}
        )

        class Question:
            question_id = "Q-EXAM-1"
            subject_id = "MATHEMATICS"
            subtopic_id = "ST1"
            exam_targets = ("JEE Main",)

        result = verifier.verify(Question())
        self.assertTrue(result.verified)
        self.assertIn("JEE Main 2026", result.evidence)

    def test_rejects_missing_mapping_and_unconfigured_version(self):
        from question_engine.curriculum import CurriculumSnapshot
        from question_engine.scope_verification import ScopeVerificationResult

        curriculum = CurriculumSnapshot(
            subjects=[{"id": "MATHEMATICS"}], units=[], chapters=[],
            subtopics=[{"id": "ST1", "code": "U1_CH1_ST1"}],
        )

        class PassingBaseVerifier:
            def verify(self, question):
                return ScopeVerificationResult(question.question_id, True, "base", "ok")

        class Question:
            question_id = "Q-EXAM-2"
            subject_id = "MATHEMATICS"
            subtopic_id = "ST1"
            exam_targets = ("JEE Advanced",)

        verifier = ExamVersionedQuestionScopeVerifier(
            curriculum, PassingBaseVerifier(), ExamSyllabusRegistry([source()], []),
            {"JEE Advanced": "2026"},
        )
        self.assertFalse(verifier.verify(Question()).verified)

        verifier_without_version = ExamVersionedQuestionScopeVerifier(
            curriculum, PassingBaseVerifier(), ExamSyllabusRegistry([source()], []), {}
        )
        self.assertIn("No explicitly configured", verifier_without_version.verify(Question()).reason)


if __name__ == "__main__":
    unittest.main()
