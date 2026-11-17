# P1 Progress — Syllabus, PYQ & Blueprint Foundation

**Programme:** Question Factory OS v3.0 — MECP v1.2  
**Phase:** P1  
**Actual start:** 2026-11-17  
**Planned P1 window:** 2026-11-18 to 2026-11-26 (7 working days; baseline retained)  
**Repository:** https://github.com/vinothkumarar/QuestionFactory  
**Audited branch:** `feature/dual-question-engine-v1`  
**Baseline HEAD at P1 start:** `4fe34c92e77c511aabbe1b18f4663714ab74c701`  
**Status:** ACTIVE — EXIT GATE NOT PASSED

## Operating controls

- Preserve existing architecture, taxonomy IDs, catalogues, QP/QPC/archetype records and prior work.
- No production question generation during P1.
- Official exam scope is versioned separately for JEE Main and JEE Advanced.
- Internal unit/chapter numbering is not treated as official syllabus numbering.
- A URL, indexed PDF text or a link marked accessible is not the same as local PDF acquisition.
- No source is treated as hash-verified until local bytes are available and SHA-256 is calculated.
- No blueprint version is declared authoritative without the complete approved artifact and provenance.

## Dated evidence log

### 2026-11-17 — P1 commencement and initial evidence review

#### Official syllabus source status

1. **JEE Main 2027 — official NTA source found and PDF text retrieved.**
   - Official NTA documents register: https://jeemain.nta.nic.in/documents/
   - Official syllabus PDF: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/20261024683680768.pdf
   - The NTA register lists “Syllabus 2027” (1 MB). The PDF is accessible through the official indexed source and its subject/unit text was inspected.
   - Official Paper 1 subject structure: Mathematics 14 units, Physics 20 units, Chemistry 20 units.
   - Local PDF bytes could not be downloaded into the working environment on this date; local-file status remains NOT ACQUIRED and SHA-256 remains PENDING.
   - This corrects the older repository note that only described the official listing and blocked local retrieval. It does not claim local acquisition.

2. **JEE Advanced 2027 — official syllabus not yet published.**
   - Official portal: https://jeeadv.ac.in/
   - Official 2027 syllabus page: https://jeeadv.ac.in/syllabus.html
   - The page explicitly displays “Coming soon ... This page will be updated shortly.”
   - Use the official 2026 syllabus only as a provisional comparison baseline:
     https://jeeadv.ac.in/documents/jee-advanced-2026-syllabus.pdf
   - The 2026 PDF explicitly states that the 2026 syllabus remains the same as 2025.
   - Local PDF bytes and SHA-256 remain pending. No 2027 Advanced mapping can be approved from the 2026 baseline alone.

#### Initial internal taxonomy inventory (repository CSV snapshot)

| Subject | Internal units | Chapters | Subtopics | Unit enable flags | Chapter enable flags | Subtopic enable flags |
|---|---:|---:|---:|---:|---:|---:|
| Mathematics | 15 | 95 | 533 | 2 enabled | 2 enabled | 533 enabled |
| Physics | 23 | 42 | 233 | 1 enabled | 1 enabled | 233 enabled |
| Chemistry | 29 | 48 | 260 | 0 enabled | 0 enabled | 260 enabled |
| **Total** | **67** | **185** | **1,026** | **3 enabled** | **3 enabled** | **1,026 enabled** |

- These are repository snapshot counts, not claims about the live Supabase database.
- Parent/child enablement is inconsistent in the snapshot: every subtopic is locally marked enabled even where its chapter or unit is disabled. Effective manufacturing eligibility must therefore be computed hierarchically (subject AND unit AND chapter AND subtopic enabled, with exam-scope verification) rather than trusting the leaf flag alone.
- No taxonomy IDs or enable flags were changed in this initial audit.
- Detailed unit/chapter/subtopic mapping against official 2027 Main and provisional 2026 Advanced syllabus remains in progress.

#### PYQ inventory and acquisition audit

Sources inspected:
- Library workbook: `JEE_PYQ_Phase1_Complete_Paper_Shift_Inventory_2002_2026.xlsx`
- Library workbook: `JEE_PYQ_Phase2_1_Audited_Source_Registry.xlsx`
- Library workbook: `JEE_PYQ_Phase2_2_2026_English_Acquisition_Registry.xlsx`
- Repository: `QuestionEngine/README.md`, `QuestionEngine/catalogs/exam_syllabus_sources.csv`, `QuestionEngine/catalogs/exam_syllabus_source_status.csv`, and `QuestionEngine/question_engine/pyq_registry.py`

Audited 2002–2026 inventory:
- 247 unique paper/source records: 21 IIT-JEE historical, 13 AIEEE, 185 JEE Main, 28 JEE Advanced.
- 137 rows are marked Historical verification; 110 are marked Ready for acquisition.
- In the audited tracker, all 247 are “Not yet acquired”; PDF Verified = No for 247; Answer Key Verified = No for 247.
- In that tracker, PDF URL, Answer Key URL, Solution URL and SHA256 are blank for all 247 rows.
- The repository tree contains no PDF files.
- These 247 records are an inventory/target list, not 247 acquired papers or verified question sets.

2026 English acquisition tracker:
- Contains 21 2026 records: 2 JEE Advanced papers, 19 JEE Main Paper 1 shifts (10 January and 9 April).
- 11 records are marked “URL verified — PDF accessible”: JEE Advanced Paper 1 and Paper 2, plus the 9 April JEE Main shifts listed by NTA.
- The 10 January JEE Main shifts remain “Not yet acquired”.
- All 21 records have Answer Key Verified = No.
- The 11 “PDF Verified = Yes” flags represent URL/access verification in this workbook; they do not establish local byte acquisition or SHA-256. No local PDF bytes or hashes were found in the audited repository or the inspected workbook records.
- NTA's current official documents register lists nine April 2026 Paper 1 shift papers. Its 2026 documents include final answer-key records for Session I and Session II, but those answer keys have not been linked/matched/verified per paper in the acquisition tracker.

README reconciliation:
- `QuestionEngine/README.md` says the Library contains 247 records and all are not yet acquired, with PDF/answer-key verification No. That matches the audited tracker but does not explain the separate 2026 workbook's 11 URL-access flags.
- Resolve this by distinguishing at least: INVENTORIED, URL_VERIFIED, BYTES_ACQUIRED, HASH_VERIFIED, TRANSCRIPTION_VERIFIED, ANSWER_KEY_SOURCE_LINKED, ANSWER_KEY_VERIFIED and SYLLABUS_MAPPED. Do not collapse URL accessibility into acquisition.
- Historical IIT-JEE and AIEEE remain separate exam families from JEE Main and JEE Advanced. Their syllabus and paper formats must not be assumed identical.

#### Blueprint authority audit — unresolved

Repository sources inspected:
- `Engine/prompts/master/05_blueprint_rules.md`
- `Engine/prompts/master/06_distractor_engineering.md`
- `Blueprint/01_RULES.md`
- `Blueprint/02_ARCHETYPES.md`
- `Blueprint/04_REBUILD.md`
- `Engine/factory/quality/rule_registry.py` (identified by repository search)
- `QuestionEngine/README.md`
- Recovered Library records: `05_BLUEPRINT_AND_QPC.md`, `01_DECISION_REGISTER.md`, `11_DECISION_RECONCILIATION_ADDENDUM.md`, and historical QGS prompt material.

Findings:
- Historical conversations mention Blueprint v1.2, v1.3, v1.4 and v1.5. The user approved the direction to embed the complete frozen v1.5, but the complete signed-off v1.5 artifact and its full rule text were not located in the repository or recovered Library sources reviewed so far.
- `Engine/prompts/master/05_blueprint_rules.md` has a working R01–R12 sequence: Concept First, Single Learning Objective, Mathematical Verification, Unique Answer, Explanation Quality, Difficulty Alignment, Language Quality, Examination Authenticity, Originality, Educational Value, Internal Consistency, Production Readiness.
- `Blueprint/01_RULES.md` reuses R01–R12 for a different continuity/difficulty/strict-verification/quality/stable-ID/rebuild/coverage/archetype/diversity/repetition/formula/saturation sequence. These namespaces conflict and must not be merged.
- `Engine/prompts/master/06_distractor_engineering.md` is the current repository working reference for DE-01 DR01–DR10 and DE-02 quality rules. Historical v1.3 notes contain a different DR01–DR07 taxonomy. Preserve both as separate historical/working references pending authoritative reconciliation.
- `Blueprint/02_ARCHETYPES.md` uses AR17–AR20 for archetype patterns. Historical blueprint notes also use AR as a rule family, including AR-01 Dynamic Count Rule; an archetype prompt uses AR-01 for the hierarchy. This is another identifier collision.
- The recovered records do not provide authoritative complete definitions for R13–R20, all AR rules, SC-01, the complete PYQ rule family, and all associated cross-references.
- S1 Foundation, S2 Easy+, S3 Medium, S4 Hard, S5 Elite is the established intended progression in the recovered decisions; legacy text containing Medium+ is not silently substituted.
- Current status: provisional working sources identified; authoritative frozen blueprint remains unresolved. No final rule freeze or production authority is granted.

## P1 work remaining

1. Complete exact official syllabus extraction and separate Main/Advanced applicability.
2. Reconcile all 67 internal units, 185 chapters and 1,026 subtopics; preserve IDs and record explicit mapping confidence/status.
3. Produce a parent/child effective-enablement matrix without silently changing existing IDs or source records.
4. Reconcile all 247 PYQ records, paper families, 2026 shift completeness, official paper URLs, local file status, hashes, answer-key sources and matching state.
5. Acquire/verify source PDFs where legally and technically available; compute SHA-256 only after bytes are present.
6. Establish a canonical PYQ record schema with page/question-level provenance and separate answer-key verification state.
7. Continue recovering the complete user-approved Blueprint v1.5 source; create a rule/version crosswalk only when source text is supported.
8. Demonstrate every MECP v1.2 P1 acceptance gate before marking P1 complete.

## Exit gate

**NOT PASSED.** P1 remains ACTIVE. No production questions have been generated in this phase. No final syllabus mapping, PYQ verification, or authoritative blueprint freeze is claimed.
