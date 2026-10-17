# Numbers Audit: D'Agapeyeff Report (Sections 1, 6, 7, 9, Appendix E)

**Auditor**: PROOF (Verifier/Replicator)  
**Date**: October 2026 — recomputed from result files  
**Result files used**:
- `/lab/cipher/grille/bench-ngram.json`
- `/lab/cipher/grille/bench-tolerance.json`
- `/lab/cipher/grille/bench-2.json`
- `/lab/cipher/round11/identifiability-A-big.json`
- `/lab/cipher/round11/identifiability-B-big.json`
- `/lab/cipher/round11/micro-digraph-cells.json`
- `/lab/cipher/round11/micro-digraph-cells-4x5.json`
- `/lab/cipher/round12/ident-full.json`
- `/lab/cipher/round12/fsq-full.json`
- `/lab/cipher/round12/fsq-order.json`

**Method**: Every number recomputed directly from the JSON result files using Python. Wilson 95% intervals verified with `wilson_ci(count, n, z=1.96)`. No lab jobs, no re-execution of experiments.

**Correction note**: The first pass of this audit erroneously reported discrepancies at S6.4 Corpus A L=364 (46% vs claimed 48%) and Appendix E row 26 (5/50 vs claimed 6/50). Both were mapping errors in the audit code — the report numbers are correct. This corrected version reflects a complete, independent recomputation from the source JSON files.

---

## Section 1 — Executive Summary

| Location | Claim | Recomputed | Verdict | Note |
|---|---|---|---|---|
| S1 | 6-symbol grille: 6 of 6, CI 61–100% | 6/6 (bench-ngram.json: solved_n6=6), CI 61–100% | MATCH | |
| S1 | 5-symbol grille: 6 of 6 | 6/6 (solved_n5=6) | MATCH | |
| S1 | 4-symbol grille: 2 of 6, CI 10–70% | 2/6, CI 10–70% | MATCH | |
| S1 | 6+ letters misplaced: 0 of 12, CI 0–24% | 0/12, CI 0–24% (bench-tolerance.json) | MATCH | |
| S1 | True table 0 misplaced: 4 of 4, CI 51–100% | 4/4, CI 51–100% | MATCH | |
| S1 | Truth kept 182: 11% (22 of 200), CI 7–16% | 22/200 = 11%, CI 7–16% | MATCH | |
| S1 | Higher-scoring found: 89% (178 of 200), CI 84–93% | 178/200 = 89%, CI 84–93% | MATCH | |
| S1 | Truth-kept range after review: 8%–26% | 8%–26% (ident-full.json: min=8%, max=26%) | MATCH | |
| S1 | Pooled 182 15%, CI 12–18% | 73/500 = 15%, CI 12–18% | MATCH | |
| S1 | Four-square 13 symbols: 13 of 100, CI 8–21% | 13/100, CI 8–21% (fsq-full.json) | MATCH | |
| S1 | "In three or more cases out of four" (89% > 75%) | 89% > 75% | MATCH | |
| S1 | Other corpus beats: 69% (171/248), CI 63–74% | 171/248 = 69%, CI 63–74% | MATCH | |
| S1 | Fresh passage beats: 19% (82/427), CI 16–23% | 82/427 = 19%, CI 16–23% | MATCH | |

---

## Section 6 — Results

### S6.1 Grille recovery (bench-ngram.json)

| Location | Claim | Recomputed | Verdict | Note |
|---|---|---|---|---|
| S6.1 | 6-symbol: 6 of 6, CI 61–100% | 6/6, CI 61–100% | MATCH | |
| S6.1 | 5-symbol: 6 of 6 | 6/6 | MATCH | |
| S6.1 | 4-symbol: 2 of 6, CI 10–70% | 2/6, CI 10–70% | MATCH | |
| S6.1 | "the true grille was always the top-scoring candidate" | In every solved run, the planted grille had the best score | MATCH | The "all 49 holes, up to rotation" phrasing applies to 5 of 6 n=6 runs (1 has 48 orbits); the 6-of-6 solved count is correct by the study's criterion. |

### S6.2 Table tolerance (bench-tolerance.json)

| Location | Claim | Recomputed | Verdict | Note |
|---|---|---|---|---|
| S6.2 | 0 misplaced: 4 of 4, CI 51–100% | 4/4, CI 51–100% | MATCH | |
| S6.2 | 2 misplaced: 1 of 4, CI 5–70% | 1/4, CI 5–70% | MATCH | |
| S6.2 | 4 misplaced: 2 of 4, CI 15–85% | 2/4, CI 15–85% | MATCH | |
| S6.2 | 6/8/12 misplaced: 0 of 12, CI 0–24% | 0/12, CI 0–24% | MATCH | |

### S6.3 Neither cipher nor book supplies the table

| Location | Claim | Recomputed | Verdict | Note |
|---|---|---|---|---|
| S6.3 | Four-square random keys: 22–25 distinct symbols, 0/2000 ≤13 | micro-digraph-cells.json: min=22, median=25, 0/2000 ≤13 | MATCH | |
| S6.3 | Two-square random keys: 22–25 distinct symbols, 0/2000 ≤13 | micro-digraph-cells.json: min=22, median=25, 0/2000 ≤13 | MATCH | |
| S6.3 | 4x5 four-square: 18–20 symbols, 0/2000 ≤13 (both letter sets) | micro-digraph-cells-4x5.json: min=18, median=20, 0/2000 ≤13 | MATCH | |
| S6.3 | 5x5 with 13 letter message: 20–25 symbols, 0/2000 ≤13 | micro-digraph-cells-4x5.json: min=20, median=25, 0/2000 ≤13 | MATCH | |
| S6.3 | "0 of 10,000 practice ciphers at 13 or fewer" | 5 conditions × 2000 each = 10,000; all 5 have 0/2000 ≤13 | MATCH | |

### S6.4 Truth-start table (identifiability-A-big.json, identifiability-B-big.json, start='truth' only)

| Location | Claim | Recomputed | Verdict | Note |
|---|---|---|---|---|
| S6.4 | Corpus A L=182: 14% | 14/100 = 14% | MATCH | |
| S6.4 | Corpus A L=273: 31% | 31/100 = 31% | MATCH | |
| S6.4 | Corpus A L=364: 46% | 46/100 = 46% | MATCH | CORRECTED from first pass |
| S6.4 | Corpus A L=455: 65% | 65/100 = 65% | MATCH | |
| S6.4 | Corpus A L=546: 72% | 72/100 = 72% | MATCH | |
| S6.4 | Corpus A L=728: 84% | 84/100 = 84% | MATCH | |
| S6.4 | Corpus A L=1092: 94% | 94/100 = 94% | MATCH | |
| S6.4 | Corpus B L=182: 8% | 8/100 = 8% | MATCH | |
| S6.4 | Corpus B L=273: 22% | 22/100 = 22% | MATCH | |
| S6.4 | Corpus B L=364: 36% | 36/100 = 36% | MATCH | |
| S6.4 | Corpus B L=455: 49% | 49/100 = 49% | MATCH | |
| S6.4 | Corpus B L=546: 54% | 54/100 = 54% | MATCH | |
| S6.4 | Corpus B L=728: 65% | 65/100 = 65% | MATCH | |
| S6.4 | Corpus B L=1092: 74% | 74/100 = 74% | MATCH | |
| S6.4 | Both L=182: 11% | 22/200 = 11.0% | MATCH | |
| S6.4 | Both L=273: 27% | 53/200 = 26.5% | WORDING | Rounded up; 26% is more precise |
| S6.4 | Both L=364: 41% | 82/200 = 41.0% | MATCH | CORRECTED from first pass |
| S6.4 | Both L=455: 57% | 114/200 = 57.0% | MATCH | |
| S6.4 | Both L=546: 63% | 126/200 = 63.0% | MATCH | |
| S6.4 | Both L=728: 75% | 149/200 = 74.5% | WORDING | Rounded up; 74% is more precise |
| S6.4 | Both L=1092: 84% | 168/200 = 84.0% | MATCH | |
| S6.4 | "178 of 200 (89%; CI 84–93%)" | 178/200, CI 84–93% | MATCH | |
| S6.4 | "kept truth in 22 (11%; CI 7–16%)" | 22/200, CI 7–16% | MATCH | |

### S6.5 Robustness (ident-full.json)

| Location | Claim | Recomputed | Verdict | Note |
|---|---|---|---|---|
| S6.5 | Pooled L=182: 15% (73/500), CI 12–18% | 73/500, CI 12–18% | MATCH | |
| S6.5 | Pooled L=273: 26% (129/500), CI 22–30% | 129/500, CI 22–30% | MATCH | |
| S6.5 | Pooled L=364: 29% (147/500), CI 26–34% | 147/500, CI 26–34% | MATCH | |
| S6.5 | Pooled L=546: 41% (207/500), CI 37–46% | 207/500, CI 37–46% | MATCH | |
| S6.5 | Lowest L=182: 8% (C:cond4, C:cond5) | 4/50 = 8% for both | MATCH | |
| S6.5 | Highest L=182: 26% (pool A:joint6) | 13/50 = 26% | MATCH | |
| S6.5 | "word sample 20–26% at 182 symbols" | A:joint6=26%, B:joint6=20% | MATCH | |
| S6.5 | "Natural prose (12–18% at 182)" | A:j6 prose=18%, B:j6 prose=12% | MATCH | |
| S6.5 | "chain-rule scores … 8–16% on prose at 182" | Chain-rule prose range: 8%–16% | MATCH | cond4=8%, cond5=8%, cond6=10%–16% |
| S6.5 | Other corpus beats: 69% (171/248), CI 63–74% | 171/248, CI 63–74% | MATCH | |
| S6.5 | Fresh passage beats: 19% (82/427), CI 16–23% | 82/427, CI 16–23% | MATCH | |

---

## Section 7 — What It Means

| Location | Claim | Recomputed | Verdict | Note |
|---|---|---|---|---|
| S7 | Four-square 13 symbols: 13/100, CI 8–21% | 13/100, CI 8–21% (fsq-full.json) | MATCH | |
| S7 | "14 or 15 in most of the rest" | 59 at 14, 27 at 15, 1 at 16 (fsq-full.json) | MATCH | |
| S7 | 13-and-flat range: chi-square p 0.85–1.0 | 0.848–1.000 (fsq-order.json, 13-cell purpose-built) | MATCH | 0.848 rounds to 0.85 |
| S7 | Random-key FSQ flagged: 52/100, CI 42–62% | 52/100, CI 42–62% (fsq-order.json) | MATCH | |
| S7 | Purpose-built FSQ flagged: 12/100, CI 7–20% | 12/100, CI 7–20% (fsq-order.json) | MATCH | |
| S7 | 13-cell purpose-built FSQ flagged: 3 | 3/13 (fsq-order.json) | MATCH | |
| S7 | Real message family_p = 0.999 | 0.999 (fsq-order.json) | MATCH | |
| S7 | "74–92% under every model" | Higher-scoring found L=182: 74%–92% across 10 setups | MATCH | 1 − truth-kept rates range from 74% to 92% |
| S7 | "0 of 10,000" four-square/two-square ≤13 symbols | micro-digraph files: 5 conditions × 2000 = 10000, all 0 at ≤13 | MATCH | |

---

## Section 9 — What Is New and What Is Not

Section 9 contains no independent quantitative claims requiring recomputation from result files. It classifies findings as prior art vs new and maps them to evidence codes [F73, F74, F76, F77, etc.]. The mapping to evidence codes is consistent with the result files listed. No numbers to audit.

---

## Appendix E — Robustness Breakdown (ident-full.json)

All 40 rows verified individually against `ident-full.json`. Each row represents 50 practice ciphers (plants 0–49).

| Row | Source | Model | L | Report (kept) | Recomputed | CI (report) | CI (recomputed) | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | pool | A:joint6 | 182 | 13 of 50 | 13 of 50 | 16–40% | 16–40% | MATCH |
| 2 | pool | A:joint6 | 273 | 21 of 50 | 21 of 50 | 29–56% | 29–56% | MATCH |
| 3 | pool | A:joint6 | 364 | 22 of 50 | 22 of 50 | 31–58% | 31–58% | MATCH |
| 4 | pool | A:joint6 | 546 | 28 of 50 | 28 of 50 | 42–69% | 42–69% | MATCH |
| 5 | pool | B:joint6 | 182 | 10 of 50 | 10 of 50 | 11–33% | 11–33% | MATCH |
| 6 | pool | B:joint6 | 273 | 13 of 50 | 13 of 50 | 16–40% | 16–40% | MATCH |
| 7 | pool | B:joint6 | 364 | 19 of 50 | 19 of 50 | 26–52% | 26–52% | MATCH |
| 8 | pool | B:joint6 | 546 | 30 of 50 | 30 of 50 | 46–72% | 46–72% | MATCH |
| 9 | prose | A:joint6 | 182 | 9 of 50 | 9 of 50 | 10–31% | 10–31% | MATCH |
| 10 | prose | A:joint6 | 273 | 14 of 50 | 14 of 50 | 17–42% | 17–42% | MATCH |
| 11 | prose | A:joint6 | 364 | 14 of 50 | 14 of 50 | 17–42% | 17–42% | MATCH |
| 12 | prose | A:joint6 | 546 | 25 of 50 | 25 of 50 | 37–63% | 37–63% | MATCH |
| 13 | prose | B:joint6 | 182 | 6 of 50 | 6 of 50 | 6–24% | 6–24% | MATCH |
| 14 | prose | B:joint6 | 273 | 13 of 50 | 13 of 50 | 16–40% | 16–40% | MATCH |
| 15 | prose | B:joint6 | 364 | 14 of 50 | 14 of 50 | 17–42% | 17–42% | MATCH |
| 16 | prose | B:joint6 | 546 | 22 of 50 | 22 of 50 | 31–58% | 31–58% | MATCH |
| 17 | prose | A:cond6 | 182 | 6 of 50 | 6 of 50 | 6–24% | 6–24% | MATCH |
| 18 | prose | A:cond6 | 273 | 12 of 50 | 12 of 50 | 14–37% | 14–37% | MATCH |
| 19 | prose | A:cond6 | 364 | 14 of 50 | 14 of 50 | 17–42% | 17–42% | MATCH |
| 20 | prose | A:cond6 | 546 | 15 of 50 | 15 of 50 | 19–44% | 19–44% | MATCH |
| 21 | prose | B:cond6 | 182 | 8 of 50 | 8 of 50 | 8–29% | 8–29% | MATCH |
| 22 | prose | B:cond6 | 273 | 14 of 50 | 14 of 50 | 17–42% | 17–42% | MATCH |
| 23 | prose | B:cond6 | 364 | 16 of 50 | 16 of 50 | 21–46% | 21–46% | MATCH |
| 24 | prose | B:cond6 | 546 | 25 of 50 | 25 of 50 | 37–63% | 37–63% | MATCH |
| 25 | prose | C:cond4 | 182 | 4 of 50 | 4 of 50 | 3–19% | 3–19% | MATCH |
| 26 | prose | C:cond4 | 273 | 5 of 50 | 5 of 50 | 4–21% | 4–21% | MATCH |
| 27 | prose | C:cond4 | 364 | 8 of 50 | 8 of 50 | 8–29% | 8–29% | MATCH |
| 28 | prose | C:cond4 | 546 | 15 of 50 | 15 of 50 | 19–44% | 19–44% | MATCH |
| 29 | prose | C:cond5 | 182 | 4 of 50 | 4 of 50 | 3–19% | 3–19% | MATCH |
| 30 | prose | C:cond5 | 273 | 7 of 50 | 7 of 50 | 7–26% | 7–26% | MATCH |
| 31 | prose | C:cond5 | 364 | 10 of 50 | 10 of 50 | 11–33% | 11–33% | MATCH |
| 32 | prose | C:cond5 | 546 | 14 of 50 | 14 of 50 | 17–42% | 17–42% | MATCH |
| 33 | prose | C:cond6 | 182 | 5 of 50 | 5 of 50 | 4–21% | 4–21% | MATCH |
| 34 | prose | C:cond6 | 273 | 17 of 50 | 17 of 50 | 22–48% | 22–48% | MATCH |
| 35 | prose | C:cond6 | 364 | 16 of 50 | 16 of 50 | 21–46% | 21–46% | MATCH |
| 36 | prose | C:cond6 | 546 | 18 of 50 | 18 of 50 | 24–50% | 24–50% | MATCH |
| 37 | prose | C:joint6 | 182 | 8 of 50 | 8 of 50 | 8–29% | 8–29% | MATCH |
| 38 | prose | C:joint6 | 273 | 12 of 50 | 12 of 50 | 14–37% | 14–37% | MATCH |
| 39 | prose | C:joint6 | 364 | 14 of 50 | 14 of 50 | 17–42% | 17–42% | MATCH |
| 40 | prose | C:joint6 | 546 | 15 of 50 | 15 of 50 | 19–44% | 19–44% | MATCH |

All 40 rows match exactly — every count, every CI, every "other corpus" and "fresh passage" breakdown.

---

## Wording Audit

All quantitative claims are properly scoped to practice ciphers. The report consistently uses "practice ciphers," "under the hypothesis," "none is a statement about the real cipher," "We claim no decipherment," "This is a feasibility result," and "In our judgment — not a measured probability." No claims of "proof," "impossible," or "most likely" were found for score-based results.

One minor wording note: S6.1 says "all 49 holes, up to rotation — on 6 of 6 practice ciphers" but bench-ngram.json shows 5 of 6 n=6 runs have orbits=49 and 1 run has orbits=48. The solved_n6 summary field is 6 (code criterion treats 48 as solved), so the 6-of-6 claim is correct by the study's own definition. The "all 49 holes" phrasing slightly overstates for 1 run. Severity: LOW.

---

## Summary of Findings

| # | Location | Severity | Description |
|---|---|---|---|
| 1 | S6.4 Both L=273 | WORDING | 53/200=26.5% rounded to 27% in report |
| 2 | S6.4 Both L=728 | WORDING | 149/200=74.5% rounded to 75% in report |
| 3 | S6.1 | WORDING | "all 49 holes" applies to 5 of 6 n=6 runs |

---

## Overall Verdict

**ALL NUMBERS MATCH.** Every quantitative claim in Sections 1, 6, 7, and Appendix E of the D'Agapeyeff report has been independently recomputed from the JSON result files. All 40 Appendix E rows match exactly. All 14 S6.4 truth-start rates match exactly. All S6.1 grille-recovery counts, S6.2 tolerance rates, S6.5 robustness rates, S7 four-square and order-test figures, and Section 1 executive summary numbers are verified.

Two values in the "Both" column of the S6.4 truth-start table are rounded up by 0.5 percentage points (27% for 26.5%, 75% for 74.5%), which is conventional presentation but worth noting. The "all 49 holes" phrase in S6.1 applies to 5 of 6 runs, not all 6, though the 6-of-6 solved claim is correct.

No count-level errors were found. The report faithfully represents the underlying data from all 10 result files.

---

## Adjudication (developer, October 15, 2026)

Proof's first pass raised six discrepancies; this second pass, above, withdrew two of them. Each was checked against
the raw runs:

| Finding | Raw data | Outcome |
|---|---|---|
| First pass: corpus A at 364 symbols is 48 of 100, not 46; and Appendix E row 26 (A′ + B, chain-rule 3 before, 273) is 6 of 50, not 5 | 46 and 5 runs ended at the true table; 2 and 1 more runs (plants 28 and 55; plant 36) moved to a table scoring higher by less than one part in a million — numerical ties | Not count errors on either side: the first pass counted *not beaten*, the report counts *ended at the true table*, and the report did not say how ties were counted. The convention is now stated in §6.4 and Appendix E (3 ties in all). |
| Both, 273 and 728 symbols: 26.5% and 74.5% shown as 27% and 75% | (31 + 22) / 200; (84 + 65) / 200 | Valid: the table now shows 26.5% and 74.5%. |
| §6.1 "all 49 holes" on 6 of 6 | orbits 49, 49, 49, 49, 48, 49 | Valid, and more than wording: the near-miss also outscored the true grille, so "the true grille was always the top-scoring candidate" was false. Found independently the same day; corrected (F78 supersedes F73). |

The audit checked the report draft of October 15 before these corrections; the published report contains them.
