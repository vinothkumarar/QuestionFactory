"""
Question Factory OS
Pipeline Engine
"""

from Engine.builders.question_builder import QuestionBuilder
from Engine.builders.question_merger import QuestionMerger

from Engine.core.validation_engine import ValidationEngine

from Engine.ai.prompt_builder import PromptBuilder
from Engine.ai.provider_factory import ProviderFactory
from Engine.ai.response_parser import ResponseParser


class PipelineEngine:
    def __init__(self) -> None:
        self.question_builder = QuestionBuilder()
        self.prompt_builder = PromptBuilder()
        self.provider = ProviderFactory.create()
        self.parser = ResponseParser()
        self.merger = QuestionMerger()
        self.validator = ValidationEngine()

    def generate(self, runtime, question_number):
        question = self.question_builder.build(runtime, question_number)

        prompt = self.prompt_builder.build(question)

        response = self.provider.generate(prompt)

        ai_data = self.parser.parse(response)

        question = self.merger.merge(question, ai_data)

        validation = self.validator.validate(question)

        return question, validation