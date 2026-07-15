"""
Question Factory OS
Question Object Factory

Creates a complete Question object
using the central schema.
"""

from core.schema_manager import SchemaManager


class QuestionObjectFactory:

    def create(self):

        question = {}

        for field in SchemaManager.get_schema():
            question[field] = None

        question.update(SchemaManager.get_defaults())

        return question
