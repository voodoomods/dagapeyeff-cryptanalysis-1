# R29 and F4 — clarifications (October 17, 2026)

Response to the request "two final clarifications", drafted by ChatGPT (OpenAI) at the author's request. Done by the
project's developer (Claude Opus 5.5). This is internal work, not independent review. No experiment was rerun on the
GPU. The two original computations were recovered from the developer session record of October 11 and rerun
unchanged: both reproduce their published output exactly.

## 1. Records examined

| Record | What it shows |
|---|---|
| Case entries F4 and R29 (`evidence/case/dagapeyeff.json`, unchanged) | the claims as recorded on October 11 |
| Developer session record, October 11: the command behind F4 | statistic, null, 20,000 seeded placements, output `4.999750012499375e-05` |
| Developer session record, October 11: the command behind R29 | design, seed `random.Random(9)`, output 40/40 at p < 0.05, 39/40 at p < 0.01, real p 0.698 |
| `round4/external_review.md` (October 11, not in the repository) | the first written form of the F4 figure ("< 1 in 20,000 random placements match, after scanning every period 2–20") |
| Agent event log, October 11 (fisher, `grid_profile`) | the platform tool on the same statistic with 2,000 shuffles: p = 0.0005 (0 of 2,000), consistent with the above |
| `docs/validation-2026-10-16/recompute_extra.json`, `REVIEW-RESPONSE.md` | the October 16 independent check (R29 39/40; F4 bound) |
| `validation/f4_events.py` → `f4_events.json` (new) | the two F4 events computed side by side |

The two original commands are now in the repository unchanged: `validation/original/f4_original.py` (only the input
path differs; its first 392 digits are identical to the file it read) and `validation/original/r29_original.py`.
Their outputs from the October 17 reruns are `f4_original.out` and `r29_original.out` in this folder. R29 needs the
PegasusDMZ agent code at commit `c908608`, the commit made immediately after it ran. That code is not in this
repository, so outsiders can rerun F4 but not R29's original code. Its separately written check is in
`validation/recompute_extra.py`.

## 2. F4 — the exact test

| Item | Definition |
|---|---|
| Data | the 196 two-digit symbols, with the 04 counted; the eight occurrences of the rare symbols 71, 92, 93, 94 and 04 at 0-based positions 41, 55, 97, 111, 125, 139, 167, 195 |
| Statistic | for each row length p = 2 … 20: the largest share of the eight occurrences in one column (residue mod p), minus 1/p (the share chance alone puts in a column); S = the maximum over p. Cipher: S = 1 − 1/14 = 0.929 (p = 14) |
| Null hypothesis | the eight positions are a uniformly random 8-subset of the 196 positions; the symbols and their counts are held fixed |
| Scan | row lengths 2–20, inside the statistic (a maximum statistic, so no further correction is needed for that choice) |
| Original computation | 20,000 placements, `random.Random(t)` for t = 0 … 19,999; none reached 0.929; reported (0 + 1)/(20,000 + 1) = 5.0 × 10⁻⁵. "Odds below 1 in 20,000" is therefore the floor 20,000 simulations can show, not an estimate of the probability |
| Exact bound (new) | with eight occurrences, S ≥ 0.929 only if all eight share one residue at some p ≥ 14 (seven of eight scores at most 0.825), so P ≤ Σ over p = 14 … 20 of P(all eight on one residue mod p) = 1.8 × 10⁻⁹ |
| Check (new) | 0 of 1,000,000 seeded placements reached 0.929 |
| Chosen after looking at the data | that the rare symbols' columns were looked at at all (van Eykelen's observation, adopted after it was noticed), and the rare set (symbols occurring at most three times). The scan covers the choice of row length only. The wider structure sweep (F16) is the project's correction for everything examined and finds only this feature. |

**The looser event is a different question.** "All eight in one column at *some* row length from 2 to 20" happens in
0.71% of random placements (7,061 of 1,000,000). 95% of those cases are at row length 2, where it means all eight in
odd positions or all in even ones (exact chance 0.0067, about 1 in 149). The cipher meets that event at row lengths 2,
7 and 14. The paper's odds do not come from this event, and the two must not be interchanged.

**Assessment.** The printed claim "below 1 in 20,000 after allowing for every row length from 2 to 20" is justified
under its statistic and null, and conservatively so (the exact bound is about four orders of magnitude smaller). No
claim is revised. The statistic is now defined in the text, and the looser event is named so the two cannot be
conflated. One ambiguity remains in the original code: it labels its output "share of random placements as aligned
(any period 2-20)". That label reads like the looser event, although the code computes the excess-over-1/p score.
The label is left as it ran, and this note explains it.

## 3. R29 — seed dependence

| Run | Design | Planted texts with order (p < 0.05) | p < 0.01 | Real message |
|---|---|---|---|---|
| Original (October 11), rerun unchanged October 17 | `random.Random(9)`; text t = word-stream letters 120,000 + 1,500 t (182 letters); its own balanced 13-group table built from the stream's first 100,000 letters; lag-1 mutual information against 400 shuffles; p = share of shuffles at least as large | **40 of 40** | 39 of 40 | p = 0.698 |
| Separately written check (October 16) | new code; seeds 2900 + t and 29; texts drawn at random from `plain_pool.txt`; tables built from the novel corpus; same test; p with a +1 correction | **39 of 40** | 38 of 40 | p = 0.72 |

The two differ in design as well as in seeds, so they are reported side by side, not pooled. The difference of one
text cannot be attributed to the seeds alone. The planted-text counts measure detectability of the order; the real
message's p-values are a separate test, and both are reported separately in the text.

**Assessment.** 40 of 40 is the actual original observation and stays, now identified as the result for the
original plants and seeds. The count is not seed-invariant. The conclusion is unchanged: under the tested conditions,
a balanced table without a transposition leaves detectable order in nearly every planted text, and the cipher's
message shows none.

## 4. Before and after

| Where | Before | After |
|---|---|---|
| §2 | "…all fall in the last column — a coincidence with odds below 1 in 20,000 after allowing for every row length from 2 to 20 [F4]." | "…all fall in the last column. To judge how unusual that is without fixing the row length in advance, we scored every row length from 2 to 20 by the largest share of the eight in any one column, less the share chance alone would put there (one in the number of columns), and kept the best score. None of 20,000 random placements of eight symbols among the 196 positions scored as high as the cipher, so the odds are below 1 in 20,000; counted exactly, the chance is at most about 2 in a billion [F4, F83]. Section 5 says what this does and does not measure." |
| §4, observed | "(odds below 1 in 20,000) [F4]" | "(odds below 1 in 20,000 on the row-length scan of Section 2) [F4, F83]" |
| §4, inferred | "A balanced table used without a transposition left detectable order in 40 of 40 planted texts; the cipher shows none [R29]." | "In the original 40 planted texts, a balanced table used without a transposition left detectable order (dependence between neighboring symbols beyond 400 shuffles, p < 0.05) in all 40 [R29]. A separately written check within the project, with new seeds and differently drawn practice texts, found it in 39 of 40, so the exact count depends on the texts sampled; both show strong detectability under the tested conditions [F82]. The cipher's own message shows no such dependence (p = 0.70)." |
| §5 (new paragraph, "The column-14 odds") | — | defines the score, gives the 2-in-a-billion bound and the 20,000 floor, names the looser 0.7% event and says it is not the source, and states what the scan does and does not cover |
| §9 table | "A polyphonic table without transposition is excluded (R29)" | "… is excluded, under the tested conditions (R29)" |
| Figure 1 caption | "Every one of the five rare symbols falls in the last column" | "All eight occurrences of the five rare symbols fall in the last column" |
| Appendix D, F4 | "(odds below 1 in 20,000)" | "(odds below 1 in 20,000 on the row-length scan: 0 of 20,000 random placements scored as high; see F83)" |
| Appendix D, R29 | "always leaves order in the text (40 of 40 practice texts) … so its order was scrambled" | "left order in the text in all 40 of the original practice texts (see F82 for a check with new seeds) … so if such a table was used its order was scrambled" |
| Appendix D | — | new F82 (R29 clarification) and F83 (F4 clarification) |

Not changed, checked: the executive summary has no F4 or R29 figure. §3's credit to van Eykelen stays as it is. The
§4 sentence on the decoder's 85–90% (R29) is not a count of planted texts. The README and validation documents
describe R29 and F4 without either figure, apart from the October 16 records. The case file is append-only, so F4
and R29 are unchanged and F82 and F83 were added with "supports" links to them. The case graph's at-risk set is
unchanged (I25, O26).

## 5. Correction to the October 16 validation

`recompute_extra.py`'s note said the row-length-2 case is "same parity, 1 in 64". The exact chance is 0.0067, about 1
in 149, because the eight positions are drawn without replacement. The note in the script is corrected. The October
16 output `docs/validation-2026-10-16/recompute_extra.json` keeps the wording it was produced with, as a record.
This is fact-check entry 117.

## 6. Did any conclusion change?

No. Both claims were faithful to the experiments actually run. F4 now says what it measures and that its odds are a
simulation floor. R29 now says its count belongs to its original plants and is not seed-invariant. Neither is
broadened: R29 is qualified "under the tested conditions", and F4's scan is limited to the row length.

## 7. Open items

| Item | Status |
|---|---|
| R29's original code depends on PegasusDMZ code not in the repository | open (documented); the separately written check is in the repository |
| F4 does not allow for the choice to examine the rare symbols' columns, made after the alignment was noticed | stated in §5; not quantifiable without a predeclared family of features |
| Original F4 output label "(any period 2-20)" reads like the looser event | explained here; code left as it ran |
| New commit SHA | assigned when the author commits |

## 8. Build and QA

- Report rebuilt: 41 pages (the §5 note adds a page), all six figures present; edited pages inspected as rendered.
- `python validation/qa_checks.py`: 20 PASS, 0 FAIL, 3 WARN (the same three self-references as on October 17's
  QA report: the checker's own description and regular expression, and the change log quoting the old spelling).
  Every cited case code, including F82 and F83, is defined in Appendix D.
- `MANIFEST.sha256` covers every file. A fresh `git clone` with `core.autocrlf=false` and with `core.autocrlf=true`
  both pass `sha256sum -c MANIFEST.sha256`; `git add --renormalize .` changes nothing; gitleaks finds no leaks.
- The PDF and manifest fingerprints are given in the reply that delivered this build: the manifest covers this file,
  so its own fingerprint cannot be printed here.
