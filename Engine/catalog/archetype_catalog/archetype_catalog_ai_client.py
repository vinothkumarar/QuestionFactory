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

    The client validates the complete Archetype catalogue
    contract before allowing the result to be persisted.
    """

    REQUIRED_FIELDS = {
        "qp_id",
        "question_possibility",
        "archetype_id",
        "archetype",
        "assessment_mechanism",
        "reasoning_path",
        "exam_fit",
        "difficulty_potential",
        "variation_capacity",
        "variation_dimensions",
    }

    VALID_VARIATION_CAPACITY = {
        "LIMITED",
        "MODERATE",
        "HIGH",
    }

    def __init__(self) -> None:

        load_dotenv(
            Path(__file__).parent.parent.parent
            / ".env"
        )

        api_key = os.getenv(
            "OPENAI_API_KEY"
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

        except json.JSONDecodeError as ex:

            raise ValueError(
                "AI did not return valid JSON."
            ) from ex

        if not isinstance(
            data,
            list,
        ):
            raise ValueError(
                "AI did not return a JSON list."
            )

        records = cast(
            list[dict[str, Any]],
            data,
        )

        self._validate_records(
            records
        )

        return records

    # ---------------------------------------------------------
    # Schema Validation
    # ---------------------------------------------------------

    def _validate_records(
        self,
        records: list[dict[str, Any]],
    ) -> None:
        """
        Validate every Archetype record.

        Missing or malformed academic metadata causes
        generation to fail immediately.
        """

        if not records:
            raise ValueError(
                "Archetype catalogue is empty."
            )

        for index, record in enumerate(
            records,
            start=1,
        ):

            if not isinstance(
                record,
                dict,
            ):
                raise ValueError(
                    f"Archetype record #{index} "
                    f"must be a JSON object."
                )

            missing_fields = (
                self.REQUIRED_FIELDS
                - set(record.keys())
            )

            if missing_fields:

                missing = ", ".join(
                    sorted(missing_fields)
                )

                raise ValueError(
                    f"Archetype record #{index} "
                    f"({record.get('archetype_id', 'UNKNOWN')}) "
                    f"is missing required fields: "
                    f"{missing}"
                )

            # -------------------------------------------------
            # String fields
            # -------------------------------------------------

            string_fields = {
                "qp_id",
                "question_possibility",
                "archetype",
                "archetype_id",
                "assessment_mechanism",
                "reasoning_path",
                "variation_capacity",
            }

            for field_name in string_fields:

                value = record[field_name]

                if not isinstance(
                    value,
                    str,
                ) or not value.strip():

                    raise ValueError(
                        f"Archetype record #{index} "
                        f"({record['archetype_id']}) "
                        f"has invalid '{field_name}'."
                    )

            # -------------------------------------------------
            # Factory-owned ID must be blank in AI output
            # -------------------------------------------------

            archetype_id = record.get("archetype_id")

            if archetype_id != "":
                raise ValueError(
                    f"Archetype record #{index} must leave "
                    "archetype_id empty; the Factory assigns it."
                )

            # -------------------------------------------------
            # List fields
            # -------------------------------------------------

            list_fields = {
                "exam_fit",
                "difficulty_potential",
                "variation_dimensions",
            }

            for field_name in list_fields:

                value = record[field_name]

                if not isinstance(
                    value,
                    list,
                ):

                    raise ValueError(
                        f"Archetype record #{index} "
                        f"({record['archetype_id']}) "
                        f"field '{field_name}' "
                        f"must be a list."
                    )

            # -------------------------------------------------
            # Variation capacity
            # -------------------------------------------------

            capacity = (
                record["variation_capacity"]
                .strip()
                .upper()
            )

            if capacity not in (
                self.VALID_VARIATION_CAPACITY
            ):

                raise ValueError(
                    f"Archetype record #{index} "
                    f"({record['archetype_id']}) "
                    f"has invalid variation_capacity: "
                    f"{record['variation_capacity']!r}. "
                    f"Expected one of: "
                    f"LIMITED, MODERATE, HIGH."
                )

            # -------------------------------------------------
            # Variation dimensions
            # -------------------------------------------------

            dimensions = (
                record["variation_dimensions"]
            )

            if not dimensions:

                raise ValueError(
                    f"Archetype record #{index} "
                    f"({record['archetype_id']}) "
                    f"has no variation_dimensions."
                )

            if not all(
                isinstance(
                    dimension,
                    str,
                )
                and dimension.strip()
                for dimension in dimensions
            ):

                raise ValueError(
                    f"Archetype record #{index} "
                    f"({record['archetype_id']}) "
                    f"contains invalid variation_dimensions."
                )


__all__ = [
    "ArchetypeCatalogAIClient",
]