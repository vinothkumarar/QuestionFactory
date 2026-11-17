# U1–CH1–ST2 Question Possibility Audit

**Branch:** `feature/dual-question-engine-v1`  
**Source of truth:** `Engine/qpc/mathematics/U1_CH1.csv`  
**Scope:** Set inclusion and representation  
**Status:** Initial source reconciliation; no archetype approval or manufacturing authorization

## Source reconciliation

The source QPC contains 10 possibilities for ST2:

| QP | Source possibility |
|---|---|
| QP001 | Correct Inclusion Relation |
| QP002 | Incorrect Inclusion Relation |
| QP003 | Complete Inclusion Chain |
| QP004 | Missing Set Identification |
| QP005 | Proper Subset Identification |
| QP006 | Superset Identification |
| QP007 | Membership using Inclusion |
| QP008 | Set Relationship Statements |
| QP009 | Counterexample to Inclusion |
| QP010 | Venn Diagram Interpretation |

The source QPC is unchanged. This audit groups the possibilities into five working concepts in `U1_CH1_ST2_concepts.csv`.

## Concept boundaries

1. **Set inclusion and chain relationships:** verify one-way inclusion, reject invalid reverse inference, and complete consistent chains.
2. **Subset and superset identification:** distinguish subset, proper subset and superset; equality and strictness must be handled explicitly.
3. **Membership inferred through inclusion:** infer membership only in the logically valid direction.
4. **Logical set relationship statements:** evaluate quantified statements and use valid counterexamples for universal claims.
5. **Venn diagram representation:** translate between diagram structure and set inclusion; do not infer more than the diagram encodes.

## Cross-QP distinctness flags

- QP001 / QP002: correct versus incorrect relation may be opposite outcomes of one assessment mechanism; do not create separate archetypes solely for true/false polarity.
- QP003 / QP004: completing a chain and identifying a missing set may share the same inference mechanism; separate only if the information-given and inference direction materially differ.
- QP005 / QP006: proper-subset and superset identification may be inverse descriptions of one relation; compare the reasoning pathway before splitting.
- QP008 / QP009: statement evaluation and counterexample construction may overlap; retain separate patterns only when the required reasoning operation differs.
- QP010: diagram presentation alone is not a distinct archetype; retain a separate archetype only when diagram-to-inference reasoning differs from the equivalent symbolic form.

## Initial JEE-worthiness gate

ST2 has more potential for meaningful reasoning than direct N/W/Z classification, particularly through multi-set inclusion chains, invalid inference diagnosis, counterexample construction and equivalence between symbolic and diagrammatic representations.

This is only a hypothesis. Do not label any archetype JEE-worthy until representative tasks demonstrate:
- a distinct reusable reasoning pathway;
- non-trivial inference rather than direct symbol recognition;
- fidelity to the originating QP;
- no duplicate reasoning across QPs;
- clear assumptions about finite/infinite sets and equality where relevant.

## Manufacturing controls

- No archetype IDs have been assigned.
- No archetype candidates have been approved.
- No question instances have been generated.
- Manufacturing remains disabled until representative-task qualification and structural validation are complete.
- Preserve source QP IDs exactly.

**Current status:** 10 source QPs reconciled; 5 provisional concept groupings; 0 approved archetypes; 0 manufacturing-enabled records.
