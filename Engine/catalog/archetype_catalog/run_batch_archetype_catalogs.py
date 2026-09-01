from __future__ import annotations

import json
from pathlib import Path

BATCH_SIZE = 10


def chunk_rows(rows: list[dict], size: int):
    for i in range(0, len(rows), size):
        yield rows[i:i + size]


def main() -> None:

    test_file = Path("c010_test.json")

    qps = json.loads(
        test_file.read_text(
            encoding="utf-8"
        )
    )

    print(
        f"Loaded {len(qps)} QPs"
    )

    batches = list(
        chunk_rows(
            qps,
            BATCH_SIZE,
        )
    )

    print(
        f"Created {len(batches)} batches"
    )

    for index, batch in enumerate(
        batches,
        start=1,
    ):
        print(
            f"Batch {index}: "
            f"{len(batch)} QPs"
        )


if __name__ == "__main__":
    main()