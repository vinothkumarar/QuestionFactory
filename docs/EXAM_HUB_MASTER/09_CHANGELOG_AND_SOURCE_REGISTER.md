# Changelog and Source Register

## Consolidation
2026-11-16 — Historical Exam Hub/Question Factory decisions recovered; repository audit completed read-only; master documentation placed in ChatGPT Library and this documentation branch.

## GitHub sources
Repository: https://github.com/vinothkumarar/QuestionFactory

Audit baseline:
- main commit 2a253dc0018bc28624a3cf2920c815a639b0aeba — Update catalog generation and factory pipeline (1 Sep 2026).
- recovery-test commit 926ad40b4be5f6e8b49e03f496666100b6f9ed6a — Add AI response recovery diagnostics (8 Aug 2026).

Key source files:
- Engine/factory/run_factory.py
- Engine/factory/factory_runner.py
- Engine/curriculum/planner/strategy_registry.py
- Engine/curriculum/planner/strategies/subtopic_strategy.py
- Engine/catalog/concept_catalog/run_all_concepts.py
- Engine/catalog/qp_catalog/run_all_qp_catalogs.py
- Engine/catalog/archetype_catalog/run_all_archetype_catalogs.py
- Engine/bootstrap/service_container.py
- Engine/factory/validation/r01_validator.py, r02_validator.py, r03_validator.py
- Engine/factory/orchestrator/factory_orchestrator.py
- Engine/factory/repair/academic_repair.py
- Engine/schema/question_schema.py
- Engine/exporters/question_csv_exporter.py
- Blueprint/01_RULES.md
- Blueprint/11_GENERATION_ENGINE.md
- Engine/prompts/master/05_blueprint_rules.md
- Engine/prompts/master/06_distractor_engineering.md

Audit limitation: static GitHub file inspection only; no compileall, mypy, tests, AI generation or end-to-end smoke test was executed.