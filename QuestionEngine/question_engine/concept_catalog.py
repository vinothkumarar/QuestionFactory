"""Validated concept registry with an explicit approval gate.

Provisional concept rows are visible for review but are never supplied to
production generation until an authorised curriculum review marks them APPROVED.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
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
        """Return only explicitly approved concepts; provisional rows are excluded."""
        return tuple(
            entry for entry in self.for_subtopic(subtopic_code)
            if entry.approved_for_generation
        )
