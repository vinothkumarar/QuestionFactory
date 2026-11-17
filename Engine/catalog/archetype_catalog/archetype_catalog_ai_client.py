from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from Engine.catalog.archetype_catalog.qp_disposition_contract import (
    validate_catalog_response,
)


class ArchetypeCatalogAIClient:
    """Generate and validate disposition-aware archetype catalogues."""

    REQUIRED_FIELDS = {
        "subject", "unit", "chapter", "subtopic", "concept_id",
        "concept", "qp_id", "question_possibility", "archetype_id",
        "archetype", "assessment_mechanism", "reasoning_path",
        "exam_fit", "difficulty_potential", "variation_capacity",
        "variation_dimensions",
    }
    VALID_VARIATION_CAPACITY = {"LIMITED", "MODERATE", "HIGH"}

    def __init__(self) -> None:
        load_dotenv(Path(__file__).parent.parent.parent / ".env")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found.")
        self._client = OpenAI(api_key=api_key, timeout=300.0)

    def generate(self, prompt: str) -> str:
        response = self._client.responses.create(
            model="gpt-5",
            input=prompt,
        )
        return response.output_text

    def generate_json(
        self,
        prompt: str,
        *,
        input_qps: list[dict[str, Any]],
    ) -> dict[str, list[dict[str, Any]]]:
        try:
            data = json.loads(self.generate(prompt))
        except json.JSONDecodeError as ex:
            raise ValueError("AI did not return valid JSON.") from ex

        validated = validate_catalog_response(
            response=data,
            input_qps=input_qps,
        )
        archetypes = validated["archetypes"]
        if archetypes:
            self._validate_records(archetypes)
        return validated

    def _validate_records(self, records: list[dict[str, Any]]) -> None:
        for index, record in enumerate(records, start=1):
            if not isinstance(record, dict):
                raise ValueError(f"Archetype record #{index} must be an object.")

            missing = self.REQUIRED_FIELDS - set(record)
            extra = set(record) - self.REQUIRED_FIELDS
            if missing or extra:
                details = []
                if missing:
                    details.append("missing fields: " + ", ".join(sorted(missing)))
                if extra:
                    details.append("unexpected fields: " + ", ".join(sorted(extra)))
                raise ValueError(
                    f"Archetype record #{index} schema mismatch: "
                    + "; ".join(details)
                )

            string_fields = {
                "subject", "unit", "chapter", "subtopic", "concept_id",
                "concept", "qp_id", "question_possibility", "archetype",
                "assessment_mechanism", "reasoning_path", "variation_capacity",
            }
            for field in string_fields:
                value = record[field]
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(
                        f"Archetype record #{index} has invalid '{field}'."
                    )

            if record["archetype_id"] != "":
                raise ValueError(
                    f"Archetype record #{index} must leave archetype_id empty; "
                    "the Factory assigns it."
                )

            for field, allowed in {
                "exam_fit": {"JEE_MAIN", "JEE_ADVANCED"},
                "difficulty_potential": {
                    "FOUNDATION", "MODERATE", "HARD", "ELITE",
                },
            }.items():
                value = record[field]
                if not isinstance(value, list) or not value or any(
                    not isinstance(item, str) or item not in allowed
                    for item in value
                ):
                    raise ValueError(
                        f"Archetype record #{index} has invalid '{field}'."
                    )

            dimensions = record["variation_dimensions"]
            if (
                not isinstance(dimensions, list)
                or not dimensions
                or any(
                    not isinstance(item, str) or not item.strip()
                    for item in dimensions
                )
            ):
                raise ValueError(
                    f"Archetype record #{index} has invalid variation_dimensions."
                )

            capacity = record["variation_capacity"]
            if capacity not in self.VALID_VARIATION_CAPACITY:
                raise ValueError(
                    f"Archetype record #{index} has invalid variation_capacity."
                )


__all__ = ["ArchetypeCatalogAIClient"]
