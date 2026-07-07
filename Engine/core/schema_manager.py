"""
Question Factory OS
Schema Manager

Provides access to the Question schema.
"""

from core.schema import (
    QUESTION_SCHEMA,
    QUESTION_DEFAULTS,
    QUESTION_FIELD_GROUPS
)


class SchemaManager:

    @staticmethod
    def get_schema():
        return QUESTION_SCHEMA

    @staticmethod
    def get_defaults():
        return QUESTION_DEFAULTS

    @staticmethod
    def get_field_groups():
        return QUESTION_FIELD_GROUPS

    @staticmethod
    def get_identity_fields():
        return QUESTION_FIELD_GROUPS["identity"]

    @staticmethod
    def get_runtime_fields():
        return QUESTION_FIELD_GROUPS["runtime"]

    @staticmethod
    def get_content_fields():
        return QUESTION_FIELD_GROUPS["content"]

    @staticmethod
    def get_exam_fields():
        return QUESTION_FIELD_GROUPS["exam"]

    @staticmethod
    def get_workflow_fields():
        return QUESTION_FIELD_GROUPS["workflow"]

    @staticmethod
    def get_media_fields():
        return QUESTION_FIELD_GROUPS["media"]
