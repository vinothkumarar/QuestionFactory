"""
Question Factory OS v3.0

Quality Pipeline

Coordinates execution of all quality validators.
"""

from __future__ import annotations

from typing import Iterable

from Engine.factory.quality.models.quality_issue import (
    QualityIssue,
)
from Engine.factory.quality.models.quality_report import (
    QualityReport,
)
from Engine.factory.quality.models.quality_score import (
    QualityScore,
)
from Engine.factory.quality.models.validation_context import (
    ValidationContext,
)
from Engine.factory.quality.models.validation_result import (
    ValidationResult,
)
from Engine.factory.quality.validators.base_validator import (
    BaseValidator,
)


class QualityPipeline:
    """
    Executes validators sequentially and produces
    a QualityReport.
    """

    def __init__(
        self,
        validators: Iterable[BaseValidator],
    ) -> None:
        self._validators = list(validators)

    def validate(
        self,
        context: ValidationContext,
    ) -> QualityReport:
        """
        Execute all validators.
        """

        report = QualityReport()

        for validator in self._validators:
            result = validator.validate(context)
            report.add_result(result)

        report.score = self._build_score(report)

        return report

    def _build_score(
        self,
        report: QualityReport,
    ) -> QualityScore:
        """
        Construct the quality score from the report.
        """

        score = QualityScore()

        for result in report.validation_results:

            if result.passed:
                score.passed_rules += 1
            else:
                score.failed_rules += 1

            for issue in result.issues:
                self._count_issue(score, issue)

        return score

    @staticmethod
    def _count_issue(
        score: QualityScore,
        issue: QualityIssue,
    ) -> None:
        """
        Update score counters using issue severity.
        """

        severity = issue.severity.name

        if severity == "WARNING":
            score.warnings += 1

        elif severity == "ERROR":
            score.errors += 1

        elif severity == "CRITICAL":
            score.critical_errors += 1


__all__ = [
    "QualityPipeline",
]