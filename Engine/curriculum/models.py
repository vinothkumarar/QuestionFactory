"""
Question Factory OS v2.2
========================

Curriculum Models

Immutable curriculum domain models.

Rules
-----
- UUID is the primary identifier.
- Business codes remain separate.
- Models are immutable.
"""

from __future__ import annotations

from dataclasses import dataclass


# ============================================================
# Subject
# ============================================================

@dataclass(frozen=True, slots=True)
class SubjectModel:
    """
    Curriculum Subject.

    Example
    -------
    Mathematics
    Physics
    Chemistry
    Biology
    Aptitude
    """

    id: str
    code: str
    name: str
    folder_name: str
    display_order: int
    is_test_enabled: bool

    @property
    def uuid(self) -> str:
        return self.id


# ============================================================
# Unit
# ============================================================

@dataclass(frozen=True, slots=True)
class UnitModel:
    """
    Curriculum Unit.
    """

    id: str
    subject_id: str
    code: str
    name: str
    display_order: int
    is_test_enabled: bool

    @property
    def uuid(self) -> str:
        return self.id


# ============================================================
# Chapter
# ============================================================

@dataclass(frozen=True, slots=True)
class ChapterModel:
    """
    Curriculum Chapter.
    """

    id: str
    unit_id: str
    code: str
    name: str
    display_order: int
    is_test_enabled: bool

    @property
    def uuid(self) -> str:
        return self.id


# ============================================================
# Subtopic
# ============================================================

@dataclass(frozen=True, slots=True)
class SubtopicModel:
    """
    Curriculum Subtopic.
    """

    id: str
    chapter_id: str
    code: str
    name: str
    display_order: int
    is_test_enabled: bool

    @property
    def uuid(self) -> str:
        return self.id
        