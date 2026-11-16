"""Print a concise readiness report for the existing curriculum CSVs."""

from __future__ import annotations

import argparse
from pathlib import Path

from .curriculum import CurriculumLoader
from .pyq_registry import PYQSourceRegistry


def main() -> int:
    parser = argparse.ArgumentParser(description="Dual Question Engine curriculum check")
    parser.add_argument(
        "--curriculum-root",
        type=Path,
        default=Path("Engine") / "curriculum",
        help="Path to the existing curriculum folder",
    )
    registry_group = parser.add_mutually_exclusive_group()
    registry_group.add_argument(
        "--pyq-registry", type=Path, default=None,
        help="Optional audited PYQ source-registry CSV to summarize",
    )
    registry_group.add_argument(
        "--pyq-registry-xlsx", type=Path, default=None,
        help="Optional audited PYQ source-registry XLSX to summarize",
    )
    args = parser.parse_args()

    snapshot = CurriculumLoader(args.curriculum_root).load()
    print("Dual Question Engine — Curriculum Readiness")
    print(f"Subjects: {len(snapshot.subjects)}")
    print(f"Units: {len(snapshot.units)}")
    print(f"Chapters: {len(snapshot.chapters)}")
    print(f"Subtopics: {len(snapshot.subtopics)}")

    if args.pyq_registry or args.pyq_registry_xlsx:
        registry = (
            PYQSourceRegistry.load_csv(args.pyq_registry)
            if args.pyq_registry
            else PYQSourceRegistry.load_xlsx(args.pyq_registry_xlsx)
        )
        summary = registry.summary()
        print("\\nPYQ SOURCE REGISTRY (acquisition status only)")
        print(f"Records: {summary.total_records}")
        print(f"Direct PDF URLs: {summary.direct_pdf_urls}")
        print(f"PDFs verified: {summary.pdf_verified}")
        print(f"Answer keys verified: {summary.answer_keys_verified}")
        print(f"Not yet acquired: {summary.not_yet_acquired}")
        for exam, count in sorted(summary.by_exam.items()):
            print(f"- {exam}: {count}")

    if snapshot.incomplete_subjects:
        print("\nINCOMPLETE CURRICULA:")
        for item in snapshot.incomplete_subjects:
            print(f"- {item}")
        return 1

    print("\nAll supported subject curricula are structurally available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
