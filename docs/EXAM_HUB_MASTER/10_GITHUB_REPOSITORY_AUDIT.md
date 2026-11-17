# GitHub Repository Audit — Read-only

**Date:** 16 November 2026  
**Repository:** https://github.com/vinothkumarar/QuestionFactory  
**Baseline:** main, commit 2a253dc0018bc28624a3cf2920c815a639b0aeba (1 September 2026).

## Repository baseline
Branches observed: main and recovery-test. Main is default. The latest commit is “Update catalog generation and factory pipeline”. The combined status response returned no CI status entries. smoke_test.log is empty. No tests were executed during this audit.

## Production chain
The v3.0 CLI in Engine/factory/run_factory.py builds a manufacturing request and queue, then invokes ProductionOrchestrator and FactoryRunner. FactoryRunner still identifies as 2.5.0. The pipeline reaches QuestionGenerator, FactoryOrchestrator, AI generation, validation, repair/revalidation and CSV export.

## Catalog pipeline
Separate Concept Catalog, QP Catalog and Archetype Catalog scripts exist. The latest commit touched 74 concept JSONs, 9 QP JSONs and 5 archetype JSONs. These are partial artifacts, not proof of full curriculum coverage. The new concept runner reads Engine/qp_catalog/syllabus.csv (40 selected Mathematics rows, U2/U3/U4/U8); it does not include U1_CH1_ST1.

Legacy U1 assets exist:
- Engine/qpc/mathematics/U1_CH1.csv — 1,105 lines of subtopic-scoped question possibilities.
- Engine/qp_catalog/catalogs/U1_CH1_Number_System.json and CSV — chapter-level QP/archetype records using A001-style IDs.

The new-format U1_CH1_ST1 concept/QP JSON files were not found at the expected catalog paths. Legacy data must be mapped deliberately; do not overwrite stable IDs.

## Production blockers
1. SubtopicStrategy calls ArchetypeCatalogLoader.load(request.subtopic), e.g. ST1. Catalog generators write full-scope filenames such as U2_CH8_ST1.json. The lookup contract does not match.
2. StrategyRegistry defaults to InMemoryCurriculumRepository containing only Physics P1 CH1 ST1–ST4. The CSV-backed CurriculumRegistry exists in a separate service container, but the v3.0 CLI does not use that container.
3. CLI still accepts --questions-per-batch (default 20); the strategy creates one work item per archetype per set. Autonomous workload sizing is not demonstrated.
4. ServiceContainer registers R01, R02 and R03 only.
5. R03Validator has _validate_blueprint_attributes and _validate_jee_quality methods that are not invoked by validate().
6. FactoryOrchestrator performs one repair pass and one revalidation, not an iterative regenerate/rebuild loop.
7. No 100% coverage gate is verified in the production path.
8. QuestionCSVExporter writes all 29 declared columns and fills absent values with empty strings; simplified CSV target is not implemented.

## Blueprint conflicts
Engine/prompts/master/05_blueprint_rules.md defines R01 Concept First through R12 Production Readiness. Blueprint/01_RULES.md defines a different R01–R12 set (Continuity through Saturation Monitoring). Engine/prompts/master/06_distractor_engineering.md defines DE-01 DR01–DR10 and DE-02 quality rules. AR17–AR20 are archetype patterns, not validators. A versioned Blueprint v1.5 file was not located.

## Curriculum snapshot
Mathematics: 15 units, 95 chapters, 533 subtopics; 2 units and 2 chapters enabled, all 533 subtopics flagged enabled. Physics: 23 units, P1 enabled. Chemistry: 29 units, none enabled. The Mathematics snapshot differs from the earlier U1–U11 baseline.

## Branch/security notes
recovery-test differs from main in factory_runner.py. Its response_parser logs the first 5,000 characters of raw AI response; main does not. Do not merge without review. .gitignore excludes .env, but engine_structure.txt lists Engine/.env; the contents were not accessed. Verify tracked status and rotate credentials if exposed.

## Verification limit
This was static read-only inspection. No test suite, compileall, mypy, CLI run, AI call or production smoke test was executed. Historical success reports are not current verification.