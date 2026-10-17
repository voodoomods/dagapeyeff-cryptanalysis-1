# Response to the final review before publication (October 17, 2026)

The review came from ChatGPT (OpenAI) at the author's request. It is an AI review, not peer review. It examined the
PDF with SHA-256 `cbb37c201bb628783a5d43d2de3849ee407cf085764250596269d538d4d5a5c6` and made three findings. Each was
checked against the evidence, found correct, and fixed. No experiment was rerun: all three concern wording or the
validation checker, and the evidence already in the repository decides them.

| Finding | Checked against | Verdict | Change |
|---|---|---|---|
| 1. §6.3 says two practice ciphers had their grille recovered exactly, then drifted from 2 to 5 wrong letters | `lab/cipher/round11/validate.json`: plant 0 started from 49/49 orbits, 2 → 5 wrong; plant 1 from 19/49 orbits, 2 → 8 | Correct. The case entry I47 was right ("other plants 2 to 8"); the report overstated it. | §6.3 now describes the one cipher with its grille recovered (2 → 5) and the second without (2 → 8). Appendix D I47, §8 sample sizes ("on 1, a second without the grille recovered") and the contributions table ("table repair moves away from the truth") match. Fact-check 120. |
| 2. "Never" for ordinary tables and ordinary text contradicts the shipped flatness outputs | `docs/validation-2026-10-16/flatness/`: random merges 1/1,000 and 2/2,000 English; Latin 10, 6, 9, 14 per 1,000 (ten editions) and 1, 3, 1, 1 (six editions); fixed-pattern letter pairs 0 in every run; F31's own record says merges 0–5/1,000 | Correct. | "Never" is kept only where the count is zero (fixed-pattern pairs; the book's sign system, 0 of 400 [R31]). Elsewhere: "rarely", with the rates. Changed in §2, §4, Appendix D (F31, F65), Appendix B and the contributions and timeline rows. New case entry F84, linked to F31 and F65. The contrast with deliberately balanced tables (364/1,000 English) is unchanged; the inference is stated less absolutely. Fact-check 121. |
| 3. The comparator still expects the superseded 17–22 range, and exits 0 despite a FAIL | `validation/compare.py` | Correct. Its I47 check also read only the first record, so it could not catch finding 1. | The predeclared check is kept as it was, marked `superseded_by`. A versioned check of the corrected range (S2-letters-v2) and a check of F84 are added. The I47 check now reads both 2-wrong-letter records and their starting grilles. The script exits 1 on any FAIL that is not an expected, superseded one. Rerun on the shipped October 16 reruns: 19 PASS, 2 PARTIAL (F71 controls; R29 39/40), 1 FAIL (the superseded S2 check, expected), exit status 0 (`compare.json` here). The October 16 `compare.json` is kept unchanged as the record of that day. Fact-check 122–123. |
| Note: the unit runner prints "pass" after a skipped test | `lab/cipher/lib/test_label_distance.py` | Correct. | Documented in `validation/README.md` ("count `test_e` as skipped"). The file is unchanged because its fingerprint is cited in the October 15 engineering record. |

The case graph's at-risk set is unchanged (I25, O26). No experiment script, archived evidence file or published
result file was changed.
