"""Print a concise readiness report for the existing curriculum CSVs."""

from __future__ import annotations

import argparse
from pathlib import Path

from .curriculum import CurriculumLoader


def main() -> int:
    parser = argparse.ArgumentParser(description="Dual Question Engine curriculum check")
    parser.add_argument(
        "--curriculum-root",
        type=Path,
        default=Path("Engine") / "curriculum",
        help="Path to the existing curriculum folder",
    )
    args = parser.parse_args()

    snapshot = CurriculumLoader(args.curriculum_root).load()
    print("Dual Question Engine — Curriculum Readiness")
    print(f"Subjects: {len(snapshot.subjects)}")
    print(f"Units: {len(snapshot.units)}")
    print(f"Chapters: {len(snapshot.chapters)}")
    print(f"Subtopics: {len(snapshot.subtopics)}")

    if snapshot.incomplete_subjects:
        print("\nINCOMPLETE CURRICULA:")
        for item in snapshot.incomplete_subjects:
            print(f"- {item}")
        return 1

    print("\nAll supported subject curricula are structurally available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
