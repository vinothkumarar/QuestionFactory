from __future__ import annotations

import json

from Engine.catalog.archetype_catalog.batch_archetype_catalog_generator import (
    BatchArchetypeCatalogGenerator,
)


def main() -> None:

    with open(
        "c010_test.json",
        encoding="utf-8",
    ) as f:
        qps = json.load(f)

    batch = qps[:10]

    generator = (
        BatchArchetypeCatalogGenerator()
    )

    prompt = generator.load_prompt(
        qps=batch,
    )

    with open(
        "c010_prompt_preview.txt",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(prompt)

    print(
        "Prompt created:"
    )

    print(
        "c010_prompt_preview.txt"
    )

    print()

    print(
        f"QPs in batch: {len(batch)}"
    )

    print(
        f"Prompt length: {len(prompt)} chars"
    )


if __name__ == "__main__":
    main()