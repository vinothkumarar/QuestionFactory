from __future__ import annotations

import json
from pathlib import Path

from Engine.catalog.archetype_catalog.archetype_catalog_ai_client import (
    ArchetypeCatalogAIClient,
)
from Engine.catalog.archetype_catalog.batch_archetype_catalog_generator import (
    BatchArchetypeCatalogGenerator,
)


def main() -> None:
    qps = [
        {
            "subject": "Chemistry",
            "unit": "Chemical Bonding and Molecular Structure",
            "chapter": "Chemical Bonding",
            "subtopic": "Ionic Bond",
            "concept_id": "C001",
            "concept": (
                "Nature of Ionic Bond "
                "(electron transfer and electrostatic attraction)"
            ),
            "qp_id": "QP001",
            "question_possibility": (
                "Identify ionic bonding as formation via complete electron "
                "transfer followed by electrostatic attraction between ions"
            ),
        }
    ]

    prompt = BatchArchetypeCatalogGenerator().load_prompt(qps=qps)
    result = ArchetypeCatalogAIClient().generate_json(
        prompt,
        input_qps=qps,
    )

    output_file = Path(__file__).parent / "test_archetype_output.json"
    output_file.write_text(
        json.dumps(result, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    print("SUCCESS: disposition-aware archetype schema validation passed.")
    print(f"Saved: {output_file}")
    print(f"QP dispositions: {len(result['qp_dispositions'])}")
    print(f"Archetypes: {len(result['archetypes'])}")
    for item in result["qp_dispositions"]:
        print(
            f"{item['qp_id']} | {item['disposition']} | "
            f"{item['rationale']}"
        )
    for record in result["archetypes"]:
        print(
            f"{record['qp_id']} | {record['variation_capacity']} | "
            f"{record['variation_dimensions']}"
        )


if __name__ == "__main__":
    main()
