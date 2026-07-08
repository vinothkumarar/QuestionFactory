"""
Question Factory OS
Response Parser

Converts AI responses into Question objects.
"""


class ResponseParser:

    def parse(self, response: str, question: dict) -> dict:
        """
        Parses the AI response and updates the question object.

        For now, store the raw response.
        """

        question["raw_ai_response"] = response

        return question
        