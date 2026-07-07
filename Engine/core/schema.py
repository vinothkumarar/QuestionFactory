"""
Question Factory OS
Schema Definition

Single source of truth for the Question schema.
"""

QUESTION_SCHEMA = [

    "id",
    "question_code",

    "created_at",
    "updated_at",
    "created_by",

    "subject_id",
    "unit_id",
    "chapter_id",
    "subtopic_id",

    "subject_name",
    "unit_name",
    "chapter_name",
    "subtopic_name",

    "difficulty",
    "difficulty_score",

    "question_type",
    "answer_type",

    "question_text",

    "option_a",
    "option_b",
    "option_c",
    "option_d",

    "correct_option",
    "answer",

    "explanation",
    "more_explanation",

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
    "solution_image_url"
]
