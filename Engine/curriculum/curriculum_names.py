"""
Question Factory OS v3.0
Curriculum Name Registry

Phase 1:
    Lightweight curriculum lookup.

Phase 2:
    This module will become the backing store for CurriculumRepository.
"""

from typing import Dict, Tuple


# ============================================================
# SUBJECTS
# ============================================================

SUBJECT_NAMES: Dict[str, str] = {
    "MATH": "Mathematics",
    "PHYS": "Physics",
    "CHEM": "Chemistry",
}


# ============================================================
# SETS
# ============================================================

SET_NAMES: Dict[str, str] = {
    "S1": "Foundation",
    "S2": "Easy+",
    "S3": "Medium",
    "S4": "Hard",
    "S5": "Elite",
}


# ============================================================
# MATHEMATICS UNITS
# ============================================================

UNIT_NAMES: Dict[str, str] = {

    "U1": "Number System",

    "U2": "Algebra",

    "U3": "Coordinate Geometry",

    "U4": "Geometry",

    "U5": "Mensuration",

    "U6": "Statistics",

    "U7": "Probability",

    "U8": "Trigonometry",

    "U9": "Functions",

    "U10": "Limits, Continuity and Differentiability",

    "U11": "Integral Calculus",

}


# ============================================================
# CHAPTERS
#
# Key:
#     (UnitCode, ChapterCode)
# ============================================================

CHAPTER_NAMES: Dict[Tuple[str, str], str] = {

    # Example

    ("U1", "CH1"): "Integers",

    ("U1", "CH2"): "Fractions",

    ("U2", "CH1"): "Quadratic Equations",

}


# ============================================================
# SUBTOPICS
#
# Key:
#     (UnitCode, ChapterCode, SubtopicCode)
# ============================================================

SUBTOPIC_NAMES: Dict[Tuple[str, str, str], str] = {

    # Example

    ("U2", "CH1", "ST1"): "Nature of Roots",

    ("U2", "CH1", "ST2"): "Discriminant",

}


# ============================================================
# Helper Functions
# ============================================================

def get_subject_name(subject_code: str) -> str:
    return SUBJECT_NAMES.get(subject_code, subject_code)


def get_unit_name(unit_code: str) -> str:
    return UNIT_NAMES.get(unit_code, unit_code)


def get_chapter_name(unit_code: str, chapter_code: str) -> str:
    return CHAPTER_NAMES.get((unit_code, chapter_code), chapter_code)


def get_subtopic_name(
    unit_code: str,
    chapter_code: str,
    subtopic_code: str,
) -> str:
    return SUBTOPIC_NAMES.get(
        (unit_code, chapter_code, subtopic_code),
        subtopic_code,
    )


def get_set_name(set_code: str) -> str:
    return SET_NAMES.get(set_code, set_code)