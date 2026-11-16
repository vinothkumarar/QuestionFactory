"""Original-question selection: no fixed quota, only quality-approved candidates."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import islice
from typing import Iterable, List

from .generation import GenerationRequest, QuestionGenerationProvider
from .models import QuestionCandidate, QuestionOrigin
from .quality import QuestionQualityGate, QualityDecision


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
    ) -> OriginalEngineResult:
        """Generate a bounded candidate batch, then apply the normal review gates.

        The provider does not get to approve its own output. Every candidate is
        passed through the same hard gates and duplicate checks as supplied data.
        """
        candidates = islice(provider.generate(request), request.candidate_limit)
        return self.review(candidates)

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
