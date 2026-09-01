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
    csv_exporter = QPCatalogCSVExporter()

    for index, concept_file in enumerate(
        concept_files,
        start=1,
    ):

        concepts = json.loads(
            concept_file.read_text(
                encoding="utf-8"
            )
        )

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

        # -----------------------------------------------------
        # Load existing progress for this ST
        # -----------------------------------------------------

        all_qps: list[dict] = []

        if json_file.exists():

            try:
                existing_data = json.loads(
                    json_file.read_text(
                        encoding="utf-8"
                    )
                )

                if isinstance(
                    existing_data,
                    list,
                ):
                    all_qps = existing_data

            except json.JSONDecodeError:

                print(
                    f"WARNING: Could not read "
                    f"{json_file.name}. "
                    f"Starting with empty QP catalog."
                )

                all_qps = []

        # -----------------------------------------------------
        # Determine concepts already completed
        # -----------------------------------------------------

        completed_concept_ids = {
            str(row.get("concept_id", "")).strip()
            for row in all_qps
            if row.get("concept_id")
        }

        first_row = concepts[0]

        print()
        print(
            "=" * 80
        )

        print(
            f"[{index}/{total}] "
            f"{file_base}"
        )

        print(
            f"{first_row['unit']} | "
            f"{first_row['chapter']} | "
            f"{first_row['subtopic']}"
        )

        print(
            f"Existing QPs: {len(all_qps)}"
        )

        print(
            f"Completed concepts: "
            f"{len(completed_concept_ids)}"
        )

        print(
            "=" * 80
        )

        # -----------------------------------------------------
        # Process concepts one by one
        # -----------------------------------------------------

        for concept_row in concepts:

            subject = concept_row["subject"]
            unit = concept_row["unit"]
            chapter = concept_row["chapter"]
            subtopic = concept_row["subtopic"]

            concept_id = str(
                concept_row["concept_id"]
            ).strip()

            concept = concept_row["concept"]

            # -------------------------------------------------
            # Resume check
            # -------------------------------------------------

            if concept_id in completed_concept_ids:

                print(
                    f"SKIP {concept_id} | "
                    f"already persisted"
                )

                continue

            # -------------------------------------------------
            # Generate QPs
            # -------------------------------------------------

            print()
            print(
                f"START {concept_id} | "
                f"{concept}"
            )

            prompt = generator.load_prompt(
                subject=subject,
                unit=unit,
                chapter=chapter,
                subtopic=subtopic,
                concept_id=concept_id,
                concept=concept,
            )

            result = client.generate_json(
                prompt
            )

            # -------------------------------------------------
            # Validate basic response
            # -------------------------------------------------

            if not isinstance(
                result,
                list,
            ):

                raise ValueError(
                    f"QP generation for "
                    f"{concept_id} did not return "
                    f"a list."
                )

            # -------------------------------------------------
            # Add generated QPs
            # -------------------------------------------------

            all_qps.extend(result)

            completed_concept_ids.add(
                concept_id
            )

            print(
                f"DONE {concept_id} | "
                f"Generated QPs: {len(result)}"
            )

            # -------------------------------------------------
            # Persist immediately
            # -------------------------------------------------

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
                f"SAVED {file_base} | "
                f"Total QPs: {len(all_qps)}"
            )

            print(
                f"JSON: {json_file}"
            )

            print(
                f"CSV:  {csv_file}"
            )

        # -----------------------------------------------------
        # ST summary
        # -----------------------------------------------------

        print()
        print(
            f"COMPLETED ST: {file_base}"
        )

        print(
            f"Total QPs: {len(all_qps)}"
        )

        print(
            f"JSON: {json_file}"
        )

        print(
            f"CSV:  {csv_file}"
        )

    print()
    print(
        "QP catalog generation complete."
    )


if __name__ == "__main__":
    main()