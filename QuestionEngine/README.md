# Dual Question Engine v1.0

An independent implementation of two question workflows for JEE Main, JEE Advanced, NEET and BITSAT. It shares the existing curriculum hierarchy but does not modify the legacy `Engine/` factory or write to Supabase.

## Core rules

1. Quality and meaningful conceptual coverage over question count; no fixed quota per subtopic.
2. Exact PYQs, PYQ-inspired questions and original questions have distinct identities and provenance.
3. A generated question is only a draft until both its answer and syllabus scope are independently verified.
4. PYQ content is never reconstructed from model memory or silently rewritten and labelled authentic.
5. Missing source pages, diagrams, options or answer keys remain pending; they are never invented.

## Current implementation

- Existing curriculum CSV loader with relationship checks and incomplete-subject reporting.
- Shared question model, hard quality gates, 40/50 rubric floor and exact-duplicate checks.
- Original-question engine with provider-neutral generation interface.
- OpenAI Chat Completions adapter using `OPENAI_API_KEY` and `OPENAI_MODEL`; JSON response parsing, candidate shape validation and deterministic draft IDs.
- Draft generation path which always clears provider-supplied answer/syllabus approval flags.
- Separate answer-verification and syllabus-scope-verification contracts. Both must return matching question IDs, a method and evidence before approval.
- PYQ intake gate requiring paper provenance, verified transcription and traceable answer-key/solution reference.
- Audited PYQ registry loader for CSV and XLSX, including duplicate-ID checks and acquisition reporting.
- PDF text intake with SHA-256 fingerprinting, page-level provenance, file checks and explicit OCR-required page reporting.
- Conservative page-level PYQ segmentation that preserves raw text and source page, detects option labels, and leaves uncertain/continuation fragments pending manual review.
- Deterministic CSV staging export preserving options, rubric scores, answer/scope verification evidence and PYQ provenance.
- Single-subtopic original-question draft pilot CLI.
- GitHub Actions compile and unit-test workflow.

## Not complete yet

- The OpenAI adapter is implemented but has not been connected to a live API account in this repository. It needs a secret API key and an API-enabled model ID at runtime.
- No concrete independent mathematical solver or curriculum-scope verifier is connected yet; only strict contracts and approval gates exist.
- PDF downloading, OCR execution, answer-key matching and bulk PYQ reconstruction are not complete. The initial question-boundary segmenter is heuristic and explicitly marks ambiguous fragments for manual review; it is not an authenticity or correctness verifier.
- Student practice UI and final Supabase import schema are not connected. CSV is a staging contract only.
- NEET and BITSAT historical source inventories need separate acquisition audits.

## OpenAI configuration

Set these in the local environment or secret manager. Never commit an API key.

- `OPENAI_API_KEY`: API key for the OpenAI project.
- `OPENAI_MODEL`: model ID enabled for that API project.
- Optional `OPENAI_BASE_URL`: defaults to `https://api.openai.com/v1`.

The adapter uses the official Chat Completions endpoint with JSON response mode and rejects malformed candidates instead of silently repairing them. See the [Chat Completions API reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) and [Structured Outputs guidance](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=chat).

## Run from repository root

~~~bash
python -m pip install -r QuestionEngine/requirements.txt
PYTHONPATH=QuestionEngine python -m question_engine --curriculum-root Engine/curriculum
python -m unittest discover -s QuestionEngine/tests -v
python -m compileall QuestionEngine
~~~

Generate up to three unverified draft candidates for Mathematics U1–CH1–ST1:

~~~bash
PYTHONPATH=QuestionEngine python -m question_engine.pilot \
  --subtopic-code U1_CH1_ST1 \
  --exam-target 'JEE Main' \
  --concept-id natural-numbers \
  --outcome 'Classify natural numbers, whole numbers and integers.' \
  --candidate-limit 3 \
  --output output/maths_u1_ch1_st1_drafts.csv
~~~

The pilot exports drafts only. It does not mark answers or syllabus scope as verified and does not write to Supabase.

Optional source-registry readiness reports can be run with the curriculum CLI using `--pyq-registry path/to/registry.csv` or `--pyq-registry-xlsx path/to/registry.xlsx`.

## Existing JEE source inventory

The ChatGPT Library contains a JEE 2002–2026 inventory with 247 paper/source records and associated source registries. The audited tracker currently marks all 247 as not yet acquired; all 247 have PDF Verified = No and Answer Key Verified = No. These are acquisition records, not downloaded PDFs or verified questions. Reuse the existing inventory rather than recreating it.

## Safety and integration boundaries

- Existing `Engine/`, legacy catalogs, `main` branch and the earlier documentation PR are untouched.
- The current branch is `feature/dual-question-engine-v1`; PR #2 remains a draft.
- Do not merge until the pilot, independent verification adapters and import contract have been reviewed.
- Usage rights must be reviewed before external redistribution of historical paper content.


## First concept-coverage pilot

A provisional concept catalog for Mathematics U1–CH1–ST1 is maintained at `catalogs/maths_u1_ch1_st1_concepts.csv`. It is a planning aid, not an approved syllabus mapping. Every row is marked `PROVISIONAL_REVIEW_REQUIRED`; in particular, the natural-number convention and placement of absolute value/additive inverse/closure must be checked against the active exam syllabus and the approved chapter map before production generation. The catalog defines coverage candidates, not a target question count. Generate only where a distinct learning opportunity is justified.
