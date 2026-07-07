"""
Question Factory OS
Identity Validator

Validates question identity.
"""


class IdentityValidator:

    def validate(self, question: dict):

        errors = []

        code = question.get("question_code")

        if code is None:
            errors.append("question_code is missing")

        elif not isinstance(code, str):
            errors.append("question_code is invalid")

        elif code.strip() == "":
            errors.append("question_code is empty")

        elif "_Q" not in code:
            errors.append("question_code format is invalid")

        return {
    "validator": "IdentityValidator",
    "passed": len(errors) == 0,
    "errors": errors
}
        