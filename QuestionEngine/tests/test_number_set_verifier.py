"""Tests for deterministic N/W/Z membership answer verification."""

from __future__ import annotations

import unittest

from question_engine.models import QuestionCandidate, QuestionOrigin
from question_engine.verification import NumberSetMembershipVerifier


class NumberSetMembershipVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.verifier = NumberSetMembershipVerifier()

    @staticmethod
    def question(text: str, options: tuple[str, ...], answer: str, **overrides):
        values = dict(
            question_id="ST1-MEMBERSHIP-001",
            origin=QuestionOrigin.ORIGINAL,
            subject_id="math",
            unit_id="u1",
            chapter_id="ch1",
            subtopic_id="st1",
            question_text=text,
            answer_type="SINGLE_CORRECT",
            options=options,
            correct_answer=answer,
            explanation="Membership is determined from the exact definition of the set.",
        )
        values.update(overrides)
        return QuestionCandidate(**values)

    def test_verifies_natural_number_when_zero_is_excluded(self) -> None:
        result = self.verifier.verify(self.question(
            "Which of these values is a natural number? Natural numbers exclude zero.",
            ("0", "-2", "3/2", "4"),
            "4",
        ))
        self.assertTrue(result.verified)
        self.assertIn("positive integer", result.evidence)

    def test_verifies_natural_number_when_zero_is_included(self) -> None:
        result = self.verifier.verify(self.question(
            "Which of these values is a natural number? Natural numbers include zero.",
            ("0", "-2", "3/2", "-1"),
            "0",
        ))
        self.assertTrue(result.verified)
        self.assertIn("non-negative integer", result.evidence)

    def test_requires_explicit_natural_number_convention(self) -> None:
        result = self.verifier.verify(self.question(
            "Which of these values is a natural number?",
            ("0", "-2", "3/2", "4"),
            "4",
        ))
        self.assertFalse(result.verified)
        self.assertIn("convention must explicitly", result.reason)

    def test_verifies_whole_number_and_integer_membership(self) -> None:
        whole = self.verifier.verify(self.question(
            "Which of these values is a whole number?",
            ("-1", "0", "2.5", "-3/2"),
            "0",
        ))
        integer = self.verifier.verify(self.question(
            "Which of these values is an integer?",
            ("-3", "0.5", "3/2", "2.5"),
            "-3",
        ))
        self.assertTrue(whole.verified)
        self.assertTrue(integer.verified)

    def test_verifies_non_membership(self) -> None:
        result = self.verifier.verify(self.question(
            "Which of these values is not an integer?",
            ("2", "0", "3/2", "-4"),
            "3/2",
        ))
        self.assertTrue(result.verified)

    def test_rejects_wrong_answer_and_multiple_matching_options(self) -> None:
        wrong = self.verifier.verify(self.question(
            "Which of these values is an integer?",
            ("-3", "0.5", "3/2", "2.5"),
            "3/2",
        ))
        multiple = self.verifier.verify(self.question(
            "Which of these values is a whole number?",
            ("0", "1", "2.5", "-3/2"),
            "0",
        ))
        self.assertFalse(wrong.verified)
        self.assertIn("disagrees", wrong.reason)
        self.assertFalse(multiple.verified)
        self.assertIn("found 2", multiple.reason)

    def test_rejects_equivalent_duplicate_options(self) -> None:
        result = self.verifier.verify(self.question(
            "Which of these values is an integer?",
            ("1", "1.0", "0", "3/2"),
            "1",
        ))
        self.assertFalse(result.verified)
        self.assertIn("four distinct exact numeric values", result.reason)

    def test_rejects_unsupported_format_and_answer_type(self) -> None:
        unsupported = self.verifier.verify(self.question(
            "Classify the following number.",
            ("1", "2", "3", "4"),
            "1",
        ))
        multiple_correct = self.verifier.verify(self.question(
            "Which of these values is an integer?",
            ("-3", "0.5", "3/2", "2.5"),
            "-3",
            answer_type="MULTIPLE_CORRECT",
        ))
        self.assertFalse(unsupported.verified)
        self.assertFalse(multiple_correct.verified)


if __name__ == "__main__":
    unittest.main()
