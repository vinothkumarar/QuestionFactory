# U2–CH8–ST1 Archetype Batch 001 — Real Matrix

**Source catalogue:** `Engine/catalog/qp_catalog/catalogs/U2_CH8_ST1.json`  
**Source QP range processed:** C001 / QP001–QP010  
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


## Batch 002 disposition extension — QP006–QP010

The next five QPs were reviewed and retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| QP006 | Transpose of a real matrix | Transpose reorders entries; realness is preserved directly |
| QP007 | Complex conjugation / conjugate transpose | For real entries, conjugation leaves entries unchanged; direct property recognition |
| QP008 | Inverse of an invertible real matrix | Standard inverse property; the source statement alone does not establish a distinct reasoning mechanism |
| QP009 | Polynomial/rational expressions in real matrices | Direct closure under defined operations with real coefficients |
| QP010 | Trace, determinant, minors and cofactors | Direct sums/products of real entries |

No additional archetypes were added. The two Batch 001 candidate IDs remain unchanged. The catalogue now contains 10 explicit QP dispositions and 2 draft archetypes; the remaining 340 QPs are untouched.

**Next:** review QP011–QP015 against the two existing candidate mechanisms and preserve zero-archetype dispositions where no distinct reasoning is justified.


## Batch 003 disposition extension — QP011–QP015

The next five source possibilities were reviewed and retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| QP011 | Inclusion hierarchy of integer/rational/real/complex matrix sets | Direct scalar-set hierarchy applied entrywise |
| QP012 | Count independent real parameters in an m×n real matrix | Direct count of mn independently selectable entries |
| QP013 | Interpret real-matrix set notation | Notation recognition |
| C002 / QP001 | Classify real versus complex matrix from entries | Direct definition-level recognition |
| C002 / QP002 | Compute the complex conjugate of a matrix | Direct entrywise operation |

No additional archetypes were added. The catalogue now has 15 explicit dispositions and retains the two draft candidate archetypes from QP002 and QP005. The remaining 335 source QPs are untouched.

**Next:** review C002 / QP003–QP007. Check whether Hermitian, skew-Hermitian and unitary conditions create genuinely distinct mechanisms before adding any archetype.


## Batch 004 disposition and archetype extension — C002 / QP003–QP007

| QP | Disposition | Reason |
|---|---|---|
| QP003 | FOUNDATION_ONLY | Conjugate transpose is a direct entrywise operation |
| QP004 | FOUNDATION_ONLY | Hermitian verification is a direct comparison with the conjugate transpose |
| QP005 | FOUNDATION_ONLY | Skew-Hermitian verification is the sign counterpart of the Hermitian check, not a separate reasoning mechanism |
| QP006 | ELIGIBLE | Unitary verification requires checking the conjugate-transpose product against the identity |
| QP007 | ELIGIBLE | Parameter constraints for Hermitian/skew-Hermitian/unitary conditions require simultaneous real/imaginary equations |

Two additional draft candidates have been created:

- `U2_CH8_ST1_AR00003`: Verify unitarity through the conjugate-transpose identity.
- `U2_CH8_ST1_AR00004`: Derive parameter constraints for Hermitian, skew-Hermitian or unitary structure.

Both are JEE Main candidates only, with Moderate/Hard potential, and remain `DRAFT_CORE_REQUIRES_ACADEMIC_REVIEW` with `manufacturing_enabled=FALSE`.

The cumulative catalogue now has 20 QP dispositions and 4 draft archetypes. The remaining 330 QPs are untouched.


## Batch 005 — complex-matrix structural mechanisms (C002 / QP008–QP012)

| QP | Disposition | Reason |
|---|---|---|
| QP008 | ELIGIBLE | Canonical decomposition into Hermitian and skew-Hermitian components is a reusable construction |
| QP009 | FOUNDATION_ONLY | Scalar multiplication effects are direct consequences of adjoint identities |
| QP010 | FOUNDATION_ONLY | Sum/difference type outcomes are direct closure checks |
| QP011 | ELIGIBLE | Product/inverse structure requires adjoint reversal and commutativity/invertibility checks |
| QP012 | FOUNDATION_ONLY | The adjoint identities themselves are foundational rules; the multi-step application is represented by QP011 |

New draft candidates:

- `U2_CH8_ST1_AR00005`: Decompose a complex matrix into Hermitian and skew-Hermitian components.
- `U2_CH8_ST1_AR00006`: Infer product or inverse structure using adjoint reversal and commutativity.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled. The cumulative catalogue now contains 25 dispositions and 6 archetypes; 325 source QPs remain untouched.
