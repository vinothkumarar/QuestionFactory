from __future__ import annotations

import json
from pathlib import Path

from Engine.catalog.concept_catalog.concept_catalog_ai_client import (
    ConceptCatalogAIClient,
)

from Engine.catalog.concept_catalog.concept_catalog_generator import (
    ConceptCatalogGenerator,
)


def main() -> None:

    generator = ConceptCatalogGenerator()

    client = ConceptCatalogAIClient()

    prompt = generator.load_prompt(
        subject="Mathematics",
        unit="U1",
        chapter="CH1",
        subtopic="Number System",
    )

    print(
        "Generating Concept Catalog..."
    )

    result = client.generate_json(
        prompt
    )

    output_file = (
        Path(__file__).parent
        / "concepts.json"
    )

    output_file.write_text(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        f"Concept catalog saved: {output_file}"
    )


if __name__ == "__main__":
    main()