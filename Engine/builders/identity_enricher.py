"""
Question Factory OS
Identity Enricher

Applies identity fields to a Question object.
"""

from core.question_code_generator import QuestionCodeGenerator


class IdentityEnricher:

    def __init__(self):
        self.code_generator = QuestionCodeGenerator()

    def apply(
        self,
        question: dict,
        runtime: dict,
        question_number: int
    ):

        question["question_code"] = self.code_generator.generate(
            runtime["current_project"],
            runtime["current_chapter"],
            runtime["current_subtopic"],
            runtime["current_set"],
            question_number
        )

        return question
        