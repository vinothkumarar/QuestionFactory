from pathlib import Path
import csv
import json
import tempfile
import unittest

from question_engine.curriculum import CurriculumLoader
from question_engine.export import CSV_FIELDS, QuestionCSVExporter
from question_engine.generation import GenerationRequest
from question_engine.models import (
    PYQProvenance,
    QuestionCandidate,
    QuestionOrigin,
    QuestionQualityScores,
)
from question_engine.original_engine import OriginalQuestionEngine
from question_engine.pyq_engine import PYQPracticeEngine
from question_engine.pyq_registry import PYQSourceRegistry
from question_engine.pdf_ingest import PDFTextExtractor, PDFPageText, PDFExtractionResult
from question_engine.pyq_segmenter import PYQTextSegmenter
from question_engine.verification import AnswerVerificationResult
from question_engine.scope_verification import ScopeVerificationResult
from question_engine.openai_provider import (
    OpenAIProviderError,
    OpenAIQuestionGenerationProvider,
)
from question_engine.quality import QuestionQualityGate
from question_engine.pilot import build_request


REPO_ROOT = Path(__file__).resolve().parents[2]


def make_question(origin=QuestionOrigin.ORIGINAL, **overrides):
    values = dict(
        question_id="Q-MAT-U1-CH1-ST1-0001",
        origin=origin,
        subject_id="subject-math",
        unit_id="unit-u1",
        chapter_id="chapter-ch1",
        subtopic_id="subtopic-st1",
        question_text="For a positive integer n, which statement is always true?",
        answer_type="SINGLE_CORRECT",
        options=("A", "B", "C", "D"),
        correct_answer="A",
        explanation="The property follows directly from the definition.",
        difficulty="Medium",
        exam_targets=("JEE Main",),
        concept_ids=("number-classification",),
        reasoning_signature="classify-positive-integer-by-divisibility",
        uniqueness_key="positive-integer-classification-001",
        answer_verified=True,
        answer_verification_method="independent-symbolic-check",
        answer_verification_evidence="Worked solution independently checked against the result.",
        syllabus_scope_verified=True,
        syllabus_verification_method="curriculum-cross-reference",
        syllabus_verification_evidence="Mapped to the active subject/unit/chapter/subtopic hierarchy.",
        quality_scores=QuestionQualityScores(9, 8, 9, 8, 8),
    )
    values.update(overrides)
    return QuestionCandidate(**values)


class CurriculumTests(unittest.TestCase):
    def test_loads_four_exam_subjects_and_reports_incomplete_curriculum(self):
        snapshot = CurriculumLoader(REPO_ROOT / "Engine" / "curriculum").load()
        names = {row["name"] for row in snapshot.subjects}
        self.assertEqual(names, {"Mathematics", "Physics", "Chemistry", "Biology"})
        self.assertTrue(snapshot.subtopics)
        self.assertTrue(any(item.startswith("Biology:") for item in snapshot.incomplete_subjects))

    def test_pilot_request_resolves_subtopic_to_full_curriculum_hierarchy(self):
        snapshot = CurriculumLoader(REPO_ROOT / "Engine" / "curriculum").load()
        request = build_request(
            snapshot,
            "U1_CH1_ST1",
            ("JEE Main", "JEE Advanced"),
            ("natural-numbers", "integers"),
            ("Classify natural numbers, whole numbers and integers.",),
            3,
        )
        subtopic = snapshot.find_subtopic("U1_CH1_ST1")
        chapter = next(row for row in snapshot.chapters if row["id"] == subtopic["chapter_id"])
        unit = next(row for row in snapshot.units if row["id"] == chapter["unit_id"])
        subject = next(row for row in snapshot.subjects if row["id"] == unit["subject_id"])
        self.assertEqual(request.subject_id, subject["id"])
        self.assertEqual(request.unit_id, unit["id"])
        self.assertEqual(request.chapter_id, chapter["id"])
        self.assertEqual(request.subtopic_id, subtopic["id"])
        self.assertEqual(request.candidate_limit, 3)

    def test_finds_existing_subtopic_code(self):
        snapshot = CurriculumLoader(REPO_ROOT / "Engine" / "curriculum").load()
        row = snapshot.find_subtopic("U1_CH1_ST1")
        self.assertEqual(row["subtopic_name"], "Natural Numbers, Whole Numbers and Integers")


class QualityTests(unittest.TestCase):
    def test_approves_worthy_original_question(self):
        result = QuestionQualityGate().evaluate(make_question())
        self.assertTrue(result.approved)
        self.assertEqual(result.score, 42)

    def test_rejects_unverified_answer(self):
        result = QuestionQualityGate().evaluate(make_question(answer_verified=False))
        self.assertFalse(result.approved)
        self.assertIn("Correct answer has not been independently verified", result.reasons)

    def test_verified_original_requires_verification_evidence(self):
        question = make_question(answer_verification_evidence="")
        result = QuestionQualityGate().evaluate(question)
        self.assertFalse(result.approved)
        self.assertIn(
            "Independent answer verification evidence is missing",
            result.reasons,
        )

    def test_original_engine_has_no_fixed_question_quota(self):
        result = OriginalQuestionEngine().review([make_question()])
        self.assertEqual(len(result.approved), 1)

    def test_exact_duplicates_are_removed(self):
        first = make_question()
        second = make_question(question_id="Q-2")
        result = OriginalQuestionEngine().review([first, second])
        self.assertEqual(len(result.approved), 1)
        self.assertEqual(len(result.duplicates), 1)

    def test_pyq_inspired_question_requires_source_pyq_identity(self):
        question = make_question(
            origin=QuestionOrigin.PYQ_INSPIRED,
            inspired_by_pyq_id="JEE-MAIN-2025-P1-S1-Q12",
        )
        self.assertTrue(QuestionQualityGate().evaluate(question).approved)

        missing_source = make_question(origin=QuestionOrigin.PYQ_INSPIRED)
        result = QuestionQualityGate().evaluate(missing_source)
        self.assertFalse(result.approved)
        self.assertIn("PYQ-inspired question lacks its source PYQ ID", result.reasons)


class OpenAIProviderTests(unittest.TestCase):
    @staticmethod
    def _request():
        return GenerationRequest(
            subject_id="subject-math",
            unit_id="unit-u1",
            chapter_id="chapter-ch1",
            subtopic_id="subtopic-st1",
            exam_targets=("JEE Main",),
            concept_ids=("number-classification",),
            learning_outcomes=("Classify integers using divisibility.",),
            candidate_limit=2,
        )

    @staticmethod
    def _candidate():
        return {
            "question_text": "Which of these integers is divisible by 6?",
            "answer_type": "SINGLE_CORRECT",
            "options": ["12", "14", "15", "25"],
            "correct_answer": "12",
            "explanation": "12 = 6 × 2, so it is divisible by 6.",
            "difficulty": "Easy",
            "concept_ids": ["divisibility"],
            "reasoning_signature": "test-divisibility-by-six",
            "uniqueness_key": "divisibility-six-check",
            "quality_scores": {
                "academic_accuracy": 9,
                "reasoning_depth": 8,
                "clarity": 9,
                "distractor_quality": 8,
                "exam_relevance": 8,
            },
            "tags": ["number-system"],
        }

    def test_provider_parses_candidates_but_never_self_verifies(self):
        captured = {}

        def fake_transport(url, headers, body, timeout):
            captured["url"] = url
            captured["headers"] = headers
            captured["body"] = json.loads(body)
            payload = {"questions": [self._candidate()]}
            return json.dumps({
                "choices": [{"message": {"content": json.dumps(payload)}}]
            }).encode("utf-8")

        provider = OpenAIQuestionGenerationProvider(
            api_key="test-secret",
            model="test-model",
            transport=fake_transport,
        )
        candidates = list(provider.generate(self._request()))
        self.assertEqual(len(candidates), 1)
        candidate = candidates[0]
        self.assertEqual(candidate.origin, QuestionOrigin.ORIGINAL)
        self.assertFalse(candidate.answer_verified)
        self.assertFalse(candidate.syllabus_scope_verified)
        self.assertEqual(candidate.subject_id, "subject-math")
        self.assertTrue(candidate.question_id.startswith("DRAFT-"))
        self.assertEqual(captured["url"], "https://api.openai.com/v1/chat/completions")
        self.assertEqual(captured["headers"]["Authorization"], "Bearer test-secret")
        self.assertEqual(captured["body"]["response_format"], {"type": "json_object"})

    def test_provider_rejects_missing_configuration(self):
        with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY"):
            OpenAIQuestionGenerationProvider(api_key="", model="test-model")
        with self.assertRaisesRegex(ValueError, "OPENAI_MODEL"):
            OpenAIQuestionGenerationProvider(api_key="test-secret", model="")

    def test_provider_rejects_malformed_mcq_instead_of_repairing_it(self):
        def fake_transport(url, headers, body, timeout):
            invalid = self._candidate()
            invalid["options"] = ["12", "14"]
            payload = {"questions": [invalid]}
            return json.dumps({
                "choices": [{"message": {"content": json.dumps(payload)}}]
            }).encode("utf-8")

        provider = OpenAIQuestionGenerationProvider(
            api_key="test-secret",
            model="test-model",
            transport=fake_transport,
        )
        with self.assertRaisesRegex(OpenAIProviderError, "exactly four options"):
            list(provider.generate(self._request()))


class GenerationTests(unittest.TestCase):
    def test_provider_output_is_capped_and_still_quality_reviewed(self):
        class FakeProvider:
            def generate(self, request):
                for index in range(1, 4):
                    yield make_question(
                        question_id=f"GEN-{index}",
                        question_text=f"Generated candidate {index}: evaluate a distinct divisibility property.",
                        uniqueness_key=f"generated-concept-{index}",
                    )

        request = GenerationRequest(
            subject_id="subject-math",
            unit_id="unit-u1",
            chapter_id="chapter-ch1",
            subtopic_id="subtopic-st1",
            exam_targets=("JEE Main",),
            concept_ids=("number-classification",),
            learning_outcomes=("Classify integers using divisibility.",),
            candidate_limit=2,
        )
        class FakeVerifier:
            def verify(self, question):
                return AnswerVerificationResult(
                    question_id=question.question_id,
                    verified=True,
                    method="independent-symbolic-check",
                    evidence="Recomputed independently and substituted into the original condition.",
                )

        class FakeScopeVerifier:
            def verify(self, question):
                return ScopeVerificationResult(
                    question_id=question.question_id,
                    verified=True,
                    method="curriculum-cross-reference",
                    evidence="Confirmed subject, unit, chapter and subtopic mapping.",
                )

        result = OriginalQuestionEngine().generate_and_review(
            request, FakeProvider(), FakeVerifier(), FakeScopeVerifier()
        )
        self.assertEqual(len(result.approved), 2)
        self.assertEqual(result.approved[0].question_id, "GEN-1")
        self.assertEqual(
            result.approved[0].answer_verification_method,
            "independent-symbolic-check",
        )

    def test_draft_generation_resets_provider_approval_flags(self):
        class FakeProvider:
            def generate(self, request):
                yield make_question(
                    answer_verified=True,
                    syllabus_scope_verified=True,
                    answer_verification_method="fake",
                    answer_verification_evidence="fake evidence",
                )

        request = GenerationRequest(
            subject_id="subject-math",
            unit_id="unit-u1",
            chapter_id="chapter-ch1",
            subtopic_id="subtopic-st1",
            exam_targets=("JEE Main",),
            concept_ids=("number-classification",),
            learning_outcomes=("Classify integers using divisibility.",),
        )
        drafts = OriginalQuestionEngine().generate_drafts(request, FakeProvider())
        self.assertEqual(len(drafts), 1)
        self.assertFalse(drafts[0].answer_verified)
        self.assertFalse(drafts[0].syllabus_scope_verified)
        self.assertEqual(drafts[0].answer_verification_method, "")
        self.assertIn("Awaiting independent", drafts[0].answer_verification_notes)

    def test_generator_cannot_self_approve_without_verifier_approval(self):
        class FakeProvider:
            def generate(self, request):
                yield make_question(answer_verified=True)

        class RejectingVerifier:
            def verify(self, question):
                return AnswerVerificationResult(
                    question_id=question.question_id,
                    verified=False,
                    method="",
                    evidence="",
                    reason="Independent recomputation disagreed with the supplied answer.",
                )

        request = GenerationRequest(
            subject_id="subject-math",
            unit_id="unit-u1",
            chapter_id="chapter-ch1",
            subtopic_id="subtopic-st1",
            exam_targets=("JEE Main",),
            concept_ids=("number-classification",),
            learning_outcomes=("Classify integers using divisibility.",),
        )
        class FakeScopeVerifier:
            def verify(self, question):
                return ScopeVerificationResult(
                    question_id=question.question_id,
                    verified=True,
                    method="curriculum-cross-reference",
                    evidence="Confirmed curriculum mapping.",
                )

        result = OriginalQuestionEngine().generate_and_review(
            request, FakeProvider(), RejectingVerifier(), FakeScopeVerifier()
        )
        self.assertEqual(result.approved, [])
        self.assertTrue(any(
            "Independent recomputation disagreed" in reason
            for reason in result.rejected[0][1].reasons
        ))

    def test_generation_request_rejects_missing_learning_outcomes(self):
        with self.assertRaises(ValueError):
            GenerationRequest(
                subject_id="subject-math",
                unit_id="unit-u1",
                chapter_id="chapter-ch1",
                subtopic_id="subtopic-st1",
                exam_targets=("JEE Main",),
                concept_ids=("number-classification",),
                learning_outcomes=(),
            )


class ExportTests(unittest.TestCase):
    def test_csv_export_preserves_options_and_question_text(self):
        question = make_question(
            question_text="Which number is divisible by both 2 and 3?",
            options=("6, 12", "5", "7", "11"),
            tags=("foundation", "number-system"),
        )
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "out" / "questions.csv"
            count = QuestionCSVExporter().export([question], destination)
            self.assertEqual(count, 1)
            with destination.open("r", encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(tuple(row.keys()), CSV_FIELDS)
            self.assertEqual(row["question_text"], question.question_text)
            self.assertEqual(json.loads(row["options_json"]), list(question.options))
            self.assertEqual(json.loads(row["tags_json"]), list(question.tags))
            self.assertEqual(row["origin"], "ORIGINAL")

    def test_csv_export_keeps_pyq_provenance(self):
        provenance = PYQProvenance(
            exam="JEE Main", year=2025, paper="Paper 1", shift="Shift 1",
            question_number="Q12", source_file="paper.pdf",
            answer_key_reference="official-key.pdf",
            transcription_verified=True, answer_verified=True,
        )
        question = make_question(
            origin=QuestionOrigin.PYQ,
            pyq_provenance=provenance,
        )
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "pyq.csv"
            QuestionCSVExporter().export([question], destination)
            with destination.open("r", encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle))
        exported = json.loads(row["pyq_provenance_json"])
        self.assertEqual(exported["exam"], "JEE Main")
        self.assertEqual(exported["source_file"], "paper.pdf")
        self.assertTrue(exported["transcription_verified"])


class PYQRegistryTests(unittest.TestCase):
    def test_loads_source_manifest_without_claiming_papers_are_acquired(self):
        content = (
            "PYQ_ID,Year,Exam,Paper,Language,Source,Primary Source URL,PDF URL,"
            "Answer Key URL,Solution URL,Acquisition Status,PDF Verified,"
            "Answer Key Verified,Audit Status\n"
            "JEE-2025-P1,2025,JEE Main,Paper 1,English,Official archive,"
            "https://example.org/archive,, , ,Not yet acquired,No,No,Ready for acquisition\n"
            "JEE-2024-P2,2024,JEE Advanced,Paper 2,English,Official archive,"
            "https://example.org/archive,https://example.org/paper.pdf,"
            "https://example.org/key.pdf,,Acquired,Yes,Yes,Verified\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.csv"
            path.write_text(content, encoding="utf-8")
            registry = PYQSourceRegistry.load_csv(path)
        summary = registry.summary()
        self.assertEqual(summary.total_records, 2)
        self.assertEqual(summary.direct_pdf_urls, 1)
        self.assertEqual(summary.pdf_verified, 1)
        self.assertEqual(summary.answer_keys_verified, 1)
        self.assertEqual(summary.not_yet_acquired, 1)
        self.assertFalse(registry.records[0].ready_for_verified_practice)

    def test_loads_audited_xlsx_worksheet(self):
        from openpyxl import Workbook

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audited.xlsx"
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "Audited Tracker"
            worksheet.append([
                "PYQ_ID", "Year", "Exam", "Paper", "Language", "Source",
                "Primary Source URL", "PDF URL", "Answer Key URL",
                "Solution URL", "Acquisition Status", "PDF Verified",
                "Answer Key Verified", "Audit Status",
            ])
            worksheet.append([
                "JEE-2026-P1", 2026, "JEE Advanced", "Paper 1", "English",
                "Official archive", "https://example.org/archive",
                "https://example.org/paper.pdf", "https://example.org/key.pdf",
                None, "Acquired", "Yes", "Yes", "Ready",
            ])
            workbook.save(path)
            workbook.close()

            registry = PYQSourceRegistry.load_xlsx(path)
        self.assertEqual(registry.summary().total_records, 1)
        self.assertEqual(registry.records[0].pyq_id, "JEE-2026-P1")
        self.assertTrue(registry.records[0].pdf_verified)
        self.assertEqual(registry.records[0].answer_key_url, "https://example.org/key.pdf")

    def test_registry_rejects_duplicate_pyq_ids(self):
        content = (
            "PYQ_ID,Year,Exam,Paper,Acquisition Status\n"
            "DUP,2025,JEE Main,Paper 1,Not yet acquired\n"
            "DUP,2024,JEE Main,Paper 2,Not yet acquired\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.csv"
            path.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate PYQ_ID"):
                PYQSourceRegistry.load_csv(path)


class PDFIngestionTests(unittest.TestCase):
    def test_extracts_page_count_hash_and_marks_scanned_pages_for_ocr(self):
        from pypdf import PdfWriter

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scanned-source.pdf"
            writer = PdfWriter()
            writer.add_blank_page(width=612, height=792)
            writer.add_blank_page(width=612, height=792)
            with path.open("wb") as handle:
                writer.write(handle)

            result = PDFTextExtractor().extract(path)

        self.assertEqual(result.page_count, 2)
        self.assertEqual(len(result.sha256), 64)
        self.assertEqual(result.pages_needing_ocr, (1, 2))
        self.assertEqual(result.extracted_text_page_count, 0)

    def test_rejects_non_pdf_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "not-a-pdf.pdf"
            path.write_text("not a PDF", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not a valid PDF header"):
                PDFTextExtractor().extract(path)

    def test_enforces_pdf_size_limit(self):
        from pypdf import PdfWriter

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.pdf"
            writer = PdfWriter()
            writer.add_blank_page(width=612, height=792)
            with path.open("wb") as handle:
                writer.write(handle)
            with self.assertRaisesRegex(ValueError, "size limit"):
                PDFTextExtractor(max_file_size_bytes=1).extract(path)


class PYQSegmentationTests(unittest.TestCase):
    def test_segments_numbered_questions_and_preserves_source_page(self):
        page = PDFPageText(
            page_number=4,
            text=(
                "12. Which of the following integers is divisible by 6?\n"
                "(A) 12\n(B) 14\n(C) 15\n(D) 25\n"
                "13. Find the next integer after 99.\n"
                "(A) 98\n(B) 100\n(C) 101\n(D) 102"
            ),
            needs_ocr=False,
        )
        result = PYQTextSegmenter().segment_page(
            page, source_path="paper.pdf", source_sha256="abc123"
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].question_number, "12")
        self.assertEqual(result[0].page_number, 4)
        self.assertEqual(result[0].detected_option_labels, ("A", "B", "C", "D"))
        self.assertIn("Which of the following", result[0].raw_text)
        self.assertEqual(result[0].source_sha256, "abc123")
        self.assertFalse(result[0].needs_manual_review)
        self.assertTrue(result[1].needs_manual_review)
        self.assertTrue(any("continue onto the next page" in reason for reason in result[1].pending_reasons))

    def test_unrecognized_page_is_preserved_as_pending_not_discarded(self):
        page = PDFPageText(
            page_number=7,
            text="Some text extracted from a paper with uncertain numbering.",
            needs_ocr=False,
        )
        result = PYQTextSegmenter().segment_page(page, "paper.pdf", "hash")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].question_number, "")
        self.assertTrue(result[0].needs_manual_review)
        self.assertIn("Some text extracted", result[0].raw_text)

    def test_segment_pdf_reports_pages_without_question_boundaries(self):
        extraction = PDFExtractionResult(
            source_path="paper.pdf",
            sha256="paper-hash",
            page_count=2,
            pages=(
                PDFPageText(1, "1. A sufficiently long question?\n(A) a\n(B) b\n(C) c\n(D) d", False),
                PDFPageText(2, "Header and footer only", False),
            ),
        )
        result = PYQTextSegmenter().segment_pdf(extraction)
        self.assertEqual(result.pages_without_question_boundaries, (2,))
        self.assertEqual(result.fragments[0].page_number, 1)


class PYQTests(unittest.TestCase):
    def test_unverified_pyq_stays_pending(self):
        question = make_question(
            origin=QuestionOrigin.PYQ,
            pyq_provenance=PYQProvenance(
                exam="JEE Main",
                year=2025,
                paper="Paper 1",
                shift="Shift 1",
                question_number="Q12",
                source_file="2025-paper.pdf",
            ),
        )
        result = PYQPracticeEngine().ingest(question)
        self.assertFalse(result.verified_for_practice)
        self.assertTrue(any("not verified" in reason for reason in result.pending_reasons))

    def test_pyq_with_unreferenced_answer_key_stays_pending(self):
        provenance = PYQProvenance(
            exam="JEE Main", year=2025, paper="Paper 1", shift="Shift 1",
            question_number="Q12", source_file="paper.pdf",
            transcription_verified=True, answer_verified=True,
        )
        result = PYQPracticeEngine().ingest(
            make_question(origin=QuestionOrigin.PYQ, pyq_provenance=provenance)
        )
        self.assertFalse(result.verified_for_practice)
        self.assertIn("PYQ answer-key/solution reference is missing", result.pending_reasons)

    def test_verified_pyq_enters_practice_collection(self):
        provenance = PYQProvenance(
            exam="JEE Main",
            year=2025,
            paper="Paper 1",
            shift="Shift 1",
            question_number="Q12",
            source_file="2025-paper.pdf",
            answer_key_reference="official-final-key.pdf",
            transcription_verified=True,
            answer_verified=True,
        )
        question = make_question(origin=QuestionOrigin.PYQ, pyq_provenance=provenance)
        result = PYQPracticeEngine().ingest(question)
        self.assertTrue(result.verified_for_practice)


class IntegerArithmeticVerifierTests(unittest.TestCase):
    def setUp(self):
        from question_engine.verification import IntegerArithmeticExpressionVerifier
        self.verifier = IntegerArithmeticExpressionVerifier()

    def _question(self, **overrides):
        values = dict(
            question_id="MATH-INT-001", origin=QuestionOrigin.ORIGINAL,
            subject_id="math", unit_id="u1", chapter_id="ch1", subtopic_id="st1",
            question_text="Evaluate: -8 + 3 * 4", answer_type="SINGLE_CORRECT",
            options=("4", "12", "-20", "0"), correct_answer="4",
            explanation="Apply multiplication before addition.",
        )
        values.update(overrides)
        return QuestionCandidate(**values)

    def test_verifies_supported_integer_expression(self):
        result = self.verifier.verify(self._question())
        self.assertTrue(result.verified)
        self.assertIn("evaluated to 4", result.evidence)

    def test_rejects_incorrect_answer(self):
        result = self.verifier.verify(self._question(correct_answer="12"))
        self.assertFalse(result.verified)
        self.assertIn("disagrees", result.reason)

    def test_rejects_unsupported_question_format(self):
        result = self.verifier.verify(self._question(question_text="Which integer is largest?"))
        self.assertFalse(result.verified)

    def test_rejects_function_calls(self):
        result = self.verifier.verify(self._question(question_text="Evaluate: abs(-4)"))
        self.assertFalse(result.verified)

    def test_rejects_division_by_zero(self):
        result = self.verifier.verify(self._question(question_text="Evaluate: 8 // 0"))
        self.assertFalse(result.verified)

    def test_rejects_non_integer_and_duplicate_options(self):
        self.assertFalse(self.verifier.verify(
            self._question(options=("4", "12", "3/4", "0"))
        ).verified)
        self.assertFalse(self.verifier.verify(
            self._question(options=("4", "4", "12", "0"))
        ).verified)

    def test_rejects_missing_result_and_excessive_values(self):
        self.assertFalse(self.verifier.verify(
            self._question(options=("5", "12", "-20", "0"))
        ).verified)
        self.assertFalse(self.verifier.verify(
            self._question(question_text="Evaluate: 999999999999999 * 999999999999999")
        ).verified)


class DivisibilityRuleVerifierTests(unittest.TestCase):
    def setUp(self):
        from question_engine.verification import DivisibilityRuleVerifier
        self.verifier = DivisibilityRuleVerifier()

    def _question(self, **overrides):
        values = dict(
            question_id="MATH-DIV-001", origin=QuestionOrigin.ORIGINAL,
            subject_id="math", unit_id="u1", chapter_id="ch1", subtopic_id="st1",
            question_text="Which of these integers is divisible by 6?",
            answer_type="SINGLE_CORRECT",
            options=("12", "14", "15", "25"), correct_answer="12",
            explanation="12 = 6 × 2.",
        )
        values.update(overrides)
        return QuestionCandidate(**values)

    def test_verifies_unique_divisible_option(self):
        result = self.verifier.verify(self._question())
        self.assertTrue(result.verified)
        self.assertIn("exactly one option (12)", result.evidence)

    def test_rejects_wrong_supplied_answer(self):
        result = self.verifier.verify(self._question(correct_answer="14"))
        self.assertFalse(result.verified)
        self.assertIn("disagrees", result.reason)

    def test_rejects_multiple_or_zero_matching_options(self):
        self.assertFalse(self.verifier.verify(
            self._question(options=("12", "18", "15", "25"))
        ).verified)
        self.assertFalse(self.verifier.verify(
            self._question(options=("13", "14", "15", "25"))
        ).verified)

    def test_rejects_unsupported_format_and_non_single_correct(self):
        self.assertFalse(self.verifier.verify(
            self._question(question_text="Find all multiples of 6.")
        ).verified)
        self.assertFalse(self.verifier.verify(
            self._question(answer_type="MULTIPLE_CORRECT")
        ).verified)

    def test_rejects_invalid_divisor_and_option_values(self):
        self.assertFalse(self.verifier.verify(
            self._question(question_text="Which of these integers is divisible by 0?")
        ).verified)
        self.assertFalse(self.verifier.verify(
            self._question(options=("12", "14", "15.0", "25"))
        ).verified)
        self.assertFalse(self.verifier.verify(
            self._question(options=("12", "12", "15", "25"))
        ).verified)
        self.assertFalse(self.verifier.verify(
            self._question(options=("1200000000000", "14", "15", "25"))
        ).verified)


class ApprovedCatalogScopeVerifierTests(unittest.TestCase):
    def setUp(self):
        from question_engine.curriculum import CurriculumSnapshot
        from question_engine.concept_catalog import ConceptCatalog, ConceptEntry
        from question_engine.scope_verification import ApprovedCatalogScopeVerifier

        snapshot = CurriculumSnapshot(
            subjects=[{"id": "S1", "name": "Mathematics"}],
            units=[{"id": "U1", "subject_id": "S1"}],
            chapters=[{"id": "C1", "unit_id": "U1"}],
            subtopics=[{"id": "ST1", "chapter_id": "C1", "code": "U1_CH1_ST1"}],
        )
        catalog = ConceptCatalog([
            ConceptEntry(
                "INTEGER-CLASS", "U1_CH1_ST1", "Integer classification",
                "Classify integers.", "APPROVED",
                reviewer_id="reviewer", reviewed_at="2026-11-16T12:00:00Z",
                review_source="Approved syllabus mapping v1",
                approval_rationale="Explicitly reviewed against the approved scope.",
            ),
            ConceptEntry(
                "PROVISIONAL", "U1_CH1_ST1", "Provisional",
                "Pending review.", "PROVISIONAL_REVIEW_REQUIRED",
            ),
        ])
        self.verifier = ApprovedCatalogScopeVerifier(snapshot, catalog)

    def _question(self, **overrides):
        values = dict(
            question_id="SCOPE-001", origin=QuestionOrigin.ORIGINAL,
            subject_id="S1", unit_id="U1", chapter_id="C1", subtopic_id="ST1",
            question_text="Classify the integer 7.", answer_type="SHORT_ANSWER",
            correct_answer="integer", explanation="7 is an integer.",
            concept_ids=("INTEGER-CLASS",),
        )
        values.update(overrides)
        return QuestionCandidate(**values)

    def test_approves_exact_hierarchy_and_approved_concept_mapping(self):
        result = self.verifier.verify(self._question())
        self.assertTrue(result.verified)
        self.assertIn("Approved syllabus mapping v1", result.evidence)

    def test_rejects_mismatched_parent_hierarchy(self):
        result = self.verifier.verify(self._question(unit_id="WRONG"))
        self.assertFalse(result.verified)
        self.assertIn("unit_id", result.reason)

    def test_rejects_provisional_concept(self):
        result = self.verifier.verify(self._question(concept_ids=("PROVISIONAL",)))
        self.assertFalse(result.verified)
        self.assertIn("not approved", result.reason)

    def test_rejects_unknown_subtopic(self):
        result = self.verifier.verify(self._question(subtopic_id="UNKNOWN"))
        self.assertFalse(result.verified)


class CompositeQuestionAnswerVerifierTests(unittest.TestCase):
    def setUp(self):
        from question_engine.verification import CompositeQuestionAnswerVerifier
        self.Composite = CompositeQuestionAnswerVerifier

    def test_uses_first_independent_verifier_that_proves_answer(self):
        class RejectingVerifier:
            def verify(self, question):
                return AnswerVerificationResult(
                    question.question_id, False, "unsupported-v1", "",
                    "Question format is outside this verifier's scope",
                )

        class AcceptingVerifier:
            def verify(self, question):
                return AnswerVerificationResult(
                    question.question_id, True, "independent-check-v1",
                    "Recomputed result and matched the unique answer.",
                )

        result = self.Composite([
            RejectingVerifier(), AcceptingVerifier()
        ]).verify(make_question())
        self.assertTrue(result.verified)
        self.assertEqual(result.method, "independent-check-v1")

    def test_rejects_mismatched_question_id_from_verifier(self):
        class MismatchedVerifier:
            def verify(self, question):
                return AnswerVerificationResult(
                    "SOME-OTHER-ID", True, "bad-verifier-v1",
                    "This must never approve the current question.",
                )

        result = self.Composite([MismatchedVerifier()]).verify(make_question())
        self.assertFalse(result.verified)
        self.assertIn("mismatched question_id", result.reason)

    def test_rejects_positive_result_without_evidence(self):
        class EvidenceFreeVerifier:
            def verify(self, question):
                return AnswerVerificationResult(
                    question.question_id, True, "empty-evidence-v1", ""
                )

        result = self.Composite([EvidenceFreeVerifier()]).verify(make_question())
        self.assertFalse(result.verified)
        self.assertIn("lacked method or evidence", result.reason)

    def test_requires_at_least_one_verifier(self):
        with self.assertRaises(ValueError):
            self.Composite([])

    def test_reports_all_failed_verifiers_without_approving(self):
        class RejectingVerifier:
            def __init__(self, reason):
                self.reason = reason

            def verify(self, question):
                return AnswerVerificationResult(
                    question.question_id, False, "reject-v1", "", self.reason
                )

        result = self.Composite([
            RejectingVerifier("not arithmetic"),
            RejectingVerifier("not divisibility"),
        ]).verify(make_question())
        self.assertFalse(result.verified)
        self.assertIn("not arithmetic", result.reason)
        self.assertIn("not divisibility", result.reason)


if __name__ == "__main__":
    unittest.main()
