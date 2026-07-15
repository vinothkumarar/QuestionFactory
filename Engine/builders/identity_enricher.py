"""
Question Factory OS
Identity Enricher

Applies identity fields to a Question object.
"""

from core.question_code_generator import QuestionCodeGenerator


class IdentityEnricher:

    def __init__(self):

        self.code_generator = QuestionCodeGenerator()

    def apply(self, question: dict, runtime: dict, question_number: int):

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
