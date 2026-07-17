"""
Question Factory OS
Question Object Factory

Creates a complete Question object
using the central schema.
"""

from typing import Any

from Engine.core.schema_manager import SchemaManager


class QuestionObjectFactory:
    def create(self) -> dict[str, Any]:
        question: dict[str, Any] = {}

        for field in SchemaManager.get_schema():
            question[field] = None

        question.update(SchemaManager.get_defaults())

        return question
        