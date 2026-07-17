"""
Question Factory OS
Identity Enricher

Applies identity fields to a Question object.
"""

from typing import Any

from Engine.core.question_code_generator import QuestionCodeGenerator


class IdentityEnricher:
    def __init__(self) -> None:
        self.code_generator = QuestionCodeGenerator()

    def apply(
        self,
        question: dict[str, Any],
        runtime: dict[str, Any],
        question_number: int,
    ) -> dict[str, Any]:
        # --------------------------------------------------
        # Runtime Identity
        # --------------------------------------------------

        question["project_code"] = runtime["current_project"]
        question["chapter_code"] = runtime["current_chapter"]
        question["subtopic_code"] = runtime["current_subtopic"]
        question["set_no"] = runtime["current_set"]
        question["question_no"] = question_number

        # Batch support (default for now)
        question["batch_no"] = runtime.get("current_batch", 1)

        # --------------------------------------------------
        # Question Code
        # --------------------------------------------------

        question["question_code"] = self.code_generator.generate(
            runtime["current_project"],
            runtime["current_chapter"],
            runtime["current_subtopic"],
            runtime["current_set"],
            question_number,
        )

        return question
        