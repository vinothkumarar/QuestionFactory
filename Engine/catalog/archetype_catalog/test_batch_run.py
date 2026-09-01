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

    # ---------------------------------------------------------
    # Test QP
    # ---------------------------------------------------------

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
                "Identify ionic bonding as formation via "
                "complete electron transfer followed by "
                "electrostatic attraction between resulting ions"
            ),
        }
    ]

    # ---------------------------------------------------------
    # Generate prompt
    # ---------------------------------------------------------

    batch = qps[:1]

    generator = (
        BatchArchetypeCatalogGenerator()
    )

    prompt = generator.load_prompt(
        qps=batch,
    )

    # ---------------------------------------------------------
    # Call AI
    # ---------------------------------------------------------

    client = (
        ArchetypeCatalogAIClient()
    )

    print()
    print(
        "Calling GPT-5..."
    )

    result = (
        client.generate_json(
            prompt
        )
    )

    # ---------------------------------------------------------
    # Save TEST output only
    # ---------------------------------------------------------

    output_file = (
        Path(__file__).parent
        / "test_archetype_output.json"
    )

    output_file.write_text(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print()
    print(
        "SUCCESS: Archetype schema validation passed."
    )

    print(
        f"Saved: {output_file}"
    )

    print(
        f"Records: {len(result)}"
    )

    # ---------------------------------------------------------
    # Display variation information
    # ---------------------------------------------------------

    print()
    print(
        "Variation metadata:"
    )

    for record in result:

        print(
            f"{record['archetype_id']} | "
            f"{record['variation_capacity']} | "
            f"{record['variation_dimensions']}"
        )


if __name__ == "__main__":
    main()