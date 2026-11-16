"""CSV/XLSX source-registry loader for historical PYQ acquisition tracking.

This tracks paper/source availability only. A registry row is not a question,
a downloaded PDF, or a verified PYQ.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


def _first(row: Mapping[str, object], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
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
    def _from_rows(
        cls, rows: Iterable[Mapping[str, object]], source_label: str
    ) -> "PYQSourceRegistry":
        records = []
        for line_number, row in enumerate(rows, start=2):
            pyq_id = _first(row, "PYQ_ID")
            if not pyq_id:
                raise ValueError(f"{source_label}:{line_number}: empty PYQ_ID")
            try:
                year = int(_first(row, "Year"))
            except ValueError as exc:
                raise ValueError(
                    f"{source_label}:{line_number}: invalid Year for {pyq_id}"
                ) from exc
            if year < 1900 or year > 2100:
                raise ValueError(
                    f"{source_label}:{line_number}: out-of-range Year for {pyq_id}"
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
            return cls._from_rows(reader, str(source))

    @classmethod
    def load_xlsx(
        cls, path: Path | str, sheet_name: str = "Audited Tracker"
    ) -> "PYQSourceRegistry":
        """Load the audited Excel registry; openpyxl is a declared dependency."""
        try:
            from openpyxl import load_workbook
        except ImportError as exc:
            raise RuntimeError(
                "XLSX registry import requires openpyxl; install QuestionEngine/requirements.txt"
            ) from exc

        source = Path(path)
        workbook = load_workbook(source, read_only=True, data_only=True)
        try:
            if sheet_name not in workbook.sheetnames:
                raise ValueError(
                    f"{source}: worksheet {sheet_name!r} not found; "
                    f"available: {', '.join(workbook.sheetnames)}"
                )
            worksheet = workbook[sheet_name]
            values = worksheet.iter_rows(values_only=True)
            header_values = next(values, None)
            if not header_values:
                raise ValueError(f"{source}:{sheet_name}: worksheet is empty")
            headers = [str(value).strip() if value is not None else "" for value in header_values]
            missing = cls.REQUIRED_COLUMNS - set(headers)
            if missing:
                raise ValueError(
                    "PYQ source registry missing columns: "
                    + ", ".join(sorted(missing))
                )
            rows = (
                {header: value for header, value in zip(headers, values_row) if header}
                for values_row in values
            )
            return cls._from_rows(rows, f"{source}:{sheet_name}")
        finally:
            workbook.close()

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
