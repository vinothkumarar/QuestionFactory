# P1 Exit Gate Checklist — MECP v1.2

**Audit date:** 2026-11-17  
**Actual P1 start:** 2026-11-17 (one calendar day ahead of the MECP planned start of 2026-11-18)  
**Planned P1 window:** 2026-11-18 to 2026-11-26 (7 working days)  
**Overall status:** **NOT PASSED — P1 IN PROGRESS**

This checklist applies the P1 activities, deliverables and exit gate in `Question_Factory_OS_v3_MECP_v1.2.md`. A provisional disposition is not final academic approval.

## 1. P1 activities

| # | MECP v1.2 activity | Current status | Evidence / remaining work |
|---:|---|---|---|
| 1 | Verify latest official Main and Advanced syllabi | PARTIAL PASS | Main 2027 official NTA PDF verified. Advanced 2027 remains Coming Soon; official 2026 PDF used as provisional baseline. Revalidate on publication. |
| 2 | Record publisher, URL, publication/session, retrieval, local file, SHA-256 | PARTIAL | Official URLs and access status recorded. Local PDF bytes and SHA-256 still pending for PYQ source files. |
| 3 | Build authoritative Subject→Unit→Chapter→Subtopic hierarchy with separate Main/Advanced applicability | INITIAL CROSSWALK COMPLETE | All 1,026 subtopic rows have provisional Main/Advanced dispositions; all remain PENDING_INDEPENDENT_REVIEW. |
| 4 | Reconcile Mathematics U1–U15, Physics P1–P23, Chemistry C1–C29 | PARTIAL | All current subtopic rows have dispositions. Chapter-level inherited mappings and partial/no-direct topics need independent academic review; 6 empty chapters remain gaps. |
| 5 | Reconcile parent/child enable flags | PARTIAL | Effective-enabled snapshot is 26 TRUE / 1,000 FALSE. Empty chapters and scope gaps are documented. Full parent-child cascade audit still required. |
| 6 | Preserve historical taxonomy IDs and record mappings | PASS — CURRENT SNAPSHOT | 1,026 unique subtopic codes and IDs; zero duplicates in the mapping register. No source curriculum tables or stable IDs were changed during P1. |
| 7 | Audit PYQ inventory 2002–2026; separate IIT-JEE/AIEEE from Main/Advanced | INVENTORY PASS; ACQUISITION PARTIAL | 247 inventory rows reconciled: Main 185, Advanced 28, IIT-JEE 21, AIEEE 13. Paper acquisition and historical source validation remain incomplete. |
| 8 | Record paper/session/question/page/source/URL/hash/key/match/confidence | PARTIAL | Two 2-Apr-2026 Shift 1 questions have official question-ID/option-ID matches and independent solutions. All 19 Main shift records now have official session-level key source URLs in `P1_2026_SESSION_KEY_LINKAGE.csv`, and both Advanced papers have official final-key URLs. Most records still lack local bytes, hashes and question-level key matching. |
| 9 | Reconcile workbook inventory with QuestionEngine source status and README claims | PARTIAL | 247 unique IDs in acquisition/audited trackers. The nine-row official-source label mismatch is reconciled; 11 paper URLs are URL-access-verified. The original workbook still has no Answer Key URL or SHA-256 values; the derived linkage register records all 21 official key URLs. |
| 10 | Resolve authoritative frozen blueprint source and rule crosswalk | BLOCKED | v1.5 fragments recovered, but complete canonical v1.5 artifact is missing. Repository rule namespaces and schemas conflict. |
| 11 | Record unresolved mappings as explicit unknowns | PASS | Partial/no-direct mappings, empty chapters, unavailable PDFs, missing hashes and unknown blueprint thresholds are explicitly recorded. |

## 2. P1 deliverables

| Deliverable | Status | Evidence |
|---|---|---|
| Official syllabus source register and local evidence/hashes where obtainable | PARTIAL | `P1_OFFICIAL_SYLLABUS_SOURCE_AUDIT.md`; Main/Advanced official URLs verified, PYQ local hashes pending |
| Reconciled syllabus master and Main/Advanced applicability map | INITIAL CROSSWALK COMPLETE; REVIEW PENDING | `P1_TAXONOMY_MAPPING_REGISTER.csv`; 1,026 rows, all provisional |
| Taxonomy reconciliation and enablement report | PARTIAL | `P1_UNIT_LEVEL_TAXONOMY_RECONCILIATION.md`, subject scope docs, `P1_EMPTY_CHAPTER_AND_COVERAGE_GAP_AUDIT.md` |
| PYQ source/acquisition/answer-key register | PARTIAL | `P1_PYQ_SOURCE_AUDIT.md`, `P1_PYQ_ANSWER_KEY_AUDIT.md`, `P1_PYQ_EVIDENCE_REGISTER.csv` |
| Authoritative blueprint reference and rule crosswalk | BLOCKED | `P1_BLUEPRINT_AUTHORITY_AUDIT.md`; original v1.5 source artifact not located |
| Candidate pilot sequence with source confidence | CANDIDATE ONLY | `P1_CANDIDATE_PILOT_SEQUENCE.md`; no pilot or production order authorised |

## 2A. Additional second-pass evidence — 2026-11-17

- `P1_SAMPLE_MAPPING_SECOND_PASS.md` reviews all four question-level PYQ samples against the internal taxonomy, official scope and parent-chain enablement. It is an internal second pass, not independent human academic sign-off.
- `P1_CHEMISTRY_COVERAGE_GAP_SECOND_PASS.md` scans all 260 Chemistry subtopic names and records the cross-unit chromatography entry, the remaining Main Unit 13 gaps, Practical Chemistry coverage gaps and empty Vitamins chapter.
- The Chemistry gap audit now distinguishes partial Unit 13 coverage from a wholly absent taxonomy path. No IDs, parent paths or enablement flags were changed.

## 2B. Physics Experimental Skills second-pass evidence — 2026-11-17

- `P1_PHYSICS_EXPERIMENTAL_SKILLS_SECOND_PASS.md` crosswalks the 18 official Main 2027 Physics Unit 20 activities against existing Physics taxonomy paths.
- Related theory topics exist for many activities, but practical procedures/apparatus/observations/graphs are not represented as a dedicated Experimental Skills hierarchy. The P5 metre-scale/moments activity is additionally affected by two empty chapters.
- Corrected the explicit Main simple-pendulum mapping for `P10_CH1_ST8` from `NO_DIRECT_EXPLICIT_SCOPE` to `MAPPED_PROVISIONAL`, based on NTA 2027 Physics Unit 10 and Unit 20 wording. UUID, flags and pending academic-review status were preserved.
- Revalidated structural totals: Main 2027 = 589 mapped, 130 partial, 307 no direct; Advanced 2026 unchanged = 688 mapped, 107 partial, 231 no direct. All 1,026 rows remain pending independent review.

## 3. Mapping register structural validation

- Total rows: 1,026.
- Unique subtopic codes: 1,026.
- Unique subtopic IDs: 1,026.
- Duplicate codes/IDs: 0.
- Missing required mapping fields: 0.
- Main status totals: 589 provisional mapped, 130 partial, 307 no direct explicit scope.
- Advanced status totals: 688 provisional mapped, 107 partial, 231 no direct explicit scope.
- Mapping basis: 285 chapter-level provisional, 155 chapter-level no-direct, 524 subtopic-level provisional, 52 subtopic-level no-direct, 10 cross-unit/subject.
- All 1,026 rows: `PENDING_INDEPENDENT_REVIEW`.
- Effective-enabled snapshot: 26 TRUE, 1,000 FALSE.

The mapping-basis categories are a review aid; they do not mean that all 1,026 subtopics have passed independent academic validation.

## 4. PYQ evidence status

- Master inventory: 247 records covering 2002–2026.
- 2026 subset: 21 records (19 JEE Main, 2 JEE Advanced).
- 11 official question-paper URLs are marked accessible (9 April Main shifts, 2 Advanced papers).
- 10 January 2026 Main shifts remain without an acquired/verified paper URL in the tracker.
- Main Session I and II final answer-key PDFs are linked to all 19 Main shifts at session level in `P1_2026_SESSION_KEY_LINKAGE.csv`.
- Four questions are matched and independently solved: two Main questions from 2 April 2026 Shift 1, Advanced Paper 1 Q3 and Advanced Paper 2 Q1.
- Local PDF bytes and SHA-256 values remain pending; no bulk answer-key reconciliation is claimed.

## 5. Blueprint authority status

Recovered from prior conversations: v1.5 R01–R12 names/intent, AR01–AR20 names, DR01–DR12 names, AR-01 saturation intent, BS-01 batch size 10, and partial DI/META/CM/PYQ/SV/QE/RL/EDF rules.

Still missing: complete original v1.5 file, exact saturation thresholds, full archetype definitions/quotas, full DE/DR definitions, complete schema and exact difficulty/distribution tables. The current repo contains conflicting legacy and prompt registries.

**No production questions may be generated until this authority blocker is resolved or explicitly isolated by an approved P1 exit decision.**

## 6. P1 exit gate — MECP v1.2

| Exit criterion | Status | Reason |
|---|---|---|
| Pilot subtopic has evidence-backed official syllabus mapping | PARTIAL | Candidate Physics P1_CH1_ST4/ST6 map to explicit Main/Advanced baseline scope; independent review pending |
| Required PYQ/source evidence sufficient for meaningful analysis, or gaps explicitly accepted and bounded | PARTIAL | Two matched questions from one shift; local bytes/hashes and broader representativeness remain incomplete |
| Rule authority identified and conflicts resolved or isolated from pilot | BLOCKED | Canonical v1.5 artifact missing; current registries conflict; no production use |
| Taxonomy IDs and enablement state traceable | PASS — CURRENT SNAPSHOT | Unique IDs/codes, enablement snapshot and gap register exist |
| Pilot not selected solely from catalogue maturity | PASS | Candidate selection uses official scope and matched PYQ evidence, not catalogue size |

<badge color="danger">P1 exit gate NOT PASSED</badge>

## 7. Next actions

1. Resolve the canonical frozen v1.5 source: locate the original file or explicitly approve a separately versioned recovery candidate from verified fragments.
2. Independently review the chapter-level provisional taxonomy mappings and all partial/no-direct exceptions.
3. Complete parent/child enablement cascade validation and document any disabled-parent/active-child anomalies.
4. Continue official PYQ acquisition; obtain local bytes and hashes where available.
5. Link answer keys to exact paper/shift/question IDs; expand beyond the two-question sample.
6. Reconcile the 25/26/29-column schema variants, JSON output contract and latest simplified CSV rule without changing production code during P1.
7. Revalidate Advanced mapping when the official 2027 syllabus is published.

**No P1 completion claim, production-question generation, schema mutation, taxonomy renumbering or bulk enablement change is authorised by this checklist.**


## 2C. PYQ tracker reconciliation — 2026-11-17

- Raw comparison of the 247-row Acquisition Tracker and 247-row Audited Source Registry confirms identical 247 `PYQ_ID` values and no row-level ID differences.
- The nine official-source label differences are exactly the nine April 2026 Main shift rows (`Yes` vs `Yes — NTA archive exists`). Aggregate non-No count is 66 in both trackers. The discrepancy is CLOSED as a label-only mismatch; canonical field normalization remains pending.
- The 2026 Acquisition Tracker is a 247-row master workbook containing a 21-row 2026 subset, not a 21-row-only workbook.
- Eleven question-paper URLs remain URL-access-verified only; no local PDF bytes or hashes are present. Answer Key URL cells remain empty in both trackers.
- Direct download retries failed due to DNS resolution in the working container; no local bytes/hash are claimed.

## 6. Updated P1 evidence disposition — 2026-11-17

**Closed in this pass:** Nine-row official-source label discrepancy is explained by exact row-level comparison; both workbooks contain the same 247 IDs and the same aggregate 66 non-No source-confirmation records.

**Still open:** Derived canonical source-label normalization, 2026 answer-key URL linkage, 10 January Main PDF sourcing, local PDF acquisition and SHA-256, broad question/key matching, full taxonomy academic review, and canonical Blueprint v1.5 authority.

**P1 remains IN PROGRESS — EXIT GATE NOT PASSED.**


## 2D. Official 2026 answer-key source linkage — 2026-11-17

- Session I final key covers the 10 January Main shifts; Session II final key covers the 9 April Main shifts. Both Advanced 2026 final-key PDFs are identified.
- Derived register `P1_2026_SESSION_KEY_LINKAGE.csv` contains all 21 2026 records with official answer-key source URLs. This closes session/paper-level key-source linkage, not full question-level matching.
- Four question-level matches are independently verified. Remaining question-level matching is pending.
- Original Library workbook is unchanged; its Answer Key URL column remains empty. Local PDF bytes and hashes remain pending.
