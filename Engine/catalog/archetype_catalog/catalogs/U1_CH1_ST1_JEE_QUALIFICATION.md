# U1–CH1–ST1 JEE Qualification Review

**Branch:** `feature/dual-question-engine-v1`  
**Source:** `Engine/qpc/mathematics/U1_CH1.csv`  
**Related registry:** `Engine/catalog/archetype_catalog/catalogs/U1_CH1_ST1.csv`  
**Status:** Foundation-only recommendation; manufacturing remains disabled

## Decision summary

ST1 is restricted to classifying membership in Natural Numbers (N), Whole Numbers (W) and Integers (Z). Under that strict boundary, the source possibilities do not provide enough mathematical structure to justify a separate JEE-level archetype catalogue.

The seven previously retained candidates were stress-tested against the JEE-worthiness rule: a reusable, distinct reasoning mechanism that requires meaningful inference beyond direct recall, recognition or routine classification. None currently clears that threshold without importing a different QP or a neighbouring concept.

**Recommendation: route all interpretable ST1 possibilities to the foundation/prerequisite track. Do not count any ST1 archetype toward JEE Main/Advanced catalogue coverage.** This is a quality-control decision, not deletion of the QPs or their IDs.

## Scope and conventions

- Keep ST1 limited to N, W and Z membership/classification.
- Configurable project default: N = positive integers; W = non-negative integers; Z = all integers.
- The active convention must be explicit whenever zero is involved.
- Do not import divisibility, parity, primes, HCF/LCM, rational/irrational classification, closure proofs or other adjacent concepts into ST1.
- A task that needs those ideas belongs to its own QP/subtopic and must not be used to inflate ST1's JEE-worthiness.

## Candidate stress-test

| QP | Source possibility | What a stronger task would require | Result |
|---|---|---|---|
| QP010 | Classify Given Number | Derive sign/integrality from constraints before classification | Still reduces to membership once the value is known; deeper algebra would be another QP |
| QP011 | Classify Multiple Numbers | Aggregate membership patterns across several values | Repeated classification/counting; no distinct JEE mechanism within N/W/Z alone |
| QP012 | Smallest Applicable Number Set | Compare nested-set membership with zero/sign boundaries | A short decision rule, not a sufficiently rich reusable JEE mechanism |
| QP017 | Classification after Arithmetic Operation | Infer sign and integrality from an operation's structure | Routine evaluation/classification; closure or divisibility reasoning belongs elsewhere |
| QP018 | Statement-based Classification | Combine multiple membership claims and implications | Elementary set-inclusion logic; deeper proof structure overlaps QP019 or another QP |
| QP019 | True/False Classification | Prove or disprove a universal membership claim | Valid foundation exercise, but counterexample/proof remains elementary under this scope |
| QP020 | Error Detection in Classification | Locate the first invalid inference in a classification argument | Definition-checking/diagnostic practice; multi-step algebra would exceed this QP |

This is a scope-based assessment. A future approved expansion of a QP may justify a new review, but do not assume that possibility now.

## Foundation prerequisite lane — all 19 interpretable QPs

QP001–QP015 and QP017–QP020 remain available for:
- prerequisite diagnostics;
- concept introduction and remediation;
- basic mastery checks;
- short warm-up questions before more advanced Number System topics.

They are not deleted and their source identifiers remain unchanged. They must not be presented as JEE-worthy archetypes merely by increasing wording, numerical complexity or the number of values.

## Quarantine

QP016 remains quarantined because the source text is malformed:

`Boundary Classification (?1`

Do not infer whether the intended value was +1, -1 or something else. No archetype or question may be manufactured from QP016 until the source is authoritatively corrected.

## Registry and manufacturing controls

- Preserve all existing archetype IDs AR00001–AR00052.
- The 19 core candidates remain drafts and must be treated as foundation-only pending any future approved scope revision.
- The other 33 candidates remain parked; do not restore them without documented source justification and a distinct reasoning mechanism.
- All rows remain `manufacturing_enabled=FALSE`.
- No JEE approval is granted by this review.
- Any later change must preserve the existing IDs and record its academic rationale.

## Next production direction

Do not spend more cycles manufacturing artificial complexity from ST1. Move to the next source-backed subtopic whose QPs support richer mathematical reasoning, and qualify it independently before enabling production.

**Current disposition:** 19 foundation/prerequisite QPs; 7 formerly provisional JEE candidates downgraded to foundation-only; 33 parked archetype candidates; QP016 quarantined; zero manufacturing-enabled rows.
