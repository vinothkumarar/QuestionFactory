# U1–CH1–ST1 JEE Qualification Review

**Branch:** `feature/dual-question-engine-v1`  
**Source:** `Engine/qpc/mathematics/U1_CH1.csv`  
**Related registry:** `Engine/catalog/archetype_catalog/catalogs/U1_CH1_ST1.csv`  
**Status:** Academic gate; no manufacturing authorization

## Why this review exists

The archetype discovery prompt requires meaningful reasoning and explicitly rejects archetypes based primarily on direct recall, memorization or trivial recognition. The current 19-row core draft includes several direct definition and elementary membership checks. Those are useful as prerequisite learning diagnostics, but they should not be represented as JEE-worthy archetypes without stronger evidence.

To avoid both over-generation and blocking the entire subtopic, use two lanes:

- **Foundation prerequisite lane:** retain for diagnostic/practice learning, but do not count as JEE archetype coverage and do not include in JEE production batches.
- **JEE candidate lane:** retain as draft candidates only. Their actual reasoning depth must be demonstrated through representative questions and academic review before approval.

## Provisional disposition

### Foundation prerequisite only — 12 QPs

| QP | Source possibility | Reason |
|---|---|---|
| QP001 | Definition of Natural Numbers | Definition recall alone |
| QP002 | Definition of Whole Numbers | Definition recognition alone |
| QP003 | Definition of Integers | Definition recall alone |
| QP004 | Identify Natural Number | Direct membership test |
| QP005 | Identify Whole Number | Direct membership test |
| QP006 | Identify Integer | Direct membership test |
| QP007 | Identify Non-Natural Number | Direct exclusion/membership test |
| QP008 | Identify Non-Whole Number | Direct exclusion/membership test |
| QP009 | Identify Non-Integer | Direct integrality recognition |
| QP013 | Membership of Zero | Single boundary fact unless embedded in a deeper argument |
| QP014 | Membership of Positive Integer | Direct sign and integrality test |
| QP015 | Membership of Negative Integer | Direct sign and integrality test |

These are not deleted. They may support onboarding, diagnostic tests, remediation and prerequisite mastery. They must not be used to inflate the JEE archetype count.

### JEE candidate lane — 7 QPs

| QP | Source possibility | Required evidence before approval |
|---|---|---|
| QP010 | Classify Given Number | Multi-condition classification where the value's form or constraints require non-trivial inference, not a simple sign check |
| QP011 | Classify Multiple Numbers | A genuine aggregate/set-membership reasoning task; avoid mere repetitive classification |
| QP012 | Smallest Applicable Number Set | A decision requiring comparison of nested-set membership and explicit convention handling |
| QP017 | Classification after Arithmetic Operation | Exact evaluation plus non-trivial sign/integrality reasoning; no routine one-step arithmetic |
| QP018 | Statement-based Classification | Multi-claim consistency or logical implication analysis grounded strictly in N/W/Z |
| QP019 | True/False Classification | Proposition evaluation with a meaningful proof or counterexample requirement |
| QP020 | Error Detection in Classification | Diagnose the first invalid inference in a multi-step classification argument |

The candidate lane remains provisional. If representative tasks cannot meet JEE standards without importing another QP or concept, downgrade that QP to the foundation lane rather than stretching its scope.

## Boundary rules

1. Keep scope restricted to N, W and Z.
2. Use the project's configurable default convention: N = positive integers; W = non-negative integers; Z = all integers. Every test must inherit the convention explicitly.
3. Do not add divisibility, primes, HCF/LCM, rational/irrational classification or unrelated properties to ST1.
4. Do not create separate archetypes for changes in numbers, symbols, signs or presentation alone.
5. A JEE candidate must demonstrate a distinct reusable reasoning pathway, not merely be labelled HARD or ADVANCED.
6. Keep all current IDs stable. Do not delete or recycle parked IDs.
7. QP016 remains quarantined because its source text is malformed.

## Execution decision

The next safe manufacturing path is **not** to manufacture all 19 QPs indiscriminately.

1. Build a compact representative-task set for the seven JEE candidates.
2. Independently solve and verify every task.
3. Apply ambiguity, answer, distractor, novelty and R03 checks.
4. Retain only the candidates that genuinely pass the JEE-worthiness gate.
5. Route the 12 foundation-only QPs to a separate prerequisite practice track.
6. Do not enable manufacturing until the catalogue gate and runtime checks are implemented and verified.

**Current counts:** 19 core draft candidates; 12 provisionally foundation-only; 7 provisional JEE candidates; 33 parked candidates; 0 manufacturing-enabled rows.
