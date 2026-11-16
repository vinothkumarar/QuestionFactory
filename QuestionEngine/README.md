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
- Conservative deterministic integer-expression verifier for the exact `Evaluate: <integer expression>` format. It uses a restricted AST interpreter (no `eval`), checks four distinct integer options and rejects unsupported formats or incorrect answers.
- Conservative deterministic divisibility-rule verifier for the exact `Which of these integers is divisible by N?` single-correct MCQ format; checks all four options independently and rejects zero/multiple matches, malformed options or unsupported wording.
- Approved-catalog scope verifier that checks the full subject → unit → chapter → subtopic ID chain and requires every referenced concept to be explicitly approved with audit metadata.
- Exam-versioned official syllabus source/mapping registry with provenance, effective dates, optional document hash, reviewer audit fields and exact-match lookup; APPROVED mappings additionally require a retrieved official document with a recorded SHA-256 fingerprint and an explicit effective-from date. A separate prior-year baseline resolver selects the latest earlier registered version for provisional comparison only, rejects ambiguous years and never approves exam scope.
- Exam-target scope-verification wrapper that requires a configured syllabus version and an approved official mapping for every exam target.
- PYQ intake gate requiring paper provenance, verified transcription and traceable answer-key/solution reference.
- Audited PYQ registry loader for CSV and XLSX, including duplicate-ID checks and acquisition reporting.
- PDF text intake with SHA-256 fingerprinting, page-level provenance, file checks and explicit OCR-required page reporting.
- Conservative page-level PYQ segmentation that preserves raw text and source page, detects option labels, and leaves uncertain/continuation fragments pending manual review.
- Deterministic CSV staging exporter preserving options, rubric scores, answer/scope verification evidence and PYQ provenance.
- Single-subtopic original-question draft pilot CLI.
- GitHub Actions compile and unit-test workflow.
- Concept approval gate now requires reviewer identity, ISO-8601 review timestamp, source reference and rationale for both APPROVED and REJECTED decisions. Provisional concepts remain excluded from generation.

## Not complete yet

- The OpenAI adapter is implemented but has not been connected to a live API account in this repository. It needs a secret API key and an API-enabled model ID at runtime.
- The deterministic answer verifier currently supports only a narrow integer-expression MCQ format. It is not a general symbolic mathematics solver; all other question formats remain unverified until a suitable independent verifier is added.
- The exam-versioned registry and enforcement path are implemented. Eight official source identities are registered: NMC UGMEB NEET (UG)-2026 and NTA NEET portal status for 2027; NTA JEE Main 2026 and 2027; IIT Delhi JEE Advanced 2026 and 2027; and BITSAT 2026 plus the official BITS portal status for 2027. NEET 2026, JEE Main 2026, JEE Advanced 2026 and BITSAT 2026 source documents are accessible as official indexed text, but local PDF bytes and SHA-256 fingerprints remain pending. The official NEET and BITS admission portals currently list 2026 materials, not a 2027 syllabus/brochure; those portal-status observations are tracked separately and are not treated as source documents. JEE Main 2026 Mathematics Unit 1 is `Sets, Relations and Functions`; internal Mathematics U1 `Number System` is not equivalent by unit number and has no approved mapping to it. NTA's official JEE Main 2027 listing identifies a 1 MB syllabus document, but direct PDF retrieval and SHA-256 remain pending. JEE Advanced 2027 currently says the syllabus is coming soon. Use the 2026 official syllabi as provisional comparison baselines where 2027 text is not yet verifiable; do not infer official mappings or approval. No subtopic mappings are approved. Exact wording extraction, source fingerprinting and human review are required. Source acquisition state is tracked separately in `catalogs/exam_syllabus_source_status.csv`.
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


### JEE Main 2027 acquisition and Mathematics U1 pilot status

NTA's official documents listing identifies a 1 MB entry titled `Syllabus 2027` (see the official [Syllabus 2027 page](https://jeemain.nta.nic.in/document/syllabus-2027/) and [Documents listing](https://jeemain.nta.nic.in/documents/)). The candidate 2027 CDN endpoint remains unverified: local PDF retrieval and SHA-256 fingerprinting are pending because outbound DNS/network retrieval failed. The official NTA-hosted [JEE Main 2026 syllabus PDF](https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/10/202510311323551056.pdf), [JEE Advanced 2026 syllabus PDF](https://jeeadv.ac.in/documents/jee-advanced-2026-syllabus.pdf), [NEET UG 2026 syllabus](https://www.nmc.org.in/MCIRest/open/getDocument?path=%2FDocuments%2FPublic%2FPortal%2FLatestNews%2FPublic+Notice_NEET_removed.pdf), and [BITSAT 2026 brochure](https://www.bitsadmission.com/FD/downloads/BITSAT-2026_brochure.pdf) are registered as previous-year official baselines and accessible as indexed text. Local bytes and SHA-256 remain pending for each. Do not approve mappings from unverified local document fingerprints or use unofficial mirrors as authoritative evidence.

The internal Mathematics U1 label is `Number System`; the official 2026 JEE Main Mathematics Unit 1 is `Sets, Relations and Functions`. The seven Number System concepts therefore have no approved direct mapping to that official unit and must not be forced into it. All seven U1-CH1-ST1 concept candidates remain `PROVISIONAL_REVIEW_REQUIRED` and excluded from exam-targeted production generation. Use the 2026 official syllabus only as a provisional comparison where 2027 text is unavailable; promote no mapping until exact official wording, source fingerprint and reviewer evidence are recorded.
