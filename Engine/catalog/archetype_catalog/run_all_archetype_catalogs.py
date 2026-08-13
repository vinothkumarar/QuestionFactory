from __future__ import annotations

import json
from pathlib import Path

from Engine.catalog.archetype_catalog.archetype_catalog_ai_client import (
    ArchetypeCatalogAIClient,
)

from Engine.catalog.archetype_catalog.archetype_catalog_generator import (
    ArchetypeCatalogGenerator,
)

from Engine.catalog.archetype_catalog.archetype_catalog_csv_exporter import (
    ArchetypeCatalogCSVExporter,
)


def safe_name(text: str) -> str:
    return (
        text.replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
        .replace(":", "_")
    )


def main() -> None:

    qp_dir = (
        Path(__file__).parent.parent
        / "qp_catalog"
        / "catalogs_test"
    )

    qp_files = sorted(
        qp_dir.glob("*.json")
    )

    total = len(qp_files)

    output_dir = (
        Path(__file__).parent
        / "catalogs"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    generator = ArchetypeCatalogGenerator()

    client = ArchetypeCatalogAIClient()

    csv_exporter = (
        ArchetypeCatalogCSVExporter()
    )

    for index, qp_file in enumerate(
        qp_files,
        start=1,
    ):

        qps = json.loads(
            qp_file.read_text(
                encoding="utf-8"
            )
        )

        all_archetypes = []

        if not qps:
            continue

        file_base = qp_file.stem

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

        first_row = qps[0]

        print(
            f"[{index}/{total}] Generating: "
            f"{first_row['unit']} | "
            f"{first_row['chapter']} | "
            f"{first_row['subtopic']}"
        )

        for qp_row in qps:

            subject = qp_row["subject"]
            unit = qp_row["unit"]
            chapter = qp_row["chapter"]
            subtopic = qp_row["subtopic"]

            concept_id = qp_row["concept_id"]
            concept = qp_row["concept"]

            qp_id = qp_row["qp_id"]

            question_possibility = (
                qp_row["question_possibility"]
            )

            prompt = (
                generator.load_prompt(
                    subject=subject,
                    unit=unit,
                    chapter=chapter,
                    subtopic=subtopic,
                    concept_id=concept_id,
                    concept=concept,
                    qp_id=qp_id,
                    question_possibility=question_possibility,
                )
            )

            print(
                f"START {qp_id}"
            )

            result = (
                client.generate_json(
                    prompt
                )
            )

            print(
                f"DONE {qp_id}"
            )

            all_archetypes.extend(
                result
            )

        json_file.write_text(
            json.dumps(
                all_archetypes,
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
        "\nArchetype catalog generation complete."
    )


if __name__ == "__main__":
    main()