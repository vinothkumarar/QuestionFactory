"""Run a bounded original-question draft pilot for one curriculum subtopic.

This command exports unverified drafts only. It never marks generated answers or
syllabus scope as approved and never writes to Supabase.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .curriculum import CurriculumLoader, CurriculumSnapshot
from .export import QuestionCSVExporter
from .generation import GenerationRequest
from .openai_provider import OpenAIQuestionGenerationProvider
from .original_engine import OriginalQuestionEngine


def build_request(
    snapshot: CurriculumSnapshot,
    subtopic_code: str,
    exam_targets: Sequence[str],
    concept_ids: Sequence[str],
    learning_outcomes: Sequence[str],
    candidate_limit: int,
) -> GenerationRequest:
    subtopic = snapshot.find_subtopic(subtopic_code)
    chapter = next(
        (row for row in snapshot.chapters if row["id"] == subtopic["chapter_id"]),
        None,
    )
    if chapter is None:
        raise ValueError(f"Subtopic {subtopic_code} references an unknown chapter")
    unit = next(
        (row for row in snapshot.units if row["id"] == chapter["unit_id"]),
        None,
    )
    if unit is None:
        raise ValueError(f"Chapter {chapter['code']} references an unknown unit")
    subject = next(
        (row for row in snapshot.subjects if row["id"] == unit["subject_id"]),
        None,
    )
    if subject is None:
        raise ValueError(f"Unit {unit['code']} references an unknown subject")

    return GenerationRequest(
        subject_id=subject["id"],
        unit_id=unit["id"],
        chapter_id=chapter["id"],
        subtopic_id=subtopic["id"],
        exam_targets=tuple(exam_targets),
        concept_ids=tuple(concept_ids),
        learning_outcomes=tuple(learning_outcomes),
        candidate_limit=candidate_limit,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate unverified original-question drafts for one subtopic"
    )
    parser.add_argument(
        "--curriculum-root",
        type=Path,
        default=Path("Engine") / "curriculum",
    )
    parser.add_argument("--subtopic-code", required=True)
    parser.add_argument("--exam-target", action="append", required=True)
    parser.add_argument("--concept-id", action="append", required=True)
    parser.add_argument("--outcome", action="append", required=True)
    parser.add_argument("--candidate-limit", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    snapshot = CurriculumLoader(args.curriculum_root).load()
    request = build_request(
        snapshot,
        args.subtopic_code,
        args.exam_target,
        args.concept_id,
        args.outcome,
        args.candidate_limit,
    )
    provider = OpenAIQuestionGenerationProvider()
    engine = OriginalQuestionEngine()
    drafts = engine.generate_drafts(request, provider)
    exported = QuestionCSVExporter().export(drafts, args.output)

    print("Original Question Engine — Draft Pilot")
    print(f"Subtopic: {args.subtopic_code}")
    print(f"Draft candidates exported: {exported}")
    print(f"Output: {args.output}")
    print("Approval status: UNVERIFIED — independent answer and syllabus checks required")
    print("Supabase writes: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
