# Curriculum and Database

## Hierarchy
Subject → Unit → Chapter → Subtopic.

## Historical Mathematics units U1–U11
U1 Number System; U2 Algebra; U3 Coordinate Geometry; U4 Geometry; U5 Mensuration; U6 Statistics; U7 Probability; U8 Trigonometry; U9 Functions; U10 Limits, Continuity and Differentiability; U11 Integral Calculus.

## Physics baseline
P1 Units and Measurements; CH1 historical subtopics include Physical Quantities, SI Units, Dimensions and Errors in Measurement.

## Repository curriculum snapshots
- Mathematics: 15 units, 95 chapters, 533 subtopics.
- Physics: 23 units; P1 enabled in unit CSV.
- Chemistry: 29 units; none enabled in unit CSV.
- Mathematics raw flags: 2/15 units enabled, 2/95 chapters enabled, 533/533 subtopics enabled.

These snapshots differ from the earlier U1–U11 record. Define effective hierarchical enablement so child flags cannot bypass disabled parents.

## Database entities historically discussed
subjects, units, chapters, subtopics, questions, test_sessions, test_attempts, subscription_plans, user_devices, user_sessions, user_test_results, test_questions. Proposed Horizons cache: questions_cache, sync_logs, test_sessions, test_attempts.

## Question export fields
The repository's legacy 29-column schema includes question_code, subject_id, unit_id, chapter_id, subtopic_id, difficulty, question_type, answer_type, question_text, option_a–d, correct_option, answer, explanation, more_explanation, concept_tested, question_archetype, exam_level, source_type, tags, estimated_time_sec, marks, negative_marks, language, status, version and set_no.

The user-requested simplified schema retains subject_id and removes unnecessary empty fields. Reconcile exact required fields against Supabase before changing the exporter.

## Data boundary
Supabase remains master academic data. Factory CSV upload is the historical integration boundary; no direct DB integration was part of the agreed design.