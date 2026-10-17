# Audit follow-up — dagapeyeff-cryptanalysis (October 15, 2026)

Response to "D'Agapeyeff Cryptanalysis — Independent Audit Follow-up", an audit request written by ChatGPT (OpenAI) at the author's request (an AI review, not human peer review); §6 answers its follow-up request. Performed by the developer (Claude Opus 5.5)
at the author's request. **This is an internal audit by the project, not independent external review.** No raw experiment
record was modified. The wording patch (`proposed.patch`) was approved and applied the same day (case entry O34).
Scripts and outputs are in the repository at `lab/cipher/audit/`; their SHA-256 fingerprints are in the repository's
`MANIFEST.sha256`.

## 1. Issue register

| # | Item | Verdict | Severity | Evidence |
|---|---|---|---|---|
| 1 | Four-square: README and executive summary combine the frequency result (13/100) with the order result | **CONFIRMED WORDING ISSUE** | Medium | 13 windows reach 13 cells with χ² p ≥ 0.05; 3 of them (34, 77, 95) are flagged by the family-wise order test at α = 0.05; 10/100 meet both criteria. README says "13 flat symbols with little detectable order in 13 of 100"; summary says "mostly without detectable order" without the 10/100 count. §2 below. |
| 2 | §7 "Packing the message into few symbols also removes most of the dependence between the two symbols of each pair" | **CONFIRMED WORDING ISSUE** | Medium | Not demonstrated: on the uncorrected pair statistics (mi_even or mi_odd), 7 of the 13 flat windows show dependence at p < 0.05 (0, 3, 34, 57, 72, 77, 95). The lower family-wise flag rate (12/100 vs 52/100 random) is real but is not "most of the dependence removed". |
| 3 | §7 / §9 / Appendix D / case O33: "reproduce … its lack of (detectable) order" | **CONFIRMED WORDING ISSUE** | Low–medium | Holds for 10/100 under one test at α = 0.05; non-detection is not absence of order. |
| 4 | Order-test p-values and family-wise correction (fsq_order.py) | **NO ISSUE** | — | Right-tailed per-statistic p = (1 + #shuffles ≥ observed)/(B + 1); min-p family correction against the shuffles' own min-p. An independent implementation with fresh shuffles (B = 5,000) under two conventions for the shuffles' own p-values (as in the original, and leave-one-out) flags exactly the same 3 of the 13 flat windows; overall 11/100 purpose-built and 54/100 random (stored, 2,000 shuffles: 12 and 52) — Monte-Carlo variation, same conclusions. |
| 5 | Greedy label matching in round12 `wrong()` | **NO ISSUE for reported results**; implementation note | Low | Greedy is not optimal in general (counterexample: greedy 4, optimal 3). On 220 regenerated runs the *kept / exact* flag is identical under raw, greedy and optimal distances; no run ended at a pure relabelling; greedy overstated the size of an error by 1 letter in 6 of 200 round-12 runs, all already "not kept". The report never cites round-12 error sizes; §6.3's "2 to 5 wrong letters" (I47) comes from table_test.py, which uses raw distance. `truth_beaten` depends only on distance > 0 and the score, so it is unaffected. |
| 6 | Is relabelling-invariant distance the right metric? | **IMPLEMENTATION NOTE** | Low | In the truth-start test the cipher symbols are observed, so a table with permuted group labels is a *different* key; raw letterwise distance (round 11) is the conceptually correct measure. It made no difference here (item 5). Recommend raw distance in future code; no published number changes. |
| 7 | Score comparability across tables | **NO ISSUE (previously checked, F79)**; scorer independently re-derived | — | Independent CPU float64 scorer matches the experiment's to ≤ 6.3 × 10⁻⁷ on 50 random cases; hand-checked toy values exact. Score superiority vs table recoverability is distinguished in §6.4/§8 already. |
| 8 | Four-square streams, cell counts and χ² flatness | **VERIFIED (no issue)** | — | Independent reconstruction from the Wells texts, seeds and stored P1/P2 keys: 100/100 windows match stored S1/S2 cell counts and merged counts; 13/13 χ² p-values match to 5 × 10⁻⁵ (regularized gamma, not scipy.stats.chisquare). |
| 9 | Truth-start outcomes (independent search) | **VERIFIED (no issue)** | — | Independent steepest ascent (CPU, float64) on 10 published runs: kept/not-kept identical 10/10; error size identical 9/10, the tenth differing by the greedy overstatement of item 5. |
| 10 | Evidence integrity (MANIFEST.sha256) | **VERIFIED (no issue)** | — | 111/111 entries OK; no unlisted files; no missing entries. Not redistributed (fingerprint only): Hendrick 2026 manuscript, D'Agapeyeff book extracts, literature-search abstracts, two Christie novels, `model_text_big.txt` (rebuildable byte-exactly from the corpus). |

**Final determination.** No headline numerical result changes. The truth-start, robustness, comparability and grille
results stand as reported. One reporting change is needed: the purpose-built four-square result must keep the frequency
finding (13/100) separate from the order finding (10/100 not flagged at α = 0.05 by one test), and must not describe
non-detection as absence of order or as "most of the dependence removed". The interpretation of O33 as a feasibility
result and open lead survives; its scope narrows.

## 2. Source-to-claim crosswalk (four-square, as published in the repository)

| Location | Original text | Supported result | Proposed |
|---|---|---|---|
| README.md:32–34 | "a key designed around the message reached 13 flat symbols with little detectable order in 13 of 100 passages (O33)" | 13/100 at 13 cells and χ² p ≥ 0.05; 10/100 also not flagged (α = 0.05) | Separate the two counts (patch) |
| report/front.md:39–41 (PDF p. 3) | "reached 13 symbols in 13 of 100 passages, as flat as the cipher's and mostly without detectable order" | as above | Separate counts; non-detection ≠ absence (patch) |
| report/body_final.md:75–76 (PDF p. 7) | "a four-square … is also consistent with them" (all three observations) | frequency: yes; order: 10/100 not flagged | Narrow (patch) |
| report/body_final.md:309–313 (PDF p. 14) | "Packing the message … removes most of the dependence between the two symbols of each pair: an order test that flags 52 of 100 … flags only 12 of 100 … and 3 of the 13" | 12/100 vs 52/100 and 3/13 are correct; "removes most of the dependence" is not shown (7/13 uncorrected pair p < 0.05) | Describe the test, name windows 34/77/95, state 10/100, add caveat (patch) |
| report/body_final.md:315–316 (PDF p. 14) | "can reproduce the cipher's 13 symbols, its flatness and its lack of detectable order" | 13/100 and 10/100 | Narrow (patch) |
| report/body_final.md:373 (PDF p. 16) | "can reproduce the cipher's symbol usage, flatness and lack of order (O33)" | as above | Narrow (patch) |
| report/codes.md:40 (PDF p. 30) | "fits … 13 symbols (13 of 100), its flatness and, mostly, its lack of order" | as above | Narrow (patch) |
| report/back.md:209 (PDF p. 20) | "purpose-built four-square fits the clues (O33)" | usage and flatness | Narrow (patch) |
| docs/FINDINGS-ADDENDUM.md:17 | "it reaches 13 flat symbols with little order" | as above | Narrow (patch) |
| evidence/case/dagapeyeff.json, O33 | "fits every structural clue … leaves little order - 12 of 100 … (3 of the 13 flat ones)" | numbers correct; "fits every structural clue" overstates | Append-only record: add a superseding entry (§4), do not edit O33 |
| report/body_final.md:310–313 numbers; Appendix A.11 | 52/100, 12/100, 3/13, p = 0.999 | match fsq-order.json | no change |

No figure or caption concerns the four-square result.

## 3. Reproduction log

Environment (lab container): Python 3.12.13, numpy 2.5.2, scipy 1.18.1, torch 2.11.0+cu128 (CUDA 12.8), NVIDIA
GeForce RTX 5060 Laptop GPU. Corpus and Wells texts as fingerprinted in `lab/cipher/lm/CORPUS.md`.

| Check | Kind | Command (lab job) | Result |
|---|---|---|---|
| Four-square streams, cell counts | **Independent calculation** (own code; inputs: Wells texts, recorded seeds `Random(31000+w)`, stored P1/P2) | `audit_fsq.py` (20261015-190929-531f, CPU, 17 min) | 100/100 match |
| χ² flatness | **Independent calculation** (regularized gamma) | same | 13/13 match (tol. 5 × 10⁻⁵) |
| Order test | **Independent calculation** (own MI, fresh shuffles PCG64 seed 20261015, B = 5,000; two min-p conventions) | same | flat-13 flagged: 34, 77, 95 (identical); overall 11/100 vs 54/100 |
| Greedy vs optimal vs raw distance | **Original-script rerun** to regenerate final tables (`review_checks.repair`, `grille_engine.repair_table`, same seeds) + independent distance code | `label_audit.py` (20261015-190929-f0a6, GPU, 18 min) | 220 runs; kept flag identical; regenerated round-12 greedy distances = published 200/200; round-11 raw = published 20/20 |
| n-gram scorer | **Independent calculation** (CPU, float64) + toy cases | `ngram_indep.py` (20261015-192842-bf8d, CPU, 19 min; first attempt 20261015-190929-0dde failed on a JSON-serialization bug in the audit script, fixed) | toy exact; ≤ 6.3 × 10⁻⁷ vs experiment |
| Truth-start (10 runs) | **Independent calculation** (own search and scorer; true tables from the documented rule, checked equal to the original's) | same | kept flag 10/10; error size 9/10 (the tenth: greedy overstatement) |
| Manifest | **Check of stored outputs** | `sha256sum -c MANIFEST.sha256` | 111/111 OK |

Not done here: a full fresh rerun of every experiment (the internal clean-room reproduction of October 15 already
compares the first 20/10/30 cases field by field; Section 10 of the report). Corpus B needs the two Christie novels,
which are not redistributed; they were available locally. GPU float32 sums are not bit-for-bit deterministic across
hardware, but every rerun so far matched exactly.

## 4. Proposed case-file entry (append-only record; not yet added)

> **O34** (supersedes O33's wording; O33 stays as history). Four-square with a key built on purpose for the message,
> by hill-climbing the plaintext squares for a given 182-letter passage (the plaintext is used, as the encipherer would):
> 13 of 100 passages reach 13 cells with χ² p ≥ 0.05 (0.85–1.0). On the order test (mi_even, mi_odd, max lag 1–26
> MI; 2,000 shuffles; family-wise min-p; α = 0.05), 3 of those 13 are flagged (windows 34, 77, 95), so 10 of 100 meet
> both criteria; 7 of the 13 show uncorrected pair dependence at p < 0.05. Overall 12/100 purpose-built vs 52/100
> random keys flagged; the real message is not flagged (p = 0.999). Non-detection is not absence of order. A
> feasibility result; not evidence that D'Agapeyeff used four-square; unsearched.
> Evidence: fsq-full.json, fsq-order.json; audit-2026-10-15/outputs/audit_fsq.json.

## 5. Guardrails observed

Synthetic known-answer experiments only; no claim that the historical cipher is solved. Non-rejection of an order
statistic is not treated as evidence of randomness. 13/100 is not a probability for random keys (keys were optimized
per passage). Local optimizer behavior is not described as an identifiability theorem. This audit is internal.

## 6. Follow-up (second audit request, October 15, 2026)

### 6.1 Issue register

| # | Item | Verdict | Affected | Evidence | Change |
|---|---|---|---|---|---|
| F1 | Greedy label matching (`round12/review_checks.py`, `wrong`, lines 92–100; docstring says "best label matching") | **Possible issue → no effect on any published result** | `ident-full.json` field `wrong_found` and summary `mean_wrong` only | All 2,000 robustness runs regenerated (`label_full.py`): every field matches the published record, 2,000/2,000. Greedy ≠ exact in 80 runs, always by exactly 1 letter; truth-kept flag changes 0; higher-scoring flag changes 0; fresh-passage and other-corpus comparisons unchanged; pure relabellings 0. Unit test `test_label_distance.py` (counterexample greedy 4 / exact 3). | Appendix E notes it; the report never cites `wrong_found` or `mean_wrong`. Executed script left unchanged (proposed docstring clarification below, not applied). |
| F2 | §10 "using independently written code" | **Possible issue (clarity) → corrected** | report/back.md §10 (PDF p. 17) | The checking code was written by the developer within the project. | Now: "run within the project by the developer, with checking code written separately from the experiment code, and not a replication by an unaffiliated researcher". |
| F3 | §10 audit claims not substantiated inside the repository | **Confirmed gap → corrected** | Section 10; repository contents | The audit's scripts and outputs were outside the repository; `report/AUDIT-proof.md` is Proof's numbers audit, not this audit. | Shipped: `lab/cipher/audit/` (scripts, outputs) and `docs/audit-2026-10-15/` (this report, the applied patch); README rows and commands. |
| F4 | §10 internal-reproduction counts | **No issue** | report/back.md §10 | `round12/repro/repro-compare.json`: 18/18, 40+40 = 80/80, 200/200, 30/30, order summary identical. | — |
| F5 | §6.5 / F79 comparability figures | **No issue** | report/body_final.md §6.5 | `comparability.json`: mass 2.1007–2.1108 (A′), 1.4470–1.4537 (B), spread 0.0021 / 0.0020 log10 over 306 tables; neighbours beating truth 0/9,150 at 10,000 and at 100,000 symbols (2 corpora × 3 scores × 5 true tables × 305 neighbours, per length), 158/9,150 at 182 (1.4–2.6% per group), 5/9,150 at 1,092 (≤ 1/1,525 per group); renormalized truth-start kept flag 200/200 = published. | — |
| F6 | Manifest and release integrity | **No issue** | MANIFEST.sha256 | Recomputed after the final build (see §6.4). | — |
| F7 | 13/100 vs 10/100 four-square distinction | **No issue (fixed earlier, O34)** | README, §1, §7, §9, Appendix D | Re-checked after the final build. | — |

### 6.2 Greedy vs exact distance where they differ (by setup and length; all other setups identical)

| Setup | Runs | Greedy ≠ exact | Mean wrong, greedy (published) | Mean wrong, exact | Mean wrong, raw | Truth-kept changes | Higher-scoring changes |
|---|---|---|---|---|---|---|---|
| E1 A:joint6 pool L182 | 50 | 3 | 2.60 | 2.54 | 2.54 | 0 | 0 |
| E1 A:joint6 pool L273 | 50 | 1 | 1.52 | 1.50 | 1.50 | 0 | 0 |
| E1 A:joint6 prose L182 | 50 | 2 | 2.46 | 2.42 | 2.42 | 0 | 0 |
| E1 B:joint6 pool L182 | 50 | 1 | 2.60 | 2.58 | 2.58 | 0 | 0 |
| E1 B:joint6 pool L273 | 50 | 1 | 1.96 | 1.94 | 1.94 | 0 | 0 |
| E1 B:joint6 prose L182 | 50 | 2 | 2.36 | 2.32 | 2.34 | 0 | 0 |
| E1 B:joint6 prose L273 | 50 | 1 | 1.74 | 1.72 | 1.74 | 0 | 0 |
| E3 C:joint6 prose L182 | 50 | 8 | 2.60 | 2.44 | 2.60 | 0 | 0 |
| E3 C:joint6 prose L273 | 50 | 10 | 2.10 | 1.90 | 2.10 | 0 | 0 |
| E3 C:joint6 prose L364 | 50 | 5 | 1.74 | 1.64 | 1.74 | 0 | 0 |
| E3 C:joint6 prose L546 | 50 | 3 | 1.56 | 1.50 | 1.56 | 0 | 0 |
| E3 C:cond4 prose L182 | 50 | 2 | 3.52 | 3.48 | 3.52 | 0 | 0 |
| E3 C:cond4 prose L273 | 50 | 4 | 2.64 | 2.56 | 2.62 | 0 | 0 |
| E3 C:cond4 prose L364 | 50 | 6 | 2.38 | 2.26 | 2.38 | 0 | 0 |
| E3 C:cond4 prose L546 | 50 | 4 | 1.76 | 1.68 | 1.76 | 0 | 0 |
| E3 C:cond5 prose L182 | 50 | 4 | 2.84 | 2.76 | 2.82 | 0 | 0 |
| E3 C:cond5 prose L273 | 50 | 4 | 2.14 | 2.06 | 2.14 | 0 | 0 |
| E3 C:cond5 prose L364 | 50 | 2 | 1.84 | 1.80 | 1.84 | 0 | 0 |
| E3 C:cond5 prose L546 | 50 | 3 | 1.62 | 1.56 | 1.62 | 0 | 0 |
| E3 C:cond6 prose L182 | 50 | 5 | 2.40 | 2.30 | 2.40 | 0 | 0 |
| E3 C:cond6 prose L273 | 50 | 6 | 1.64 | 1.52 | 1.64 | 0 | 0 |
| E3 C:cond6 prose L364 | 50 | 2 | 1.44 | 1.40 | 1.44 | 0 | 0 |
| E3 C:cond6 prose L546 | 50 | 1 | 1.32 | 1.30 | 1.32 | 0 | 0 |

Raw (letterwise) distance is the conceptually correct measure for this test, because the cipher symbols are
observed; exact relabelling and raw agree on 1,931 of 2,000 runs.

Proposed docstring clarification for `round12/review_checks.py` — **not applied**, because that file is the code that
produced the published results and changing it would change its fingerprint:

```diff
-    """letters whose group differs from the truth, up to relabelling of groups (best label matching)."""
+    """letters whose group differs from the truth, up to relabelling of groups (GREEDY label matching: can exceed the
+    exact minimum by a letter; see lab/cipher/audit/test_label_distance.py and label_full.json)."""
```

### 6.3 PASS / FAIL

| Priority | Result |
|---|---|
| 1 — group-label matching | **PASS** — no published value changes; 80/2,000 runs differ by one letter in an unreported field |
| 2 — reproduction and audit language | **PASS after correction** — evidence shipped in the repository; "independently written" narrowed to "written separately within the project" |
| 3 — release integrity | **PASS** — manifest, PDF, comparability figures and four-square counts verified |

### 6.4 Commands and fingerprints

Run from the repository's `lab/cipher/` mounted at `/lab/cipher` (README "Reproduce"):

```
run python audit/test_label_distance.py      # unit test, seconds
run python audit/audit_fsq.py                # CPU, ~17 min
run python audit/ngram_indep.py              # CPU, ~19 min
run python audit/label_audit.py              # GPU, ~18 min
run python audit/label_full.py               # GPU, ~80 min
```

Lab jobs: audit_fsq 20261015-190929-531f; label_audit 20261015-190929-f0a6; ngram_indep 20261015-192842-bf8d;
label_full 20261015-200644-a5cd.

| File | SHA-256 |
|---|---|
| `lab/cipher/audit/test_label_distance.py` | `160eaa71523214fbd0ab150b0e7691bfb6dc8eba7a1e2f4da001b541cbec50fc` |
| `lab/cipher/audit/audit_fsq.py` | `81dc627e9039964c9c903249e45618183a63c0468ac76b8cbab465acf779c9f0` |
| `lab/cipher/audit/label_audit.py` | `ac606f4cac7d627211750f7601fe842d8c2e99478ab929ef1cde4eab4c00c899` |
| `lab/cipher/audit/ngram_indep.py` | `f31d231ac74e4f0c1c9e6cd103b75e14caa2ae681343115e92d38b00cb1b2c59` |
| `lab/cipher/audit/label_full.py` | `2ae66f1aae61974a8955775ff1e2057ce117950385a354e593326ab948d7a973` |
| `lab/cipher/audit/audit_fsq.json` | `4cacca4bef7ed485a43a12652e1ba7e3dbe842feecd6a2cc318c17e10c9eda43` |
| `lab/cipher/audit/label_audit.json` | `39b7d9396105ff3b0487593414c2d488ef85c9abcf444c3863a8a0cba507cfa8` |
| `lab/cipher/audit/ngram_indep.json` | `43352c35bececa8e37558c2a65352a89da2af6a0bf0e1993a4f275fcea3c04c4` |
| `lab/cipher/audit/label_full.json` | `8a12442de522847a0d7946794336dd8b16b2abd2af3d68004f2ce1dd6704cb87` |
