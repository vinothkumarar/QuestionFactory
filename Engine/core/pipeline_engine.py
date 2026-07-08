"""
Question Factory OS
Pipeline Engine
"""

from builders.question_builder import QuestionBuilder
from builders.question_merger import QuestionMerger

from ai.prompt_builder import PromptBuilder
from ai.provider_factory import ProviderFactory
from ai.response_parser import ResponseParser

from core.validation_engine import ValidationEngine


class PipelineEngine:

    def __init__(self):

        self.question_builder = QuestionBuilder()

        self.prompt_builder = PromptBuilder()

        self.provider = ProviderFactory.create()

        self.parser = ResponseParser()

        self.merger = QuestionMerger()

        self.validator = ValidationEngine()

    def generate(
        self,
        runtime,
        question_number
    ):

        question = self.question_builder.build(
            runtime,
            question_number
        )

        prompt = self.prompt_builder.build(
            question
        )

        response = self.provider.generate(
            prompt
        )

        ai_data = self.parser.parse(
            response
        )

        question = self.merger.merge(
            question,
            ai_data
        )

        validation = self.validator.validate(
            question
        )

        return question, validation
        