# P1 PYQ Source Acquisition Audit

**Audit date:** 2026-11-17  
**Status:** SOURCE INVENTORY RECONCILED — PDF/KEY ACQUISITION NOT COMPLETE

## 1. Master inventory

The Library inventory covers 2002–2026 and contains 247 records across four distinct exam families:

| Exam family | Records |
|---|---:|
| JEE Main | 185 |
| JEE Advanced | 28 |
| IIT-JEE historical | 21 |
| AIEEE historical | 13 |
| **Total** | **247** |

The Acquisition Tracker and Audited Source Registry each contain 247 unique `PYQ_ID` values with zero duplicate IDs. The separate Paper Inventory sheet contains 247 rows but does not carry the same stable `PYQ_ID` column.

These are inventory records, not 247 acquired PDFs, transcribed question sets or verified answers.

## 2. Tracker reconciliation

| Field | 2026 English Acquisition Tracker | Phase 2.1 Audited Source Registry |
|---|---:|---:|
| Rows | 247 | 247 |
| Acquisition status — Not yet acquired | 236 | 247 |
| URL verified — PDF accessible | 11 | 0 |
| PDF Verified = Yes | 11 | 0 |
| PDF Verified = No | 236 | 247 |
| Answer Key Verified = Yes | 0 | 0 |
| Answer Key Verified = No | 247 | 247 |
| Populated PDF URL | 11 | 0 |
| Populated Answer Key URL | 0 | 0 |
| Populated SHA-256 | 0 | 0 |

Important: the Acquisition Tracker's 11 `PDF Verified = Yes` values are URL/access checks only. They do not prove that PDF bytes were saved locally, that a hash was calculated, or that the PDF was fully inspected.

### Official-source flag discrepancy

The two trackers use different labels/counts for the same 66 non-`No` official-source flags:

| Official Source Confirmed value | Acquisition Tracker | Audited Registry |
|---|---:|---:|
| Yes | 11 | 2 |
| Yes — official archive | 26 | 26 |
| Yes — NTA archive exists | 29 | 38 |
| No | 181 | 181 |

The total non-`No` count is 66 in both, but the categorisation differs. Reconcile the nine-row label difference before treating these fields as a canonical source-quality measure.

## 3. 2026 acquisition state

The 2026 subset contains 21 records:
- JEE Main: 19 Paper 1 shifts — 10 January and 9 April.
- JEE Advanced: Paper 1 and Paper 2.

Eleven question-paper URLs are marked accessible:
- Nine official NTA April JEE Main shifts.
- Two official JEE Advanced 2026 paper PDFs.

The ten January JEE Main shifts remain without an acquired/verified question-paper PDF URL in the current tracker.

The 2026 Acquisition Tracker has zero populated Answer Key URL values and zero SHA-256 values. The official NTA Main Session I and Session II final answer-key PDFs have been identified separately in `P1_PYQ_ANSWER_KEY_AUDIT.md`, but they have not yet been linked to all 19 Main shifts in the tracker.

The official JEE Advanced 2026 question-paper PDFs are accessible. The exact official final answer-key PDF URL and Paper 1/Paper 2 question-ID matches remain pending.

## 4. Question-level evidence achieved

Two questions from the official 2 April 2026 JEE Main Paper 1 Shift 1 Physics paper were matched to the NTA Session II final answer key and independently solved:

| Question | Internal subtopic | Paper question ID | Key option ID | Option/value | Independent check |
|---|---|---:|---:|---|---|
| Q26 | P1_CH1_ST4 — Dimensional Analysis | 69112126 | 69112187 | B / 1 | `[epsilon0 E^2]` is energy density, `M L^-1 T^-2`; the requested combination equals 1 |
| Q27 | P1_CH1_ST6 — Errors and Measurements | 69112127 | 69112191 | B / 1.65 | Error propagation in `Y=4FL/(pi*d^2*x)` gives relative error 0.0276667 and `alpha=1.65` |

Detailed source URLs, question identifiers, answer-key identifiers, independent calculations and source-page references are stored in `P1_PYQ_EVIDENCE_REGISTER.csv`.

This is a two-question, one-shift sample only. It does not establish year-wise topic frequency, shift representativeness or complete paper verification.

## 5. Provenance status model

Keep these states distinct:

1. `INVENTORIED`
2. `SOURCE_URL_IDENTIFIED`
3. `URL_ACCESS_VERIFIED`
4. `PDF_BYTES_ACQUIRED`
5. `SHA256_VERIFIED`
6. `PAPER_METADATA_VERIFIED`
7. `QUESTION_TRANSCRIPTION_VERIFIED`
8. `ANSWER_KEY_SOURCE_LINKED`
9. `ANSWER_KEY_PAPER_MATCHED`
10. `ANSWER_KEY_QUESTION_MATCHED`
11. `ANSWER_INDEPENDENTLY_VERIFIED`
12. `SYLLABUS_MAPPING_APPROVED`

A record may advance only when evidence for that exact state exists. A shared answer-key PDF URL is not proof that every paper/shift/question has been matched.

## 6. Source acquisition blockers and actions

| Blocker | Required action | P1 handling |
|---|---|---|
| 2002–2025 source quality is mixed | Verify primary/official sources or label archive-only | Keep source confidence separate from paper availability |
| 10 January 2026 Main papers not located | Search official NTA response-sheet/question-paper publication and preserve non-official copies as such | Do not mark acquired without source evidence |
| 9 April 2026 Main PDFs accessible but not local | Acquire bytes where technically/legal available, record file size and SHA-256 | Current state URL-access-verified only |
| Main Session I/II keys not linked to all shifts | Match date, shift, subject and question IDs for every paper | Two Session II Q26/Q27 matches only |
| Advanced 2026 final key URL not recovered | Locate official final key and map both papers | Keep both Advanced papers unverified |
| No local hashes | Acquire exact bytes and calculate SHA-256 | Do not invent or copy hashes |
| Source flags differ between two trackers | Reconcile labels while preserving original workbook snapshots | No destructive overwrite |

## 7. P1 decision

The 247-record inventory is structurally usable as a target list, but not as a verified PYQ bank. The 2026 sample proves that official question IDs can be matched to final answer-key option IDs and independently checked. It does not satisfy bulk source acquisition, complete answer-key reconciliation or cross-year representativeness.

No bulk question transcription, PYQ-driven production batch or production-question generation is authorised by this audit.
