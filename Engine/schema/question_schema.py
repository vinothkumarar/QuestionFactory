"""
Question Factory OS
Question Schema

Milestone : M7
Sprint    : S1
Release   : R1
"""

QUESTION_COLUMNS = [
    # -------------------------------------------------
    # Foreign Keys
    # -------------------------------------------------
    "subject_id",
    "chapter_id",
    "unit_id",
    "subtopic_id",
    # -------------------------------------------------
    # AI Generated Content
    # -------------------------------------------------
    "difficulty",
    "question_type",
    "question_text",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "answer",
    "explanation",
    "more_explanation",
    "correct_option",
    "difficulty_score",
    "answer_type",
    "concept_tested",
    "question_archetype",
    "exam_level",
    "source_type",
    "tags",
    "estimated_time_sec",
    "marks",
    "negative_marks",
    "bloom_level",
    "chapter_weightage",
    "exam_relevance",
    "pyq_inspired",
    "pyq_exam",
    "pyq_year",
    "pyq_topic",
    "status",
    "version",
    "is_verified",
    "reviewed_by",
    "review_date",
    "image_required",
    "has_diagram",
    "latex_required",
    "language",
    "question_image_url",
    "solution_image_url",
    # -------------------------------------------------
    # Factory Metadata
    # -------------------------------------------------
    "question_code",
    "subject_name",
    "unit_name",
    "chapter_name",
    "subtopic_name",
    "set_no",
]


SYSTEM_COLUMNS = ["id", "created_at", "updated_at", "created_by"]


EXPORT_COLUMNS = QUESTION_COLUMNS
