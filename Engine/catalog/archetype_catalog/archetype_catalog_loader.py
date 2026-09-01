"""
Question Factory OS v2.2

Archetype Catalog Loader

Loads Archetype Catalog JSON files and returns
their contents as Python dictionaries.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ArchetypeCatalogLoader:
    """
    Loads Archetype Catalog files.
    """

    CATALOG_DIRECTORY = (
        Path(__file__).parent / "catalogs"
    )

    def load(
        self,
        catalog_name: str,
    ) -> list[dict[str, Any]]:
        """
        Load a catalog JSON file.

        Example:
            TEST1
            TEST2
            U1_CH1_ST4
        """

        file_path = (
            self.CATALOG_DIRECTORY
            / f"{catalog_name}.json"
        )

        if not file_path.exists():

            raise FileNotFoundError(
                f"Archetype catalog not found: "
                f"{file_path}"
            )

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            payload = json.load(
                file,
            )

        if isinstance(
            payload,
            list,
        ):
            return payload

        if isinstance(
            payload,
            dict,
        ):

            archetypes = payload.get(
                "archetypes",
                [],
            )

            if not isinstance(
                archetypes,
                list,
            ):
                raise ValueError(
                    "Invalid archetype catalog format."
                )

            return archetypes

        raise ValueError(
            "Invalid archetype catalog format."
        )

    def available_catalogs(
        self,
    ) -> list[str]:
        """
        Return all catalog names.
        """

        if not self.CATALOG_DIRECTORY.exists():
            return []

        return sorted(
            path.stem
            for path in self.CATALOG_DIRECTORY.glob(
                "*.json"
            )
        )