from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from Engine.catalog.archetype_catalog.archetype_catalog_ai_client import (
    ArchetypeCatalogAIClient,
)
from Engine.catalog.archetype_catalog.archetype_catalog_csv_exporter import (
    ArchetypeCatalogCSVExporter,
)
from Engine.catalog.archetype_catalog.batch_archetype_catalog_generator import (
    BatchArchetypeCatalogGenerator,
)
from Engine.catalog.archetype_catalog.qp_disposition_contract import (
    qp_key,
    validate_catalog_response,
)


BATCH_SIZE = 5


def load_existing_catalog(json_file: Path) -> dict[str, list[dict[str, Any]]]:
    if not json_file.exists():
        return {"qp_dispositions": [], "archetypes": []}
    data = json.loads(json_file.read_text(encoding="utf-8"))
    if isinstance(data, list):
        raise ValueError(
            f"Legacy flat-list catalogue detected at {json_file}. "
            "It has no explicit QP dispositions and cannot be resumed safely. "
            "Preserve it and migrate explicitly before running this pipeline."
        )
    if not isinstance(data, dict) or set(data) != {
        "qp_dispositions", "archetypes",
    }:
        raise ValueError(f"Invalid disposition-aware catalogue: {json_file}")
    if not isinstance(data["qp_dispositions"], list) or not isinstance(
        data["archetypes"], list
    ):
        raise ValueError(f"Malformed catalogue arrays: {json_file}")
    return data


def get_next_archetype_number(
    *,
    archetypes: list[dict[str, Any]],
    scope_id: str,
) -> int:
    pattern = re.compile(rf"^{re.escape(scope_id)}_AR(\d+)$")
    highest = 0
    for row in archetypes:
        value = row.get("archetype_id", "")
        if isinstance(value, str):
            match = pattern.match(value)
            if match:
                highest = max(highest, int(match.group(1)))
    return highest + 1


def assign_archetype_ids(
    *,
    archetypes: list[dict[str, Any]],
    scope_id: str,
    existing_archetypes: list[dict[str, Any]],
) -> None:
    next_number = get_next_archetype_number(
        archetypes=existing_archetypes,
        scope_id=scope_id,
    )
    existing_ids = {
        row.get("archetype_id") for row in existing_archetypes
    }
    for row in archetypes:
        if row.get("archetype_id") != "":
            raise ValueError("AI archetype IDs must be blank before factory assignment.")
        candidate = f"{scope_id}_AR{next_number:05d}"
        while candidate in existing_ids:
            next_number += 1
            candidate = f"{scope_id}_AR{next_number:05d}"
        row["archetype_id"] = candidate
        existing_ids.add(candidate)
        next_number += 1


def persist_catalog(
    *,
    json_file: Path,
    archetype_csv: Path,
    disposition_csv: Path,
    catalog: dict[str, list[dict[str, Any]]],
    source_qps: list[dict[str, Any]],
    exporter: ArchetypeCatalogCSVExporter,
) -> None:
    json_file.write_text(
        json.dumps(catalog, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )
    exporter.export(json_file=json_file, csv_file=archetype_csv)
    exporter.export_dispositions(
        json_file=json_file,
        csv_file=disposition_csv,
        source_qps=source_qps,
    )


def main() -> None:
    qp_dir = Path(__file__).parent.parent / "qp_catalog" / "catalogs"
    qp_files = sorted(qp_dir.glob("*.json"))
    output_dir = Path(__file__).parent / "catalogs"
    output_dir.mkdir(parents=True, exist_ok=True)

    generator = BatchArchetypeCatalogGenerator()
    client = ArchetypeCatalogAIClient()
    exporter = ArchetypeCatalogCSVExporter()

    for file_index, qp_file in enumerate(qp_files, start=1):
        qps = json.loads(qp_file.read_text(encoding="utf-8"))
        if not isinstance(qps, list) or not qps:
            print(f"[{file_index}/{len(qp_files)}] Skipping empty/invalid source: {qp_file.name}")
            continue

        scope_id = qp_file.stem
        json_file = output_dir / f"{scope_id}.json"
        archetype_csv = output_dir / f"{scope_id}.csv"
        disposition_csv = output_dir / f"{scope_id}_qp_dispositions.csv"
        complete_file = output_dir / f"{scope_id}.complete"

        if complete_file.exists():
            print(f"[{file_index}/{len(qp_files)}] Already complete: {scope_id}")
            continue

        catalog = load_existing_catalog(json_file)
        # Validate all persisted dispositions and archetypes against the
        # original source before resuming. Empty archetype arrays are valid.
        if catalog["qp_dispositions"] or catalog["archetypes"]:
            persisted_keys = {
                (item.get("concept_id"), item.get("qp_id"))
                for item in catalog["qp_dispositions"]
            }
            validate_catalog_response(
                response=catalog,
                input_qps=[
                    row for row in qps if qp_key(row) in persisted_keys
                ],
            )

        completed_keys = {
            (item.get("concept_id"), item.get("qp_id"))
            for item in catalog["qp_dispositions"]
        }
        remaining = [row for row in qps if qp_key(row) not in completed_keys]

        print(
            f"\n[{file_index}/{len(qp_files)}] {scope_id}: "
            f"{len(qps)} source QPs, {len(completed_keys)} dispositioned, "
            f"{len(remaining)} remaining."
        )

        for offset in range(0, len(remaining), BATCH_SIZE):
            batch = remaining[offset:offset + BATCH_SIZE]
            print(f"  Processing QPs: {[row['qp_id'] for row in batch]}")

            prompt = generator.load_prompt(qps=batch)
            result = client.generate_json(prompt, input_qps=batch)

            new_archetypes = result["archetypes"]
            assign_archetype_ids(
                archetypes=new_archetypes,
                scope_id=scope_id,
                existing_archetypes=catalog["archetypes"],
            )

            catalog["qp_dispositions"].extend(result["qp_dispositions"])
            catalog["archetypes"].extend(new_archetypes)

            # Validate the accumulated state against the complete source set
            # represented so far, including valid zero-archetype QPs.
            processed_keys = {
                (item["concept_id"], item["qp_id"])
                for item in catalog["qp_dispositions"]
            }
            processed_qps = [
                row for row in qps if qp_key(row) in processed_keys
            ]
            validate_catalog_response(
                response=catalog,
                input_qps=processed_qps,
            )
            persist_catalog(
                json_file=json_file,
                archetype_csv=archetype_csv,
                disposition_csv=disposition_csv,
                catalog=catalog,
                source_qps=qps,
                exporter=exporter,
            )
            print(
                f"  Saved {len(result['qp_dispositions'])} dispositions; "
                f"{len(new_archetypes)} archetypes."
            )

        final_keys = {
            (item["concept_id"], item["qp_id"])
            for item in catalog["qp_dispositions"]
        }
        source_keys = {qp_key(row) for row in qps}
        if final_keys != source_keys:
            missing = sorted(source_keys - final_keys)
            raise RuntimeError(
                f"Cannot mark {scope_id} complete; missing dispositions: {missing}"
            )

        validate_catalog_response(response=catalog, input_qps=qps)
        persist_catalog(
            json_file=json_file,
            archetype_csv=archetype_csv,
            disposition_csv=disposition_csv,
            catalog=catalog,
            source_qps=qps,
            exporter=exporter,
        )
        complete_file.touch()
        print(
            f"  COMPLETE: {scope_id} | QPs: {len(qps)} | "
            f"Archetypes: {len(catalog['archetypes'])}"
        )

    print("\nDisposition-aware archetype catalogue generation complete.")


if __name__ == "__main__":
    main()
