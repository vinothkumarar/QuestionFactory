# P1 PYQ and Answer-Key Audit — Initial Findings

**Audit date:** 2026-11-17  
**Scope:** IIT-JEE/AIEEE historical records and JEE Main/JEE Advanced, 2002–2026  
**Status:** IN PROGRESS — NOT AN ACQUISITION OR QUESTION-VERIFICATION CERTIFICATE

## Inventory integrity

The Library master inventory contains 247 data rows and 247 unique PYQ IDs:

| Family | Records |
|---|---:|
| IIT-JEE historical | 21 |
| AIEEE historical | 13 |
| JEE Main | 185 |
| JEE Advanced | 28 |
| **Total** | **247** |

The audited tracker splits these into 137 Historical verification records and 110 Ready for acquisition records.

The audited tracker currently reports:
- Acquisition Status = Not yet acquired for all 247.
- PDF Verified = No for all 247.
- Answer Key Verified = No for all 247.
- No populated PDF URL, Answer Key URL, Solution URL or SHA256 in those 247 tracker rows.
- No PDF files are present in the audited repository tree.

This inventory must not be represented as 247 acquired PDFs, transcribed questions, verified answers or syllabus-mapped questions.

## 2026 English acquisition workbook reconciliation

The 2026 workbook contains 21 records:
- JEE Advanced Paper 1 and Paper 2.
- JEE Main Paper 1: 10 January shifts and 9 April shifts.

Eleven records are marked “URL verified — PDF accessible” (two JEE Advanced papers and nine April JEE Main shifts). The ten January JEE Main records remain “Not yet acquired”.

The workbook's PDF Verified = Yes field is an access/URL status in these records; it is not proof that local bytes were acquired and hashed. No local PDF bytes or SHA-256 values were present in the inspected files or repository tree.

All 21 2026 records still have Answer Key Verified = No in the workbook. Official key documents were found separately, but no per-question or per-shift reconciliation has yet been completed.

## Official JEE Main 2026 final answer-key evidence

NTA's official documents register links final answer-key documents for both Paper 1 sessions:

1. **Session I final answer key**
   - Official PDF: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/02/20260216459398513.pdf
   - The PDF is titled “JEE (Main) - 2026: SESSION - 1 FINAL ANSWER KEY OF B.E./B.Tech AS ON 16.02.2026”.
   - Its pages identify examination dates and shifts, with Mathematics, Physics and Chemistry question IDs and correct options/option IDs.

2. **Session II final answer key**
   - Official PDF: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/04/20260420409057044.pdf
   - The PDF is titled “JEE (Main) - 2026: SESSION - 2 FINAL ANSWER KEY OF B.E./B.Tech ON WHICH RESULT COMPILED”.
   - Its pages identify examination dates and shifts, with subject-wise question IDs and correct option IDs.

NTA official documents index: https://jeemain.nta.nic.in/documents/

**Verification state:** The official answer-key sources are located and their indexed contents are accessible. The tracker still needs the exact answer-key URL, local bytes, SHA-256, exam date/shift matching, and question-ID matching for each paper. Therefore the 2026 answer keys are not yet marked VERIFIED at record/question level.

## Official JEE Advanced 2026 answer-key evidence

The official JEE Advanced 2026 Information Brochure states:
- Candidate responses were scheduled to be available on 21 May 2026.
- Provisional answer keys for both papers were scheduled for 25 May 2026.
- Final answer keys were scheduled for 1 June 2026.

Official brochure: https://jeeadv.ac.in/documents/IBEnglish_2026.pdf

The official 2027 site archive currently exposes question-paper links through 2025, and a direct 2026 final answer-key PDF URL was not recovered in this audit. The 2026 Advanced key source and exact Paper 1/Paper 2 matching remain pending.

## Important scope separation

- IIT-JEE (pre-2013), AIEEE and JEE Main are separate exam families.
- JEE Advanced is separate from JEE Main; the paper structure, question types, marking and syllabus scope differ.
- The historical inventory must retain family, year, paper/session, language and variant.
- Do not merge papers merely because the same year or topic appears.
- Do not treat memory-based reproductions as official papers.
- Preserve question-paper source, answer-key source and solution source as separate provenance fields.

## Required status model

Use distinct states rather than a single “verified” flag:

1. INVENTORIED
2. SOURCE_URL_IDENTIFIED
3. URL_ACCESS_VERIFIED
4. PDF_BYTES_ACQUIRED
5. SHA256_VERIFIED
6. PAPER_METADATA_VERIFIED
7. QUESTION_TRANSCRIPTION_VERIFIED
8. ANSWER_KEY_SOURCE_LINKED
9. ANSWER_KEY_PAPER_MATCHED
10. ANSWER_KEY_QUESTION_MATCHED
11. ANSWER_INDEPENDENTLY_VERIFIED
12. SYLLABUS_MAPPING_APPROVED

Every transition must have evidence and must not be inferred from a previous state.

## Next audit actions

- Obtain official/legitimate paper PDFs and keys where available.
- Capture local source bytes and SHA-256 hashes.
- Reconcile the 2026 January Main inventory against NTA's official publication/response-sheet availability; keep non-official reconstructions labelled accordingly.
- Reconcile 2026 April Main papers and both answer-key documents at date/shift/question-ID level.
- Locate official JEE Advanced 2026 final answer keys and match both papers.
- Audit the remaining 2002–2025 inventory by paper family and primary source.
- Do not begin bulk transcription or production-question generation until provenance and rights review are recorded.


## First question-level match — 2026-11-17

Two Physics questions from the official 2 April 2026 Shift 1 JEE Main Paper 1 were inspected in the official question-paper PDF and matched to the official NTA Session II final answer key by question ID and correct option ID:

| Question | Internal candidate | Official paper reference | Official final-key match | Status |
|---|---|---|---|---|
| Q26 | P1_CH1_ST4 — Dimensional Analysis | Question ID 69112126; paper PDF page index 9 | Correct Option ID 69112187 (option B; displayed value 1) | Question ID and option ID matched |
| Q27 | P1_CH1_ST6 — Errors and Measurements | Question ID 69112127; paper PDF page index 10 | Correct Option ID 69112191 (option B; displayed value 1.65) | Question ID and option ID matched |

Official paper PDF: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/04/202604092096865379.pdf

Official Session II final key: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/04/20260420409057044.pdf

The paper/key question identifiers are matched, but local bytes and SHA-256 remain pending. This is two questions from one shift only and does not support cross-year frequency/trend claims.
