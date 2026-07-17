"""
Question Factory OS
Schema Validator

Ensures every schema field exists.
"""

from typing import Any

from Engine.core.schema_manager import SchemaManager


class SchemaValidator:
    def validate(self, question: dict[str, Any]) -> dict[str, Any]:
        missing: list[str] = []

        for field in SchemaManager.get_schema():
            if field not in question:
                missing.append(field)

        return {
            "validator": "SchemaValidator",
            "passed": len(missing) == 0,
            "errors": missing,
        }
        