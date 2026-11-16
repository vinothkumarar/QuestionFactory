"""Validated loader for reusable question-archetype recipes."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ArchetypeEntry:
    archetype_id: str
    qp_id: str
    subtopic_code: str
    question_possibility: str
    archetype_name: str
    construction_pattern: str
    target_skill: str
    suggested_format: str
    difficulty_band: str
    variation_dimensions: str
    distractor_strategy: str
    independent_verification_route: str
    scope_status: str
    notes: str = ""

    @property
    def blocked_for_generation(self) -> bool:
        return self.scope_status == "BLOCKED_SOURCE_TEXT"

    @property
    def available_for_internal_draft_design(self) -> bool:
        """True means a recipe may guide an internal draft, not exam approval."""
        return self.scope_status == "INTERNAL_CATALOGUE_ONLY"


class ArchetypeCatalogError(ValueError):
    """Raised when archetype records are incomplete or inconsistent."""


class ArchetypeCatalog:
    REQUIRED_COLUMNS = {
        "archetype_id",
        "qp_id",
        "subtopic_code",
        "question_possibility",
        "archetype_name",
        "construction_pattern",
        "target_skill",
        "suggested_format",
        "difficulty_band",
        "variation_dimensions",
        "distractor_strategy",
        "independent_verification_route",
        "scope_status",
        "notes",
    }
    ALLOWED_SCOPE_STATUSES = {
        "INTERNAL_CATALOGUE_ONLY",
        "BLOCKED_SOURCE_TEXT",
    }

    def __init__(self, entries: Iterable[ArchetypeEntry]) -> None:
        self.entries = tuple(entries)
        seen: set[str] = set()
        for entry in self.entries:
            if entry.archetype_id in seen:
                raise ArchetypeCatalogError(
                    f"Duplicate archetype_id: {entry.archetype_id}"
                )
            seen.add(entry.archetype_id)

            required_values = (
                entry.archetype_id,
                entry.qp_id,
                entry.subtopic_code,
                entry.question_possibility,
                entry.archetype_name,
                entry.construction_pattern,
                entry.target_skill,
                entry.suggested_format,
                entry.difficulty_band,
                entry.variation_dimensions,
                entry.distractor_strategy,
                entry.independent_verification_route,
            )
            if not all(value.strip() for value in required_values):
                raise ArchetypeCatalogError(
                    f"Archetype {entry.archetype_id} has blank required fields"
                )
            if entry.scope_status not in self.ALLOWED_SCOPE_STATUSES:
                raise ArchetypeCatalogError(
                    f"Unsupported scope_status for {entry.archetype_id}: "
                    f"{entry.scope_status}"
                )
            if not entry.archetype_id.startswith(
                f"{entry.subtopic_code}_"
            ):
                raise ArchetypeCatalogError(
                    f"Archetype ID does not match subtopic: {entry.archetype_id}"
                )
            if not entry.qp_id.startswith(f"{entry.subtopic_code}_QP"):
                raise ArchetypeCatalogError(
                    f"QPC ID does not match subtopic: {entry.qp_id}"
                )
            if entry.blocked_for_generation and not entry.notes.strip():
                raise ArchetypeCatalogError(
                    f"Blocked archetype requires an explanatory note: "
                    f"{entry.archetype_id}"
                )

    @classmethod
    def load(
        cls,
        archetype_path: Path | str,
        qpc_path: Path | str,
    ) -> "ArchetypeCatalog":
        """Load recipes and verify them against the authoritative QPC CSV."""
        archetypes = cls._read_csv(Path(archetype_path), cls.REQUIRED_COLUMNS)
        qpc_rows = cls._read_csv(
            Path(qpc_path),
            {"qp_id", "subtopic_code", "question_possibility"},
        )
        entries = [ArchetypeEntry(**row) for row in archetypes]
        catalog = cls(entries)
        catalog.validate_qpc_alignment(qpc_rows)
        return catalog

    @staticmethod
    def _read_csv(
        path: Path, required_columns: set[str]
    ) -> list[dict[str, str]]:
        if not path.is_file():
            raise FileNotFoundError(f"Archetype/QPC catalog not found: {path}")
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            missing = required_columns - set(reader.fieldnames or ())
            if missing:
                raise ArchetypeCatalogError(
                    f"{path}: missing columns: {', '.join(sorted(missing))}"
                )
            return [
                {key: (value or "").strip() for key, value in row.items() if key}
                for row in reader
            ]

    def validate_qpc_alignment(
        self, qpc_rows: Iterable[dict[str, str]]
    ) -> None:
        """Require exact QPC identity/description alignment and full coverage."""
        qpc_by_id = {
            row["qp_id"]: row
            for row in qpc_rows
            if row.get("qp_id") and row.get("subtopic_code")
        }
        subtopics = {entry.subtopic_code for entry in self.entries}
        expected = {
            row["qp_id"]: row
            for row in qpc_by_id.values()
            if row["subtopic_code"] in subtopics
        }
        actual = {entry.qp_id for entry in self.entries}

        missing = sorted(set(expected) - actual)
        unknown = sorted(actual - set(expected))
        if missing or unknown:
            details = []
            if missing:
                details.append("missing QPC IDs: " + ", ".join(missing))
            if unknown:
                details.append("unknown QPC IDs: " + ", ".join(unknown))
            raise ArchetypeCatalogError("; ".join(details))

        for entry in self.entries:
            source = expected[entry.qp_id]
            if source["subtopic_code"] != entry.subtopic_code:
                raise ArchetypeCatalogError(
                    f"Subtopic mismatch for QPC {entry.qp_id}"
                )
            if source["question_possibility"] != entry.question_possibility:
                raise ArchetypeCatalogError(
                    f"Question possibility text mismatch for QPC {entry.qp_id}"
                )

    def for_subtopic(self, subtopic_code: str) -> tuple[ArchetypeEntry, ...]:
        return tuple(
            entry for entry in self.entries
            if entry.subtopic_code == subtopic_code
        )

    def for_qp(self, qp_id: str) -> tuple[ArchetypeEntry, ...]:
        return tuple(entry for entry in self.entries if entry.qp_id == qp_id)

    def available_for_internal_draft_design(
        self, subtopic_code: str
    ) -> tuple[ArchetypeEntry, ...]:
        """Return non-blocked recipes for internal drafts only.

        This does not establish official exam-syllabus eligibility, answer
        verification, or production approval.
        """
        return tuple(
            entry for entry in self.for_subtopic(subtopic_code)
            if entry.available_for_internal_draft_design
        )
