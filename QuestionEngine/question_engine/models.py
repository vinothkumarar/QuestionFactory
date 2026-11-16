"""Shared, provenance-aware data models for both question engines."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple


class QuestionOrigin(str, Enum):
    ORIGINAL = "ORIGINAL"
    PYQ = "PYQ"
    PYQ_INSPIRED = "PYQ_INSPIRED"


@dataclass(frozen=True)
class QuestionQualityScores:
    """Human/AI-assisted rubric scores. Each dimension is scored 0..10."""

    academic_accuracy: int
    reasoning_depth: int
    clarity: int
    distractor_quality: int
    exam_relevance: int

    @property
    def total(self) -> int:
        return (
            self.academic_accuracy
            + self.reasoning_depth
            + self.clarity
            + self.distractor_quality
            + self.exam_relevance
        )

    def valid_range(self) -> bool:
        return all(
            0 <= score <= 10
            for score in (
                self.academic_accuracy,
                self.reasoning_depth,
                self.clarity,
                self.distractor_quality,
                self.exam_relevance,
            )
        )


@dataclass(frozen=True)
class PYQProvenance:
    """Evidence needed to identify and verify an historical question."""

    exam: str
    year: int
    paper: str
    shift: str
    question_number: str
    source_file: str
    page_number: Optional[int] = None
    source_url: Optional[str] = None
    answer_key_reference: Optional[str] = None
    transcription_verified: bool = False
    answer_verified: bool = False
    diagram_verified: bool = False
    usage_rights_reviewed: bool = False


@dataclass(frozen=True)
class QuestionCandidate:
    """Canonical question record shared by original and PYQ workflows."""

    question_id: str
    origin: QuestionOrigin
    subject_id: str
    unit_id: str
    chapter_id: str
    subtopic_id: str
    question_text: str
    answer_type: str
    correct_answer: str
    explanation: str
    options: Tuple[str, ...] = field(default_factory=tuple)
    difficulty: str = "Medium"
    exam_targets: Tuple[str, ...] = field(default_factory=tuple)
    concept_ids: Tuple[str, ...] = field(default_factory=tuple)
    reasoning_signature: str = ""
    uniqueness_key: str = ""
    answer_verified: bool = False
    syllabus_scope_verified: bool = False
    quality_scores: Optional[QuestionQualityScores] = None
    pyq_provenance: Optional[PYQProvenance] = None
    inspired_by_pyq_id: Optional[str] = None
    tags: Tuple[str, ...] = field(default_factory=tuple)
