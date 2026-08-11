from __future__ import annotations
from dotenv import load_dotenv
from pathlib import Path
import json
import os

from openai import OpenAI


class QPCatalogAIClient:
    """
    Standalone AI client used only for
    QP Catalog generation.

    Completely independent from the
    Question Factory AI subsystem.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-5",
    ) -> None:
        load_dotenv(
            Path(__file__).parent.parent / ".env",
            override=True,
        )

        self._api_key = (
            api_key
            or os.getenv("OPENAI_API_KEY")
        )

        if not self._api_key:
            raise ValueError(
                "OPENAI_API_KEY not found."
            )

        self._client = OpenAI(
            api_key=self._api_key
        )

        self._model = model

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate catalog JSON.
        """

        response = (
            self._client.responses.create(
                model=self._model,
                input=prompt,
            )
        )

        return response.output_text.strip()

    def generate_json(
        self,
        prompt: str,
    ) -> list[dict]:
        """
        Generate and parse JSON.
        """

        text = self.generate(
            prompt
        )

        return json.loads(text)