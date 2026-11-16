"""Load and validate the repository's existing curriculum CSV hierarchy."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


SUPPORTED_SUBJECTS = {"Mathematics", "Physics", "Chemistry", "Biology"}


@dataclass(frozen=True)
class CurriculumSnapshot:
    subjects: List[dict]
    units: List[dict]
    chapters: List[dict]
    subtopics: List[dict]

    def find_subtopic(self, code: str) -> dict:
        for row in self.subtopics:
            if row["code"] == code:
                return row
        raise KeyError(f"Unknown subtopic code: {code}")


class CurriculumLoader:
    """Read existing CSVs without changing IDs or requiring optional columns."""

    def __init__(self, curriculum_root: Path | str):
        self.root = Path(curriculum_root)

    @staticmethod
    def _read(path: Path, required: Iterable[str]) -> List[dict]:
        if not path.is_file():
            raise FileNotFoundError(f"Curriculum file not found: {path}")
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or [])
            missing = set(required) - headers
            if missing:
                raise ValueError(
                    f"{path}: missing required columns: {', '.join(sorted(missing))}"
                )
            return [
                {key: (value or "").strip() for key, value in row.items() if key}
                for row in reader
            ]

    @staticmethod
    def _unique(rows: List[dict], label: str) -> None:
        seen = set()
        for row in rows:
            record_id = row.get("id", "")
            if not record_id:
                raise ValueError(f"{label}: record with empty id")
            if record_id in seen:
                raise ValueError(f"{label}: duplicate id {record_id}")
            seen.add(record_id)

    def load(self) -> CurriculumSnapshot:
        subjects = self._read(
            self.root / "subjects.csv",
            ("id", "code", "name", "folder_name", "display_order", "is_test_enabled"),
        )
        subjects = [row for row in subjects if row["name"] in SUPPORTED_SUBJECTS]
        if not subjects:
            raise ValueError("No supported subjects found in curriculum/subjects.csv")

        units: List[dict] = []
        chapters: List[dict] = []
        subtopics: List[dict] = []

        for subject in subjects:
            folder = self.root / subject["folder_name"]
            subject_units = self._read(
                folder / "units.csv",
                ("id", "subject_id", "code", "unit_name", "display_order", "is_test_enabled"),
            )
            if any(row["subject_id"] != subject["id"] for row in subject_units):
                raise ValueError(f"Unit subject_id mismatch in {folder / 'units.csv'}")
            subject_chapters = self._read(
                folder / "chapters.csv",
                ("id", "unit_id", "code", "chapter_name", "display_order", "is_test_enabled"),
            )
            subject_subtopics = self._read(
                folder / "subtopics.csv",
                ("id", "chapter_id", "code", "subtopic_name", "display_order", "is_test_enabled"),
            )
            units.extend(subject_units)
            chapters.extend(subject_chapters)
            subtopics.extend(subject_subtopics)

        self._unique(subjects, "subjects")
        self._unique(units, "units")
        self._unique(chapters, "chapters")
        self._unique(subtopics, "subtopics")

        unit_ids = {row["id"] for row in units}
        chapter_ids = {row["id"] for row in chapters}
        for row in chapters:
            if row["unit_id"] not in unit_ids:
                raise ValueError(f"Chapter {row['code']} references unknown unit_id")
        for row in subtopics:
            if row["chapter_id"] not in chapter_ids:
                raise ValueError(f"Subtopic {row['code']} references unknown chapter_id")

        return CurriculumSnapshot(subjects, units, chapters, subtopics)
