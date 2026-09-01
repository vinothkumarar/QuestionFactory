from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from Engine.catalog.archetype_catalog.archetype_catalog_ai_client import (
    ArchetypeCatalogAIClient,
)

from Engine.catalog.archetype_catalog.batch_archetype_catalog_generator import (
    BatchArchetypeCatalogGenerator,
)

from Engine.catalog.archetype_catalog.archetype_catalog_csv_exporter import (
    ArchetypeCatalogCSVExporter,
)


BATCH_SIZE = 5


def load_existing_archetypes(
    json_file: Path,
) -> list[dict[str, Any]]:
    """
    Load previously generated Archetype records.

    An existing JSON file represents a partially
    completed catalog when the .complete marker
    does not exist.
    """

    if not json_file.exists():
        return []

    data = json.loads(
        json_file.read_text(
            encoding="utf-8",
        )
    )

    if not isinstance(data, list):
        raise ValueError(
            f"Archetype catalog must contain a JSON list: "
            f"{json_file}"
        )

    return data


def get_completed_qp_keys(
    archetypes: list[dict[str, Any]],
) -> set[tuple[str, str]]:
    """
    Return unique QP identities already represented
    in the generated Archetype Catalog.

    QP identity is:

        concept_id + qp_id

    qp_id alone is NOT globally unique.
    """

    completed: set[tuple[str, str]] = set()

    for row in archetypes:

        concept_id = row.get(
            "concept_id",
            "",
        )

        qp_id = row.get(
            "qp_id",
            "",
        )

        if (
            isinstance(concept_id, str)
            and concept_id
            and isinstance(qp_id, str)
            and qp_id
        ):
            completed.add(
                (
                    concept_id,
                    qp_id,
                )
            )

    return completed


def get_next_archetype_number(
    *,
    archetypes: list[dict[str, Any]],
    scope_id: str,
) -> int:
    """
    Determine the next permanent Archetype number.

    Existing Archetype IDs are preserved.

    Example:

        U1_CH1_ST1_AR00001
        U1_CH1_ST1_AR00002

    returns:

        3
    """

    pattern = re.compile(
        rf"^{re.escape(scope_id)}_AR(\d+)$"
    )

    highest = 0

    for row in archetypes:

        archetype_id = row.get(
            "archetype_id",
            "",
        )

        if not isinstance(
            archetype_id,
            str,
        ):
            continue

        match = pattern.match(
            archetype_id
        )

        if match is None:
            continue

        number = int(
            match.group(1)
        )

        highest = max(
            highest,
            number,
        )

    return highest + 1


def assign_archetype_ids(
    *,
    archetypes: list[dict[str, Any]],
    scope_id: str,
    existing_archetypes: list[dict[str, Any]],
) -> None:
    """
    Assign permanent Archetype IDs to newly
    generated records.

    Existing Archetype IDs are preserved.
    """

    next_number = (
        get_next_archetype_number(
            archetypes=existing_archetypes,
            scope_id=scope_id,
        )
    )

    for row in archetypes:

        existing_id = row.get(
            "archetype_id",
            "",
        )

        if (
            isinstance(existing_id, str)
            and existing_id.strip()
        ):
            continue

        row["archetype_id"] = (
            f"{scope_id}_AR"
            f"{next_number:05d}"
        )

        next_number += 1
    """
    Assign permanent Archetype IDs to newly
    generated records.

    The AI does not control Archetype identity.

    IDs are assigned by the factory.

    Existing non-empty IDs are preserved.
    """

    next_number = (
        get_next_archetype_number(
            archetypes=archetypes,
            scope_id=scope_id,
        )
    )

    for row in archetypes:

        existing_id = row.get(
            "archetype_id",
            "",
        )

        if (
            isinstance(existing_id, str)
            and existing_id.strip()
        ):
            continue

        row["archetype_id"] = (
            f"{scope_id}_AR"
            f"{next_number:05d}"
        )

        next_number += 1


def validate_archetype_records(
    *,
    records: list[dict[str, Any]],
    batch_qp_ids: list[str],
) -> None:
    """
    Validate the structural integrity of one
    generated Archetype batch.
    """

    required_fields = [
        "subject",
        "unit",
        "chapter",
        "subtopic",
        "concept_id",
        "concept",
        "qp_id",
        "question_possibility",
        "archetype",
    ]

    for index, row in enumerate(
        records,
        start=1,
    ):

        if not isinstance(
            row,
            dict,
        ):
            raise RuntimeError(
                "Archetype batch contains "
                f"non-object record at index {index}."
            )

        for field in required_fields:

            value = row.get(
                field,
                "",
            )

            if not isinstance(
                value,
                str,
            ) or not value.strip():

                raise RuntimeError(
                    "Archetype record is missing "
                    f"required field '{field}' "
                    f"at index {index}."
                )

    returned_qp_ids = {
        row["qp_id"]
        for row in records
    }

    missing_qp_ids = [
        qp_id
        for qp_id in batch_qp_ids
        if qp_id not in returned_qp_ids
    ]

    if missing_qp_ids:

        raise RuntimeError(
            "Archetype batch did not return "
            "records for every supplied QP. "
            f"Missing QPs: {missing_qp_ids}"
        )


def write_catalog(
    *,
    json_file: Path,
    csv_file: Path,
    archetypes: list[dict[str, Any]],
    csv_exporter: ArchetypeCatalogCSVExporter,
) -> None:
    """
    Persist the current catalog state.

    JSON is written first.

    CSV is then regenerated from the
    current JSON state.
    """

    json_file.write_text(
        json.dumps(
            archetypes,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    csv_exporter.export(
        json_file=json_file,
        csv_file=csv_file,
    )


def main() -> None:

    qp_dir = (
        Path(__file__).parent.parent
        / "qp_catalog"
        / "catalogs"
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

    generator = (
        BatchArchetypeCatalogGenerator()
    )

    client = (
        ArchetypeCatalogAIClient()
    )

    csv_exporter = (
        ArchetypeCatalogCSVExporter()
    )

    for index, qp_file in enumerate(
        qp_files,
        start=1,
    ):

        qps = json.loads(
            qp_file.read_text(
                encoding="utf-8",
            )
        )

        if not qps:

            print(
                f"[{index}/{total}] "
                f"Skipping empty catalog: "
                f"{qp_file.name}"
            )

            continue

        # -------------------------------------------------
        # Permanent catalog scope
        # -------------------------------------------------

        scope_id = qp_file.stem

        json_file = (
            output_dir
            / f"{scope_id}.json"
        )

        csv_file = (
            output_dir
            / f"{scope_id}.csv"
        )

        complete_file = (
            output_dir
            / f"{scope_id}.complete"
        )

        # -------------------------------------------------
        # Completed catalog
        # -------------------------------------------------

        if complete_file.exists():

            print(
                f"[{index}/{total}] "
                f"Skipping completed: "
                f"{scope_id}"
            )

            continue

        # -------------------------------------------------
        # Load existing partial catalog
        # -------------------------------------------------

        all_archetypes = (
            load_existing_archetypes(
                json_file,
            )
        )

        completed_qp_keys = (
            get_completed_qp_keys(
                all_archetypes,
            )
        )

        # -------------------------------------------------
        # Existing ID information
        # -------------------------------------------------

        next_archetype_number = (
            get_next_archetype_number(
                archetypes=all_archetypes,
                scope_id=scope_id,
            )
        )

        # -------------------------------------------------
        # Basic source information
        # -------------------------------------------------

        first_row = qps[0]

        print()

        print(
            f"[{index}/{total}] "
            f"Generating: "
            f"{first_row['unit']} | "
            f"{first_row['chapter']} | "
            f"{first_row['subtopic']}"
        )

        print(
            f"  Catalog scope: {scope_id}"
        )

        print(
            f"  Source QPs: {len(qps)}"
        )

        print(
            "  Next Archetype ID: "
            f"{scope_id}_AR"
            f"{next_archetype_number:05d}"
        )

        if completed_qp_keys:

            print(
                f"  Resume mode: "
                f"{len(completed_qp_keys)} QPs "
                f"already completed."
            )

        # -------------------------------------------------
        # Process only QPs not already completed
        # -------------------------------------------------

        remaining_qps = [
            qp
            for qp in qps
            if (
                qp.get(
                    "concept_id",
                    "",
                ),
                qp.get(
                    "qp_id",
                    "",
                ),
            ) not in completed_qp_keys
        ]

        if not remaining_qps:

            print(
                "  All QPs already generated."
            )

            complete_file.touch()

            print(
                f"  Created completion marker: "
                f"{complete_file.name}"
            )

            continue

        # -------------------------------------------------
        # Batch processing
        # -------------------------------------------------

        total_remaining = len(
            remaining_qps
        )

        batch_count = (
            total_remaining
            + BATCH_SIZE
            - 1
        ) // BATCH_SIZE

        for batch_index in range(
            batch_count
        ):

            start = (
                batch_index
                * BATCH_SIZE
            )

            end = min(
                start + BATCH_SIZE,
                total_remaining,
            )

            batch = remaining_qps[
                start:end
            ]

            batch_qp_ids = [
                qp["qp_id"]
                for qp in batch
            ]

            print()

            print(
                f"  Batch "
                f"{batch_index + 1}/"
                f"{batch_count}"
            )

            print(
                f"  QPs: "
                f"{batch_qp_ids}"
            )

            # -------------------------------------------------
            # Build batch prompt
            # -------------------------------------------------

            prompt = (
                generator.load_prompt(
                    qps=batch,
                )
            )

            print(
                "  START API"
            )

            # -------------------------------------------------
            # API call
            # -------------------------------------------------

            result = (
                client.generate_json(
                    prompt,
                )
            )

            print(
                "  DONE API"
            )

            print(
                f"  Archetypes returned: "
                f"{len(result)}"
            )

            # -------------------------------------------------
            # Validate AI output
            # -------------------------------------------------

            validate_archetype_records(
                records=result,
                batch_qp_ids=batch_qp_ids,
            )

            # -------------------------------------------------
            # Assign permanent factory IDs
            # -------------------------------------------------

            assign_archetype_ids(
                archetypes=result,
                scope_id=scope_id,
                existing_archetypes=all_archetypes,
            )

            # -------------------------------------------------
            # Validate assigned IDs
            # -------------------------------------------------

            existing_ids = {
                row.get(
                    "archetype_id",
                    "",
                )
                for row in all_archetypes
            }

            new_ids = [
                row["archetype_id"]
                for row in result
            ]

            duplicate_ids = [
                archetype_id
                for archetype_id in new_ids
                if archetype_id in existing_ids
            ]

            if duplicate_ids:

                raise RuntimeError(
                    "Duplicate permanent "
                    "Archetype IDs detected: "
                    f"{duplicate_ids}"
                )

            # -------------------------------------------------
            # Append successful batch
            # -------------------------------------------------

            all_archetypes.extend(
                result
            )

            # -------------------------------------------------
            # Immediate persistence
            # -------------------------------------------------

            write_catalog(
                json_file=json_file,
                csv_file=csv_file,
                archetypes=all_archetypes,
                csv_exporter=csv_exporter,
            )

            print(
                f"  JSON updated: "
                f"{json_file.name}"
            )

            print(
                f"  CSV updated : "
                f"{csv_file.name}"
            )

            print(
                f"  Archetypes saved this batch: "
                f"{len(result)}"
            )

            print(
                f"  Total archetypes saved: "
                f"{len(all_archetypes)}"
            )

        # -------------------------------------------------
        # Entire subtopic completed
        # -------------------------------------------------

        complete_file.touch()

        print()

        print(
            f"  COMPLETE: "
            f"{scope_id}"
        )

        print(
            f"  Total QPs processed: "
            f"{len(qps)}"
        )

        print(
            f"  Total archetypes: "
            f"{len(all_archetypes)}"
        )

        print(
            f"  Completion marker: "
            f"{complete_file.name}"
        )

    print()

    print(
        "Archetype catalog generation complete."
    )


if __name__ == "__main__":
    main()