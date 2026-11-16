"""Independent curriculum hierarchy and approved-concept scope verification."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .models import QuestionCandidate


@dataclass(frozen=True)
class ScopeVerificationResult:
    question_id: str
    verified: bool
    method: str
    evidence: str
    reason: str = ""


class QuestionScopeVerifier(Protocol):
    """Check each question against the authoritative curriculum hierarchy."""

    def verify(self, question: QuestionCandidate) -> ScopeVerificationResult:
        ...


class ApprovedCatalogScopeVerifier:
    """Verify hierarchy IDs and concept membership against reviewed CSV catalogs.

    This checks the repository's approved curriculum/concept mapping. It does
    not independently prove inclusion in every exam's current official syllabus;
    that requires a separately curated, exam-versioned syllabus source.
    """

    METHOD = "approved-curriculum-concept-catalog-v1"

    def __init__(self, curriculum, concept_catalog):
        self.curriculum = curriculum
        self.concept_catalog = concept_catalog

    def verify(self, question: QuestionCandidate) -> ScopeVerificationResult:
        def reject(reason: str) -> ScopeVerificationResult:
            return ScopeVerificationResult(question.question_id, False, self.METHOD, "", reason)

        subtopic = next(
            (row for row in self.curriculum.subtopics if row.get("id") == question.subtopic_id),
            None,
        )
        if subtopic is None:
            return reject("Question subtopic_id is not present in the loaded curriculum")
        chapter = next(
            (row for row in self.curriculum.chapters if row.get("id") == subtopic.get("chapter_id")),
            None,
        )
        if chapter is None:
            return reject("Curriculum subtopic references an unknown chapter")
        unit = next(
            (row for row in self.curriculum.units if row.get("id") == chapter.get("unit_id")),
            None,
        )
        if unit is None:
            return reject("Curriculum chapter references an unknown unit")
        subject = next(
            (row for row in self.curriculum.subjects if row.get("id") == unit.get("subject_id")),
            None,
        )
        if subject is None:
            return reject("Curriculum unit references an unknown subject")

        for supplied, actual, field_name in (
            (question.chapter_id, chapter.get("id"), "chapter_id"),
            (question.unit_id, unit.get("id"), "unit_id"),
            (question.subject_id, subject.get("id"), "subject_id"),
        ):
            if supplied != actual:
                return reject(f"Question {field_name} does not match the curriculum hierarchy")

        if not question.concept_ids:
            return reject("Question has no concept_ids to verify against the approved catalog")
        approved_entries = self.concept_catalog.approved_for_generation(subtopic.get("code", ""))
        approved = {entry.concept_id: entry for entry in approved_entries}
        unknown = sorted(set(question.concept_ids) - set(approved))
        if unknown:
            if not approved:
                return reject("No reviewed APPROVED concepts are available for this subtopic")
            return reject(
                "Question references concepts not approved for this subtopic: " + ", ".join(unknown)
            )

        sources = sorted({approved[concept_id].review_source for concept_id in question.concept_ids})
        evidence = (
            f"Matched subject/unit/chapter/subtopic IDs to the loaded curriculum; "
            f"all question concepts are approved for {subtopic.get('code')}. "
            f"Concept review source(s): {'; '.join(sources)}."
        )
        return ScopeVerificationResult(question.question_id, True, self.METHOD, evidence)
