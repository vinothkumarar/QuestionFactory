from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class QPCatalogGenerator:
    """
    Generates a Question Possibility Catalog
    for a single Concept.
    """

    def load_prompt(
        self,
        *,
        subject: str,
        unit: str,
        chapter: str,
        subtopic: str,
        concept_id: str,
        concept: str,
    ) -> str:

        prompt_file = (
            Path(__file__).parent
            / "prompts"
            / "qp_catalog_prompt.txt"
        )

        prompt = prompt_file.read_text(
            encoding="utf-8"
        )

        prompt += f"""

CONTEXT INFORMATION

Subject:
{subject}

Unit:
{unit}

Chapter:
{chapter}

Subtopic:
{subtopic}

Concept ID:
{concept_id}

Concept:
{concept}

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
                "QP catalog must be a JSON list."
            )

        return data