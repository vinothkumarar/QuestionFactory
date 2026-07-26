"""
Question Factory OS
Question Schema

Milestone : M7
Sprint    : S1
Release   : R1
"""

QUESTION_COLUMNS = [
    # -------------------------------------------------
    # Identity
    # -------------------------------------------------
    "question_code",
    "subject_id",
    "unit_id",
    "chapter_id",
    "subtopic_id",

    # -------------------------------------------------
    # Question
    # -------------------------------------------------
    "difficulty",
    "question_type",
    "answer_type",
    "question_text",

    "option_a",
    "option_b",
    "option_c",
    "option_d",

    "correct_option",
    "answer",

    # -------------------------------------------------
    # Learning
    # -------------------------------------------------
    "explanation",
    "more_explanation",
    "concept_tested",
    "question_archetype",

    # -------------------------------------------------
    # Classification
    # -------------------------------------------------
    "exam_level",
    "source_type",
    "tags",

    # -------------------------------------------------
    # Runtime
    # -------------------------------------------------
    "estimated_time_sec",
    "marks",
    "negative_marks",
    "language",
    "status",
    "version",

    # -------------------------------------------------
    # Factory
    # -------------------------------------------------
    "set_no",
]


SYSTEM_COLUMNS = ["id", "created_at", "updated_at", "created_by"]


EXPORT_COLUMNS = QUESTION_COLUMNS
