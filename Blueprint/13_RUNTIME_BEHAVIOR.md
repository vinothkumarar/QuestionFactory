# RT-01 Runtime Behavior

Purpose

Define state transitions for Question Factory execution.

Pipeline

AUTORUN
↓
Read progress.json
↓
Locate current node
↓
Generate batch
↓
R01-R12
↓
STRICT R03 Verification
↓
RB-01 Rebuild Loops
↓
AR-01 Saturation Review
↓
SV-01 Schema Validation
↓
Release Final Batch
↓
Update batch_manifest.json
↓
Update metadata.json
↓
Update progress.json
↓
Determine next node
↓
Create folders automatically if needed
↓
Continue

Batch Completion

ACTIVE
↓
COMPLETE

Set Completion

Batches exhausted
↓
AR-01 Review
↓
CONTINUE or CLOSE

Subtopic Completion

S1-S5 completed
↓
SATURATED
↓
Move to next subtopic

Chapter Completion

All subtopics complete
↓
Move to next chapter

Unit Completion

All chapters complete
↓
Move to next unit

Principles

Coverage > Count

Quality > Speed

Repair > Expand

Stable IDs Forever

Only Final Releases

Factory ≠ Warehouse
