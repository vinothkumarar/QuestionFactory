"""Validated concept registry with an explicit, auditable approval gate.

Provisional concepts are visible for review but are never supplied to production
generation. Approved/rejected decisions require reviewer, timestamp, source and
rationale metadata so a status edit cannot silently become an unaudited release.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ConceptEntry:
    concept_id: str
    subtopic_code: str
    concept_name: str
    learning_outcome: str
    review_status: str
    notes: str = ""
    reviewer_id: str = ""
    reviewed_at: str = ""
    review_source: str = ""
    approval_rationale: str = ""

    @property
    def approved_for_generation(self) -> bool:
        return self.review_status == "APPROVED"


class ConceptCatalogError(ValueError):
    """Raised when a concept catalog is malformed or internally inconsistent."""


class ConceptCatalog:
    REQUIRED_COLUMNS = {
        "concept_id",
        "subtopic_code",
        "concept_name",
        "learning_outcome",
        "review_status",
        "notes",
        "reviewer_id",
        "reviewed_at",
        "review_source",
        "approval_rationale",
    }
    ALLOWED_STATUSES = {"PROVISIONAL_REVIEW_REQUIRED", "APPROVED", "REJECTED"}

    def __init__(self, entries: Iterable[ConceptEntry]):
        self.entries = tuple(entries)
        seen: set[str] = set()
        for entry in self.entries:
            if not all((
                entry.concept_id.strip(),
                entry.subtopic_code.strip(),
                entry.concept_name.strip(),
                entry.learning_outcome.strip(),
            )):
                raise ConceptCatalogError("Concept entries require IDs, names and outcomes")
            if entry.review_status not in self.ALLOWED_STATUSES:
                raise ConceptCatalogError(
                    f"Unsupported review status for {entry.concept_id}: {entry.review_status}"
                )
            if entry.concept_id in seen:
                raise ConceptCatalogError(f"Duplicate concept_id: {entry.concept_id}")
            seen.add(entry.concept_id)

            if entry.review_status != "PROVISIONAL_REVIEW_REQUIRED":
                audit_fields = (
                    entry.reviewer_id,
                    entry.reviewed_at,
                    entry.review_source,
                    entry.approval_rationale,
                )
                if not all(value.strip() for value in audit_fields):
                    raise ConceptCatalogError(
                        f"{entry.review_status} concept {entry.concept_id} "
                        "requires reviewer_id, reviewed_at, review_source and approval_rationale"
                    )
                try:
                    datetime.fromisoformat(entry.reviewed_at.replace("Z", "+00:00"))
                except ValueError as exc:
                    raise ConceptCatalogError(
                        f"Invalid ISO-8601 reviewed_at for {entry.concept_id}"
                    ) from exc

    @classmethod
    def load(cls, path: Path | str) -> "ConceptCatalog":
        source = Path(path)
        if not source.is_file():
            raise FileNotFoundError(f"Concept catalog not found: {source}")
        with source.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or ())
            missing = cls.REQUIRED_COLUMNS - headers
            if missing:
                raise ConceptCatalogError(
                    f"Missing concept catalog columns: {', '.join(sorted(missing))}"
                )
            entries = [
                ConceptEntry(
                    concept_id=(row.get("concept_id") or "").strip(),
                    subtopic_code=(row.get("subtopic_code") or "").strip(),
                    concept_name=(row.get("concept_name") or "").strip(),
                    learning_outcome=(row.get("learning_outcome") or "").strip(),
                    review_status=(row.get("review_status") or "").strip().upper(),
                    notes=(row.get("notes") or "").strip(),
                    reviewer_id=(row.get("reviewer_id") or "").strip(),
                    reviewed_at=(row.get("reviewed_at") or "").strip(),
                    review_source=(row.get("review_source") or "").strip(),
                    approval_rationale=(row.get("approval_rationale") or "").strip(),
                )
                for row in reader
            ]
        return cls(entries)

    def for_subtopic(self, subtopic_code: str) -> tuple[ConceptEntry, ...]:
        return tuple(
            entry for entry in self.entries
            if entry.subtopic_code == subtopic_code
        )

    def approved_for_generation(
        self, subtopic_code: str
    ) -> tuple[ConceptEntry, ...]:
        """Return only explicitly approved and fully audited concepts."""
        return tuple(
            entry for entry in self.for_subtopic(subtopic_code)
            if entry.approved_for_generation
        )
