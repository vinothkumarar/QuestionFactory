"""Deterministic CSV export for quality-reviewed question records.

This is a staging/export contract, not a claim that the live Supabase import
schema has been confirmed. Nested collections are serialized as compact JSON
so option text and provenance are preserved without lossy delimiter tricks.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from .models import QuestionCandidate


CSV_FIELDS = (
    "question_id",
    "origin",
    "subject_id",
    "unit_id",
    "chapter_id",
    "subtopic_id",
    "question_text",
    "answer_type",
    "options_json",
    "correct_answer",
    "explanation",
    "difficulty",
    "exam_targets_json",
    "concept_ids_json",
    "reasoning_signature",
    "uniqueness_key",
    "answer_verified",
    "answer_verification_method",
    "answer_verification_evidence",
    "answer_verification_notes",
    "syllabus_scope_verified",
    "syllabus_verification_method",
    "syllabus_verification_evidence",
    "syllabus_verification_notes",
    "quality_scores_json",
    "pyq_provenance_json",
    "inspired_by_pyq_id",
    "tags_json",
)


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def question_to_csv_row(question: QuestionCandidate) -> dict[str, str]:
    """Convert one canonical record to a stable, lossless-enough staging row."""
    scores = asdict(question.quality_scores) if question.quality_scores else None
    provenance = asdict(question.pyq_provenance) if question.pyq_provenance else None
    return {
        "question_id": question.question_id,
        "origin": question.origin.value,
        "subject_id": question.subject_id,
        "unit_id": question.unit_id,
        "chapter_id": question.chapter_id,
        "subtopic_id": question.subtopic_id,
        "question_text": question.question_text,
        "answer_type": question.answer_type,
        "options_json": _json(list(question.options)),
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "difficulty": question.difficulty,
        "exam_targets_json": _json(list(question.exam_targets)),
        "concept_ids_json": _json(list(question.concept_ids)),
        "reasoning_signature": question.reasoning_signature,
        "uniqueness_key": question.uniqueness_key,
        "answer_verified": str(question.answer_verified).lower(),
        "answer_verification_method": question.answer_verification_method,
        "answer_verification_evidence": question.answer_verification_evidence,
        "answer_verification_notes": question.answer_verification_notes,
        "syllabus_scope_verified": str(question.syllabus_scope_verified).lower(),
        "syllabus_verification_method": question.syllabus_verification_method,
        "syllabus_verification_evidence": question.syllabus_verification_evidence,
        "syllabus_verification_notes": question.syllabus_verification_notes,
        "quality_scores_json": _json(scores) if scores is not None else "",
        "pyq_provenance_json": _json(provenance) if provenance is not None else "",
        "inspired_by_pyq_id": question.inspired_by_pyq_id or "",
        "tags_json": _json(list(question.tags)),
    }


class QuestionCSVExporter:
    """Write canonical question records to a deterministic UTF-8 CSV file."""

    def export(
        self,
        questions: Iterable[QuestionCandidate],
        destination: Path | str,
    ) -> int:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, extrasaction="raise")
            writer.writeheader()
            for question in questions:
                writer.writerow(question_to_csv_row(question))
                count += 1
        return count
