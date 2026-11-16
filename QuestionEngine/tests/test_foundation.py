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
from question_engine.pdf_ingest import PDFTextExtractor
from question_engine.quality import QuestionQualityGate


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
        syllabus_scope_verified=True,
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
        result = OriginalQuestionEngine().generate_and_review(request, FakeProvider())
        self.assertEqual(len(result.approved), 2)
        self.assertEqual(result.approved[0].question_id, "GEN-1")

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


if __name__ == "__main__":
    unittest.main()
