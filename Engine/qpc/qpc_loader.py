from __future__ import annotations

import csv
from pathlib import Path


class QPCLoader:
    """
    Loads Question Possibility Catalogue (QPC)
    for a chapter and filters by subtopic.
    """

    def __init__(
        self,
        root: str = "Engine/qpc/mathematics",
    ) -> None:

        self.root = Path(root)

    def load(
        self,
        chapter_code: str,
        subtopic_code: str,
    ) -> list[dict[str, str]]:

        file_path = self.root / f"{chapter_code}.csv"

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        possibilities: list[dict[str, str]] = []

        with open(
            file_path,
            newline="",
            encoding="utf-8",
        ) as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:

                if (
                    row["subtopic_code"].strip()
                    == subtopic_code
                ):
                    possibilities.append(row)

        return possibilities