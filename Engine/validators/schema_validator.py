"""
Question Factory OS
Schema Validator

Ensures every schema field exists.
"""

from core.schema_manager import SchemaManager


class SchemaValidator:

    def validate(self, question: dict):

        missing = []

        for field in SchemaManager.get_schema():

            if field not in question:
                missing.append(field)

        return {
    "validator": "SchemaValidator",
    "passed": len(missing) == 0,
    "errors": missing
}
