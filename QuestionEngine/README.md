# Dual Question Engine v1.0

A small, independent foundation for two complementary question workflows:

- **Original Question Engine** — accepts generated candidates only when they add meaningful learning value and pass quality gates.
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

## Current scope

This first foundation provides:
- curriculum loading and relationship validation;
- a shared question data model;
- explicit quality gates and duplicate checks;
- separate original-question review and PYQ provenance intake;
- standard-library unit tests.

It does **not** claim to extract 20 years of papers automatically or to generate verified academic content without a configured provider and source material. PDF/OCR extraction, AI provider integration, practice delivery and final CSV mapping are subsequent increments.

## Run

From the repository root:

```bash
python -m unittest discover -s QuestionEngine/tests -v
python -m compileall QuestionEngine
```
