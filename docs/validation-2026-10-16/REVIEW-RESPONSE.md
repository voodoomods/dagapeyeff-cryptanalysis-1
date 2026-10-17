# Response to the final release-candidate validation request

Validation of the D'Agapeyeff preprint and repository, run October 16–17, 2026, at the author's request, in answer to
the validation request drafted by ChatGPT (OpenAI). Performed by the project's developer (Claude Opus 5.5), not by an
unaffiliated party. This is internal validation, not independent replication and not peer review.

Everything below is in this folder (`docs/validation-2026-10-16/`): `validation-results.json` (machine-readable
record: environment, every command, exit code, elapsed seconds, SHA-256 of every file), `compare.json` (every check
with expected and observed values), `logs/`, `rerun/` (the rerun outputs), and `QA-REPORT-2026-10-17.md`. The
criteria were written down before the reruns finished: `validation/CRITERIA.md`.

## 1. Release candidate

| Item | Value |
|---|---|
| Frozen candidate | `voodoomods/dagapeyeff-cryptanalysis`, branch `main`, commit `44f7b233d76744e98b5ed164d4144a93f6f0cd0d` |
| Integrity of the candidate | fresh clone; `sha256sum -c MANIFEST.sha256`: 130 of 130 files OK; byte-identical to the local release folder |
| Where the reruns ran | a working copy of that clone (Christie novels added, model text rebuilt; its fingerprint matched `CORPUS.md`), in Podman containers with no network, UID 1002 |
| Published results | read from a second, untouched clone; never written |
| Original evidence in the workspace | untouched; the one script that writes to a fixed workspace path (F66) was run from a copy writing elsewhere |
| Updated repository | builds on the candidate with the corrections listed in section 4. It has no commit yet: the author commits and pushes manually, and the new commit SHA is assigned then. Its `MANIFEST.sha256` fingerprint is in section 6 |

## 2. Matrix

Kinds of check: **rerun** = the published script, at full size, with its published arguments and seeds, compared
record by record with the published file and every printed number recomputed from the rerun; **recomputation** =
new code written for this validation from the definitions in the report and case file; **source inspection** = the
printed number recomputed from the published result file.

| Request | Kind | Command | Output | Observed | Expected (printed) | Status |
|---|---|---|---|---|---|---|
| F78 grille recovery, true table given | rerun | `python grille/bench_ngram.py` | `rerun/grille/bench-ngram.json` | 18 / 18 records identical; six-symbol 6 of 6 (5 exact, min 48), five-symbol 6 of 6 (3 exact, min 47), four-symbol 2 of 6 | the same | **PASS** |
| F74 table must be essentially exact | rerun | `python grille/bench_tolerance.py` | `rerun/grille/bench-tolerance.json` | 24 / 24 identical; 4/4, 1/4, 2/4, 0/4, 0/4, 0/4 | the same | **PASS** |
| F76 identifiability, corpus A | rerun | `python round11/identifiability.py A 100 182,…,1092 -val` | `rerun/round11/identifiability-A-val.json` | 1,400 / 1,400 identical; 14, 31, 46, 65, 72, 84, 94 % | the same | **PASS** |
| F76 identifiability, corpus B | rerun | `… identifiability.py B 100 … -val` | `rerun/round11/identifiability-B-val.json` | 1,400 / 1,400 identical; 8, 22, 36, 49, 54, 65, 74 % | the same | **PASS** |
| F76 both corpora, 178 / 200, ≈ 420 symbols | rerun | (from the two above) | `compare.json` | 11, 26.5, 41, 57, 63, 74.5, 84 %; 178 of 200 beaten at 182; one in two at 420 | the same | **PASS** |
| F77 robustness (2,000 runs), Appendix E | rerun | `python round12/review_checks.py ident 50 182,273,364,546 -val` | `rerun/round12/ident-val.json` | 2,000 / 2,000 identical; lowest / highest / pooled 8/26/15, 10/42/26, 16/44/29, 28/60/41 %; 171 of 248 other corpus; 82 of 427 fresh passage | the same | **PASS** |
| F79 score comparability | rerun | `python round12/comparability.py -val` | `rerun/round12/comparability-val.json` | identical except the `tag` field (the output suffix on the command line); mass 2.10 / 1.45, spread 0.002 log10; 0 of 9,150 neighbors beat the truth at 10k and 100k symbols; 200 normalized runs | the same | **PASS** |
| R35 random-key four-square / two-square | rerun | `python round11/micro_digraph_cells.py 2000`; `python round11/micro_digraph_cells_4x5.py` | `rerun/round11/micro-digraph-cells*.json` | identical; 22–25 and 18–20 symbols; none ≤ 13 in 10,000 | the same | **PASS** |
| O34 purpose-built four-square | rerun | `python round12/review_checks.py fsq 100 10 -val 50000` | `rerun/round12/fsq-val.json` | 100 / 100 identical; 13 of 100 at 13 symbols, all flat (p 0.848–1.0) | 13 of 100; p 0.85–1.0 | **PASS** |
| O34 order test | rerun | `python round12/fsq_order.py 2000` | `rerun/round12/fsq-order.json` | identical; 12 / 100 vs 52 / 100 flagged; 3 of 13 (34, 77, 95); 7 of 13 pair statistics; real p = 0.999 | the same | **PASS** |
| F71 grille recovered with the letter key | rerun | `python grille/bench2.py` | `rerun/grille/bench-2.json` | key given: 3 / 3 identical, all 49 orbits. Key-unknown controls (600 s wall-clock each, no number printed) differ: 15, 15, 14 orbits vs 14, 19, 15, unrecovered in both | 3 of 3 | **PARTIAL** (controls are wall-clock-bounded; printed claim reproduced) |
| I47 table repair moves away from the truth | rerun | `python round11/table_test.py validate` | `rerun/round11/validate.json` | 7 / 7 identical; 2 wrong → 5 | 2 → 5 | **PASS** |
| F68 joint grille-and-table search has no power | rerun (platform engine, not in the repository) | `python compound/compound_engine.py power-rerun.cfg.json` (configuration of lab job `20261012-230606-edb3`) | `f68/power-rerun.json` | 0/3 at 60 s, 0/3 at 300 s, 0/3 at 1,200 s per phase | 0 of 3 at every budget | **PASS** |
| F31 / F80 flatness, English and Latin | recomputation, standalone (`flatness_standalone.py`: wordfreq 3.1.1 + SciPy, no platform code) | `python validation/flatness_standalone.py --lang en [--windows 2000]`; `--lang la --seed 0..3`, and with `--latin-files augustine-confessiones.txt,caesar-bello-gallico.txt,cicero-orations.txt,descartes-meditationes.txt,newton-principia.txt,virgil-aeneid.txt` | `flatness/*.json` | English 364/1000 (top letters 1/2000 in the 2,000-window run); Latin 358, 374, 366, 357; six editions 182, 167, 172, 174 — the same counts as the platform tool, seed for seed | 364; 345–374; 167–182 | **PASS** |
| §2 "natural passages use 17 to 22 different letters" | recomputation | (same runs) | `flatness/*.json` | English 18–25 (median 22); Latin 14–25 (median 20) | 17–22 | **FAIL → corrected** (F81; section 4) |
| F4 rare symbols in one column, p < 1 / 20,000 | recomputation (new code) | `python validation/recompute_extra.py` | `recompute_extra.json` | statistic 0.929 at row length 14; exact bound 1.8 × 10⁻⁹; 0 of 200,000 shuffles | below 1 / 20,000 | **PASS** (holds for the platform's excess-over-1/p statistic; a cruder "all in one residue for any row length" statistic gives about 0.7 %, almost all from row length 2) |
| F32 no order | recomputation (new code) | same | `recompute_extra.json` | rows 0.087, columns 0.304, halves 0.094 / 0.494, lag family 0.902 | 0.08, 0.30, 0.10 / 0.60, 0.91 | **PASS** (left/right split assumed: columns 1–6 vs 8–13) |
| R29 polyphonic table leaves order | recomputation (new code, new seeds) | same | `recompute_extra.json` | 39 of 40 at p < 0.05 (38 at p < 0.01); real message p = 0.72 | 40 of 40 (39 at p < 0.01); p = 0.70 | **PARTIAL** (conclusion reproduced; exact count is seed-dependent; original code not in the repository) |
| F66 replication of Hendrick's test | rerun of the original script (unseeded), 20 times, from a copy writing elsewhere | `sh validation/run_f66.sh f66 20` | `f66/rep*.json` | family-wise p 0.251–0.594 (median 0.39); smallest statistic always info lag 3 | 0.29; not significant | **PASS** (0.29 is one Monte Carlo draw — range now given in the text) |
| Standalone Latin check | delivered | `validation/flatness_standalone.py` | — | runs with wordfreq + SciPy only; needs the ten Latin editions (`CORPUS.md` lists eBook numbers and fingerprints) | — | **PASS** |
| Single entry-point run script + expected-output comparison | delivered | `validation/run_all.sh gpu|cpu`; `validation/compare.py` | `compare.json` | 13 steps, 0 nonzero exits, 32,652 s (9.1 h) | — | **PASS** |
| New date-stamped QA report | delivered | `python validation/qa_checks.py <repo>` | `QA-REPORT-2026-10-17.md` | see that report | — | **PASS** |
| License-exception summary (README / front matter) | delivered | — | README "License exceptions"; report rights paragraph | wordfreq-derived files CC BY-SA 4.0; Gutenberg texts not covered by CC BY | — | **PASS** |
| DOI not claimed live | checked | `curl https://doi.org/10.5281/zenodo.23306263` | — | 404 (not registered); README now says "reserved … resolves once the Zenodo record is published" | — | **PASS** |
| No external peer review claimed | checked | `qa_checks.py` | QA report | none; every mention carries "not" | — | **PASS** |

Totals (`compare.json`): 17 PASS, 2 PARTIAL, 1 FAIL (corrected), 0 NOT RUN.

Elapsed time per rerun step (seconds): F71 2,168 · F78 1,490 · F74 1,840 · I47 1,312 · F76-A 3,018 · F76-B 5,806 ·
F77 8,489 · F79 725 · R35 6 + 4 · O34 2,757 + 351 · F68 4,686. Recomputations: flatness under 1 minute per run,
`recompute_extra.py` 33 s, F66 about 7 s per rerun.

## 3. Readiness

**CONDITIONAL.**

- *Scientific content: ready.* Every headline result reproduces in a full-size, no-network rerun from a fresh clone of
  the candidate. Of 4,959 published records compared (each summary-only file — F79, R35, the order test —
  counted as one record), 4,956 are identical apart from elapsed time; the other 3 are the wall-clock-bounded F71
  controls. Every printed number recomputed from the reruns equals the printed value. One
  printed figure was wrong (the §2 letter range); it is corrected and the conclusion it supports is unchanged.
- *Conditions before release* (the author's to complete): commit and push the updated repository; publish the
  Zenodo record so the reserved DOI resolves; make the GitHub repository public (today it returns 404 to an
  anonymous request). After the push, `sha256sum -c MANIFEST.sha256` on a fresh clone should pass, as it does on
  the local build.

## 4. Changes made because of this validation

| Change | Where | Why |
|---|---|---|
| §2 letter range "17 to 22" → "18 to 25 … in English (median 22) and 14 to 25 in Latin (median 20)" | report §2; case entry F81 (supports F31); fact-check entry 109; codes F81 | recomputed (section 2) |
| F66 "0.29" → "0.29; 0.25 to 0.59 across 20 reruns of the same test" | report §7; codes F66; fact-check 110 | unseeded test (section 2) |
| License exceptions | README; report rights paragraph | request |
| DOI marked reserved | README | not registered yet |
| README container recipe installs SciPy | README "Reproduce" | four scripts import SciPy; the PyTorch image used in the old recipe has none |
| "licence" → "license" | `CORPUS.md`, Appendix F, NOTICE, `sources.json` | American English |
| `validation/` folder and this folder shipped | repository | request |

Fact-check entries 111–113 record checks that needed no change (F4, R29, F32). No experiment script, archived
evidence file or published result file was changed. The case graph's at-risk set is unchanged (I25, O26 — older,
unrelated entries).

## 5. Remaining gaps

| Gap | Severity | Note |
|---|---|---|
| No replication by an unaffiliated party; the AI review is not peer review | Medium | Stated in the report, README and here. The repository is built for it. |
| F4, F32, R29 and F31 rest on platform analysis code that is not in the repository | Medium → Low | The standalone recomputations now in `validation/` reproduce F31/F80 exactly and F4/F32 within sampling; R29 39 of 40 vs 40 of 40 printed. |
| R29 printed "40 of 40" not reproduced exactly from the repository | Low | Optional wording: "39 or 40 of 40 depending on the seed". Not changed; needs the author's decision. |
| F68 needs the PegasusDMZ engine; the exact `grille_engine.py` present at the original run was not preserved | Low | Rerun with the last committed version before that run; same outcome. Outsiders cannot rerun F68 from the repository. |
| F66 test is unseeded | Low | Range now printed. |
| GPU key-unknown controls (F71) are wall-clock-bounded, so not bit-reproducible | Low | No printed number depends on them. |
| The README's Docker recipe was not executed end-to-end with the public PyTorch image | Low | Validation used the platform's lab image (Python 3.12.13, NumPy 2.5.2, SciPy 1.18.1, PyTorch 2.11.0, CUDA 12.8). |
| Christie novels and Latin editions are not redistributed; Project Gutenberg files may change after 2026-10-11 | Low | Fingerprints in `CORPUS.md` let an outsider confirm a download matches. |
| The origin of the old "17 to 22" range is not recorded | Info | Corrected; recorded as F81. |
| F81's case-file evidence path reads `docs/validation-2026-10-16/results/flatness/`; the files are at `docs/validation-2026-10-16/flatness/` | Info | The case file is append-only; noted here. |
| Raw lab logs (`logs/F68_power.log`) carry times of day | Info | Evidence, kept as produced; no report or document carries them. |
