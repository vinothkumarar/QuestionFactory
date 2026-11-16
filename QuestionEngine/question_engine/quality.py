"""Shared quality gates and conservative duplicate detection."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List, Set

from .models import QuestionCandidate, QuestionOrigin


@dataclass(frozen=True)
class QualityDecision:
    approved: bool
    reasons: tuple[str, ...]
    score: int | None


class QuestionQualityGate:
    """Reject hard failures first; then apply the agreed 40/50 quality floor."""

    MINIMUM_SCORE = 40
    MULTIPLE_CHOICE_TYPES = {"SINGLE_CORRECT", "MULTIPLE_CORRECT"}

    @staticmethod
    def _normalise(text: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", text.casefold())

    def evaluate(self, question: QuestionCandidate) -> QualityDecision:
        reasons: List[str] = []

        if not question.question_id.strip():
            reasons.append("Missing stable question_id")
        if not all((question.subject_id, question.unit_id, question.chapter_id, question.subtopic_id)):
            reasons.append("Incomplete curriculum references")
        if not question.question_text.strip():
            reasons.append("Missing question text")
        if not question.correct_answer.strip():
            reasons.append("Missing correct answer")
        if not question.explanation.strip():
            reasons.append("Missing explanation")
        if not question.syllabus_scope_verified:
            reasons.append("Syllabus scope has not been verified")
        if not question.answer_verified:
            reasons.append("Correct answer has not been independently verified")
        elif question.origin != QuestionOrigin.PYQ:
            if not question.answer_verification_method.strip():
                reasons.append("Independent answer verification method is missing")
            if not question.answer_verification_evidence.strip():
                reasons.append("Independent answer verification evidence is missing")

        if question.answer_type.upper() in self.MULTIPLE_CHOICE_TYPES:
            if len(question.options) != 4:
                reasons.append("MCQ must contain exactly four options")
            elif len({self._normalise(option) for option in question.options}) != 4:
                reasons.append("MCQ contains duplicate options")

        if question.origin in {QuestionOrigin.ORIGINAL, QuestionOrigin.PYQ_INSPIRED}:
            if not question.reasoning_signature.strip():
                reasons.append("Original question lacks a reasoning signature")
            if not question.uniqueness_key.strip():
                reasons.append("Original question lacks a uniqueness key")

        if question.origin == QuestionOrigin.PYQ_INSPIRED:
            if not question.inspired_by_pyq_id:
                reasons.append("PYQ-inspired question lacks its source PYQ ID")

        if question.origin == QuestionOrigin.PYQ:
            evidence = question.pyq_provenance
            if evidence is None:
                reasons.append("Exact PYQ has no source provenance")
            else:
                if not all((evidence.exam, evidence.paper, evidence.question_number, evidence.source_file)):
                    reasons.append("PYQ provenance is incomplete")
                if evidence.year < 1900 or evidence.year > 2100:
                    reasons.append("PYQ provenance has an invalid examination year")
                if evidence.page_number is not None and evidence.page_number < 1:
                    reasons.append("PYQ source page number must be positive")
                if not evidence.answer_key_reference:
                    reasons.append("PYQ answer-key/solution reference is missing")
                if not evidence.transcription_verified:
                    reasons.append("PYQ transcription is not verified against its source")
                if not evidence.answer_verified:
                    reasons.append("PYQ answer is not verified against an answer-key/solution source")

        scores = question.quality_scores
        score = scores.total if scores and scores.valid_range() else None
        if scores is None:
            reasons.append("Quality rubric has not been scored")
        elif not scores.valid_range():
            reasons.append("Quality rubric scores must each be between 0 and 10")
        elif score is not None and score < self.MINIMUM_SCORE:
            reasons.append(f"Quality score {score}/50 is below {self.MINIMUM_SCORE}/50")

        return QualityDecision(not reasons, tuple(reasons), score)

    def remove_exact_duplicates(
        self, questions: Iterable[QuestionCandidate]
    ) -> tuple[list[QuestionCandidate], list[QuestionCandidate]]:
        """Remove exact text/explicit-key duplicates; semantic similarity stays reviewable."""
        accepted: List[QuestionCandidate] = []
        rejected: List[QuestionCandidate] = []
        seen_text: Set[str] = set()
        seen_keys: Set[str] = set()

        for question in questions:
            text_key = self._normalise(question.question_text)
            unique_key = (
                f"{question.subject_id}:{question.subtopic_id}:"
                f"{question.uniqueness_key.strip().casefold()}"
            )
            duplicate = bool(text_key and text_key in seen_text)
            duplicate = duplicate or bool(question.uniqueness_key.strip() and unique_key in seen_keys)
            if duplicate:
                rejected.append(question)
                continue
            if text_key:
                seen_text.add(text_key)
            if question.uniqueness_key.strip():
                seen_keys.add(unique_key)
            accepted.append(question)

        return accepted, rejected
