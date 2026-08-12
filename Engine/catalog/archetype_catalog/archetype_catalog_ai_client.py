from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, cast

from dotenv import load_dotenv
from openai import OpenAI


class ArchetypeCatalogAIClient:
    """
    AI client for Archetype Catalog generation.
    """

    def __init__(self) -> None:

        load_dotenv(
            Path(__file__).parent.parent.parent
            / ".env"
        )

        api_key = (
            os.getenv("OPENAI_API_KEY")
        )

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found."
            )

        self._client = OpenAI(
            api_key=api_key,
            timeout=300.0,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = (
            self._client.responses.create(
                model="gpt-5",
                input=prompt,
            )
        )

        return response.output_text

    def generate_json(
        self,
        prompt: str,
    ) -> list[dict[str, Any]]:

        text = self.generate(
            prompt
        )

        try:

            data = json.loads(
                text
            )

            if not isinstance(
                data,
                list,
            ):
                raise ValueError(
                    "AI did not return a JSON list."
                )

            return cast(
                list[dict[str, Any]],
                data,
            )

        except json.JSONDecodeError as ex:

            raise ValueError(
                "AI did not return valid JSON."
            ) from ex