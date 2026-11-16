# Exam Hub — Master Project Documentation

**Consolidation date:** 16 November 2026  
**Documentation baseline:** recovered project decisions plus read-only audit of QuestionFactory main at 2a253dc.

## 1. Product vision and scope

Exam Hub is the student-facing college-entrance preparation platform. AIR-X provides scheduled national-level assessment and ranking capability. Pragatipath supports progress tracking and personalized improvement.

In-scope entrance examinations: JEE Main, JEE Advanced, NEET and BITSAT. Banking, SSC, UPSC and railway examination preparation are explicitly out of scope.

Student journeys historically defined:
- General Student dashboard.
- Enrolled Student dashboard.
- Chapter tests, mock tests, PYQ practice, adaptive tests and daily challenges.
- AIR-X monthly scheduled tests and rankings.

Administrative roles:
- Super Admin
- Admin
- Q-Admin
- T-Admin

## 2. Platform and data boundaries

Historical platform choices:
- Hostinger Horizons for the student-facing frontend.
- Supabase as the master academic/business database.
- Question Factory OS as a separate manufacturing system.
- Approved CSV/manual upload from Question Factory into Supabase; no direct factory-to-Supabase integration was the agreed boundary.

A Supabase → Horizons backend/cache → Horizons frontend flow was proposed because direct Supabase integration from Horizons was constrained. The cache concepts discussed were questions_cache, sync_logs, test_sessions and test_attempts, with manual and six-hour periodic synchronization proposals. Actual deployment and sync behavior remain unverified.

## 3. Product capabilities

Exam Hub capabilities:
- Chapter-wise tests (historically 25 questions / 1 hour; confirm against current product configuration).
- Full mock tests.
- PYQ practice.
- Adaptive practice.
- Daily challenge.
- AIR-X scheduled tests.
- Student results, progress and performance views.
- Subscription and enrollment flows.

The actual live implementation, authentication, reset-password flow, RLS, iframe/CSP behavior and role permissions were not inspected in this repository audit.

## 4. Academic hierarchy and curriculum

The intended hierarchy is:

Subject → Unit → Chapter → Subtopic.

Historical Mathematics unit baseline:
- U1 Number System
- U2 Algebra
- U3 Coordinate Geometry
- U4 Geometry
- U5 Mensuration
- U6 Statistics
- U7 Probability
- U8 Trigonometry
- U9 Functions
- U10 Limits, Continuity and Differentiability
- U11 Integral Calculus

Physics P1: Units and Measurements. Historical CH1 subtopics included Physical Quantities, SI Units, Dimensions and Errors in Measurement.

Repository curriculum CSV snapshots are broader than the earlier Mathematics U1–U11 record: Mathematics has 15 units, 95 chapters and 533 subtopics; Physics has 23 units; Chemistry has 29 units. Mathematics enable flags show 2/15 units, 2/95 chapters and 533/533 subtopics enabled. The syllabus scope and hierarchical enablement rule require reconciliation.

## 5. Question Factory OS and AMA

Question Factory OS progressed through v2.0, v2.1, v2.2, v2.2.1, v2.3, v2.5 and v3.0. The governing high-level target is Question Factory OS v3.0 — Autonomous Manufacturing Architecture (AMA v1.0).

AMA principles:
- Curriculum defines WHERE.
- AI discovers WHAT.
- Production intelligence decides HOW MUCH.
- Planner creates work.
- Factory executes.
- Validators certify.
- Repair restarts validation at R01.
- Coverage determines completion.
- Export happens only after all quality and coverage gates pass.

Intended stages include curriculum repository, concept/archetype discovery, production intelligence, manufacturing planner, execution, R01–R20 plus DE/AR validation, repair, coverage/saturation and CSV export.

## 6. Catalog and question possibility workflow

The intended discovery chain is:

Concept Catalog → Question Possibility (QP) Catalog → Archetype Catalog → Production Planning → Question Generation.

QPC is a possibility catalogue, not a generated question bank. Concepts and question possibilities are distinct. PYQs are evidence for patterns, not a boundary on future question possibilities. Avoid duplication, chapter-boundary drift and unstable IDs.

Historical QPC Master Prompt v2.0 requirements included considering PYQs across decades, NCERT, standard references, theory, edge cases, misconceptions and future examination patterns.

The repository contains separate concept, QP and archetype generator scripts, but the full production chain is only partially populated and not fully integrated with the CLI.

## 7. Blueprint and quality rules

Historical blueprint versions discussed: v1.2, v1.3, v1.4 and v1.5. v1.3 introduced distractor engineering and a distractor registry. The repository currently contains two incompatible R01–R12 namespaces; see the decision register and reconciliation addendum.

Current repository prompt files:
- Engine/prompts/master/05_blueprint_rules.md
- Engine/prompts/master/06_distractor_engineering.md

The latter defines DE-01 misconception categories DR01–DR10 and DE-02 distractor quality rules.

Difficulty sets:
- S1 Foundation
- S2 Easy+
- S3 Medium
- S4 Hard
- S5 Elite

Stable IDs, question verification, unique answers, clear explanations, examination authenticity, originality, distractor plausibility, repair-before-expand and production readiness remain core requirements.

## 8. Database entities and export

Historical Supabase entities include subjects, units, chapters, subtopics, questions, test_sessions, test_attempts, subscription_plans, user_devices, user_sessions, user_test_results and test_questions. The Horizons cache proposal included questions_cache and sync_logs.

The repository's current question export schema has 29 columns, including question_code, subject_id, unit_id, chapter_id, subtopic_id, difficulty, question_type, answer_type, question_text, options, answer, explanation, concept, archetype, exam metadata, runtime metadata, status, version and set_no. The exporter fills missing fields with empty strings.

The latest user requirement is a simplified CSV schema retaining subject_id and removing unnecessary empty fields. That requirement is not yet implemented in the audited repository; reconcile it against the Supabase import contract before changing the exporter.

## 9. Engineering and preservation rules

- Preserve completed modules and stable IDs.
- Do not rewrite completed modules unless fixing a verified defect.
- Prefer complete-file replacements for approved code changes.
- Apply SOLID principles and preserve architecture consistency.
- Run compileall, mypy and relevant tests after code changes.
- Perform R03 audits, repairs and bounded rebuilds internally without requesting approval for every issue.
- Repair before expanding.
- Do not export unvalidated or incomplete batches.
- No direct Supabase write from the factory; manual CSV upload remains the historical boundary.

## 10. Historical implementation record

Historical completion reports recorded AI subsystem, repair, validation, orchestration, execution pipeline, planning, repositories and service container compileall/mypy success at different milestones. These are historical reports, not current verification.

Repository milestones include:
- 0a6c907 — v3.0 end-to-end pipeline milestone (1 August 2026, historical record).
- 926ad40 — AI response recovery diagnostics (8 August 2026).
- 2a253dc — catalog generation and factory pipeline update (1 September 2026).

The current repository contains a v3.0 CLI but a FactoryRunner still labelled v2.5.0. See the audit report for verified implementation gaps.

## 11. Current position

The master project history and decisions have been consolidated. The GitHub audit is read-only and no source code was changed. Major implementation gaps remain in curriculum wiring, catalog lookup, validation completeness, iterative repair, coverage gates and CSV contract alignment.

See 01_DECISION_REGISTER.md, 08_STATUS_AND_ROADMAP.md, 10_GITHUB_REPOSITORY_AUDIT.md and 11_DECISION_RECONCILIATION_ADDENDUM.md for the authoritative current status.