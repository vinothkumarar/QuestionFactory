# Dual Question Engine v1.0

A small, independent foundation for two complementary question workflows:

- **Original Question Engine** — reviews generated candidates only when they add meaningful learning value and pass quality gates.
- **PYQ Practice Engine** — preserves historical questions with source provenance and keeps unverified transcriptions out of the verified practice collection.

Both use the existing curriculum hierarchy and a shared question model. This package does not replace or modify the legacy `Engine/` implementation.

## Design principles

1. Quality and meaningful coverage over question count. No fixed per-subtopic quota.
2. PYQs are source-backed historical records, never reconstructed from model memory.
3. Exact PYQ, PYQ-inspired and original questions have distinct provenance.
4. Incorrect answers, out-of-syllabus questions and unverified PYQ transcriptions cannot be marked approved.
5. Preserve existing curriculum IDs. Do not write to Supabase; CSV/database adapters are added only after the import contract is confirmed.
6. Keep the first implementation dependency-light and testable.

## Curriculum input

The loader reads the existing files under `Engine/curriculum/`:

- `subjects.csv`
- `<subject-folder>/units.csv`
- `<subject-folder>/chapters.csv`
- `<subject-folder>/subtopics.csv`

It includes Mathematics, Physics, Chemistry and Biology. Aptitude is deliberately excluded from this examination scope. Extra historical columns such as `created_at` are tolerated but not required.

**Current data finding:** Biology is listed in `subjects.csv`, but its current units, chapters and subtopics CSV files are empty. The loader reports Biology as incomplete; it does not invent curriculum records. The existing Mathematics, Physics and Chemistry data is loaded and relationship-checked.

## Current implementation boundary

This first foundation provides:
- curriculum loading and relationship validation;
- a shared question data model;
- explicit quality gates and exact-duplicate checks;
- separate original/PYQ-inspired review and PYQ provenance intake;
- deterministic UTF-8 CSV export that preserves options, rubric scores and PYQ provenance in JSON columns;
- a curriculum readiness command;
- standard-library unit tests.

`QuestionCSVExporter` writes a staging CSV with an explicit stable column order. It is intentionally not represented as the final Supabase import schema until that contract is confirmed.\n\nThe original engine currently reviews candidates; an AI generation provider is not yet wired in. The PYQ engine currently verifies intake metadata; bulk PDF/OCR extraction and 20-year paper collection are not yet implemented. These are the next delivery increments, not features we claim are already complete.

Exact PYQs require traceable paper provenance, verified transcription and verified answer evidence before they enter the verified practice collection. Usage rights must be reviewed before external redistribution.

## Run

From the repository root:

```bash
PYTHONPATH=QuestionEngine python -m question_engine --curriculum-root Engine/curriculum
python -m unittest discover -s QuestionEngine/tests -v
python -m compileall QuestionEngine
```

## Existing PYQ acquisition work to reuse

The ChatGPT Library already contains a JEE paper inventory and source registries:
- `JEE_PYQ_Phase1_Complete_Paper_Shift_Inventory_2002_2026.xlsx` — 247 inventory rows across historical IIT-JEE, AIEEE, JEE Main and JEE Advanced.
- `JEE_PYQ_Phase2_Source_Registry.xlsx` and `JEE_PYQ_Phase2_1_Audited_Source_Registry.xlsx` — source and verification references.
- `JEE_PYQ_Phase2_2_2026_English_Acquisition_Registry.xlsx` — acquisition status and official-paper references.

These are acquisition manifests, not proof that every listed PDF has already been downloaded or verified. Reuse them as the starting manifest; do not recreate the JEE inventory. The current first code increment does not yet import these Library workbooks. NEET and BITSAT source inventories still need a separate audit before claiming complete coverage.
