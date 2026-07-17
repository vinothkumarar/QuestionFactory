"""
Question Factory OS
Question Builder

Builds a production-ready Question dictionary.
"""

from .question_object_factory import QuestionObjectFactory
from .metadata_enricher import MetadataEnricher
from .identity_enricher import IdentityEnricher


class QuestionBuilder:
    def __init__(self) -> None:
        self.object_factory = QuestionObjectFactory()
        self.metadata_enricher = MetadataEnricher()
        self.identity_enricher = IdentityEnricher()

    def build(self, runtime: dict, question_number: int):
        question = self.object_factory.create()

        question = self.metadata_enricher.apply(question, runtime)

        question = self.identity_enricher.apply(
            question,
            runtime,
            question_number,
        )

        return question