# Question Factory OS v3.0 — AMA v1.0

## Governing principle
Autonomous manufacturing should transform a curriculum scope into validated, coverage-complete question data without per-question operator intervention.

## Architecture phases
- Phase 0 — Foundation: AI engine, prompt builder, response parser, runtime repository, blueprint loader, factory runner, orchestrator, CSV exporter, repair engine and dependency injection.
- Phase 1 — Curriculum Repository: curriculum data and hierarchy only; no manufacturing logic.
- Phase 2 — AI Archetype Discovery: discover concepts/question possibilities/archetypes, with confidence and versioning rather than a hardcoded exhaustive catalogue.
- Phase 3 — Production Intelligence: combine curriculum, catalogues, coverage and difficulty requirements.
- Phase 4 — Manufacturing Planner: operator defines scope; planner computes workload and queue.
- Phase 5 — Factory Execution: generate questions from planned work items.
- Phase 6 — Validation: R01–R20 plus DE/AR and technical checks.
- Phase 7 — Repair: repair defects; every repaired item restarts validation at R01.
- Phase 8 — Coverage: continue until required coverage is complete, with bounded stop conditions.
- Phase 9 — CSV Export: export only after validation and coverage gates pass.

## Design principles
- Curriculum defines WHERE.
- AI discovers WHAT.
- Production intelligence decides HOW MUCH.
- Planner creates work.
- Factory executes.
- Validators certify.
- Repair restarts R01.
- Coverage determines completion.
- Export only after gates pass.

## Repository conformance
The repository has a v3.0 CLI and partial catalog pipeline, but currently registers R01–R03 only, performs one repair/revalidation pass and has no verified 100% coverage gate. The default CLI strategy registry still uses a Physics-only in-memory sample. Treat AMA as the governing target, not proof of complete implementation.