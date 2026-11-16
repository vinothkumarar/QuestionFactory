"""Original-question selection: no fixed quota, only quality-approved candidates."""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import islice
from typing import Iterable, List

from .generation import GenerationRequest, QuestionGenerationProvider
from .models import QuestionCandidate, QuestionOrigin
from .quality import QuestionQualityGate, QualityDecision
from .verification import QuestionAnswerVerifier


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

    def generate_and_review(
        self,
        request: GenerationRequest,
        provider: QuestionGenerationProvider,
        verifier: QuestionAnswerVerifier,
    ) -> OriginalEngineResult:
        """Generate candidates, independently verify answers, then review.

        Any answer_verified flag supplied by the generator is discarded. Only
        the separate verifier can restore that flag, and only with method and
        evidence. Every resulting candidate then passes the shared quality gate.
        """
        verified_candidates = []
        candidates = islice(provider.generate(request), request.candidate_limit)
        for candidate in candidates:
            unverified = replace(
                candidate,
                answer_verified=False,
                answer_verification_method="",
                answer_verification_evidence="",
                answer_verification_notes="",
            )
            verification = verifier.verify(unverified)
            if verification.question_id != candidate.question_id:
                verified_candidates.append(
                    replace(
                        unverified,
                        answer_verification_notes=(
                            "Verifier returned a mismatched question_id"
                        ),
                    )
                )
            elif (
                verification.verified
                and verification.method.strip()
                and verification.evidence.strip()
            ):
                verified_candidates.append(
                    replace(
                        unverified,
                        answer_verified=True,
                        answer_verification_method=verification.method.strip(),
                        answer_verification_evidence=verification.evidence.strip(),
                    )
                )
            else:
                verified_candidates.append(
                    replace(
                        unverified,
                        answer_verification_notes=(
                            verification.reason
                            or "Independent verifier did not approve the answer"
                        ),
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
