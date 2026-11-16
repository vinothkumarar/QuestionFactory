# Product and Platform

## Product family
- **Exam Hub:** student-facing college-entrance preparation platform.
- **AIR-X:** scheduled national-level assessments and ranking.
- **Pragatipath:** progress tracking and personalized improvement.

## Examination scope
JEE Main, JEE Advanced, NEET and BITSAT. Banking, SSC, UPSC and railways are explicitly excluded.

## Student roles and journeys
- General Student dashboard.
- Enrolled Student dashboard.
- Super Admin, Admin, Q-Admin and T-Admin administrative roles.

## Learning and assessment engines
- Chapter tests (historical baseline: 25 questions, 1 hour).
- Mock Test Engine.
- PYQ Engine.
- Adaptive Test Engine.
- Daily Challenge Engine.
- AIR-X monthly scheduled tests.

## Platform decisions
- Hostinger Horizons frontend.
- Supabase master database.
- Question Factory OS remains a separate question-manufacturing system.
- Approved CSV/manual upload is the historical factory-to-Supabase integration boundary.

## Proposed cache/sync architecture
Supabase → Horizons backend/cache → Horizons frontend. Cache entities discussed: questions_cache, sync_logs, test_sessions and test_attempts. Manual sync and six-hour periodic sync were proposals; deployment and actual job status remain unverified.

## Unresolved product verification
Live student/admin flows, subscriptions, test delivery, result analytics, authentication, reset-password, RLS, iframe/CSP and sync behavior require platform access.