# P1 Taxonomy Duplicate and Overlap Audit

**Audit date:** 2026-11-17  
**Source snapshot:** `feature/dual-question-engine-v1` curriculum CSVs  
**Status:** INITIAL EXACT-NAME AUDIT — semantic adjudication pending

## Integrity checks

| Subject | Subtopic rows | Duplicate subtopic codes | Duplicate subtopic UUIDs | Exact-name duplicate groups |
|---|---:|---:|---:|---:|
| Mathematics | 533 | 0 | 0 | 30 |
| Physics | 233 | 0 | 0 | 5 |
| Chemistry | 260 | 0 | 0 | 7 |
| **Total** | **1,026** | **0** | **0** | **42** |

Duplicate chapter-name groups:
- Mathematics: 2 groups.
- Physics: 0.
- Chemistry: 0.

No code or UUID collisions were found in the inspected subtopic CSVs. The groups below are exact display-name matches, not proof that two records have identical learning outcomes. Do not delete, merge, rename or remap IDs from this report alone.

## Mathematics — 30 exact-name groups

| Exact subtopic name | Existing stable paths | Initial assessment |
|---|---|---|
| Number Line Representation | U1/U1_CH1/ST3; U1/U1_CH4/ST3; U15/U15_CH2/ST3 | Likely overlap; inspect number-system vs set/interval context |
| Basic Properties | U1/U1_CH10/ST2; U1/U1_CH11/ST2; U1/U1_CH12/ST2 | Generic label; context-specific review |
| Applications | U1/U1_CH12/ST6; U1/U1_CH2/ST8; U1/U1_CH9/ST4 | Generic label; context-specific review |
| Basic Set Concepts | U15/U15_CH1/ST1; U2/U2_CH1/ST1; U9/U9_CH1/ST1 | High-confidence duplicate candidate |
| Operations on Sets | U15/U15_CH1/ST3; U2/U2_CH1/ST3; U9/U9_CH1/ST2 | High-confidence duplicate candidate |
| Venn Diagrams | U15/U15_CH1/ST4; U2/U2_CH1/ST4; U9/U9_CH1/ST3 | High-confidence duplicate candidate |
| Parametric Coordinates | U3/U3_CH3/ST2; U3/U3_CH4/ST3; U3/U3_CH5/ST3 | Same pattern under different conics; retain context until reviewed |
| Chord and Tangent | U3/U3_CH3/ST3; U3/U3_CH4/ST4; U3/U3_CH5/ST4 | Same pattern under different conics; retain context until reviewed |
| Definition | U1/U1_CH10/ST1; U1/U1_CH11/ST1 | Generic label; context-specific review |
| Periodicity | U1/U1_CH11/ST6; U1/U1_CH13/ST4 | Possible overlap; verify concept scope |
| Density Property | U1/U1_CH2/ST4; U1/U1_CH4/ST2 | Possible duplicate; inspect rational/real number context |
| Recurring Decimals | U1/U1_CH2/ST6; U1/U1_CH7/ST2 | Likely overlap; inspect conversion/representation outcomes |
| Intervals | U1/U1_CH4/ST4; U2/U2_CH1/ST5 | Possible overlap; number-line vs set notation |
| Initial Value Problems | U12/U12_CH2/ST3; U12/U12_CH4/ST4 | Possible duplicate within differential equations |
| Shortest Distance Between Skew Lines | U13/U13_CH4/ST6; U13/U13_CH6/ST4 | High-confidence duplicate candidate unless geometry context differs |
| Logical Equivalence | U14/U14_CH1/ST6; U14/U14_CH2/ST4 | Possible overlap; inspect proposition/compound statement scope |
| Representation of Sets | U15/U15_CH1/ST2; U2/U2_CH1/ST2 | High-confidence duplicate candidate |
| Equivalence Relations | U15/U15_CH3/ST4; U9/U9_CH1/ST5 | High-confidence duplicate candidate |
| Definition of Functions | U15/U15_CH4/ST1; U2/U2_CH2/ST1 | High-confidence duplicate candidate |
| One-One and Onto Functions | U15/U15_CH4/ST4; U9/U9_CH2/ST3 | High-confidence duplicate candidate |
| Many-One and Into Functions | U15/U15_CH4/ST5; U9/U9_CH2/ST4 | High-confidence duplicate candidate |
| Polynomial Functions | U15/U15_CH5/ST2; U9/U9_CH4/ST1 | High-confidence duplicate candidate |
| Modulus Functions | U15/U15_CH5/ST3; U9/U9_CH4/ST3 | High-confidence duplicate candidate |
| Greatest Integer Functions | U15/U15_CH5/ST4; U9/U9_CH4/ST4 | High-confidence duplicate candidate |
| Exponential and Logarithmic Functions | U15/U15_CH5/ST5; U9/U9_CH4/ST5 | High-confidence duplicate candidate |
| Periodic Functions | U15/U15_CH5/ST6; U9/U9_CH4/ST6 | High-confidence duplicate candidate |
| Inverse Functions | U15/U15_CH6/ST3; U2/U2_CH2/ST5 | High-confidence duplicate candidate |
| Existence of Inverse Functions | U15/U15_CH6/ST4; U9/U9_CH6/ST1 | High-confidence duplicate candidate |
| Sample Space and Events | U2/U2_CH10/ST1; U7/U7_CH1/ST1 | High-confidence duplicate candidate |
| Common Tangents | U3/U3_CH2/ST6; U4/U4_CH3/ST5 | Likely overlap; circle vs broader geometry context |

Duplicate chapter titles in Mathematics:
- “Types of Functions”: U15/U15_CH5 and U9/U9_CH4.
- “Sets and Relations”: U2/U2_CH1 and U9/U9_CH1.

## Physics — 5 exact-name groups

| Exact subtopic name | Existing stable paths | Initial assessment |
|---|---|---|
| Resonance | P10/P10_CH1/ST10; P16/P16_CH1/ST8 | Different physical contexts (oscillations vs AC); do not merge |
| Series Combination | P11/P11_CH2/ST4; P12/P12_CH1/ST7 | Capacitors vs resistors; do not merge without content comparison |
| Parallel Combination | P11/P11_CH2/ST5; P12/P12_CH1/ST8 | Capacitors vs resistors; do not merge without content comparison |
| Magnification | P18/P18_CH1/ST4; P18/P18_CH3/ST4 | Mirror vs lens context; retain context |
| First Law | P3/P3_CH1/ST1; P8/P8_CH3/ST2 | Newton's First Law vs First Law of Thermodynamics; not duplicates |

## Chemistry — 7 exact-name groups

| Exact subtopic name | Existing stable paths | Initial assessment |
|---|---|---|
| Electronic Configuration | C15/C15_CH1/ST1; C17/C17_CH1/ST1; C2/C2_CH1/ST9 | Related but context-specific (s-block, d-block, atomic structure) |
| Concentration Terms | C1/C1_CH1/ST9; C9/C9_CH1/ST2 | High-confidence duplicate candidate; compare learning outcomes and formula coverage |
| General Characteristics | C15/C15_CH2/ST1; C17/C17_CH1/ST2 | Generic label; context-specific review |
| Oxidation States | C17/C17_CH1/ST3; C18/C18_CH1/ST4 | d-block vs f-block; retain context unless exact outcomes duplicate |
| Nomenclature | C19/C19_CH1/ST3; C21/C21_CH1/ST2 | Coordination vs organic nomenclature; do not merge |
| Isomerism | C19/C19_CH1/ST5; C21/C21_CH1/ST3 | Coordination vs organic isomerism; do not merge |
| Vapour Pressure | C4/C4_CH2/ST3; C9/C9_CH1/ST6 | States of matter vs solution vapour pressure; inspect scope |

## Required semantic adjudication

For each duplicate-name group, compare:
1. Learning outcome and prerequisite concepts.
2. Exact subtopic descriptions, formulas and canonical examples.
3. PYQ mapping and exam applicability.
4. Whether the duplication is a true duplicate, contextual reuse, parent-child overlap or merely a generic display label.
5. Stable-ID lineage if a future consolidation is approved.

Use dispositions: `TRUE_DUPLICATE_CANDIDATE`, `CONTEXTUAL_REUSE`, `PARENT_CHILD_OVERLAP`, `GENERIC_LABEL`, `NOT_DUPLICATE`, `UNRESOLVED`.

No changes to the source taxonomy have been made. Existing codes and UUIDs remain untouched.
