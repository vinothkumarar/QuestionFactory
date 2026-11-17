# JEE Mathematics Sets/Relations Curriculum Source Audit

**Branch:** `feature/dual-question-engine-v1`  
**Audit date:** 2026-11-17  
**Status:** Repository structure audit complete; no QP or archetype generation authorized by this audit.

## Executive finding

The earlier working assumption that `U9_CH1` is the canonical Sets and Relations chapter is incorrect. The curriculum contains a duplicate/overlapping structure:

- `U9` is named **Functions**, but its `U9_CH1` chapter is named **Sets and Relations**.
- `U15` is named **Sets and Relations**, and its `U15_CH1` chapter is named **Sets and Operations on Sets**.
- The dedicated `U15` structure continues with relations and functions in later chapters.
- The QPC directory currently contains only `Engine/qpc/mathematics/U1_CH1.csv`; neither `U9_CH1.csv` nor `U15_CH1.csv` exists.

Therefore, do not create a QPC file or generate catalogues against U9 or U15 until the canonical curriculum identity and duplicate handling are formally resolved.

## Repository evidence

### Unit records

| Unit code | Unit name | Unit ID |
|---|---|---|
| U9 | Functions | `b79eca7a-3617-40da-a8d1-8b35f818b328` |
| U15 | Sets and Relations | `dd844648-a3ad-4945-85d3-3bb41a6215cd` |

### Chapter records

| Chapter | Chapter name | Parent unit |
|---|---|---|
| U9_CH1 | Sets and Relations | U9 (Functions) |
| U9_CH2–CH7 | Concept of Functions; Domain/Codomain/Range; Types; Composition; Inverse; Graphs | U9 |
| U15_CH1 | Sets and Operations on Sets | U15 (Sets and Relations) |
| U15_CH2 | Intervals and Number Line | U15 |
| U15_CH3 | Relations | U15 |
| U15_CH4–CH6 | Functions and Mapping; Types of Functions; Composition and Inverse Functions | U15 |

### U15_CH1 subtopics

1. U15_CH1_ST1 — Basic Set Concepts
2. U15_CH1_ST2 — Representation of Sets
3. U15_CH1_ST3 — Operations on Sets
4. U15_CH1_ST4 — Venn Diagrams
5. U15_CH1_ST5 — Cardinality of Sets
6. U15_CH1_ST6 — Principle of Inclusion and Exclusion

### QPC source inventory

The recursive feature-branch tree shows only:

- `Engine/qpc/mathematics/U1_CH1.csv`

No QPC source file exists for U9_CH1 or U15_CH1. The earlier attempted U9 path failure was not evidence that the curriculum topic was absent; the actual issue is that the QPC source has not been created and the curriculum has duplicate chapter placement.

## Academic alignment guardrail

The official JEE Main 2027 Mathematics syllabus explicitly includes sets and representation, union, intersection, complement and their algebraic properties, power set, relations (including equivalence relations), functions, one-one/into/onto and composition.

The official JEE Advanced 2026 syllabus includes sets and representations, kinds of sets, set algebra, intersection, complement, difference, symmetric difference, De Morgan's laws, Cartesian products, ordered pairs, relations, domain/codomain, equivalence relations and functions.

These syllabus references establish topic relevance; they do not automatically approve every curriculum subtopic or every possible QP. Each QP must still pass concept-boundary, PYQ-evidence and JEE-fit review.

## Required handling

1. Treat U15 as the likely dedicated Sets and Relations curriculum container, but do not silently migrate or rename any IDs.
2. Treat U9_CH1 as a duplicate/misplaced curriculum record pending owner-level curriculum reconciliation.
3. Preserve both existing curriculum records and all IDs until a controlled mapping decision is made.
4. Do not create U9_CH1 or U15_CH1 QPC rows by copying the other chapter or by assuming their subtopic lists are equivalent.
5. After canonical mapping is resolved, create a source-backed QPC catalogue for the official syllabus scope, then perform concept and archetype qualification.
6. Keep non-syllabus enrichment and foundational material separately classified; do not force every curriculum item into JEE manufacturing.

## Production gate

- QPC source for canonical Sets/Relations chapter: **NOT CREATED**
- Concept catalogue: **NOT STARTED**
- Archetype catalogue: **NOT STARTED**
- Question generation: **BLOCKED**
- Manufacturing approval: **0**
- Existing curriculum IDs modified: **0**
- Existing source files modified: **0**

This is a repository and academic-scope audit only. No code tests or question-generation runs were executed.
