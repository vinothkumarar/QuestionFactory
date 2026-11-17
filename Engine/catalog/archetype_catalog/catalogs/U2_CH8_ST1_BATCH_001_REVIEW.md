# U2–CH8–ST1 Archetype Batch 001 — Real Matrix

**Source catalogue:** `Engine/catalog/qp_catalog/catalogs/U2_CH8_ST1.json`  
**Source QP range processed:** C001 / QP001–QP005  
**Source QP catalogue size:** 350 possibilities across 27 concepts  
**Status:** Draft archetype candidates; academic approval pending; manufacturing disabled

## Disposition decisions

| QP | Disposition | Rationale |
|---|---|---|
| QP001 | FOUNDATION_ONLY | Direct recognition of real entries is definition-level classification |
| QP002 | ELIGIBLE | Simultaneous reality constraints across parameterized matrix entries form a reusable parameter-constraint mechanism |
| QP003 | FOUNDATION_ONLY | Addition/subtraction closure is a direct entrywise property |
| QP004 | FOUNDATION_ONLY | Product/integer-power closure is a direct consequence of real arithmetic |
| QP005 | ELIGIBLE | Reality of a linear combination can require coefficient constraints and matrix independence/dependence reasoning |

## Draft archetypes

### U2_CH8_ST1_AR00001 — Simultaneous reality constraints in a parameterized matrix

- Source: C001 / QP002.
- Core operation: set the imaginary part of every matrix entry to zero and solve the simultaneous parameter constraints.
- Difficulty potential: Moderate.
- Exam fit: JEE Main candidate only.
- Distinctness: differs from direct classification because multiple entry constraints may interact and require a simultaneous solution.

### U2_CH8_ST1_AR00002 — Reality of a linear combination of real matrices

- Source: C001 / QP005.
- Core operation: express the imaginary component of the linear combination as a matrix equation and use the stated linear independence/dependence of the matrices to constrain scalar coefficients.
- Difficulty potential: Moderate.
- Exam fit: JEE Main candidate only.
- Distinctness: coefficient constraints in a matrix combination are not the same as forcing the entries of one parameterized matrix to be real.

## Controls

- Both archetypes are draft candidates, not academically approved.
- `approval_status=DRAFT_CORE_REQUIRES_ACADEMIC_REVIEW`.
- `manufacturing_enabled=FALSE`.
- No question instances have been generated.
- QP001, QP003 and QP004 are retained in the disposition CSV and do not receive artificial archetypes.
- Only the first five QPs are dispositioned. The remaining 345 source QPs are untouched and will be processed in later batches.
- Factory-assigned IDs are stable: `U2_CH8_ST1_AR00001` and `U2_CH8_ST1_AR00002`.

## Next batch

Continue with QP006–QP010. Compare every candidate against the two existing mechanisms before adding a new archetype. Merge duplicate reasoning, keep zero-archetype dispositions where appropriate, and preserve the source QP metadata exactly.
