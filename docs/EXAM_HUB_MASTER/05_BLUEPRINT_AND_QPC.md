# Blueprint, QPC and Catalog Rules

## Blueprint history
Versions v1.2, v1.3, v1.4 and v1.5 were discussed. v1.3 introduced distractor engineering (DE-01/DE-02). A versioned authoritative v1.5 artifact was not found in the audited repository.

## R01–R12 conflict
- Engine/prompts/master/05_blueprint_rules.md: Concept First, Single Learning Objective, Mathematical Verification, Unique Answer, Explanation Quality, Difficulty Alignment, Language Quality, Examination Authenticity, Originality, Educational Value, Internal Consistency, Production Readiness.
- Blueprint/01_RULES.md: Continuity, Difficulty Progression, Strict Verification, Quality, Stable IDs, Internal Rebuild, Coverage Expansion, Archetype Activation, Diversity, Pattern Repetition, Formula Diversity, Saturation Monitoring.

These are separate rule namespaces using the same IDs. Do not merge or renumber without reconciling the frozen source.

## Distractor engineering
Current repository prompt Engine/prompts/master/06_distractor_engineering.md defines DE-01 misconception categories DR01–DR10 and DE-02 distractor quality rules. Historical DR01–DR07 notes differ; retain them as history, not as a combined registry.

## Archetype patterns
Blueprint/02_ARCHETYPES.md defines AR17 Case Splitting, AR18 Optimization, AR19 Functional Relation and AR20 Mixed Concept. These are archetypes, not validator IDs.

## Difficulty sets
S1 Foundation; S2 Easy+; S3 Medium; S4 Hard; S5 Elite.

## QPC design
QPC is a complete possibility catalogue for one subtopic, not a generated question bank. Concepts and QPs are distinct. Use historical PYQs as evidence of patterns, not the limit of possible question forms. Consider NCERT, standard references, theory, edge cases, misconceptions and future examination patterns. Prevent duplicates and chapter-boundary drift.

## Catalog chain
Concept Catalog → QP Catalog → Archetype Catalog → Production Planner → Question Generator.

The current repository has separate generators but partial scope coverage and an unresolved full-scope catalog lookup contract. Preserve stable IDs during any migration.