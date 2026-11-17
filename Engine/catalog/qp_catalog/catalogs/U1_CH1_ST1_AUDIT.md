# U1–CH1–ST1 Catalogue Audit — v1.2

**Repository:** `vinothkumarar/QuestionFactory`  
**Branch:** `feature/dual-question-engine-v1`  
**Subtopic:** Mathematics / U1 / CH1 / ST1  
**Source of truth:** `Engine/qpc/mathematics/U1_CH1.csv`

## Source reconciliation

- The source QPC contains 20 ST1 question possibilities: `U1_CH1_ST1_QP001` through `U1_CH1_ST1_QP020`.
- The source QPC was not modified.
- Eight concept groupings are recorded in `U1_CH1_ST1_concepts.csv`.
- QP016 is quarantined because its source text is malformed; no meaning is inferred.
- Fifty-two archetype candidates remain across the 19 interpretable QPs. All 52 rows carry machine-readable `approval_status=DRAFT_REQUIRES_ACADEMIC_REVIEW` and `manufacturing_enabled=FALSE` gates.

## Pairwise overlap pass

The first candidate list contained 57 rows. Five were removed before approval because they were duplicates, presentation-only variants, or belonged more naturally to another QP:

| Removed candidate | Reason |
|---|---|
| Initial AR00002 (QP001) | Selecting a formal definition is a response-format variant of recalling/recognizing the definition, not a distinct assessment mechanism |
| Initial AR00003 (QP001) | Zero-convention boundary is explicitly covered by QP013; cross-QP duplication |
| Initial AR00008 (QP003) | Set-builder recognition duplicates recognition of the integer-set definition |
| Initial AR00020 (QP007) | Sign/zero exclusion is the same membership test as direct non-natural identification |
| Initial AR00025 (QP009) | Selecting a non-integral member from a list is a presentation variant of determining non-integrality |

The retained candidates were re-numbered sequentially from `AR00001` to `AR00052` before catalogue release. These identifiers are now stable; do not renumber them in subsequent revisions. If a later audit rejects an item, retain its ID as deprecated rather than recycling it.

## Cross-QP review flags

These pairs are related and must be checked for genuine distinctness during the next academic review:

- QP001 / QP004: definition knowledge versus applying membership to a supplied value.
- QP004 / QP010 / QP012: target-set membership versus broad classification versus smallest-set classification.
- QP007 / QP008 / QP009: excluded-from-set identification for N, W and Z; preserve only where the target set changes the actual reasoning.
- QP018 / QP019 / QP020: statement evaluation, true/false classification and error diagnosis; do not create superficial variants of the same proposition test.
- QP013 / QP018: zero-specific convention statements versus general set-membership statements.

These are review flags, not automatic merges: distinct QPs may legitimately test different knowledge outcomes. Final decisions must compare the actual reasoning mechanism, not only the wording.

## QP016 quarantine

The source row is exactly:

`U1_CH1_ST1_QP016,U1_CH1_ST1,Boundary Classification (?1`

Repository search found no corroborating corrected wording. The trailing `?1` cannot safely be interpreted as `-1`, `+1`, or any other value. QP016 remains quarantined and must not be generated until the original catalogue author/source is checked.

## Scope controls

- Scope remains limited to Natural Numbers, Whole Numbers and Integers.
- Operational default for this India-focused JEE catalogue: **N = {1, 2, 3, ...}**, **W = {0, 1, 2, ...}**, and **Z = {..., -2, -1, 0, 1, 2, ...}**. This makes zero a whole number and integer, but not a natural number.
- Keep the natural-number convention configurable at subject/test level; if an approved source explicitly defines N to include zero, that test configuration overrides the default. Every generated item involving zero must inherit and state the active convention where ambiguity is possible.
- Broader sets, divisibility, primes, HCF/LCM and unrelated Number System topics must not be imported into ST1.
- JEE fit and difficulty fields are candidate assessments, not official syllabus mapping approval.

## Structural validation

| Check | Result |
|---|---:|
| Source ST1 QPs | 20 |
| Interpretable QPs | 19 |
| Concept rows | 8 |
| Retained archetype candidates | 52 |
| Candidate rows marked draft | 52 |
| Candidate rows manufacturing-enabled | 0 |
| Distinct sequential archetype IDs | 52 |
| ID range | AR00001–AR00052 |
| QP016 | QUARANTINED |
| Source QPC modifications | None |

## Important quality limitation

The current `assessment_mechanism` and `reasoning_path` columns were populated as structured draft descriptions. Some use broad templates and are not yet sufficiently specific to serve as final academic approval evidence. They must be rewritten or verified against each archetype's actual mathematical reasoning before manufacturing is enabled. The registry now carries an explicit machine-readable approval gate: all rows are DRAFT and manufacturing is FALSE.

## Release status

**ST1 catalogue remains DRAFT / NOT APPROVED FOR MANUFACTURING.**

Next autonomous gate:
1. Rewrite and validate the 52 assessment mechanisms and reasoning paths individually.
2. Complete the flagged cross-QP distinctness review.
3. Resolve QP016 from an authoritative source if possible.
4. Run repository tests and catalogue validation.
5. Only then enable the first Foundation manufacturing batch.

No question instances have been generated by this catalogue audit.


## Autonomous simplification pass — v1.2

To prevent speculative archetype expansion from delaying production, the registry has been reorganized without deleting or recycling any existing IDs.

- **19 core candidates** remain, one for each interpretable source QP (QP001–QP015 and QP017–QP020).
- **33 additional candidates** are retained but parked with `approval_status=PARKED_NOT_YET_JUSTIFIED_BY_SOURCE_QP`. They are not treated as approved archetypes and cannot enter manufacturing.
- The 19 core rows now have QP-specific assessment mechanisms, reasoning paths and variation dimensions. Generic template reasoning has been replaced with descriptions tied to the actual N/W/Z membership task.
- Difficulty claims have been made conservative: core candidates are tagged FOUNDATION or MODERATE and JEE_MAIN only. No JEE_ADVANCED, HARD or ELITE suitability is claimed at this stage.
- All 52 rows remain `manufacturing_enabled=FALSE`. The 19 core candidates remain drafts pending academic review; this simplification is not an approval to manufacture.
- Existing archetype IDs are preserved. Parked IDs must not be reused; a later review may restore a parked candidate only with a documented distinct reasoning mechanism and evidence from the source QP or an approved expanded QP specification.

### Why this is the faster safe route

The source QPC provides short possibility labels, not detailed sub-archetype specifications. It is therefore safer to start with one defensible core mechanism per source QP, generate and validate representative questions, and add a secondary archetype only when question analysis demonstrates a genuinely different cognitive operation. This avoids manufacturing complexity unsupported by the source while preserving room to expand later.

### Remaining release gates

1. Confirm the natural-number zero convention as a configurable, explicit syllabus setting.
2. Resolve malformed QP016 from an authoritative source; until then it remains excluded.
3. Perform academic review of the 19 core candidates and cross-QP boundaries.
4. Run the repository's actual catalogue validators/tests before enabling manufacturing.
5. Pilot a small Foundation batch from the approved core candidates, then expand by demonstrated need.

**Current status: 19 streamlined core drafts + 33 parked candidates; zero manufacturing-enabled rows.**


### Operational convention decision

To avoid blocking catalogue work on a convention debate, the project adopts the common school-level convention used for this India-focused JEE workflow: N is positive counting numbers, W includes zero, and Z includes all signed integers. This is a configurable project default, not a claim that every textbook or source uses identical notation. The generator and question metadata must carry the active convention; no question may rely on an unstated convention.
