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


## Batch 029 — symmetric-matrix parameter constraints and decomposition (global QP141–QP145)

| QP | Disposition | Reason |
|---|---|---|
| C013 / QP002 | ELIGIBLE | Pairwise equality constraints between transposed entries define a reusable parameter mechanism |
| C013 / QP003 | FOUNDATION_ONLY | Direct count of independent diagonal and off-diagonal pair entries |
| C013 / QP004 | FOUNDATION_ONLY | Symmetric component formula is included in the full decomposition |
| C013 / QP005 | ELIGIBLE | Canonical symmetric/skew-symmetric decomposition is a reusable construction |
| C013 / QP006 | FOUNDATION_ONLY | Uniqueness follows directly from the decomposition identities |

New draft candidates:

- `U2_CH8_ST1_AR00023`: Derive parameter constraints for a symmetric matrix.
- `U2_CH8_ST1_AR00024`: Decompose a square matrix into symmetric and skew-symmetric parts.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 145 dispositions and 24 draft archetypes; 205 source QPs remain untouched.


## Batch 030 — symmetric-matrix products and closure (global QP146–QP150)

| QP | Disposition | Reason |
|---|---|---|
| C013 / QP007 | FOUNDATION_ONLY | Linear combinations preserve symmetry by transpose linearity |
| C013 / QP008 | ELIGIBLE | Symmetry of AB reduces to a commutativity condition when factors are symmetric |
| C013 / QP009 | FOUNDATION_ONLY | Powers/polynomials preserve symmetry by direct transpose identities |
| C013 / QP010 | FOUNDATION_ONLY | Inverse of an invertible symmetric matrix remains symmetric |
| C013 / QP011 | FOUNDATION_ONLY | Adjugate of a symmetric matrix remains symmetric |

New draft candidate:

- `U2_CH8_ST1_AR00025`: Determine symmetry of a matrix product through commutativity.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 150 dispositions and 25 draft archetypes; 200 source QPs remain untouched.


## Batch 031 — symmetric congruence and block-matrix constraints (global QP151–QP155)

| QP | Disposition | Reason |
|---|---|---|
| C013 / QP012 | FOUNDATION_ONLY | Direct transpose identities for A±Aᵀ |
| C013 / QP013 | ELIGIBLE | Congruence PᵀAP preserves symmetry by transpose reversal |
| C013 / QP014 | FOUNDATION_ONLY | Entry-wise symmetry is direct pairwise equality |
| C013 / QP015 | ELIGIBLE | Block symmetry imposes diagonal-block symmetry and transpose-paired off-diagonal blocks |
| C013 / QP016 | FOUNDATION_ONLY | Symmetric and triangular together imply diagonal |

New draft candidates:

- `U2_CH8_ST1_AR00026`: Prove symmetry is preserved by a congruence transform.
- `U2_CH8_ST1_AR00027`: Derive symmetry constraints for a block-partitioned matrix.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 155 dispositions and 27 draft archetypes; 195 source QPs remain untouched.


## Batch 032 — symmetric/skew-symmetric boundary and constraints (global QP156–QP160)

| QP | Disposition | Reason |
|---|---|---|
| C013 / QP017 | FOUNDATION_ONLY | Symmetric and skew-symmetric together imply the zero matrix |
| C013 / QP018 | REQUIRES_REVIEW | Transpose relations are not specified in the source possibility |
| C013 / QP019 | REQUIRES_REVIEW | Entry constraints and field are unspecified for the requested count |
| C014 / QP001 | FOUNDATION_ONLY | Direct skew-symmetric definition check |
| C014 / QP002 | ELIGIBLE | Paired negative-entry and zero-diagonal constraints form a reusable parameter/missing-entry mechanism |

New draft candidate:

- `U2_CH8_ST1_AR00028`: Derive parameter and missing-entry constraints for a skew-symmetric matrix.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 160 dispositions and 28 draft archetypes; 190 source QPs remain untouched. Four QPs are held for review because their source specifications are insufficiently precise.


## Batch 033 — skew-symmetric decomposition and core properties (global QP161–QP165)

All five possibilities are retained as `FOUNDATION_ONLY`:

| QP | Source mechanism | Disposition rationale |
|---|---|---|
| C014 / QP003 | Skew-symmetric component/decomposition | Already covered by the full decomposition archetype AR00024 |
| C014 / QP004 | Diagonal and trace properties | Direct consequences of skew-symmetry |
| C014 / QP005 | General element-wise form | Direct pairwise sign pattern |
| C014 / QP006 | Count independent parameters | Direct n(n−1)/2 count |
| C014 / QP007 | Closure/invariance operations | Direct transpose identities |

No new archetypes were added. Cumulative status: 165 dispositions and 28 draft archetypes; 185 source QPs remain untouched.


## Batch 034 — skew-symmetric powers, product algebra and order parity (global QP166–QP170)

| QP | Disposition | Reason |
|---|---|---|
| C014 / QP008 | ELIGIBLE | Power parity determines symmetric/skew-symmetric type; polynomial expressions split into even/odd powers |
| C014 / QP009 | ELIGIBLE | Transpose reversal classifies products, commutators and anticommutators across symmetry types |
| C014 / QP010 | ELIGIBLE | Determinant sign under transpose proves odd-order skew-symmetric matrices singular |
| C014 / QP011 | FOUNDATION_ONLY | Inverse of an invertible skew-symmetric matrix remains skew-symmetric |
| C014 / QP012 | FOUNDATION_ONLY | Both symmetric and skew-symmetric implies zero; already dispositioned |

New draft candidates:

- `U2_CH8_ST1_AR00029`: Classify powers and polynomials of a skew-symmetric matrix.
- `U2_CH8_ST1_AR00030`: Classify products, commutators and anticommutators by transpose rules.
- `U2_CH8_ST1_AR00031`: Infer singularity of skew-symmetric matrices from order parity.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 170 dispositions and 31 draft archetypes; 180 source QPs remain untouched.


## Batch 035 — orthogonal matrix parameter and completion mechanisms (global QP171–QP175)

| QP | Disposition | Reason |
|---|---|---|
| C014 / QP013 | REQUIRES_REVIEW | Allowed discrete entry set/counting constraints are unspecified |
| C015 / QP001 | FOUNDATION_ONLY | Direct verification by QᵀQ=I |
| C015 / QP002 | ELIGIBLE | Parameterized orthogonality creates coupled norm and inner-product equations |
| C015 / QP003 | ELIGIBLE | Completing missing entries requires constructing an orthonormal completion |
| C015 / QP004 | FOUNDATION_ONLY | Q⁻¹=Qᵀ is a direct orthogonal-matrix property |

New draft candidates:

- `U2_CH8_ST1_AR00032`: Derive parameter constraints for an orthogonal matrix.
- `U2_CH8_ST1_AR00033`: Complete a partially specified matrix to an orthogonal matrix.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 175 dispositions and 33 draft archetypes; 175 source QPs remain untouched. Five source possibilities are held for review due underspecified conditions.


## Batch 036 — orthogonal determinant, entry constraints and special families (global QP176–QP180)

| QP | Disposition | Reason |
|---|---|---|
| C015 / QP005 | ELIGIBLE | Determinant identity yields det(Q)=±1 and orientation classification |
| C015 / QP006 | FOUNDATION_ONLY | Standard closure under product, transpose, inverse and powers |
| C015 / QP007 | FOUNDATION_ONLY | Equivalent orthogonality characterizations by row/column inner products |
| C015 / QP008 | ELIGIBLE | Unit norms and zero cross-products yield entry bounds and aggregate identities |
| C015 / QP009 | ELIGIBLE | Orthogonality reduces to family-specific conditions for diagonal, permutation and block matrices |

New draft candidates:

- `U2_CH8_ST1_AR00034`: Infer determinant and orientation of an orthogonal matrix.
- `U2_CH8_ST1_AR00035`: Derive entry-wise and aggregate constraints from orthogonality.
- `U2_CH8_ST1_AR00036`: Characterize orthogonality in diagonal, permutation and block matrix families.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 180 dispositions and 36 draft archetypes; 170 source QPs remain untouched.


## Batch 037 — orthogonal scalar, metric and combined-structure reasoning (global QP181–QP185)

| QP | Disposition | Reason |
|---|---|---|
| C015 / QP010 | ELIGIBLE | Scalar scaling of A is orthogonal under a scalar equation derived from c²AᵀA=I |
| C015 / QP011 | FOUNDATION_ONLY | Row/column permutations and sign changes preserve orthonormality directly |
| C015 / QP012 | FOUNDATION_ONLY | Squareness, full rank and nonsingularity follow directly from QᵀQ=I |
| C015 / QP013 | ELIGIBLE | Orthogonal transforms preserve inner products, norms and angles |
| C015 / QP014 | ELIGIBLE | Combining orthogonality with symmetry/skew-symmetry yields stronger matrix identities and feasibility constraints |

New draft candidates:

- `U2_CH8_ST1_AR00037`: Determine scalar multiples that preserve orthogonality.
- `U2_CH8_ST1_AR00038`: Use orthogonality to preserve vector lengths and inner products.
- `U2_CH8_ST1_AR00039`: Combine orthogonality with symmetric or skew-symmetric structure.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 185 dispositions and 39 draft archetypes; 165 source QPs remain untouched.


## Batch 038 — orthogonal degrees of freedom and singularity transformations (global QP186–QP190)

| QP | Disposition | Reason |
|---|---|---|
| C015 / QP015 | ELIGIBLE | Independent degrees of freedom of O(n) are n(n−1)/2 |
| C016 / QP001 | FOUNDATION_ONLY | Direct determinant-zero singularity classification |
| C016 / QP002 | ELIGIBLE | Solve det(A(λ))=0 for singular parameter values |
| C016 / QP003 | ELIGIBLE | Propagate singularity through products, scalar multiples and powers using determinant identities |
| C016 / QP004 | ELIGIBLE | Track singularity invariance under transpose, similarity and invertible elementary operations |

New draft candidates:

- `U2_CH8_ST1_AR00040`: Count independent degrees of freedom in an orthogonal matrix.
- `U2_CH8_ST1_AR00041`: Solve determinant-zero conditions for singular matrix parameters.
- `U2_CH8_ST1_AR00042`: Propagate singularity through products, scalar multiples and powers.
- `U2_CH8_ST1_AR00043`: Track singularity under transpose, similarity and elementary operations.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 190 dispositions and 43 draft archetypes; 160 source QPs remain untouched.


## Batch 039 — singularity characterizations and adjugate rank structure (global QP191–QP195)

| QP | Disposition | Reason |
|---|---|---|
| C016 / QP005 | FOUNDATION_ONLY | Equivalent determinant/rank/inverse/dependence characterizations are standard facts |
| C016 / QP006 | ELIGIBLE | Adjugate behavior splits by rank n, n−1 and ≤n−2 |
| C017 / QP001 | FOUNDATION_ONLY | Direct nonzero-determinant/invertibility check |
| C017 / QP002 | FOUNDATION_ONLY | Nonzero determinant condition complements AR00041; no duplicate archetype |
| C017 / QP003 | FOUNDATION_ONLY | Equivalent non-singularity characterizations are standard facts |

New draft candidate:

- `U2_CH8_ST1_AR00044`: Infer adjugate structure from the rank of a matrix.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 195 dispositions and 44 draft archetypes; 155 source QPs remain untouched.


## Batch 040 — non-singular products, linear systems and elementary operations (global QP196–QP200)

| QP | Disposition | Reason |
|---|---|---|
| C017 / QP004 | FOUNDATION_ONLY | Standard determinant/inverse consequences under transpose, powers, scalar multiples and adjugate |
| C017 / QP005 | ELIGIBLE | AB nonsingular iff both compatible square factors are nonsingular |
| C017 / QP006 | ELIGIBLE | Universal existence and uniqueness of Ax=b characterizes nonsingularity |
| C017 / QP007 | ELIGIBLE | Invertible elementary row/column operations preserve rank and nonsingularity |
| C017 / QP008 | REQUIRES_REVIEW | The necessary/sufficient conditions to classify are not enumerated |

New draft candidates:

- `U2_CH8_ST1_AR00045`: Infer nonsingularity of matrix products and their factors.
- `U2_CH8_ST1_AR00046`: Connect nonsingularity with existence and uniqueness of Ax=b.
- `U2_CH8_ST1_AR00047`: Track nonsingularity under elementary row and column operations.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 200 dispositions and 47 draft archetypes; 150 source QPs remain untouched. Six QPs are held for review due unspecified source details.


## Batch 041 — non-singular counting holds and idempotent matrix mechanisms (global QP201–QP205)

| QP | Disposition | Reason |
|---|---|---|
| C017 / QP009 | REQUIRES_REVIEW | Discrete entry set and counting constraints are unspecified |
| C017 / QP010 | REQUIRES_REVIEW | Matrix constraints and allowed entries are unspecified |
| C018 / QP001 | FOUNDATION_ONLY | Direct A²=A verification |
| C018 / QP002 | ELIGIBLE | Parameterized idempotency produces simultaneous quadratic entry equations |
| C018 / QP003 | ELIGIBLE | Positive powers collapse to A; polynomial expressions reduce to a linear form in I and A |

New draft candidates:

- `U2_CH8_ST1_AR00048`: Solve parameter conditions for an idempotent matrix.
- `U2_CH8_ST1_AR00049`: Reduce powers and polynomials of an idempotent matrix.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 205 dispositions and 49 draft archetypes; 145 source QPs remain untouched. Eight source possibilities are held for review due underspecified details.


## Batch 042 — idempotent spectral, canonical and complementary structure (global QP206–QP210)

| QP | Disposition | Reason |
|---|---|---|
| C018 / QP004 | ELIGIBLE | Eigenvalues of an idempotent matrix are restricted to 0 or 1 |
| C018 / QP005 | ELIGIBLE | Idempotents are diagonalizable and similar to diag(I_r,0), classified by rank |
| C018 / QP006 | ELIGIBLE | Rank, trace, nullity and determinant follow from the 0/1 spectrum |
| C018 / QP007 | ELIGIBLE | I−A is idempotent and has complementary image/kernel and rank |
| C018 / QP008 | REQUIRES_REVIEW | Sum/product/scalar-combination rules need operand commutativity and relationship assumptions |

New draft candidates:

- `U2_CH8_ST1_AR00050`: Infer eigenvalues and multiplicities of an idempotent matrix.
- `U2_CH8_ST1_AR00051`: Classify idempotent matrices up to similarity by rank.
- `U2_CH8_ST1_AR00052`: Relate rank, trace, nullity and determinant of an idempotent matrix.
- `U2_CH8_ST1_AR00053`: Analyze the complementary idempotent I−A.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 210 dispositions and 53 draft archetypes; 140 source QPs remain untouched. Nine source possibilities are held for review.


## Batch 043 — idempotent inverse formulas and polynomial invariants (global QP211–QP215)

| QP | Disposition | Reason |
|---|---|---|
| C018 / QP009 | ELIGIBLE | I±αA for idempotent A reduce to a scalar invertibility condition and closed-form inverse |
| C018 / QP010 | ELIGIBLE | Minimal polynomial divides x(x−1); characteristic polynomial links to rank and eigenvalue multiplicity |
| C018 / QP011 | FOUNDATION_ONLY | Nontrivial idempotent existence under invariants is covered by rank/canonical classification |
| C018 / QP012 | FOUNDATION_ONLY | Similarity classification by rank is already represented |
| C018 / QP013 | REQUIRES_REVIEW | Structured classes and combinations are too broad without explicit family assumptions |

New draft candidates:

- `U2_CH8_ST1_AR00054`: Determine invertibility and inverses of I±αA for idempotent A.
- `U2_CH8_ST1_AR00055`: Derive minimal and characteristic polynomial constraints for an idempotent matrix.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 215 dispositions and 55 draft archetypes; 135 source QPs remain untouched. Ten source possibilities are held for review.


## Batch 044 — nilpotent index, parameter constraints and polynomial invariants (global QP216–QP220)

| QP | Disposition | Reason |
|---|---|---|
| C019 / QP001 | FOUNDATION_ONLY | Direct A^k=O definition check |
| C019 / QP002 | ELIGIBLE | Find the least positive power that vanishes and prove minimality |
| C019 / QP003 | ELIGIBLE | Nilpotency imposes simultaneous polynomial constraints on parameters |
| C019 / QP004 | FOUNDATION_ONLY | Zero eigenvalues, determinant and trace are direct consequences |
| C019 / QP005 | ELIGIBLE | Characteristic polynomial is λ^n; minimal polynomial is λ^k for the nilpotency index k |

New draft candidates:

- `U2_CH8_ST1_AR00056`: Determine the index of nilpotency of a matrix.
- `U2_CH8_ST1_AR00057`: Derive parameter conditions for a nilpotent matrix.
- `U2_CH8_ST1_AR00058`: Derive characteristic and minimal polynomial constraints for a nilpotent matrix.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 220 dispositions and 58 draft archetypes; 130 source QPs remain untouched.


## Batch 045 — nilpotent polynomial reduction and finite inverse construction (global QP221–QP225)

| QP | Disposition | Reason |
|---|---|---|
| C019 / QP006 | ELIGIBLE | Nilpotency truncates polynomial expressions to finite sums |
| C019 / QP007 | ELIGIBLE | Finite geometric series constructs exact inverses of I±N |
| C019 / QP008 | FOUNDATION_ONLY | Similarity invariance of nilpotency/index is a direct identity |
| C019 / QP009 | FOUNDATION_ONLY | Triangular zero-pattern nilpotency is a standard structural result |
| C019 / QP010 | FOUNDATION_ONLY | Index bounds overlap the existing nilpotency-bound mechanism |

New draft candidates:

- `U2_CH8_ST1_AR00059`: Reduce polynomial expressions in a nilpotent matrix.
- `U2_CH8_ST1_AR00060`: Construct inverses of I±N using finite geometric series.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 225 dispositions and 60 draft archetypes; 125 source QPs remain untouched.


## Batch 046 — nilpotent rank, block structure, construction and polynomial inverses (global QP226–QP230)

| QP | Disposition | Reason |
|---|---|---|
| C019 / QP011 | ELIGIBLE | Rank/nullity sequences of powers decrease/increase up to the nilpotency index |
| C019 / QP012 | ELIGIBLE | Block-triangular nilpotency depends on diagonal blocks and off-diagonal block paths |
| C019 / QP013 | REQUIRES_REVIEW | Sum/product rules require explicit commutation and compatibility assumptions |
| C019 / QP014 | ELIGIBLE | Jordan blocks construct nilpotent matrices with any admissible index 1≤k≤n |
| C019 / QP015 | ELIGIBLE | p(N) is invertible iff p(0)≠0, with finite geometric inverse when nonzero |

New draft candidates:

- `U2_CH8_ST1_AR00061`: Infer rank and nullity behavior of powers of a nilpotent matrix.
- `U2_CH8_ST1_AR00062`: Determine nilpotency of block-triangular matrices from diagonal blocks.
- `U2_CH8_ST1_AR00063`: Construct nilpotent matrices with a prescribed order and index.
- `U2_CH8_ST1_AR00064`: Determine invertibility of p(N) from the constant term.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 230 dispositions and 64 draft archetypes; 120 source QPs remain untouched. Eleven source possibilities are held for review.


## Batch 047 — involutory parameter, polynomial and spectral mechanisms (global QP231–QP235)

| QP | Disposition | Reason |
|---|---|---|
| C020 / QP001 | FOUNDATION_ONLY | Direct A²=I verification |
| C020 / QP002 | ELIGIBLE | Parameterized involutory condition gives simultaneous quadratic entry equations |
| C020 / QP003 | FOUNDATION_ONLY | An involutory matrix is its own inverse |
| C020 / QP004 | ELIGIBLE | Even powers reduce to I and odd powers to A; polynomials reduce to aI+bA |
| C020 / QP005 | ELIGIBLE | Eigenvalues are ±1; multiplicities link to trace, determinant and characteristic polynomial |

New draft candidates:

- `U2_CH8_ST1_AR00065`: Derive parameter conditions for an involutory matrix.
- `U2_CH8_ST1_AR00066`: Reduce powers and polynomials of an involutory matrix.
- `U2_CH8_ST1_AR00067`: Infer eigenvalue multiplicities of an involutory matrix.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 235 dispositions and 67 draft archetypes; 115 source QPs remain untouched.


## Batch 048 — involutory canonical forms, projectors and polynomial invariants (global QP236–QP240)

| QP | Disposition | Reason |
|---|---|---|
| C020 / QP006 | FOUNDATION_ONLY | Trace/determinant follow from ±1 eigenvalue multiplicities |
| C020 / QP007 | ELIGIBLE | Distinct roots of x²−1 give diagonalizability and canonical ±I blocks |
| C020 / QP008 | ELIGIBLE | (I±A)/2 are complementary idempotent projectors onto ±1 eigenspaces |
| C020 / QP009 | FOUNDATION_ONLY | Rank/nullity of I±A follows from projector eigenspaces |
| C020 / QP010 | ELIGIBLE | Minimal polynomial divides x²−1 and characteristic polynomial has only ±1 roots |

New draft candidates:

- `U2_CH8_ST1_AR00068`: Classify involutory matrices up to similarity into ±I blocks.
- `U2_CH8_ST1_AR00069`: Construct complementary projectors from an involutory matrix.
- `U2_CH8_ST1_AR00070`: Derive minimal and characteristic polynomial constraints for an involutory matrix.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 240 dispositions and 70 draft archetypes; 110 source QPs remain untouched.


## Batch 049 — involutory product and linear-combination inverse mechanisms (global QP241–QP245)

| QP | Disposition | Reason |
|---|---|---|
| C020 / QP011 | ELIGIBLE | Product of involutory matrices is involutory iff the factors commute |
| C020 / QP012 | ELIGIBLE | αI+βA has a closed-form inverse when α²−β²≠0 |
| C020 / QP013 | REQUIRES_REVIEW | Feasibility requires explicit field, order, invariant and nontriviality assumptions |
| C021 / QP001 | FOUNDATION_ONLY | Direct permutation-matrix pattern recognition |
| C021 / QP002 | FOUNDATION_ONLY | Direct construction from a specified permutation |

New draft candidates:

- `U2_CH8_ST1_AR00071`: Determine when a product of involutory matrices is involutory.
- `U2_CH8_ST1_AR00072`: Invert linear combinations αI+βA for involutory A.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 245 dispositions and 72 draft archetypes; 105 source QPs remain untouched. Twelve source possibilities are held for review.


## Batch 050 — permutation parity and matrix reordering (global QP246–QP250)

| QP | Disposition | Reason |
|---|---|---|
| C021 / QP003 | FOUNDATION_ONLY | Direct decoding of the permutation from row positions |
| C021 / QP004 | FOUNDATION_ONLY | Direct n! count via bijection with permutations |
| C021 / QP005 | ELIGIBLE | Determinant equals permutation sign; parity from inversions/cycles |
| C021 / QP006 | FOUNDATION_ONLY | Inverse of a permutation matrix is its transpose |
| C021 / QP007 | ELIGIBLE | Left/right multiplication reorders rows/columns with index tracking |

New draft candidates:

- `U2_CH8_ST1_AR00073`: Determine determinant sign and parity of a permutation matrix.
- `U2_CH8_ST1_AR00074`: Track row and column reordering under permutation-matrix multiplication.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 250 dispositions and 74 draft archetypes; 100 source QPs remain untouched.


## Batch 051 — permutation composition, order, powers and symmetry (global QP251–QP255)

| QP | Disposition | Reason |
|---|---|---|
| C021 / QP008 | ELIGIBLE | Permutation-matrix multiplication composes the underlying permutations |
| C021 / QP009 | ELIGIBLE | Permutation order is the LCM of disjoint cycle lengths |
| C021 / QP010 | ELIGIBLE | Powers act by modular shifts within disjoint cycles |
| C021 / QP011 | FOUNDATION_ONLY | Trace directly counts fixed points |
| C021 / QP012 | ELIGIBLE | Symmetric permutation matrices correspond exactly to self-inverse permutations with cycles of length 1 or 2 |

New draft candidates:

- `U2_CH8_ST1_AR00075`: Compose permutations through permutation-matrix multiplication.
- `U2_CH8_ST1_AR00076`: Determine permutation order from disjoint cycle lengths.
- `U2_CH8_ST1_AR00077`: Compute powers and periodicity of a permutation matrix.
- `U2_CH8_ST1_AR00078`: Characterize symmetric permutation matrices through involutions.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 255 dispositions and 78 draft archetypes; 95 source QPs remain untouched.


## Batch 052 — permutation determinant, conjugation, commutativity and group structure (global QP256–QP260)

| QP | Disposition | Reason |
|---|---|---|
| C021 / QP013 | ELIGIBLE | Row/column permutation scales determinant by permutation sign |
| C021 / QP014 | ELIGIBLE | Conjugation PAP⁻¹ realizes simultaneous index relabeling |
| C021 / QP015 | ELIGIBLE | Permutation matrices commute iff their underlying permutations commute |
| C021 / QP016 | FOUNDATION_ONLY | Every permutation matrix has full rank |
| C021 / QP017 | ELIGIBLE | Permutation matrices form a group isomorphic to S_n |

New draft candidates:

- `U2_CH8_ST1_AR00079`: Track determinant changes under permutation of rows or columns.
- `U2_CH8_ST1_AR00080`: Determine simultaneous row-column relabeling through permutation conjugation.
- `U2_CH8_ST1_AR00081`: Determine commutativity of permutation matrices from cycle structure.
- `U2_CH8_ST1_AR00082`: Establish the symmetric-group structure of permutation matrices.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 260 dispositions and 82 draft archetypes; 90 source QPs remain untouched.


## Batch 053 — elementary-matrix decoding, construction, action and inverse (global QP261–QP265)

| QP | Disposition | Reason |
|---|---|---|
| C022 / QP001 | FOUNDATION_ONLY | Direct elementary-matrix definition check |
| C022 / QP002 | ELIGIBLE | Decode swap, scaling or addition operation and recover indices/parameter |
| C022 / QP003 | ELIGIBLE | Construct elementary matrix by applying operation to identity |
| C022 / QP004 | ELIGIBLE | Left/right multiplication applies row/column operations |
| C022 / QP005 | ELIGIBLE | Inverse elementary matrix reverses the encoded operation |

New draft candidates:

- `U2_CH8_ST1_AR00083`: Decode the elementary operation represented by a matrix.
- `U2_CH8_ST1_AR00084`: Construct an elementary matrix from a specified operation.
- `U2_CH8_ST1_AR00085`: Predict matrix changes under elementary matrix multiplication.
- `U2_CH8_ST1_AR00086`: Find inverse elementary matrices and inverse operations.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 265 dispositions and 86 draft archetypes; 85 source QPs remain untouched.


## Batch 054 — elementary-matrix determinant, factorization and equivalence (global QP266–QP270)

| QP | Disposition | Reason |
|---|---|---|
| C022 / QP006 | FOUNDATION_ONLY | Determinant of elementary matrices follows directly from operation type |
| C022 / QP007 | ELIGIBLE | Gaussian elimination factors any invertible matrix into elementary matrices |
| C022 / QP008 | ELIGIBLE | Row/column equivalence is represented by products of elementary matrices |
| C022 / QP009 | REQUIRES_REVIEW | Minimal operation count lacks an explicit cost model and allowed operation set |
| C022 / QP010 | REQUIRES_REVIEW | Product-is-elementary conditions need operation-type/index/order constraints |

New draft candidates:

- `U2_CH8_ST1_AR00087`: Factor an invertible matrix into elementary matrices.
- `U2_CH8_ST1_AR00088`: Characterize row and column equivalence through elementary matrices.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 270 dispositions and 88 draft archetypes; 80 source QPs remain untouched. Fourteen source possibilities are held for review.


## Batch 055 — elementary-operation commutativity and combined transformations (global QP271–QP275)

| QP | Disposition | Reason |
|---|---|---|
| C022 / QP011 | ELIGIBLE | Commutativity depends on operation types, indices and order |
| C022 / QP012 | FOUNDATION_ONLY | A fixed operation uniquely determines its elementary matrix |
| C022 / QP013 | ELIGIBLE | Reverse-engineer whether a matrix represents exactly one elementary operation |
| C022 / QP014 | ELIGIBLE | Pre/post multiplication combines row and column transformations |
| C023 / QP001 | FOUNDATION_ONLY | Direct Hermitian definition check |

New draft candidates:

- `U2_CH8_ST1_AR00089`: Classify when two elementary matrices commute.
- `U2_CH8_ST1_AR00090`: Recognize whether a transformation is a single elementary operation.
- `U2_CH8_ST1_AR00091`: Track combined row and column transformations by pre/post multiplication.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 275 dispositions and 91 draft archetypes; 75 source QPs remain untouched.


## Batch 056 — Hermitian parameter constraints and product commutativity (global QP276–QP280)

| QP | Disposition | Reason |
|---|---|---|
| C023 / QP002 | ELIGIBLE | Hermitian condition imposes real diagonal and conjugate-paired off-diagonal constraints |
| C023 / QP003 | FOUNDATION_ONLY | General Hermitian/skew-Hermitian decomposition is already represented |
| C023 / QP004 | FOUNDATION_ONLY | Real vector-space closure follows by adjoint linearity |
| C023 / QP005 | FOUNDATION_ONLY | Powers/real polynomials preserve Hermiticity by direct identities |
| C023 / QP006 | ELIGIBLE | Product of Hermitian matrices is Hermitian iff the factors commute |

New draft candidates:

- `U2_CH8_ST1_AR00092`: Derive parameter and missing-entry constraints for a Hermitian matrix.
- `U2_CH8_ST1_AR00093`: Determine when a product of Hermitian matrices is Hermitian.

Both are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 280 dispositions and 93 draft archetypes; 70 source QPs remain untouched.


## Batch 057 — Hermitian invariants, positive semidefinite products and congruence (global QP281–QP285)

| QP | Disposition | Reason |
|---|---|---|
| C023 / QP007 | FOUNDATION_ONLY | Inverse/adjugate Hermitian properties follow directly from adjoint identities |
| C023 / QP008 | ELIGIBLE | Hermitian eigenvalues are real, giving real trace and determinant |
| C023 / QP009 | ELIGIBLE | A*A and AA* are Hermitian positive semidefinite by quadratic-form norms |
| C023 / QP010 | ELIGIBLE | Hermitian structure is preserved by congruence P*AP |
| C023 / QP011 | FOUNDATION_ONLY | Real Hermitian/symmetric and Hermitian/skew-Hermitian scalar correspondences are direct |

New draft candidates:

- `U2_CH8_ST1_AR00094`: Infer real trace and determinant invariants of a Hermitian matrix.
- `U2_CH8_ST1_AR00095`: Establish positive semidefiniteness of A*A and AA*.
- `U2_CH8_ST1_AR00096`: Prove Hermitian structure is preserved by congruence transformations.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 285 dispositions and 96 draft archetypes; 65 source QPs remain untouched.


## Batch 058 — Hermitian quadratic-form characterization and Hermitian/skew-Hermitian parameter counts (global QP286–QP290)

| QP | Disposition | Reason |
|---|---|---|
| C023 / QP012 | ELIGIBLE | A is Hermitian iff x*Ax is real for every complex x |
| C023 / QP013 | ELIGIBLE | Hermitian matrices have n² independent real parameters |
| C024 / QP001 | FOUNDATION_ONLY | Direct skew-Hermitian definition check |
| C024 / QP002 | ELIGIBLE | Purely imaginary diagonal and negative-conjugate off-diagonal constraints |
| C024 / QP003 | FOUNDATION_ONLY | General Hermitian/skew-Hermitian decomposition already represented |

New draft candidates:

- `U2_CH8_ST1_AR00097`: Characterize Hermitian matrices through real quadratic forms.
- `U2_CH8_ST1_AR00098`: Count independent real parameters of a Hermitian matrix.
- `U2_CH8_ST1_AR00099`: Derive parameter and missing-entry constraints for a skew-Hermitian matrix.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 290 dispositions and 99 draft archetypes; 60 source QPs remain untouched.


## Batch 059 — skew-Hermitian determinant, scalar and polynomial mechanisms (global QP291–QP295)

| QP | Disposition | Reason |
|---|---|---|
| C024 / QP004 | FOUNDATION_ONLY | Diagonal entries and trace are purely imaginary |
| C024 / QP005 | ELIGIBLE | Determinant is real for even order and purely imaginary for odd order |
| C024 / QP006 | ELIGIBLE | Scalar coefficient conditions distinguish preservation of skew-Hermiticity from conversion to Hermitian |
| C024 / QP007 | ELIGIBLE | Powers alternate by parity and polynomials split into even/odd parts |
| C024 / QP008 | FOUNDATION_ONLY | Real skew-Hermitian matrices are directly skew-symmetric |

New draft candidates:

- `U2_CH8_ST1_AR00100`: Infer determinant reality or pure-imaginary character from skew-Hermitian order.
- `U2_CH8_ST1_AR00101`: Classify scalar combinations of skew-Hermitian matrices.
- `U2_CH8_ST1_AR00102`: Classify powers and polynomials of skew-Hermitian matrices.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 295 dispositions and 102 draft archetypes; 55 source QPs remain untouched.


## Batch 060 — skew-Hermitian spectral, quadratic-form and product algebra (global QP296–QP300)

| QP | Disposition | Reason |
|---|---|---|
| C024 / QP009 | FOUNDATION_ONLY | Both Hermitian and skew-Hermitian implies zero |
| C024 / QP010 | ELIGIBLE | Eigenvalues of skew-Hermitian matrices are purely imaginary |
| C024 / QP011 | ELIGIBLE | x*Ax is purely imaginary for skew-Hermitian A |
| C024 / QP012 | ELIGIBLE | Adjoint reversal classifies AB±BA across symmetry types |
| C024 / QP013 | FOUNDATION_ONLY | Independent real parameter count is n², matching the Hermitian count |

New draft candidates:

- `U2_CH8_ST1_AR00103`: Infer purely imaginary eigenvalues of a skew-Hermitian matrix.
- `U2_CH8_ST1_AR00104`: Determine the scalar nature of x*Ax for skew-Hermitian A.
- `U2_CH8_ST1_AR00105`: Classify AB±BA using Hermitian and skew-Hermitian operand types.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 300 dispositions and 105 draft archetypes; 50 source QPs remain untouched.


## Batch 061 — skew-Hermitian inverse and unitary parameter constraints (global QP301–QP305)

| QP | Disposition | Reason |
|---|---|---|
| C024 / QP014 | FOUNDATION_ONLY | Inverse of an invertible skew-Hermitian matrix remains skew-Hermitian |
| C025 / QP001 | FOUNDATION_ONLY | Direct unitary verification by U*U=I |
| C025 / QP002 | ELIGIBLE | Unitary parameterization creates coupled complex norm/orthogonality equations |
| C025 / QP003 | FOUNDATION_ONLY | Inverse of a unitary matrix is its conjugate transpose |
| C025 / QP004 | FOUNDATION_ONLY | Row/column orthonormality and U*U=I are standard equivalent characterizations |

New draft candidate:

- `U2_CH8_ST1_AR00106`: Derive parameter constraints for a unitary matrix.
- JEE Main candidate only; Moderate/Hard potential; academic approval pending; manufacturing disabled.

Cumulative status: 305 dispositions and 106 draft archetypes; 45 source QPs remain untouched.


## Batch 062 — unitary scalar, determinant and diagonal constraints (global QP306–QP310)

| QP | Disposition | Reason |
|---|---|---|
| C025 / QP005 | FOUNDATION_ONLY | Products, inverses and powers preserve unitarity by direct identities |
| C025 / QP006 | ELIGIBLE | Scalar multiple is unitary exactly when the scalar has modulus one |
| C025 / QP007 | ELIGIBLE | Determinant of a unitary matrix has modulus one |
| C025 / QP008 | FOUNDATION_ONLY | Unitary matrices are invertible and full rank by definition |
| C025 / QP009 | ELIGIBLE | Diagonal unitarity reduces to modulus-one conditions on each diagonal entry |

New draft candidates:

- `U2_CH8_ST1_AR00107`: Determine scalar multiples that preserve unitarity.
- `U2_CH8_ST1_AR00108`: Derive determinant modulus constraints for a unitary matrix.
- `U2_CH8_ST1_AR00109`: Characterize diagonal unitary matrices entrywise.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 310 dispositions and 109 draft archetypes; 40 source QPs remain untouched.


## Batch 063 — triangular, block-diagonal and metric unitary properties (global QP311–QP315)

| QP | Disposition | Reason |
|---|---|---|
| C025 / QP010 | ELIGIBLE | Triangular unitarity forces a diagonal phase matrix |
| C025 / QP011 | ELIGIBLE | Block-diagonal unitarity reduces to independent unitary blocks |
| C025 / QP012 | FOUNDATION_ONLY | Real unitary matrices are orthogonal by direct conjugation restriction |
| C025 / QP013 | FOUNDATION_ONLY | Entrywise orthonormality expands U*U=I and is covered by parameter constraints |
| C025 / QP014 | ELIGIBLE | Unitary transformations preserve complex inner products and norms |

New draft candidates:

- `U2_CH8_ST1_AR00110`: Characterize triangular unitary matrices as diagonal phase matrices.
- `U2_CH8_ST1_AR00111`: Determine unitarity of block-diagonal matrices from their blocks.
- `U2_CH8_ST1_AR00112`: Use unitary transformations to preserve complex inner products and norms.

All are JEE Main candidates only, Moderate/Hard potential, and remain draft with manufacturing disabled.

Cumulative status: 315 dispositions and 112 draft archetypes; 35 source QPs remain untouched.
