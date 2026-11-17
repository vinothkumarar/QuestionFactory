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

All 21 2026 records still have Answer Key Verified = No in the workbook. Official key documents were found separately. Four question-level matches have now been completed in the separate P1 evidence register: two Main questions from 2 April 2026 Shift 1, Advanced Paper 1 Q3 and Advanced Paper 2 Q1. The workbook's aggregate field remains unchanged until the full record-level audit is complete.

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

**Verification state:** Both official answer-key sources are located and accessible. Session II has two question-ID/option-ID matches independently solved and verified for 2 April 2026 Shift 1. Session I and the remaining Session II papers still require record-level matching. Both official Advanced 2026 final-key PDFs are now located; Paper 1 Q3 and Paper 2 Q1 are both matched and independently solved. Local bytes and SHA-256 values remain pending, so no full-paper or session-wide verification claim is made.

## Official JEE Advanced 2026 answer-key evidence

The official JEE Advanced 2026 Information Brochure states:
- Candidate responses were scheduled to be available on 21 May 2026.
- Provisional answer keys for both papers were scheduled for 25 May 2026.
- Final answer keys were scheduled for 1 June 2026.

Official brochure: https://jeeadv.ac.in/documents/IBEnglish_2026.pdf

The official 2026 Advanced question papers and both official final answer-key PDFs have now been located. Paper 1 Q3 and Paper 2 Q1 are independently matched and solved; the earlier statement that the final-key URLs were not recovered is superseded by the evidence below.

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
| Q26 | P1_CH1_ST4 — Dimensional Analysis | Question ID 69112126; paper PDF page index 9 | Correct Option ID 69112187 (option B; displayed value 1) | Independently solved; key value and option matched |
| Q27 | P1_CH1_ST6 — Errors and Measurements | Question ID 69112127; paper PDF page index 10 | Correct Option ID 69112191 (option B; displayed value 1.65) | Independently solved; key value and option matched |

Official paper PDF: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/04/202604092096865379.pdf

Official Session II final key: https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/04/20260420409057044.pdf

The paper/key question identifiers are matched, but local bytes and SHA-256 remain pending. This is two questions from one shift only and does not support cross-year frequency/trend claims.


### Independent answer verification

- **Q26:** The dimensional formula of electric-field energy density is energy per volume, `M L^-1 T^-2`. Thus `a=1, b=-1, c=-2`, and `2a-b+c=1`. This agrees with option B and the official correct option ID `69112187`.
- **Q27:** Young's modulus is `Y=4FL/(pi*d^2*x)`. Ignoring load uncertainty, the relative uncertainty is `0.1/150 + 2(0.001/0.08) + 0.001/0.5 = 0.0276667`. The nominal modulus is approximately `5.968 x 10^10 Pa`; its absolute uncertainty is approximately `1.651 x 10^9 Pa`, giving `alpha=1.65`. This agrees with option B and official correct option ID `69112191`.

The two independently verified records are stored in `P1_PYQ_EVIDENCE_REGISTER.csv`. Their `local_pdf_bytes_acquired` fields remain `NO`, and both SHA-256 fields remain `PENDING`.


### JEE Advanced 2026 official final-key sample

Official final key URLs:
- Paper 1: https://jeeadv.ac.in/documents/p1_solutions_final.pdf
- Paper 2: https://jeeadv.ac.in/documents/p2_solutions_final.pdf

Paper 1 Q3 is matched to the official final key answer `B`. The question asks which 3×3 matrix can be obtained from the identity by elementary row transformations. Such a matrix must be invertible. Determinants of options A, B, C and D are respectively `0, -2, 0, 0`; only B is invertible. The independent result agrees with the official key. This record is in `P1_PYQ_EVIDENCE_REGISTER.csv` as `JEE_ADVANCED_2026_P1_MATH_Q3`.

Paper 2's official final-key URL is located, but no Paper 2 question-level match is claimed yet.


Paper 2 Q1 is also independently verified: wire resistance `R=L/(sigma*A)=1 ohm`, total current `I=1 A`, carrier density `n=6×10^28 m^-3`, and drift velocity `vd=0.2083 mm/s`, matching option C and the official Paper 2 final key. Evidence is stored as `JEE_ADVANCED_2026_P2_PHY_Q1` in the P1 evidence register.


## 2026-11-17 — Session-level answer-key linkage

Both NTA final answer-key PDFs were opened and their page headers inspected. They provide date/shift-level subject question-ID and answer-option tables:

| Main session | Exam dates and shifts represented | Official final answer-key URL | Scope of this linkage |
|---|---|---|---|
| Session I | 21, 22, 23, 24 and 28 January 2026; Shift I and Shift II on each date (10 shifts) | https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/02/20260216459398513.pdf | Official key source identified for all 10 January Main records |
| Session II | 2, 4, 5 and 6 April 2026; Shift I and Shift II; 8 April 2026 Shift II (9 shifts) | https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/04/20260420409057044.pdf | Official key source identified for all 9 April Main records |

The Session I PDF identifies each of the ten January date/shift combinations in its page headers. The Session II PDF identifies the nine April date/shift combinations, with the India and outside-India centre tables separated within the document. This closes **session-level official answer-key source identification** for all 19 Main 2026 shifts. It does not mean every question ID has been reconciled against the matching question paper.

For Advanced 2026, the official final-key sources are:
- Paper 1: https://jeeadv.ac.in/documents/p1_solutions_final.pdf — Paper 1 Mathematics Q3 is matched and independently solved.
- Paper 2: https://jeeadv.ac.in/documents/p2_solutions_final.pdf — Paper 2 Physics Q1 is matched and independently solved.

A derived 21-record linkage register is stored at `docs/p1/P1_2026_SESSION_KEY_LINKAGE.csv`. It links each of the 19 Main shift records and two Advanced papers to the relevant official key URL, preserves question-paper URL status, and separately records question-level match status. The ten January Main question-paper URLs remain absent from the tracker. The 11 accessible question-paper URLs remain URL-access-only. All local PDF byte and SHA-256 fields remain `NO` / `PENDING`.

**Important distinction:** Official answer-key source linked at session/paper level ≠ answer-key question matched ≠ answer independently verified. Only four question-level samples are currently matched and independently solved.
