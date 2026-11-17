# System Architecture

## Intended separation
1. Exam Hub application: student/admin experience, tests, subscriptions and analytics.
2. Supabase: master academic and application data.
3. Question Factory OS: offline/controlled question manufacturing, validation and CSV export.
4. Horizons backend/cache: proposed intermediary serving the frontend and syncing from Supabase.

## Academic hierarchy
Subject → Unit → Chapter → Subtopic → Concepts → Question Possibilities → Archetypes → Generated Questions.

## Intended manufacturing lifecycle
Curriculum defines scope → AI discovers concepts and archetypes → production intelligence computes coverage/workload → planner creates work items → factory generates → validators certify → repair restarts validation at R01 → coverage gate determines completion → CSV export.

## Repository implementation observation
The current CLI creates its own StrategyRegistry. That registry defaults to a sample InMemoryCurriculumRepository containing only Physics P1 CH1 ST1–ST4. A separate CSV-backed CurriculumRegistry exists but is not wired into the CLI path. The subtopic strategy also passes short identifiers such as ST1 to an archetype loader whose generated catalog files use full scope names such as U2_CH8_ST1.json.

## Integration boundary
The historical decision is manual CSV upload into Supabase. No direct Question Factory database writes should be introduced without an explicit architecture decision.

## Verification status
This architecture describes the target and historical decisions, not a claim that every component is currently deployed or wired. See 10_GITHUB_REPOSITORY_AUDIT.md.