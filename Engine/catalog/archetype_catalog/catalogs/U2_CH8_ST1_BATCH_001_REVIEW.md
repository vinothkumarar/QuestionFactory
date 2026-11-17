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


## Batch 006 — unitary characterizations and row-matrix basics (global QP026–QP030)

All five possibilities were retained as `FOUNDATION_ONLY`:

| Concept / QP | Source mechanism | Disposition rationale |
|---|---|---|
| C002 / QP013 | Characterize unitarity through orthonormal rows/columns | Equivalent to the existing unitarity identity; do not duplicate QP006 |
| C002 / QP014 | Diagonal and trace constraints for Hermitian/skew-Hermitian matrices | Consequence of definitions; overlaps the parameter-constraint candidate |
| C002 / QP015 | Real symmetric/skew-symmetric/orthogonal correspondences | Direct conceptual mapping to complex matrix classes |
| C003 / QP001 | Identify a row matrix | Direct shape definition |
| C003 / QP002 | Row-matrix order/indexing constraints | Direct dimensional interpretation |

No archetypes were added. The cumulative catalogue now contains 30 dispositions and retains 6 draft archetypes. The remaining 320 source QPs are untouched.


## Batch 007 — row-matrix possibilities (global QP031–QP035)

All five possibilities are retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| C003 / QP003 | Parameter conditions for row-matrix shape | Direct order constraint |
| C003 / QP004 | Construct a row matrix | Direct representation |
| C003 / QP005 | Row matrix also square/column | Definition-level 1×1 order check |
| C003 / QP006 | Equality with a given row matrix | Direct order and entrywise equality |
| C003 / QP007 | Addition/scalar-multiplication closure | Direct shape-preserving closure |

No new archetypes were added. Cumulative status: 35 dispositions, 6 draft archetypes, and 315 source QPs not yet dispositioned.


## Batch 008 — column-matrix possibilities (global QP036–QP040)

All five possibilities are retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| C004 / QP001 | Identify a column matrix | Direct one-column definition |
| C004 / QP002 | Construct a column matrix | Direct representation |
| C004 / QP003 | Equality of column matrices | Order and entrywise equality |
| C004 / QP004 | Transpose of a column matrix | Direct row/column shape transformation |
| C004 / QP005 | Operation compatibility for column matrices | Basic dimension compatibility |

No new archetypes were added. Cumulative status: 40 dispositions and 6 draft archetypes; 310 source QPs remain.


## Batch 009 — further column-matrix possibilities (global QP041–QP045)

All five possibilities are retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| C004 / QP006 | Result order/type for expressions involving column matrices | Routine dimension arithmetic |
| C004 / QP007 | Parameter conditions for column-matrix order | Direct order-definition constraint |
| C004 / QP008 | When a column matrix is square | 1×1 order check |
| C004 / QP009 | Extract a specified column | Direct representation/indexing |
| C004 / QP010 | Relate order and element count | Direct order interpretation |

No new archetypes were added. Cumulative status: 45 dispositions, 6 draft archetypes, 305 QPs remain untouched.


## Batch 010 — rectangular-matrix possibilities (global QP046–QP050)

All five possibilities are retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| C005 / QP001 | Classify rectangular matrix | Direct comparison of row/column counts |
| C005 / QP002 | Distinguish row/column/general rectangular matrix | Direct order interpretation |
| C005 / QP003 | Determine possible orders from constraints | Routine dimension/integer reasoning |
| C005 / QP004 | Addition/subtraction compatibility | Equal-order check |
| C005 / QP005 | Product compatibility and resulting order | Inner-dimension rule |

No new archetypes were added. Cumulative status: 50 dispositions, 6 draft archetypes; 300 QPs remain untouched.


## Batch 011 — rectangular-matrix operation constraints (global QP051–QP055)

| QP | Disposition | Reason |
|---|---|---|
| C005 / QP006 | FOUNDATION_ONLY | Basic order compatibility for self-operations and transpose |
| C005 / QP007 | FOUNDATION_ONLY | Applicability of square-only properties is a direct order check |
| C005 / QP008 | FOUNDATION_ONLY | Transpose swaps row/column counts directly |
| C005 / QP009 | ELIGIBLE | Multiple operation-definedness constraints can be combined to infer unknown dimensions |
| C005 / QP010 | FOUNDATION_ONLY | Identity-matrix order compatibility follows directly from dimensions |

New draft candidate:

- `U2_CH8_ST1_AR00007`: Infer matrix dimensions from operation-definedness constraints.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 55 dispositions and 7 draft archetypes; 295 source QPs remain untouched.


## Batch 012 — square-matrix foundations (global QP056–QP060)

All five possibilities are retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| C006 / QP001 | Classify square matrix and state order | Direct shape definition |
| C006 / QP002 | Parameter conditions for squareness | Simple row/column equality; overlaps dimension inference |
| C006 / QP003 | Determine whether a matrix expression is square | Routine dimension tracking; no distinct mechanism established |
| C006 / QP004 | Applicability of square-only constructs | Direct prerequisite check |
| C006 / QP005 | Identify principal/secondary diagonal | Direct positional recognition |

No new archetypes were added. Cumulative status: 60 dispositions, 7 draft archetypes; 290 source QPs remain untouched.


## Batch 013 — square-matrix counts, closure and block structure (global QP061–QP065)

| QP | Disposition | Reason |
|---|---|---|
| C006 / QP006 | FOUNDATION_ONLY | Direct counting of diagonal/off-diagonal positions |
| C006 / QP007 | FOUNDATION_ONLY | Direct closure properties of square matrices |
| C006 / QP008 | FOUNDATION_ONLY | Square-only property inference overlaps the existing dimension-inference candidate |
| C006 / QP009 | ELIGIBLE | Combining block-row and block-column sizes to impose squareness is a distinct constraint mechanism |
| C007 / QP001 | FOUNDATION_ONLY | Direct zero-matrix definition check |

New draft candidate:

- `U2_CH8_ST1_AR00008`: Infer square block-matrix conditions from partition dimensions.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 65 dispositions and 8 draft archetypes; 285 source QPs remain untouched.


## Batch 014 — zero-matrix properties and zero-product reasoning (global QP066–QP070)

| QP | Disposition | Reason |
|---|---|---|
| C007 / QP002 | FOUNDATION_ONLY | Entrywise zero equations for parameterized matrices |
| C007 / QP003 | FOUNDATION_ONLY | Zero-matrix order compatibility |
| C007 / QP004 | FOUNDATION_ONLY | Additive identity simplification |
| C007 / QP005 | FOUNDATION_ONLY | Direct zero-product property |
| C007 / QP006 | ELIGIBLE | Refuting AB=O ⇒ A=O or B=O using nonzero matrix zero divisors requires a distinct counterexample/nullspace mechanism |

New draft candidate:

- `U2_CH8_ST1_AR00009`: Disprove the zero-product implication with nonzero matrices.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 70 dispositions and 9 draft archetypes; 280 source QPs remain untouched.


## Batch 015 — zero-matrix scalar, transpose, structure and power properties (global QP071–QP075)

| QP | Disposition | Reason |
|---|---|---|
| C007 / QP007 | FOUNDATION_ONLY | Scalar zero/nonzero case split is a direct property check |
| C007 / QP008 | FOUNDATION_ONLY | Transpose swaps order while preserving zero entries |
| C007 / QP009 | FOUNDATION_ONLY | Structural classifications follow by direct substitution |
| C007 / QP010 | FOUNDATION_ONLY | Zero determinant/trace are direct definition consequences |
| C007 / QP011 | ELIGIBLE | Integer powers require positive/zero/negative exponent and definedness/invertibility distinctions |

New draft candidate:

- `U2_CH8_ST1_AR00010`: Classify zero-matrix integer powers by exponent and order conditions.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 75 dispositions and 10 draft archetypes; 275 source QPs remain untouched.


## Batch 016 — zero-matrix identities and diagonal-matrix parameter constraints (global QP076–QP080)

| QP | Disposition | Reason |
|---|---|---|
| C007 / QP012 | FOUNDATION_ONLY | Zero matrix is singular; inverse does not exist |
| C007 / QP013 | FOUNDATION_ONLY | Uniqueness follows by entrywise equality |
| C007 / QP014 | FOUNDATION_ONLY | A−B=O iff A=B is a direct equality identity |
| C008 / QP001 | FOUNDATION_ONLY | Diagonal recognition is a direct off-diagonal zero check |
| C008 / QP002 | ELIGIBLE | Simultaneous zero constraints on off-diagonal entries produce a reusable parameter-constraint mechanism |

New draft candidate:

- `U2_CH8_ST1_AR00011`: Derive parameter constraints for a matrix to be diagonal.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 80 dispositions and 11 draft archetypes; 270 source QPs remain untouched.


## Batch 017 — diagonal-matrix operations (global QP081–QP085)

| QP | Disposition | Reason |
|---|---|---|
| C008 / QP003 | FOUNDATION_ONLY | Singularity reduces to zero/nonzero diagonal entries |
| C008 / QP004 | FOUNDATION_ONLY | Inverse is obtained by reciprocating nonzero diagonal entries |
| C008 / QP005 | FOUNDATION_ONLY | Closure/commutativity are direct diagonal-matrix properties |
| C008 / QP006 | ELIGIBLE | Powers/polynomials reduce to scalar evaluations on diagonal entries |
| C008 / QP007 | ELIGIBLE | Left/right diagonal multiplication performs row/column scaling |

New draft candidates:

- `U2_CH8_ST1_AR00012`: Evaluate powers and polynomial expressions of a diagonal matrix.
- `U2_CH8_ST1_AR00013`: Track row and column scaling under diagonal matrix multiplication.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 85 dispositions and 13 draft archetypes; 265 source QPs remain untouched.


## Batch 018 — diagonal equations and scalar-matrix structure (global QP086–QP090)

| QP | Disposition | Reason |
|---|---|---|
| C008 / QP008 | ELIGIBLE | Diagonal matrix equations reduce to simultaneous scalar constraints on diagonal entries |
| C008 / QP009 | ELIGIBLE | Universal commutativity forces equality of all diagonal entries; test with off-diagonal matrix units |
| C009 / QP001 | FOUNDATION_ONLY | Direct scalar-matrix recognition |
| C009 / QP002 | FOUNDATION_ONLY | Direct distinction among scalar, diagonal and identity definitions |
| C009 / QP003 | ELIGIBLE | Parameterized scalar-matrix constraints require zero off-diagonal entries and equal diagonal entries |

New draft candidates:

- `U2_CH8_ST1_AR00014`: Solve diagonal-entry constraints from a diagonal matrix equation.
- `U2_CH8_ST1_AR00015`: Characterize diagonal matrices that commute with every matrix.
- `U2_CH8_ST1_AR00016`: Derive scalar-matrix conditions from a parameterized matrix.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 90 dispositions and 16 draft archetypes; 260 source QPs remain untouched.


## Batch 019 — scalar-matrix properties (global QP091–QP095)

All five possibilities are retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| C009 / QP004 | Construct a scalar matrix | Direct definition |
| C009 / QP005 | Equivalent scalar-matrix characterizations | Overlaps the universal-commutativity candidate |
| C009 / QP006 | Add/multiply scalar matrices | Direct scalar arithmetic |
| C009 / QP007 | Multiply arbitrary matrix by scalar matrix | Uniform scaling; universal commutation already represented |
| C009 / QP008 | Inverse of scalar matrix | Direct nonzero-scalar condition and reciprocal formula |

No new archetypes were added. Cumulative status: 95 dispositions and 16 draft archetypes; 255 source QPs remain untouched.


## Batch 020 — scalar-matrix powers, invariants and property classification (global QP096–QP100)

| QP | Disposition | Reason |
|---|---|---|
| C009 / QP009 | FOUNDATION_ONLY | Scalar-matrix powers reduce to scalar powers |
| C009 / QP010 | FOUNDATION_ONLY | Adjugate follows a standard order-dependent formula |
| C009 / QP011 | FOUNDATION_ONLY | Determinant/trace are direct formulas |
| C009 / QP012 | FOUNDATION_ONLY | Rank/nullity/singularity reduce to λ=0 versus λ≠0 |
| C009 / QP013 | ELIGIBLE | Multiple matrix properties reduce to scalar equations in λ, creating a reusable parameter-classification mechanism |

New draft candidate:

- `U2_CH8_ST1_AR00017`: Classify scalar-matrix properties through scalar parameter equations.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 100 dispositions and 17 draft archetypes; 250 source QPs remain untouched.


## Batch 021 — scalar-matrix parameter follow-ups and identity recognition (global QP101–QP105)

All five possibilities are retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| C009 / QP014 | Infer scalar value from constraints | Direct parameter identification; overlaps AR00017 |
| C009 / QP015 | Count scalar matrices under entry constraints | Counting admissible scalar values; no distinct mechanism established |
| C009 / QP016 | Existence/uniqueness of constrained scalar matrix | Overlaps scalar-parameter equation candidate |
| C009 / QP017 | Polynomial in a scalar matrix | Direct reduction to p(λ)I |
| C010 / QP001 | Identify identity matrix | Direct definition check |

No new archetypes were added. Cumulative status: 105 dispositions and 17 draft archetypes; 245 source QPs remain untouched.


## Batch 022 — identity-matrix fundamentals (global QP106–QP110)

All five possibilities are retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| C010 / QP002 | Construct identity matrix | Direct definition |
| C010 / QP003 | Identity order compatibility in products | Direct dimension matching |
| C010 / QP004 | Simplify using identity properties | Direct algebraic substitution |
| C010 / QP005 | Determinant, trace and rank of identity | Direct order-based formulas |
| C010 / QP006 | Classify identity among standard matrix types | Direct definition check |

No new archetypes were added. Cumulative status: 110 dispositions and 17 draft archetypes; 240 source QPs remain untouched.


## Batch 023 — identity-matrix uniqueness and algebraic characterizations (global QP111–QP115)

| QP | Disposition | Reason |
|---|---|---|
| C010 / QP007 | FOUNDATION_ONLY | Identity existence/uniqueness follows from the defining property |
| C010 / QP008 | FOUNDATION_ONLY | Left/right identity for a given matrix is direct order compatibility |
| C010 / QP009 | REQUIRES_REVIEW | The source does not specify the algebraic conditions; do not invent them |
| C010 / QP010 | FOUNDATION_ONLY | Spectral properties of identity are direct standard facts |
| C010 / QP011 | FOUNDATION_ONLY | Transpose, inverse and powers of identity are direct properties |

No new archetypes were added. One source possibility is explicitly held for review because its mathematical conditions are underspecified. Cumulative status: 115 dispositions, 17 draft archetypes; 235 QPs remain untouched.


## Batch 024 — upper-triangular matrix foundations and parameter constraints (global QP116–QP120)

| QP | Disposition | Reason |
|---|---|---|
| C011 / QP001 | FOUNDATION_ONLY | Direct zero-pattern recognition below the main diagonal |
| C011 / QP002 | ELIGIBLE | Simultaneous parameter constraints on all below-diagonal entries |
| C011 / QP003 | FOUNDATION_ONLY | Direct inclusion relationships among matrix classes |
| C011 / QP004 | FOUNDATION_ONLY | Direct closure under addition/scalar multiplication |
| C011 / QP005 | FOUNDATION_ONLY | Direct preservation under product, powers and polynomials |

New draft candidate:

- `U2_CH8_ST1_AR00018`: Derive parameter constraints for an upper-triangular matrix.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 120 dispositions and 18 draft archetypes; 230 source QPs remain untouched.


## Batch 025 — upper-triangular inverse and nilpotency mechanisms (global QP121–QP125)

| QP | Disposition | Reason |
|---|---|---|
| C011 / QP006 | FOUNDATION_ONLY | Both upper and lower triangular implies diagonal |
| C011 / QP007 | ELIGIBLE | Diagonal entries determine invertibility; inverse preserves upper-triangular structure |
| C011 / QP008 | ELIGIBLE | Strictly upper-triangular zero pattern gives a nilpotency power bound |
| C011 / QP009 | FOUNDATION_ONLY | Direct count of diagonal and above-diagonal entries |
| C011 / QP010 | REQUIRES_REVIEW | Source does not specify which elementary row/column operations are intended |

New draft candidates:

- `U2_CH8_ST1_AR00019`: Infer invertibility and inverse structure of an upper-triangular matrix.
- `U2_CH8_ST1_AR00020`: Establish nilpotency bounds for strictly upper-triangular matrices.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled. Two QPs are now explicitly held for review due underspecified source details.

Cumulative status: 125 dispositions and 20 draft archetypes; 225 source QPs remain untouched.


## Batch 026 — upper-triangular product structure and lower-triangular foundations (global QP126–QP130)

| QP | Disposition | Reason |
|---|---|---|
| C011 / QP011 | ELIGIBLE | Diagonal entries of products/powers are determined by corresponding factor diagonals |
| C012 / QP001 | FOUNDATION_ONLY | Direct lower-triangular zero-pattern recognition |
| C012 / QP002 | FOUNDATION_ONLY | Strict/unit lower-triangular distinction follows from the diagonal and zero pattern |
| C012 / QP003 | FOUNDATION_ONLY | Direct count of independent and forced-zero entries |
| C012 / QP004 | FOUNDATION_ONLY | Direct closure under addition and scalar multiplication |

New draft candidate:

- `U2_CH8_ST1_AR00021`: Infer diagonal entries of products and powers of upper-triangular matrices.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 130 dispositions and 21 draft archetypes; 220 source QPs remain untouched.


## Batch 027 — lower-triangular closure and symmetry properties (global QP131–QP135)

All five possibilities are retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| C012 / QP005 | Product of lower-triangular matrices | Direct closure |
| C012 / QP006 | Transpose relation | Direct conversion to upper-triangular form |
| C012 / QP007 | Both upper/lower or lower plus symmetric implies diagonal | Direct structural implication |
| C012 / QP008 | Powers of lower-triangular matrices | Direct repeated closure |
| C012 / QP009 | Diagonal entries of lower-triangular products/powers | Same mechanism as AR00021; do not duplicate |

No new archetypes were added. Cumulative status: 135 dispositions and 21 draft archetypes; 215 source QPs remain untouched.


## Batch 028 — lower-triangular parameter, inverse and nilpotency review (global QP136–QP140)

| QP | Disposition | Reason |
|---|---|---|
| C012 / QP010 | ELIGIBLE | Parameterized lower-triangular structure requires simultaneous above-diagonal zero constraints |
| C012 / QP011 | FOUNDATION_ONLY | Inverse triangularity mirrors the upper-triangular inverse candidate |
| C012 / QP012 | FOUNDATION_ONLY | Nonzero diagonal criterion duplicates the triangular invertibility mechanism |
| C012 / QP013 | FOUNDATION_ONLY | Strictly lower-triangular nilpotency mirrors the existing upper-triangular nilpotency mechanism |
| C013 / QP001 | FOUNDATION_ONLY | Symmetric recognition is a direct transpose-equality check |

New draft candidate:

- `U2_CH8_ST1_AR00022`: Derive parameter constraints for a lower-triangular matrix.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 140 dispositions and 22 draft archetypes; 210 source QPs remain untouched.
