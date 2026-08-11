from __future__ import annotations

import json
from pathlib import Path

from Engine.catalog.qp_catalog.qp_catalog_ai_client import (
    QPCatalogAIClient,
)

from Engine.catalog.qp_catalog.qp_catalog_generator import (
    QPCatalogGenerator,
)


def main() -> None:

    generator = QPCatalogGenerator()

    client = QPCatalogAIClient()

    prompt = generator.load_prompt(
        subject="Mathematics",
        unit="U1",
        chapter="CH1",
        subtopic="Number System",
        concept_id="C018",
        concept="Absolute Value",
    )

    print(
        "Generating QP Catalog..."
    )

    result = client.generate_json(
        prompt
    )

    output_file = (
        Path(__file__).parent
        / "qp_catalog.json"
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
        f"QP catalog saved: {output_file}"
    )


if __name__ == "__main__":
    main()