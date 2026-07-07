"""
Question Factory OS
Question Builder

Builds a production-ready Question dictionary.
"""

from core.question_code_generator import QuestionCodeGenerator
from core.schema import QUESTION_DEFAULTS
from metadata.metadata_loader import MetadataLoader
from builders.question_object_factory import QuestionObjectFactory


class QuestionBuilder:

    def __init__(self):

        self.code_generator = QuestionCodeGenerator()
        self.metadata_loader = MetadataLoader()
        self.object_factory = QuestionObjectFactory()

    def build(
        self,
        runtime: dict,
        question_number: int
    ):

        metadata_key = (
            f"{runtime['current_project']}_"
            f"{runtime['current_chapter']}_"
            f"{runtime['current_subtopic']}"
        )

        metadata = self.metadata_loader.get_metadata(metadata_key)

        question = self.object_factory.create()

        question["question_code"] = self.code_generator.generate(
            runtime["current_project"],
            runtime["current_chapter"],
            runtime["current_subtopic"],
            runtime["current_set"],
            question_number
        )

        if metadata:
            question.update(metadata)

        return question
