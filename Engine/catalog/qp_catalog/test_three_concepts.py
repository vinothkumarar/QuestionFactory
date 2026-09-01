from __future__ import annotations

import json
from pathlib import Path

from Engine.catalog.qp_catalog.qp_catalog_ai_client import (
    QPCatalogAIClient,
)

from Engine.catalog.qp_catalog.qp_catalog_generator import (
    QPCatalogGenerator,
)


CONCEPTS = [
    {
        "subject": "Mathematics",
        "unit": "Coordinate Geometry",
        "chapter": "Straight Lines",
        "subtopic": "Slope and Inclination",
        "concept_id": "C015",
        "concept": (
            "Perpendicularity criterion in terms of slopes, "
            "including special cases"
        ),
        "output": "qp_test_math.json",
    },
    {
        "subject": "Chemistry",
        "unit": "Chemical Bonding and Molecular Structure",
        "chapter": "Chemical Bonding",
        "subtopic": "Ionic Bond",
        "concept_id": "C008",
        "concept": (
            "Factors Affecting Lattice Energy "
            "(ionic charge, size, interionic distance, lattice geometry)"
        ),
        "output": "qp_test_chemistry.json",
    },
    {
        "subject": "Physics",
        "unit": "Laws of Motion",
        "chapter": "Newton's Laws",
        "subtopic": "First Law",
        "concept_id": "C007",
        "concept": "Inertial Reference Frames",
        "output": "qp_test_physics.json",
    },
]


def main() -> None:

    generator = QPCatalogGenerator()
    client = QPCatalogAIClient()

    for concept in CONCEPTS:

        print()
        print("=" * 80)
        print(
            f"Generating QP Catalog: "
            f"{concept['subject']} - {concept['concept_id']}"
        )
        print("=" * 80)

        prompt = generator.load_prompt(
            subject=concept["subject"],
            unit=concept["unit"],
            chapter=concept["chapter"],
            subtopic=concept["subtopic"],
            concept_id=concept["concept_id"],
            concept=concept["concept"],
        )

        result = client.generate_json(prompt)

        output_file = (
            Path(__file__).parent / concept["output"]
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
            f"Saved: {output_file}"
        )

        print(
            f"QP count: {len(result)}"
        )


if __name__ == "__main__":
    main()