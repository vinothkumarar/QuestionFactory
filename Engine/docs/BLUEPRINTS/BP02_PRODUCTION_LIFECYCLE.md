# Question Factory OS

# Blueprint BP02

# Production Lifecycle

Version: 1.0

Status: FROZEN

---

## Purpose

The Production Lifecycle defines every state that a Production Order passes through.

Every Production Order must always be in exactly one state.

---

## Lifecycle

PLANNED

↓

READY

↓

RUNNING

↓

VALIDATING

↓

EXPORTING

↓

COMPLETED

---

## Failure Flow

RUNNING

↓

FAILED

↓

RETRY

↓

RUNNING

---

## State Definitions

### PLANNED

The Production Planner has created the order.

No worker has accepted it.

---

### READY

The order is waiting for execution.

---

### RUNNING

A Production Worker is generating questions.

---

### VALIDATING

Questions are being verified.

---

### EXPORTING

Validated questions are being written to production CSV.

---

### COMPLETED

The order finished successfully.

---

### FAILED

The worker could not complete execution.

---

### RETRY

The order has been scheduled for another attempt.

---

## Rules

1. Every order must have exactly one lifecycle state.

2. Orders may only move forward unless entering RETRY.

3. COMPLETED orders are immutable.

4. FAILED orders retain complete error history.

5. Every state transition must be logged.

---

Blueprint Status

FROZEN
