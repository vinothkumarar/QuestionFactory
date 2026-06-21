# QuestionFactory
# Runtime State Transition Rules

Purpose

Define lifecycle transitions during Question Factory execution.

────────────────────────
Batch Lifecycle
────────────────────────

P1_CH1_ST4_S1_B1

PENDING
↓
ACTIVE
↓
COMPLETE

Rules

* A batch becomes ACTIVE when generation starts.
* A batch becomes COMPLETE only after:

  * R01-R12 pass
  * STRICT R03 verification passes
  * RB-01 rebuild loops converge
  * SV-01 schema validation passes

────────────────────────
Set Lifecycle
────────────────────────

S1

ACTIVE
↓
COMPLETE

S5

ACTIVE
↓
AR-01 Saturation Review
↓
CONTINUE or SATURATED

Rules

* Set closure is determined by coverage, not count.
* Saturation belongs to the set, not to individual batches.

────────────────────────
Subtopic Lifecycle
────────────────────────

ACTIVE
↓
COMPLETE

Rules

* S1-S5 completed.
* AR-01 indicates saturation achieved.
* Move automatically to next subtopic.

────────────────────────
Chapter Lifecycle
────────────────────────

ACTIVE
↓
COMPLETE

Rules

* All subtopics completed.

────────────────────────
Unit Lifecycle
────────────────────────

ACTIVE
↓
COMPLETE

Rules

* All chapters completed.

────────────────────────
Project Lifecycle
────────────────────────

ACTIVE
↓
COMPLETE

Rules

* All units completed.

────────────────────────
Failure Handling
────────────────────────

Generation Error
↓
RB-01 Rebuild
↓
Retry

Schema Error
↓
SV-01 Repair
↓
Retry

Upload Error
↓
SV-02 (Future)
↓
Repair rows only

────────────────────────
Global Principles

Coverage > Count

Quality > Speed

Repair > Expand

Stable IDs Forever

Only Final Releases

Factory ≠ Warehouse
