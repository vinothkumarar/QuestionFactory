"""CSV source-registry loader for historical PYQ acquisition tracking.

This tracks paper/source availability only. A registry row is not a question,
a downloaded PDF, or a verified PYQ.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


def _first(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = (row.get(key) or "").strip()
        if value:
            return value
    return ""


def _is_yes(value: str) -> bool:
    return value.strip().casefold() in {"yes", "true", "1", "verified"}


@dataclass(frozen=True)
class PYQSourceRecord:
    pyq_id: str
    year: int
    exam: str
    paper: str
    language: str
    source_name: str
    source_url: str
    pdf_url: str
    answer_key_url: str
    solution_url: str
    acquisition_status: str
    pdf_verified: bool
    answer_key_verified: bool
    audit_status: str
    priority: str = ""

    @property
    def has_direct_pdf_url(self) -> bool:
        return bool(self.pdf_url)

    @property
    def ready_for_verified_practice(self) -> bool:
        # Source records alone can never satisfy question-level verification.
        return False


@dataclass(frozen=True)
class PYQRegistrySummary:
    total_records: int
    direct_pdf_urls: int
    pdf_verified: int
    answer_keys_verified: int
    not_yet_acquired: int
    by_exam: dict[str, int]


class PYQSourceRegistry:
    """Load audited source rows without promoting acquisition status to PYQ data."""

    REQUIRED_COLUMNS = {"PYQ_ID", "Year", "Exam", "Paper", "Acquisition Status"}

    def __init__(self, records: Iterable[PYQSourceRecord]):
        self.records = tuple(records)
        ids = [record.pyq_id for record in self.records]
        if len(ids) != len(set(ids)):
            raise ValueError("PYQ source registry contains duplicate PYQ_ID values")

    @classmethod
    def load_csv(cls, path: Path | str) -> "PYQSourceRegistry":
        source = Path(path)
        with source.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or ())
            missing = cls.REQUIRED_COLUMNS - headers
            if missing:
                raise ValueError(
                    "PYQ source registry missing columns: "
                    + ", ".join(sorted(missing))
                )

            records = []
            for line_number, row in enumerate(reader, start=2):
                pyq_id = _first(row, "PYQ_ID")
                if not pyq_id:
                    raise ValueError(f"{source}:{line_number}: empty PYQ_ID")
                try:
                    year = int(_first(row, "Year"))
                except ValueError as exc:
                    raise ValueError(
                        f"{source}:{line_number}: invalid Year for {pyq_id}"
                    ) from exc
                if year < 1900 or year > 2100:
                    raise ValueError(
                        f"{source}:{line_number}: out-of-range Year for {pyq_id}"
                    )

                records.append(
                    PYQSourceRecord(
                        pyq_id=pyq_id,
                        year=year,
                        exam=_first(row, "Exam"),
                        paper=_first(row, "Paper"),
                        language=_first(row, "Language"),
                        source_name=_first(row, "Source"),
                        source_url=_first(row, "Official/Primary URL", "Primary Source URL"),
                        pdf_url=_first(row, "PDF URL"),
                        answer_key_url=_first(row, "Answer Key URL"),
                        solution_url=_first(row, "Solution URL"),
                        acquisition_status=_first(row, "Acquisition Status"),
                        pdf_verified=_is_yes(_first(row, "PDF Verified")),
                        answer_key_verified=_is_yes(_first(row, "Answer Key Verified")),
                        audit_status=_first(row, "Audit Status"),
                        priority=_first(row, "Priority"),
                    )
                )
        return cls(records)

    def summary(self) -> PYQRegistrySummary:
        by_exam: dict[str, int] = {}
        for record in self.records:
            by_exam[record.exam] = by_exam.get(record.exam, 0) + 1
        return PYQRegistrySummary(
            total_records=len(self.records),
            direct_pdf_urls=sum(record.has_direct_pdf_url for record in self.records),
            pdf_verified=sum(record.pdf_verified for record in self.records),
            answer_keys_verified=sum(record.answer_key_verified for record in self.records),
            not_yet_acquired=sum(
                record.acquisition_status.casefold() == "not yet acquired"
                for record in self.records
            ),
            by_exam=by_exam,
        )
