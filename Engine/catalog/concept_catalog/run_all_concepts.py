from __future__ import annotations

import csv
import json
from pathlib import Path

from Engine.catalog.concept_catalog.concept_catalog_ai_client import (
    ConceptCatalogAIClient,
)

from Engine.catalog.concept_catalog.concept_catalog_generator import (
    ConceptCatalogGenerator,
)

from Engine.catalog.concept_catalog.concept_catalog_csv_exporter import (
    ConceptCatalogCSVExporter,
)


def safe_name(text: str) -> str:
    return (
        text.replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
        .replace(":", "_")
    )


def main() -> None:

    syllabus_file = (
        Path(__file__).parents[2]
        / "qp_catalog"
        / "syllabus.csv"
    )

    output_dir = (
        Path(__file__).parent
        / "catalogs"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    generator = (
        ConceptCatalogGenerator()
    )

    client = (
        ConceptCatalogAIClient()
    )

    csv_exporter = (
        ConceptCatalogCSVExporter()
    )

    with syllabus_file.open(
        encoding="utf-8-sig"
    ) as fp:

        rows = list(
            csv.DictReader(fp)
        )

    total = len(rows)

    for index, row in enumerate(
        rows,
        start=1,
    ):

        subject = row["subject"]

        unit_code = row["unit_code"]
        unit = row["unit"]

        chapter_code = row["chapter_code"]
        chapter = row["chapter"]

        subtopic_code = row["subtopic_code"]
        subtopic = row["subtopic"]

        file_base = (
            f"{unit_code}_{chapter_code}_{subtopic_code}"
        )

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

        print(
            f"[{index}/{total}] "
            f"Generating: "
            f"{unit} | "
            f"{chapter} | "
            f"{subtopic}"
        )

        prompt = (
            generator.load_prompt(
                subject=subject,
                unit=unit,
                chapter=chapter,
                subtopic=subtopic,
            )
        )

        result = (
            client.generate_json(
                prompt
            )
        )

        json_file.write_text(
            json.dumps(
                result,
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
        "\nConcept generation complete."
    )


if __name__ == "__main__":
    main()