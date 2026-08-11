from __future__ import annotations

import json
from pathlib import Path

from Engine.qp_catalog.qp_catalog_csv_exporter import (
    QPCatalogCSVExporter,
)

from Engine.qp_catalog.qp_catalog_generator import (
    QPCatalogGenerator,
)

from Engine.qp_catalog.qp_catalog_ai_client import (
    QPCatalogAIClient,
)


def main() -> None:

    generator = QPCatalogGenerator()

    client = QPCatalogAIClient()

    prompt = generator.load_prompt(
        subject="Mathematics",
        unit="U1",
        chapter="CH1",
        subtopic="Number System",
    )

    print(
        "Generating QP Catalog..."
    )

    result = client.generate_json(
        prompt
    )

    output_file = (
        Path(__file__).parent
        / "catalog.json"
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
        f"Catalog saved: {output_file}"
    )

    csv_exporter = QPCatalogCSVExporter()

    csv_exporter.export(
        json_file=catalog_file,
        csv_file=(
            Path(__file__).parent
            / "catalog.csv"
        ),
    )

    print(
        "CSV saved:",
        Path(__file__).parent
        / "catalog.csv"
    )

if __name__ == "__main__":
    main()