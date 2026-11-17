# U1–CH1–ST2 JEE Qualification Review

**Subtopic:** Inclusion Relations among Number Sets  
**Source:** `Engine/qpc/mathematics/U1_CH1.csv`  
**Related concepts:** `U1_CH1_ST2_concepts.csv`  
**Status:** Academic scope review; no manufacturing authorization yet

## Scope lock

ST2 is restricted to inclusion relations among the number sets and their immediate logical consequences:

- Natural numbers N, with the project's declared convention N = {1, 2, 3, ...}
- Whole numbers W = {0, 1, 2, ...}
- Integers Z
- Rational numbers Q
- Irrational numbers R \\ Q
- Real numbers R

The canonical hierarchy is:

N ⊂ W ⊂ Z ⊂ Q ⊂ R

The irrational numbers are a subset of R and are disjoint from Q; neither Q nor R \\ Q contains the other. Whenever zero membership matters, use the project's explicit convention.

Do not import divisibility, parity, primes, intervals, modulus, polynomial roots, calculus, matrices, geometry, decimal-expansion tests, or general set algebra merely to create harder-looking questions. A future QP explicitly scoped to one of those topics may cover it separately.

## JEE-worthiness decision

ST2 is a narrow, largely foundational subtopic. It can support clean conceptual and logical questions, but it does not justify a large or artificially advanced archetype catalogue.

Potentially defensible reasoning mechanisms:

1. **Canonical inclusion verification** — determine which relation follows from the definitions of N, W, Z, Q, irrational numbers and R.
2. **Counterexample-based rejection** — disprove a proposed reverse inclusion using a valid witness, such as 0, a negative integer, or a non-integral rational, as appropriate.
3. **Transitive inclusion-chain inference** — infer a relation from a supplied chain and identify a missing link.
4. **Strictness/equality discrimination** — distinguish A ⊆ B from A ⊊ B using a witness in B that is not in A.
5. **Membership propagation** — infer x ∈ B from x ∈ A and A ⊆ B, while rejecting the converse unless separately established.
6. **Diagram-to-relation translation** — translate a correctly labelled nested-set diagram into symbolic inclusion statements. This is a presentation path, not a separate archetype unless the reasoning itself changes.

These are candidate mechanisms, not automatic approvals. Each must be tested for genuine distinction, QP fidelity, and suitable JEE demand. A diagram, true/false polarity, or changed numerical example alone does not create a new archetype.

## Cross-QP consolidation

- QP001 and QP002 should share the same inclusion-verification mechanism; correctness polarity is not a separate archetype.
- QP003 and QP004 may share transitive-chain reasoning; separate only if the missing-information structure changes the reasoning.
- QP005 and QP006 are converse descriptions of subset/superset and should not be duplicated.
- QP008 and QP009 overlap when statement evaluation is performed by constructing a counterexample; retain one mechanism unless a materially different logical task is demonstrated.
- QP010 should not become a separate archetype solely because the relation is shown in a Venn diagram.

## Provisional academic outcome

- Foundation/prerequisite questions are appropriate for the direct hierarchy and membership rules.
- Some short JEE Main conceptual questions may be defensible where students must distinguish inclusion direction, strictness, or a valid counterexample.
- No JEE Advanced archetype is approved at this stage. Do not manufacture Advanced difficulty by importing unrelated mathematical topics.
- Do not target a fixed question count if meaningful, non-duplicative variation is exhausted.

## Manufacturing gate

- Existing 20-question legacy batch: quarantined under `U1_CH1_ST2_QUESTION_AUDIT.md`.
- Approved ST2 archetypes: 0 at this review stage.
- Manufacturing-enabled archetypes: 0.
- Approved new question instances: 0.

The next manufacturing cycle must first convert the candidate mechanisms above into a small, non-duplicative, academically reviewed archetype registry. Only then may questions be generated and validated.
