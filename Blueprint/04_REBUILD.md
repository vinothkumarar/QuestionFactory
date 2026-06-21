RB-01 Autonomous Rebuild Rule

Purpose:
Ensure only final validated batches are released.

Pipeline:

Generate
↓
STRICT R03 Verification
↓
Detect inconsistencies
↓
Internal Rebuild
↓
Re-audit
↓
Repeat until clean
↓
Release

Principles:

* Unlimited internal rebuild loops.
* No user approval required.
* Preserve stable IDs.
* Repair > Expand.
* Release only final validated output.

Failure Action:

Rebuild affected questions before expanding further.
