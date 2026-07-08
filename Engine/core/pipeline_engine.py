"""
Question Factory OS
Pipeline Engine

Runs the complete Question generation pipeline.
"""

from builders.question_builder import QuestionBuilder
from core.generation_engine import GenerationEngine
from ai.response_parser import ResponseParser
from core.validation_engine import ValidationEngine


class PipelineEngine:

    def __init__(self):

        self.builder = QuestionBuilder()
        self.generator = GenerationEngine()
        self.parser = ResponseParser()
        self.validator = ValidationEngine()

    def run(
        self,
        runtime: dict,
        question_number: int
    ):

        question = self.builder.build(
            runtime,
            question_number
        )

        response = self.generator.generate(question)

        question = self.parser.parse(
            response,
            question
        )

        report = self.validator.validate(question)

        return {
            "question": question,
            "validation": report
        }
        