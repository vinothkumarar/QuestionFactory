from __future__ import annotations

import json
from pathlib import Path

from Engine.catalog.qp_catalog.qp_catalog_ai_client import (
    QPCatalogAIClient,
)

from Engine.catalog.qp_catalog.qp_catalog_generator import (
    QPCatalogGenerator,
)

from Engine.catalog.qp_catalog.qp_catalog_csv_exporter import (
    QPCatalogCSVExporter,
)


def safe_name(text: str) -> str:
    return (
        text.replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
        .replace(":", "_")
    )


def main() -> None:

    concept_dir = (
        Path(__file__).parent.parent
        / "concept_catalog"
        / "catalogs"
    )

    concept_files = sorted(
        concept_dir.glob("*.json")
    )
    
    total = len(concept_files)

    output_dir = (
        Path(__file__).parent
        / "catalogs"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    generator = QPCatalogGenerator()
    client = QPCatalogAIClient()
    csv_exporter = (
        QPCatalogCSVExporter()
    )

        

    for index, concept_file in enumerate(
        concept_files,
        start=1,
    ):
        concepts = json.loads(
            concept_file.read_text(
                encoding="utf-8"
            )
        )
        all_qps = []

        if not concepts:
            continue

        file_base = concept_file.stem

        json_file = (
            output_dir
            / f"{file_base}.json"
        )

        csv_file = (
            output_dir
            / f"{file_base}.csv"
        )

        if json_file.exists():

            print(
                f"[{index}/{total}] "
                f"Skipping: {file_base}"
            )

            continue

        first_row = concepts[0]

        print(
            f"[{index}/{total}] Generating: "
            f"{first_row['unit']} | "
            f"{first_row['chapter']} | "
            f"{first_row['subtopic']}"
        )

        for concept_row in concepts:

            subject = concept_row["subject"]
            unit = concept_row["unit"]
            chapter = concept_row["chapter"]
            subtopic = concept_row["subtopic"]

            concept_id = concept_row["concept_id"]
            concept = concept_row["concept"]

            prompt = generator.load_prompt(
                subject=subject,
                unit=unit,
                chapter=chapter,
                subtopic=subtopic,
                concept_id=concept_id,
                concept=concept,
            )

            print(
                f"START {concept_id} | {concept}"
            )

            result = client.generate_json(
                prompt
            )

            print(
                f"DONE {concept_id}"
            )

            all_qps.extend(result)

        

        json_file.write_text(
            json.dumps(
                all_qps,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        csv_exporter.export(
            json_file=json_file,
            csv_file=csv_file,
        )

        print(
            f"Created: "
            f"{csv_file.name}"
        )

    print(
        "\nQP catalog generation complete."
    )


if __name__ == "__main__":
    main()