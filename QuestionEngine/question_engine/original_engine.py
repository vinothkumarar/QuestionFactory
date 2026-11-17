"""Original-question selection: no fixed quota, only quality-approved candidates."""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import islice
from typing import Iterable, List

from .generation import GenerationRequest, QuestionGenerationProvider
from .models import QuestionCandidate, QuestionOrigin
from .quality import QuestionQualityGate, QualityDecision
from .verification import QuestionAnswerVerifier
from .scope_verification import QuestionScopeVerifier


@dataclass(frozen=True)
class OriginalEngineResult:
    approved: List[QuestionCandidate]
    rejected: List[tuple[QuestionCandidate, QualityDecision]]
    duplicates: List[QuestionCandidate]


class OriginalQuestionEngine:
    """Review original and PYQ-inspired candidates from a configured generator.

    Generation is injected rather than hardwired, so API credentials and provider
    choices stay outside the academic rules and can be configured in deployment.
    Exact historical PYQs are intentionally rejected here and belong to PYQPracticeEngine.
    """

    ACCEPTED_ORIGINS = {QuestionOrigin.ORIGINAL, QuestionOrigin.PYQ_INSPIRED}

    def __init__(self, quality_gate: QuestionQualityGate | None = None):
        self.quality_gate = quality_gate or QuestionQualityGate()

    def generate_drafts(
        self,
        request: GenerationRequest,
        provider: QuestionGenerationProvider,
    ) -> list[QuestionCandidate]:
        """Generate bounded draft candidates without granting approval status."""
        drafts: list[QuestionCandidate] = []
        for candidate in islice(provider.generate(request), request.candidate_limit):
            if candidate.origin not in self.ACCEPTED_ORIGINS:
                continue
            drafts.append(
                replace(
                    candidate,
                    answer_verified=False,
                    syllabus_scope_verified=False,
                    answer_verification_method="",
                    answer_verification_evidence="",
                    answer_verification_notes="Awaiting independent answer verification.",
                    syllabus_verification_method="",
                    syllabus_verification_evidence="",
                    syllabus_verification_notes="Awaiting independent syllabus-scope verification.",
                )
            )
        return drafts

    def generate_and_review(
        self,
        request: GenerationRequest,
        provider: QuestionGenerationProvider,
        answer_verifier: QuestionAnswerVerifier,
        scope_verifier: QuestionScopeVerifier,
    ) -> OriginalEngineResult:
        """Generate drafts, independently verify answers and syllabus scope, then review."""
        verified_candidates = []
        for draft in self.generate_drafts(request, provider):
            answer_result = answer_verifier.verify(draft)
            if (
                answer_result.question_id != draft.question_id
                or not answer_result.verified
                or not answer_result.method.strip()
                or not answer_result.evidence.strip()
            ):
                detail = answer_result.reason or "Independent answer verification failed"
                if answer_result.question_id != draft.question_id:
                    detail = "Answer verifier returned a mismatched question_id"
                verified_candidates.append(
                    replace(draft, answer_verification_notes=detail)
                )
                continue

            answer_checked = replace(
                draft,
                answer_verified=True,
                answer_verification_method=answer_result.method.strip(),
                answer_verification_evidence=answer_result.evidence.strip(),
                answer_verification_notes="",
            )
            scope_result = scope_verifier.verify(answer_checked)
            if (
                scope_result.question_id != draft.question_id
                or not scope_result.verified
                or not scope_result.method.strip()
                or not scope_result.evidence.strip()
            ):
                detail = scope_result.reason or "Independent syllabus-scope verification failed"
                if scope_result.question_id != draft.question_id:
                    detail = "Scope verifier returned a mismatched question_id"
                verified_candidates.append(
                    replace(answer_checked, syllabus_verification_notes=detail)
                )
                continue

            verified_candidates.append(
                replace(
                    answer_checked,
                    syllabus_scope_verified=True,
                    syllabus_verification_method=scope_result.method.strip(),
                    syllabus_verification_evidence=scope_result.evidence.strip(),
                    syllabus_verification_notes="",
                )
            )
        return self.review(verified_candidates)

    def review(self, candidates: Iterable[QuestionCandidate]) -> OriginalEngineResult:
        approved: List[QuestionCandidate] = []
        rejected: List[tuple[QuestionCandidate, QualityDecision]] = []

        for candidate in candidates:
            if candidate.origin not in self.ACCEPTED_ORIGINS:
                rejected.append((
                    candidate,
                    QualityDecision(False, ("Exact PYQs belong to the PYQ engine",), None),
                ))
                continue
            decision = self.quality_gate.evaluate(candidate)
            if decision.approved:
                approved.append(candidate)
            else:
                rejected.append((candidate, decision))

        unique, duplicates = self.quality_gate.remove_exact_duplicates(approved)
        return OriginalEngineResult(unique, rejected, duplicates)
