"""
Question Factory OS
Pipeline Engine
"""

from Engine.builders.question_builder import QuestionBuilder
from Engine.builders.question_merger import QuestionMerger

from Engine.core.validation_engine import ValidationEngine

from Engine.ai.prompt_builder import PromptBuilder
from Engine.ai.provider_factory import ProviderFactory
# NEW
from Engine.factory.ai.response_parser import ResponseParser


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

        print("\n========== AFTER QUESTION BUILDER ==========")
        print({
            "subject_id": question.get("subject_id"),
            "unit_id": question.get("unit_id"),
            "chapter_id": question.get("chapter_id"),
            "subtopic_id": question.get("subtopic_id"),
            "subject_name": question.get("subject_name"),
            "unit_name": question.get("unit_name"),
            "chapter_name": question.get("chapter_name"),
            "subtopic_name": question.get("subtopic_name"),
            "question_code": question.get("question_code"),
        })

        prompt = self.prompt_builder.build(question)

        response = self.provider.generate(prompt)

        ai_data = self.parser.parse(response)

        print("\n========== AI PARSED DATA ==========")
        print(ai_data)

        question = self.merger.merge(question, ai_data)

        print("\n========== AFTER MERGE ==========")
        print({
            "question_text": question.get("question_text"),
            "subject_id": question.get("subject_id"),
            "unit_id": question.get("unit_id"),
            "chapter_id": question.get("chapter_id"),
            "subtopic_id": question.get("subtopic_id"),
            "question_code": question.get("question_code"),
        })

        validation = self.validator.validate(question)

        return question, validation