# 08_UPLOAD_REPAIR.md

STATUS

RESERVED

NOT ACTIVE IN QUESTION FACTORY OS v1.0

Purpose

Reserved for future SV-02 Upload Feedback Rule.

Current architecture stops at CSV generation.

Supabase upload remains manually controlled and outside the Question Factory.

Future pipeline:

Upload Error
↓
Analyze
↓
Repair affected rows
↓
Preserve question_code
↓
Generate corrected CSV
↓
Retry upload

Activation

Will be activated only if automated upload is introduced.

Current State

RESERVED
# SV-02 Upload Feedback Rule

Purpose

Repair upload failures without regenerating complete sets.

Common Errors

- Column mismatch
- Enum violation
- Null violation
- Duplicate key
- Length violation

Pipeline

Error
↓
Analyze
↓
Repair affected rows
↓
Preserve question_code
↓
Generate corrected CSV
↓
Retry upload

Principle

Repair rows, not sets.
