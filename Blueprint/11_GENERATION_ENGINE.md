# GE-01 Generation Engine

Purpose

Provide the execution model for Question Factory.

Execution Pipeline

AUTORUN
↓
Read progress.json
↓
Locate current node
↓
Generate batch
↓
Apply R01-R12
↓
STRICT R03 Verification
↓
RB-01 Autonomous Rebuild Loops
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
Move to next node

Principles

Coverage > Count

Quality > Speed

Repair > Expand

Stable IDs Forever

Only Final Releases

Factory ≠ Warehouse
