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
