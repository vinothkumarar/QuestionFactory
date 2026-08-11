from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConceptCatalogGenerator:
    """
    Generates a Concept Catalog
    for a single subtopic.
    """

    def load_prompt(
        self,
        *,
        subject: str,
        unit: str,
        chapter: str,
        subtopic: str,
    ) -> str:

        prompt_file = (
            Path(__file__).parent
            / "prompts"
            / "concept_catalog_prompt.txt"
        )

        prompt = prompt_file.read_text(
            encoding="utf-8"
        )

        prompt += f"""

SUBTOPIC INFORMATION

Subject:
{subject}

Unit:
{unit}

Chapter:
{chapter}

Subtopic:
{subtopic}

"""

        return prompt

    def parse_response(
        self,
        response: str,
    ) -> list[dict[str, Any]]:
        """
        Parse AI response.
        """

        data = json.loads(response)

        if not isinstance(data, list):
            raise ValueError(
                "Concept catalog must be a JSON list."
            )

        return data