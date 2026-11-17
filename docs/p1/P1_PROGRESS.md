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

| Subject | Internal units | Chapters | Subtopics | Unit enable flags | Chapter enable flags | Subtopic enable flags | Effective enabled subtopics* |
|---|---:|---:|---:|---:|---:|---:|
| Mathematics | 15 | 95 | 533 | 2 enabled | 2 enabled | 533 enabled | 20 |
| Physics | 23 | 42 | 233 | 1 enabled | 1 enabled | 233 enabled | 6 |
| Chemistry | 29 | 48 | 260 | 0 enabled | 0 enabled | 260 enabled | 0 |
| **Total** | **67** | **185** | **1,026** | **3 enabled** | **3 enabled** | **1,026 enabled** | **26** |

- These are repository snapshot counts, not claims about the live Supabase database.
- Parent/child enablement is inconsistent in the snapshot: every subtopic is locally marked enabled even where its chapter or unit is disabled. A computed parent-chain flag shows only 26 of 1,026 subtopics pass the unit AND chapter AND subtopic flag check (Mathematics 20, Physics 6, Chemistry 0). This is a structural flag result only, not final exam-scope/manufacturing eligibility; official mapping and blueprint gates still apply.
- No taxonomy IDs or enable flags were changed in this initial audit.
- Created `docs/p1/P1_TAXONOMY_MAPPING_REGISTER.csv` with all 1,026 stable subtopic IDs, parent IDs, names, snapshot flags, effective parent-chain flags and separate Main/Advanced mapping status. The initial crosswalk now assigns a provisional Main 2027 and Advanced 2026 disposition to all 1,026 existing subtopic rows (Mathematics 533, Physics 233, Chemistry 260). No row is left UNREVIEWED. This is not final academic approval: all 1,026 rows are marked PENDING_INDEPENDENT_REVIEW, and 6 empty chapters are separately tracked outside the subtopic register. See `docs/p1/P1_MATHEMATICS_SCOPE_RECONCILIATION.md` and `docs/p1/P1_PHYSICS_SCOPE_RECONCILIATION.md`. Current register status — Main 2027: Mathematics 197 mapped / 104 partial / 232 no direct; Physics 209 / 8 / 16; Chemistry 182 / 18 / 60. Advanced 2026: Mathematics 247 mapped / 96 partial / 190 no direct; Physics 195 / 5 / 33; Chemistry 246 / 6 / 8. Mapping-basis classification: 285 chapter-level provisional, 155 chapter-level no-direct, 524 subtopic-level provisional, 52 subtopic-level no-direct, 10 cross-unit/subject. The basis classification is a review aid; every row remains pending independent academic validation. See `docs/p1/P1_MATHEMATICS_SCOPE_RECONCILIATION.md` for chapter-level boundaries. A separate exact-name audit found 42 duplicate subtopic-name groups (Mathematics 30, Physics 5, Chemistry 7), zero duplicate subtopic codes/UUIDs, and two duplicate Mathematics chapter titles. An empty-chapter audit found six chapters with zero subtopics (Physics P4/P5: five; Chemistry C27_CH3 Vitamins: one), all currently disabled. See `docs/p1/P1_EMPTY_CHAPTER_AND_COVERAGE_GAP_AUDIT.md`. These are candidates for semantic review, not deletion/merge decisions. See `docs/p1/P1_TAXONOMY_DUPLICATE_AUDIT.md`. Initial provisional mapping dispositions now cover all 1,026 subtopic rows. Independent academic validation, exact subtopic evidence checks and 2027 Advanced confirmation remain open.

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
- NTA's current official documents register lists nine April 2026 Paper 1 shift papers. Both official Session I and Session II final answer-key PDFs have now been opened and their contents inspected. Session I key: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/02/20260216459398513.pdf (10 pages; identifies dates/shifts and subject question IDs/correct options). Session II key: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/04/20260420409057044.pdf (18 pages; identifies dates/shifts and subject question IDs/correct option IDs). These official source documents are located, but the per-paper/per-question matching and tracker linkage are not yet complete. Four question/key pairs are now documented and independently solved in `P1_PYQ_EVIDENCE_REGISTER.csv`: two Main Physics questions from 2 April Shift 1, Advanced Paper 1 Mathematics Q3 and Advanced Paper 2 Physics Q1. This remains a sample, not bulk reconciliation; the 2026 acquisition workbook still has zero populated Answer Key URL fields and must be reconciled separately.

README reconciliation:
- `QuestionEngine/README.md` says the Library contains 247 records and all are not yet acquired, with PDF/answer-key verification No. That matches the audited tracker but does not explain the separate 2026 workbook's 11 URL-access flags.
- Resolve this by distinguishing at least: INVENTORIED, URL_VERIFIED, BYTES_ACQUIRED, HASH_VERIFIED, TRANSCRIPTION_VERIFIED, ANSWER_KEY_SOURCE_LINKED, ANSWER_KEY_VERIFIED and SYLLABUS_MAPPED. Do not collapse URL accessibility into acquisition.
- Historical IIT-JEE and AIEEE remain separate exam families from JEE Main and JEE Advanced. Their syllabus and paper formats must not be assumed identical.

#### Answer-key source follow-up — 2026-11-17\n\n- NTA JEE Main 2026 Session I and Session II final answer-key PDFs are official and text-accessible; they contain subject-wise question IDs and correct option identifiers by date/shift. The Library tracker has not yet linked these URLs to all 19 2026 Main shift records. Four question/key pairs are now independently solved and matched in the P1 evidence register: two Main questions from 2 April Shift 1, Advanced Paper 1 Mathematics Q3 and Advanced Paper 2 Physics Q1. The remaining paper/shift/question matches are pending.\n- JEE Advanced 2026 Information Brochure states that final answer keys for both papers were scheduled for online publication on 2026-06-01. Both official final-key PDF URLs have now been recovered and used for the two question-level matches recorded in the evidence register. Full-paper and question-by-question reconciliation remains pending. Official brochure: https://jeeadv.ac.in/documents/IBEnglish_2026.pdf\n\n#### Blueprint authority audit — unresolved

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
- `Engine/prompts/master/05_blueprint_rules.md` has a working R01–R12 sequence: Concept First, Single Learning Objective, Mathematical Verification, Unique Answer, Explanation Quality, Difficulty Alignment, Language Quality, Examination Authenticity, Originality, Educational Value, Internal Consistency, Production Readiness. Prior-conversation recovery now confirms these names and core intent for v1.5 R01–R12.
- `Blueprint/01_RULES.md` reuses R01–R12 for a different continuity/difficulty/strict-verification/quality/stable-ID/rebuild/coverage/archetype/diversity/repetition/formula/saturation sequence. These namespaces conflict and must not be merged.
- `Engine/prompts/master/06_distractor_engineering.md` is the current repository working reference for DE-01 DR01–DR10 and DE-02 quality rules. Historical v1.3 notes contain a different DR01–DR07 taxonomy. Preserve both as separate historical/working references pending authoritative reconciliation.
- `Blueprint/02_ARCHETYPES.md` uses AR17–AR20 for archetype patterns. Prior-conversation recovery now supplies AR01–AR20 names, AR-01 Dynamic Count/Saturation intent, and BS-01 batch size 10. Full archetype definitions and saturation thresholds remain missing; preserve the hyphen distinction between AR-01 rule and AR01 archetype.
- Prior-conversation recovery now supplies the v1.5 DR01–DR12 names, DE-01/DE-02 intent, DI-01 set labels, META-01 fields, CM-01 hierarchy, PYQ-01/02 intent, SV-01 checks, QE-01 40/50 rubric, RL-01 lifecycle and partial EDF-01 defaults. Exact thresholds, complete definitions, R13–R20, full schema and the original v1.5 artifact remain unavailable.
- S1 Foundation, S2 Easy+, S3 Medium, S4 Hard, S5 Elite is the established intended progression in the recovered decisions; legacy text containing Medium+ is not silently substituted.
- Current status: provisional working sources identified and historical fragments recovered; authoritative frozen blueprint remains unresolved. See `docs/p1/P1_BLUEPRINT_AUTHORITY_AUDIT.md`. No final rule freeze or production authority is granted.

## Unit-level taxonomy crosswalk — 2026-11-17\n\nCreated `docs/p1/P1_UNIT_LEVEL_TAXONOMY_RECONCILIATION.md` as a working draft. It maps all current internal unit labels against official JEE Main 2027 and provisional JEE Advanced 2026 headings. It identifies one clear Physics Main coverage gap (Experimental Skills), Chemistry Main gaps requiring a subtopic-level search (Purification/Characterisation and Practical Chemistry), multiple Main-vs-Advanced scope differences, and duplicate Mathematics sets/functions structures across U2/U9/U15. This is not a final approval map; every chapter and subtopic still needs exact wording review.\n\n## 2026-11-17 — Four-sample mapping second pass and evidence reconciliation

- Verified that the fourth PYQ evidence record (JEE Advanced 2026 Paper 2 Physics Q1) is present in the branch evidence register. The sample now contains two Main questions from one April shift and one question from each Advanced paper.
- Added `P1_SAMPLE_MAPPING_SECOND_PASS.md` to independently re-check all four question-to-taxonomy paths, official scope boundaries and parent/child enablement.
- The two leading Physics P1 candidates (`P1_CH1_ST4` Dimensional Analysis and `P1_CH1_ST6` Errors and Measurements) have explicit Main 2027 and Advanced 2026 baseline scope and TRUE unit/chapter/subtopic flags in the repository snapshot.
- The two additional Advanced sample paths (`U2_CH8_ST2` Matrix Operations and `P12_CH1_ST2` Drift Velocity) have provisional official-scope matches, but their parent unit/chapter flags are FALSE. Their subtopic TRUE flags do not make them effectively enabled. No enablement state was changed.
- Corrected the PYQ source audit, candidate sequence and this progress log to reflect the recovered Advanced final-key URLs and the two independently checked Advanced question matches. The 2026 acquisition workbook still has zero populated Answer Key URL cells; the question-level evidence register is separate.
- No local PDF bytes or SHA-256 hashes were acquired for these four records. Full paper/shift answer-key reconciliation remains pending.
- This second pass is internal review, not independent human academic sign-off. The 1,026-row taxonomy remains `PENDING_INDEPENDENT_REVIEW`.
- No production questions, taxonomy edits, enablement changes or schema changes were made.

## 2026-11-17 — Fresh official-source and branch-state recheck

- Rechecked the official JEE Advanced 2027 syllabus page. It still states “Coming soon”; the official JEE Advanced 2026 syllabus remains only a provisional comparison baseline for Advanced 2027. The official JEE Main 2027 documents register continues to list “Syllabus 2027”.
- Official pages: https://jeeadv.ac.in/syllabus.html and https://jeemain.nta.nic.in/documents/. The Advanced 2027 home page was launched by IIT Delhi on 2026-11-13; that announcement does not publish the syllabus.
- Attempted direct local download of the official Main paper and Advanced paper PDF sources through the working container; downloads failed. No local PDF bytes or SHA-256 values are claimed. Continue to distinguish official URL/PDF viewer access from local acquisition.
- GitHub branch comparison reports `feature/dual-question-engine-v1` is diverged from `main` (671 commits ahead, 6 behind at the time of check). P1 documentation changes remain on the feature branch. No merge, rebase, force update or production-code change was performed; branch reconciliation remains a separate controlled action.
- The P1 blueprint authority audit records the second recovery pass; the canonical v1.5 source remains unrecovered.

## 2026-11-17 — Chemistry scope second-pass review

- Scanned all 260 Chemistry subtopic names against the official Main 2027 Unit 13 Purification and Characterisation, Unit 20 Principles Related to Practical Chemistry and Unit 19 Biomolecules/vitamins scope.
- Found one existing chromatography topic, `C20_CH1_ST9`, nested under Metallurgy but correctly cross-mapped to Main Unit 13. Its parent unit/chapter are disabled, so it is not effectively enabled.
- No direct taxonomy labels were found for the other major Main Unit 13 purification/characterisation methods or for practical-chemistry exercises, salt analysis, functional-group detection and preparations. C27_CH3 Vitamins remains an empty chapter although Main Biomolecules includes vitamins.
- Added `P1_CHEMISTRY_COVERAGE_GAP_SECOND_PASS.md` and updated the unit-level and empty-chapter gap audits. No taxonomy IDs, parent paths or enablement flags were changed.
- These are inventory-level gap findings; actual external/prior catalogue content must still be inspected before proposing any new taxonomy IDs.

## 2026-11-17 — Physics Experimental Skills second-pass review

- Scanned all 233 Physics subtopic names against the 18 experiments/activities listed in official JEE Main 2027 Physics Unit 20 (NTA PDF page 5, lines 140–152).
- Found theory-level paths for many activities (simple pendulum, Young's modulus, surface energy/capillarity, viscosity/Stokes law, specific heat, meter bridge/resistivity, Ohm's law, galvanometer, optics, diode/Zener/LED), but the current taxonomy does not separately represent the required practical procedures, apparatus, observations, graphs and measurements.
- The metre-scale/moments experiment remains blocked by the two empty P5 chapters. No dedicated Experimental Skills hierarchy exists in the current internal unit list.
- Found and corrected one definite mapping error: `P10_CH1_ST8 — Simple Pendulum` was marked Main `NO_DIRECT_EXPLICIT_SCOPE`, but the official Main 2027 syllabus explicitly includes simple pendulum theory in Unit 10 and a simple-pendulum experiment in Unit 20. It is now `MAPPED_PROVISIONAL`; the stable UUID, all flags and `PENDING_INDEPENDENT_REVIEW` status are unchanged.
- Added `P1_PHYSICS_EXPERIMENTAL_SKILLS_SECOND_PASS.md`. This is an internal second pass, not independent human academic approval.
- Revalidated the mapping register after the correction: 1,026 rows; 1,026 unique codes and UUIDs; zero missing required fields; Main 2027 status totals 589 mapped / 130 partial / 307 no direct; Advanced 2026 totals unchanged at 688 mapped / 107 partial / 231 no direct; all 1,026 rows remain pending independent review; effective-enabled snapshot remains 26 TRUE / 1,000 FALSE.
- No production generation or enablement changes were made.

## MECP v1.2 P1 exit gate (verbatim acceptance conditions)\n\n- Pilot subtopic has an evidence-backed official syllabus mapping.\n- Required PYQ/source evidence is sufficient for meaningful analysis, or source gaps are explicitly accepted and bounded.\n- Rule authority is identified and conflicts are resolved or isolated from the pilot.\n- Taxonomy IDs and enablement state are traceable.\n- No pilot selection based solely on catalogue maturity.\n\nThe P1 deliverables also include the official source register, reconciled syllabus master, Main/Advanced applicability map, taxonomy/enablement report, PYQ source/acquisition/answer-key register, authoritative blueprint reference/rule crosswalk, and candidate pilot sequence with source confidence.\n\n## P1 work remaining

1. Independently validate the provisional Main/Advanced mappings against exact official syllabus wording; revalidate Advanced scope when the 2027 syllabus is published.
2. Complete independent academic review of all 67 internal units, 185 chapters and 1,026 subtopics, prioritising chapter-level inherited mappings and partial/no-direct cases; preserve IDs.
3. Validate the full parent/child enablement cascade and document disabled-parent/active-child anomalies without silently changing existing flags.
4. Continue the 247-record PYQ audit: reconcile 2026 shifts, source labels, local file status, hashes, answer-key sources and question-level matching. See `docs/p1/P1_PYQ_SOURCE_AUDIT.md`.
5. Acquire/verify source PDFs where legally and technically available; compute SHA-256 only after bytes are present.
6. Establish a canonical PYQ record schema with page/question-level provenance and separate answer-key verification state.
7. Recover the complete user-approved Blueprint v1.5 artifact or obtain explicit approval for a separately versioned recovery candidate. Reconcile all recovered rules and current code without merging namespaces.
8. Demonstrate every MECP v1.2 P1 acceptance gate before marking P1 complete.

## Exit gate

**NOT PASSED.** P1 remains ACTIVE. No production questions have been generated in this phase. No final syllabus mapping, complete PYQ verification, or authoritative blueprint freeze is claimed. Two 2026 Main question/key pairs have been independently solved and matched to official answer-key option IDs as provisional source evidence.


## 2026-11-17 mapping-register validation

- Rows: 1,026; unique subtopic codes: 1,026; unique subtopic IDs: 1,026; duplicate codes/IDs: 0.
- Required mapping fields missing: 0 (subject, subtopic ID/code, Main status, Advanced status, confidence, evidence, mapping basis, academic-review status).
- No row remains `UNREVIEWED`.
- Main 2027 dispositions across all subjects: 588 provisional mapped, 130 partial, 308 no direct explicit scope.
- Advanced 2026 dispositions across all subjects: 688 provisional mapped, 107 partial, 231 no direct explicit scope.
- Effective-enabled snapshot: 26 TRUE, 1,000 FALSE. These are preserved snapshots; no source curriculum enable flags were changed.
- All 1,026 rows remain `PENDING_INDEPENDENT_REVIEW`. The mapping-basis classification (chapter-level vs subtopic-level) is a review aid, not a claim of final academic verification.


## P1 acceptance-gate tracking

The MECP v1.2 activity/deliverable/exit criteria are now tracked explicitly in `docs/p1/P1_EXIT_GATE_CHECKLIST.md`. Overall P1 status remains **IN PROGRESS / EXIT GATE NOT PASSED**. The canonical frozen v1.5 authority is the current blocking decision; PYQ local bytes/hashes and independent taxonomy review also remain open.


## 2026-11-17 — PYQ tracker row-level reconciliation and acquisition retry

- Materialized and compared the two Library workbooks in the working environment: `JEE_PYQ_Phase2_1_Audited_Source_Registry.xlsx` and `JEE_PYQ_Phase2_2_2026_English_Acquisition_Registry.xlsx`.
- Both workbooks contain 247 rows and the exact same 247 unique `PYQ_ID` values in the same index order. The 2026 acquisition workbook is a 247-row master copy with a 21-record 2026 subset, not a separate 21-row-only workbook.
- Resolved the reported nine-record official-source discrepancy: the 9 April 2026 Main records have the same IDs and source URLs in both workbooks; only `Official Source Confirmed` labels differ. The Acquisition Tracker labels these nine records `Yes`, while the Audited Registry labels them `Yes — NTA archive exists`. Both workbooks have 66 non-`No` records in that field (11+26+29 versus 2+26+38). This is a classification-label difference, not nine missing/extra papers or a difference in source-record count.
- The 2026 Acquisition Tracker has 11 populated question-paper URLs (9 April Main + 2 Advanced) and 11 URL-access flags. The Audited Registry has zero populated PDF URL cells. Both still have zero Answer Key URL cells and zero SHA-256 cells; the 11 flags are not local-byte acquisition or hash verification.
- The ten January Main 2026 shift records remain without a populated question-paper URL in the acquisition tracker.
- Retried direct PDF downloads for Advanced 2026 Paper 1, Main 2026 April 2 Shift 1 and the official Main Session I final key. The working container failed DNS resolution for the official hosts. No PDF bytes were saved and no SHA-256 was calculated. This is a working-environment network limitation; it does not invalidate the official URLs previously verified through web access.
- No Library workbook was overwritten and no source IDs, taxonomy IDs, enablement flags or production code were changed.
