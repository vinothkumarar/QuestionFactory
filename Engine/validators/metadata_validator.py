"""
Question Factory OS
Metadata Validator

Validates metadata fields.
"""


class MetadataValidator:

    REQUIRED_METADATA = [

        "subject_name",
        "unit_name",
        "chapter_name",
        "subtopic_name"

    ]

    def validate(self, question: dict):

        errors = []

        for field in self.REQUIRED_METADATA:

            value = question.get(field)

            if value is None:
                errors.append(f"{field} is missing")

            elif isinstance(value, str) and value.strip() == "":
                errors.append(f"{field} is empty")

        return {
    "validator": "MetadataValidator",
    "passed": len(errors) == 0,
    "errors": errors
}
