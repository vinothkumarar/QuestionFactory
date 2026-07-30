"""
Question Factory OS v2.2
========================

Curriculum Loader

Loads the complete curriculum from CSV files.

Responsibilities
----------------
- Discover subjects
- Load subjects.csv
- Load units.csv
- Load chapters.csv
- Load subtopics.csv
- Validate relationships
- Produce immutable curriculum models

The loader performs NO indexing.
Indexing belongs to CurriculumRegistry.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from Engine.curriculum.models import (
    ChapterModel,
    SubjectModel,
    SubtopicModel,
    UnitModel,
)


# ============================================================
# Curriculum Data
# ============================================================


@dataclass(slots=True)
class CurriculumData:
    """
    Loaded curriculum returned by CurriculumLoader.
    """

    subjects: list[SubjectModel]
    units: list[UnitModel]
    chapters: list[ChapterModel]
    subtopics: list[SubtopicModel]


# ============================================================
# Curriculum Loader
# ============================================================


class CurriculumLoader:

    SUBJECTS_FILE = "subjects.csv"
    UNITS_FILE = "units.csv"
    CHAPTERS_FILE = "chapters.csv"
    SUBTOPICS_FILE = "subtopics.csv"

    def __init__(self, curriculum_root: Path):

        self._root = Path(curriculum_root)

        self._subjects: list[SubjectModel] = []
        self._units: list[UnitModel] = []
        self._chapters: list[ChapterModel] = []
        self._subtopics: list[SubtopicModel] = []

        self._subject_index: dict[str, SubjectModel] = {}
        self._folder_index: dict[str, SubjectModel] = {}
        self._unit_index: dict[str, UnitModel] = {}
        self._chapter_index: dict[str, ChapterModel] = {}

    # --------------------------------------------------------
    # Public
    # --------------------------------------------------------

    def load(self) -> CurriculumData:

        self._load_subjects()

        for subject in sorted(
            self._subjects,
            key=lambda x: x.display_order,
        ):
            folder = self._root / subject.folder_name

            if not folder.exists():
                raise FileNotFoundError(
                    f"Missing subject folder: {folder}"
                )

            self._load_units(folder, subject.id)

        self._load_chapters()

        self._load_subtopics()

        return CurriculumData(
            subjects=self._subjects,
            units=self._units,
            chapters=self._chapters,
            subtopics=self._subtopics,
        )
    # --------------------------------------------------------
    # Subjects
    # --------------------------------------------------------

    def _load_subjects(self) -> None:

        file_path = self._root / self.SUBJECTS_FILE

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        with file_path.open(
            "r",
            encoding="utf-8",
            newline="",
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:

                subject = SubjectModel(
                    id=row["id"].strip(),
                    code=row["code"].strip(),
                    name=row["name"].strip(),
                    folder_name=row["folder_name"].strip(),
                    display_order=int(row["display_order"]),
                    is_test_enabled=self._to_bool(
                        row["is_test_enabled"]
                    ),
                )

                if subject.id in self._subject_index:
                    raise ValueError(
                        f"Duplicate Subject UUID: {subject.id}"
                    )

                self._subjects.append(subject)
                self._subject_index[subject.id] = subject
                self._folder_index[subject.folder_name] = subject

    # --------------------------------------------------------
    # Units
    # --------------------------------------------------------

    def _load_units(
        self,
        folder: Path,
        subject_uuid: str,
    ) -> None:

        file_path = folder / self.UNITS_FILE

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        with file_path.open(
            "r",
            encoding="utf-8",
            newline="",
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:

                unit = UnitModel(
                    id=row["id"].strip(),
                    subject_id=row["subject_id"].strip(),
                    code=row["code"].strip(),
                    name=row["unit_name"].strip(),
                    display_order=int(row["display_order"]),
                    is_test_enabled=self._to_bool(
                        row["is_test_enabled"]
                    ),
                )

                if unit.subject_id != subject_uuid:
                    raise ValueError(
                        f"Unit '{unit.code}' belongs to "
                        f"subject '{unit.subject_id}' "
                        f"but is stored under "
                        f"'{folder.name}'."
                    )

                if unit.id in self._unit_index:
                    raise ValueError(
                        f"Duplicate Unit UUID: {unit.id}"
                    )

                self._units.append(unit)
                self._unit_index[unit.id] = unit
    # --------------------------------------------------------
    # Chapters
    # --------------------------------------------------------

    def _load_chapters(self) -> None:

        for subject in self._subjects:

            file_path = (
                self._root
                / subject.folder_name
                / self.CHAPTERS_FILE
            )

            if not file_path.exists():
                raise FileNotFoundError(file_path)

            with file_path.open(
                "r",
                encoding="utf-8",
                newline="",
            ) as csv_file:

                reader = csv.DictReader(csv_file)

                for row in reader:

                    chapter = ChapterModel(
                        id=row["id"].strip(),
                        unit_id=row["unit_id"].strip(),
                        code=row["code"].strip(),
                        name=row["chapter_name"].strip(),
                        display_order=int(row["display_order"]),
                        is_test_enabled=self._to_bool(
                            row["is_test_enabled"]
                        ),
                    )

                    if chapter.unit_id not in self._unit_index:
                        raise ValueError(
                            f"Unknown Unit UUID "
                            f"'{chapter.unit_id}' "
                            f"referenced by "
                            f"Chapter '{chapter.code}'."
                        )

                    if chapter.id in self._chapter_index:
                        raise ValueError(
                            f"Duplicate Chapter UUID: "
                            f"{chapter.id}"
                        )

                    self._chapters.append(chapter)
                    self._chapter_index[
                        chapter.id
                    ] = chapter

    # --------------------------------------------------------
    # Subtopics
    # --------------------------------------------------------

    def _load_subtopics(self) -> None:

        for subject in self._subjects:

            file_path = (
                self._root
                / subject.folder_name
                / self.SUBTOPICS_FILE
            )

            if not file_path.exists():
                raise FileNotFoundError(file_path)

            with file_path.open(
                "r",
                encoding="utf-8",
                newline="",
            ) as csv_file:

                reader = csv.DictReader(csv_file)

                for row in reader:

                    subtopic = SubtopicModel(
                        id=row["id"].strip(),
                        chapter_id=row["chapter_id"].strip(),
                        code=row["code"].strip(),
                        name=row["subtopic_name"].strip(),
                        display_order=int(row["display_order"]),
                        is_test_enabled=self._to_bool(
                            row["is_test_enabled"]
                        ),
                    )

                    if (
                        subtopic.chapter_id
                        not in self._chapter_index
                    ):
                        raise ValueError(
                            f"Unknown Chapter UUID "
                            f"'{subtopic.chapter_id}' "
                            f"referenced by "
                            f"Subtopic '{subtopic.code}'."
                        )

                    self._subtopics.append(
                        subtopic
                    )
    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------

    @staticmethod
    def _to_bool(value: str) -> bool:
        """
        Convert CSV boolean values into Python bool.

        Accepted values:

            true
            false
            yes
            no
            y
            n
            1
            0
        """

        normalized = value.strip().lower()

        if normalized in {
            "true",
            "1",
            "yes",
            "y",
        }:
            return True

        if normalized in {
            "false",
            "0",
            "no",
            "n",
        }:
            return False

        raise ValueError(
            f"Invalid boolean value: '{value}'"
        )

    # --------------------------------------------------------
    # Diagnostics
    # --------------------------------------------------------

    @property
    def subject_count(self) -> int:
        return len(self._subjects)

    @property
    def unit_count(self) -> int:
        return len(self._units)

    @property
    def chapter_count(self) -> int:
        return len(self._chapters)

    @property
    def subtopic_count(self) -> int:
        return len(self._subtopics)

    # --------------------------------------------------------
    # Iterators
    # --------------------------------------------------------

    @property
    def subjects(self) -> tuple[SubjectModel, ...]:
        return tuple(self._subjects)

    @property
    def units(self) -> tuple[UnitModel, ...]:
        return tuple(self._units)

    @property
    def chapters(self) -> tuple[ChapterModel, ...]:
        return tuple(self._chapters)

    @property
    def subtopics(self) -> tuple[SubtopicModel, ...]:
        return tuple(self._subtopics)
    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def validate(self) -> None:
        """
        Validate the loaded curriculum.

        This method should be called after load()
        during application startup.
        """

        if not self._subjects:
            raise ValueError("No subjects loaded.")

        if not self._units:
            raise ValueError("No units loaded.")

        if not self._chapters:
            raise ValueError("No chapters loaded.")

        if not self._subtopics:
            raise ValueError("No subtopics loaded.")

    # --------------------------------------------------------
    # Factory
    # --------------------------------------------------------

    @classmethod
    def from_directory(
        cls,
        curriculum_root: Path,
    ) -> CurriculumData:
        """
        Convenience factory method.

        Example
        -------
            data = CurriculumLoader.from_directory(path)
        """

        loader = cls(curriculum_root)

        data = loader.load()

        loader.validate()

        return data

    # --------------------------------------------------------
    # Representation
    # --------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "CurriculumLoader("
            f"subjects={self.subject_count}, "
            f"units={self.unit_count}, "
            f"chapters={self.chapter_count}, "
            f"subtopics={self.subtopic_count}"
            ")"
        )       