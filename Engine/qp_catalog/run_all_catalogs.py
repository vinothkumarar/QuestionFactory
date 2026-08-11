from __future__ import annotations

import csv
import json
from pathlib import Path

from Engine.qp_catalog.qp_catalog_ai_client import (
    QPCatalogAIClient,
)

from Engine.qp_catalog.qp_catalog_generator import (
    QPCatalogGenerator,
)

from Engine.qp_catalog.qp_catalog_csv_exporter import (
    QPCatalogCSVExporter,
)


def safe_filename(text: str) -> str:
    return (
        text.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )


def main() -> None:

    base_dir = Path(__file__).parent

    syllabus_file = (
        base_dir
        / "syllabus.csv"
    )

    catalogs_dir = (
        base_dir
        / "catalogs"
    )

    catalogs_dir.mkdir(
        exist_ok=True
    )

    generator = QPCatalogGenerator()

    client = QPCatalogAIClient()

    exporter = QPCatalogCSVExporter()

    with open(
        syllabus_file,
        newline="",
        encoding="utf-8-sig",
    ) as fp:

        reader = csv.DictReader(fp)

        for row in reader:

            subject = row["subject"]
            unit = row["unit"]
            chapter = row["chapter"]
            subtopic = row["subtopic"]

            print(
                f"Generating: "
                f"{unit} | {chapter} | {subtopic}"
            )

            prompt = generator.load_prompt(
                subject=subject,
                unit=unit,
                chapter=chapter,
                subtopic=subtopic,
            )

            result = client.generate_json(
                prompt
            )

            file_prefix = (
                f"{unit}_"
                f"{chapter}_"
                f"{safe_filename(subtopic)}"
            )

            json_file = (
                catalogs_dir
                / f"{file_prefix}.json"
            )

            csv_file = (
                catalogs_dir
                / f"{file_prefix}.csv"
            )

            json_file.write_text(
                json.dumps(
                    result,
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            exporter.export(
                json_file=json_file,
                csv_file=csv_file,
            )

            print(
                f"Created: {csv_file.name}"
            )

    print()
    print(
        "All catalogs generated."
    )


if __name__ == "__main__":
    main()