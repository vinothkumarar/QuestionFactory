"""
Question Factory OS v2.3
Curriculum Models

Immutable data models representing the complete academic curriculum.

Hierarchy:
    Curriculum
        └── Subject
              └── Unit
                    └── Chapter
                          └── Subtopic
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


# ---------------------------------------------------------------------
# Leaf Node
# ---------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class SubtopicModel:
    id: str
    chapter_id: str

    code: str
    name: str

    display_order: int
    enabled: bool


# ---------------------------------------------------------------------
# Chapter
# ---------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class ChapterModel:
    id: str
    unit_id: str

    code: str
    name: str

    display_order: int
    enabled: bool

    subtopics: Tuple[SubtopicModel, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------
# Unit
# ---------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class UnitModel:
    id: str
    subject_id: str

    code: str
    name: str

    display_order: int
    enabled: bool

    chapters: Tuple[ChapterModel, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------
# Subject
# ---------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class SubjectModel:
    id: str

    name: str

    enabled: bool

    units: Tuple[UnitModel, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------
# Root Model
# ---------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class CurriculumModel:
    subjects: Tuple[SubjectModel, ...] = field(default_factory=tuple)