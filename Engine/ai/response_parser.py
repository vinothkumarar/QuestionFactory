"""
Question Factory OS
Response Parser
"""

import json
from typing import Any, cast


class ResponseParser:
    def parse(self, response: str) -> dict[str, Any]:
        try:
            return cast(dict[str, Any], json.loads(response))

        except json.JSONDecodeError as ex:
            raise RuntimeError(
                f"Invalid JSON received from AI.\n\n{ex}"
            ) from ex