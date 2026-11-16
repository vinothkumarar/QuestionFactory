from pathlib import Path
import unittest

from question_engine.curriculum import CurriculumLoader
from question_engine.models import (
    PYQProvenance,
    QuestionCandidate,
    QuestionOrigin,
    QuestionQualityScores,
)
from question_engine.original_engine import OriginalQuestionEngine
from question_engine.pyq_engine import PYQPracticeEngine
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
