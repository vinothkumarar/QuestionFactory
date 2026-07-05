"""
Question Factory OS
CSV Writer

Purpose:
Create CSV files for generated question batches.
"""

import csv
from pathlib import Path


CSV_HEADER = [
    "id",
    "created_at",
    "subject_id",
    "chapter_id",
    "difficulty",
    "question_type",
    "question_text",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "answer",
    "explanation",
    "created_by",
    "more_explanation",
    "subject_name",
    "chapter_name",
    "correct_option",
    "unit_id",
    "subtopic_id",
    "set_no",
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
    "updated_at",
    "question_image_url",
    "solution_image_url",
    "question_code",
    "subtopic_name",
    "unit_name"
]


class CSVWriter:

    def create_batch_file(self, folder: Path, filename: str):

        file_path = folder / filename

        if file_path.exists():
            return file_path

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(CSV_HEADER)

        return file_path
        