"""
Question Factory OS v3.0

Quality Report
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass(slots=True)
class QualityReport:
    """
    Aggregated quality validation report.
    """

    passed: bool = True

    score: float = 100.0

    errors: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def add_error(self, message: str) -> None:
        self.errors.append(message)
        self.passed = False

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def add_recommendation(self, message: str) -> None:
        self.recommendations.append(message)

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    @property
    def recommendation_count(self) -> int:
        return len(self.recommendations)

    def calculate_score(self) -> float:
        """
        Recalculate the quality score.
        """

        score = 100.0

        score -= self.error_count * 10.0
        score -= self.warning_count * 2.0

        self.score = max(0.0, score)

        return self.score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "score": self.score,
            "errors": self.errors,
            "warnings": self.warnings,
            "recommendations": self.recommendations,
        }

    def __repr__(self) -> str:
        return (
            f"QualityReport("
            f"passed={self.passed}, "
            f"score={self.score:.1f}, "
            f"errors={self.error_count}, "
            f"warnings={self.warning_count})"
        )