"""
Question Factory OS
Response Parser
"""

import json


class ResponseParser:

    def parse(self, response: str) -> dict:

        try:

            return json.loads(response)

        except json.JSONDecodeError as ex:

            raise RuntimeError(f"Invalid JSON received from AI.\n\n{ex}")
