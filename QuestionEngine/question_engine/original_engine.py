"""Original-question selection: no fixed quota, only quality-approved candidates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .models import QuestionCandidate, QuestionOrigin
from .quality import QuestionQualityGate, QualityDecision


@dataclass(frozen=True)
class OriginalEngineResult:
    approved: List[QuestionCandidate]
    rejected: List[tuple[QuestionCandidate, QualityDecision]]
    duplicates: List[QuestionCandidate]


class OriginalQuestionEngine:
    """Review candidates produced by a configured AI/faculty generator.

    Generation is injected rather than hardwired, so API credentials and provider
    choices stay outside the academic rules and can be configured in deployment.
    """

    def __init__(self, quality_gate: QuestionQualityGate | None = None):
        self.quality_gate = quality_gate or QuestionQualityGate()

    def review(self, candidates: Iterable[QuestionCandidate]) -> OriginalEngineResult:
        approved: List[QuestionCandidate] = []
        rejected: List[tuple[QuestionCandidate, QualityDecision]] = []

        for candidate in candidates:
            if candidate.origin != QuestionOrigin.ORIGINAL:
                rejected.append((
                    candidate,
                    QualityDecision(False, ("Original engine accepts ORIGINAL records only",), None),
                ))
                continue
            decision = self.quality_gate.evaluate(candidate)
            if decision.approved:
                approved.append(candidate)
            else:
                rejected.append((candidate, decision))

        unique, duplicates = self.quality_gate.remove_exact_duplicates(approved)
        return OriginalEngineResult(unique, rejected, duplicates)
