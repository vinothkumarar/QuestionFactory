# Question Factory OS
# Architecture v2.0 (Frozen)

---

## Vision

Question Factory OS is an autonomous AI-powered question generation platform.

Its responsibility is NOT to be the student database.

Its responsibility is NOT to be the examination platform.

Its responsibility is to produce verified, production-ready questions.

---

# System Architecture

                AIR-X Platform

                      │

              Supabase Database
        (Master Academic Database)

                      │

        ┌─────────────┴─────────────┐

        ▼                           ▼

 Student Platform            Question Factory OS

                                      │

                                      ▼

                           Factory Runtime Engine

                                      │

                                      ▼

                           OpenAI Generation Engine

                                      │

                                      ▼

                           Validation Engine

                                      │

                                      ▼

                            Smart Export Engine

                                      │

                                      ▼

                               CSV Production

---

# Responsibility Matrix

## Supabase

Stores business data.

Examples

- Subjects
- Units
- Chapters
- Subtopics
- Questions
- Students
- Tests
- Results
- Subscriptions
- Analytics

Supabase is the MASTER DATA SOURCE.

---

## Question Factory OS

Responsible for

- Prompt construction
- AI generation
- Question validation
- Batch generation
- CSV export
- Runtime management
- Production automation

Question Factory NEVER edits academic structure.

It only consumes it.

---

## SQLite (Factory Database)

Stores Factory Runtime information ONLY.

Examples

- Runtime status
- Batch history
- Generated CSV history
- Retry queue
- Generation logs
- Engine version
- Prompt version
- Validation statistics

SQLite is NOT an academic database.

SQLite is the Factory Operating System.

---

## CSV

CSV is the Production Output.

Every CSV represents one completed production batch.

Example

P1_CH1_ST4_S1_B1.csv

CSV files are upload-ready.

---

# Production Flow

Supabase

↓

Question Factory

↓

Generate

↓

Validate

↓

Export CSV

↓

Manual Review (Optional)

↓

Upload to Supabase

---

# Design Principles

1.
One Source of Truth

Academic structure exists ONLY in Supabase.

2.
Single Responsibility

Each component has one responsibility.

3.
No Duplicate Data

Do not maintain the syllabus in multiple places.

4.
Factory First

Question Factory focuses only on production.

5.
Automation

All repetitive work should become automatic.

6.
Version Controlled

Architecture changes require version updates.

---

# Future Roadmap

v2.1

Repository Layer

v2.2

Navigation Engine

v2.3

Production Scheduler

v2.4

Retry Engine

v2.5

Autonomous Factory

---

Architecture Status

FROZEN

Version

2.0

