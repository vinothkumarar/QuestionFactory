# Current Status and Roadmap

**Audit date:** 16 November 2026  
**Baseline:** main at 2a253dc0018bc28624a3cf2920c815a639b0aeba (1 September 2026).  
**Mode:** read-only; no source code changed.

## Status

| Workstream | Finding | Status |
|---|---|---|
| Product scope | Historical product and exam scope recovered | Historical-confirmed |
| v3.0 CLI | Engine/factory/run_factory.py identifies as v3.0 | Present |
| FactoryRunner | Still reports VERSION 2.5.0 | Version drift |
| Curriculum | CSV loader exists; CLI strategy registry defaults to Physics-only in-memory sample | Partial/miswired |
| Concept/QP catalogs | Generators and selected JSON outputs exist | Partial |
| Archetype catalogs | Generator and loader exist; production coverage incomplete | Partial |
| U1_CH1_ST1 new catalog | New concept/QP JSON not found; legacy QPC/QP assets exist in older schema | Blocked |
| Validation | R01/R02/R03 registered only | Partial |
| Repair | Structural + academic repair; one pass then revalidation | Partial |
| Coverage | 100% coverage gate not verified in production path | Gap |
| CSV export | 29 columns with empty defaults; does not match simplified schema request | Contract mismatch |
| Supabase/Horizons | Live integration not inspected | Not verified |
| CI/tests | No status checks on audited HEAD; no tests run in this audit | Not verified |

## Critical blockers

1. SubtopicStrategy passes a short key such as ST1 to ArchetypeCatalogLoader, while generated catalog filenames use full scope names such as U2_CH8_ST1.json.
2. The new concept/QP pipeline does not contain U1_CH1_ST1 JSON outputs. Legacy U1 QPC and chapter-level QP/archetype assets use different naming and ID conventions.
3. StrategyRegistry defaults to InMemoryCurriculumRepository, which contains only Physics P1 CH1 ST1–ST4. The CSV-backed CurriculumRegistry exists separately but is not used by the v3.0 CLI path.
4. Only R01–R03 are registered; R03 contains checks not invoked by its public validate method.
5. FactoryOrchestrator performs one repair pass and one revalidation, not bounded iterative rebuild from R01.
6. No complete 100% coverage/saturation gate is verified.
7. The current CSV schema has 29 fields and fills missing values with empty strings, contrary to the simplified CSV target.
8. Mathematics repository data has 15 units versus the earlier U1–U11 record; enable flags need hierarchical reconciliation.

## Recommended order

1. Freeze canonical blueprint and rule namespaces.
2. Wire the full CSV-backed curriculum registry into CLI strategies.
3. Fix full-scope catalog lookup and migrate legacy U1 assets while preserving stable IDs.
4. Complete and register validation rules; ensure all required checks are invoked.
5. Implement bounded repair/rebuild restarting at R01.
6. Implement the 100% coverage/saturation gate.
7. Reconcile simplified CSV export with Supabase import requirements.
8. Run clean-checkout compileall, mypy, unit/integration tests and a bounded U1_CH1_ST1 smoke test.
9. Verify live Horizons/Supabase authentication, RLS, sync and student/admin journeys.

No source-code changes, branch merges or catalog regeneration were performed during the audit.