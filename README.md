# dagapeyeff-cryptanalysis-1

**The D'Agapeyeff Cipher (1939): grille recovery and polyphonic-table identifiability under n-gram scoring**

Nicolas Houghtaling, independent researcher ([ORCID 0009-0001-3192-544X](https://orcid.org/0009-0001-3192-544X)) · VoodooMods LLC · 2026

**Repository:** <https://github.com/voodoomods/dagapeyeff-cryptanalysis-1>

**DOI (reserved):** 10.5281/zenodo.23306263 — reserved on Zenodo for this work; it resolves once the Zenodo record is published.

**Publication status:** Research preprint. This manuscript has undergone internal verification and AI-assisted critical review but has not been formally peer-reviewed by an independent academic journal.

© 2026 VoodooMods LLC. Report, results and data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code:
Apache-2.0. See `COPYRIGHT`, `LICENSE`, `LICENSE-CC-BY-4.0.md` and `NOTICE`.

**License exceptions.** These files keep their own terms (details in `NOTICE`):

- `lab/cipher/grille/plain_pool.txt`, `lab/cipher/grille/quad_en.npy` and the practice plaintexts quoted in
  `lab/cipher/grille/bench-2.json` are derived from wordfreq data and are shared under
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), not CC BY 4.0. Credit: Speer (2022), SUBTLEX-US and
  SUBTLEX-UK.
- `lab/cipher/lm/corpus/*.txt` are Project Gutenberg texts that are public domain in the USA. They are not licensed by
  us, and their status elsewhere has not been legally reviewed.
- `docs/literature/gariazzo2026/` is R. Gariazzo's report (CC BY 4.0, by its author).
- `data/ciphertext.txt` is the 1939 challenge cipher, quoted from D'Agapeyeff's book.
- Not included: two Agatha Christie novels and the model text built from them, the ten Latin editions, Hendrick's
  manuscript and third-party abstracts. See `lab/cipher/lm/CORPUS.md` for how to obtain the texts.

## The study in brief

In 1939 Alexander D'Agapeyeff closed *Codes and Ciphers* with a 196-symbol challenge cipher that has never been read.
Prior work (Hendrick 2026) ruled out every one-to-one letter key combined with any transposition; among the
systems it left open is the turning grille. This study,
conceived and directed by Nicolas Houghtaling over seven days (October 8–14, 2026) with an AI research team, and checked further
on October 15 after reviews of the draft by a separate AI system (ChatGPT, OpenAI), tested in depth one construction consistent with every observed property — a
14 × 14 turning grille over a *polyphonic* table, in which each of the cipher's 13 symbols stands for a group of letters.
All rates below are measured on practice ciphers with known keys.

- **With the true table supplied, practice-cipher grilles were recovered** — six-symbol scoring recovered at least 45
  of 49 orbits in six of six practice ciphers, five exactly (F78; a preliminary demonstration, not recovery of the
  historical grille).
- **The table must be essentially exact** — 6 or more misplaced letters: 0 of 12 (F74; preliminary).
- **Under the n-gram scores tested, 182 symbols rarely single out the table** — started at the true table with the
  order known, the search keeps it in only 11% of 200 practice ciphers (84% at 1,092 symbols; F76), and in 8–26%
  under every plaintext, corpus and score tried after review (F77; every setup in the report's Appendix E). The
  higher-scoring tables fit the passage, not English, and the scores are comparable across tables (F79).
- **Four-square and two-square with random keys do not fit** — in 10,000 practice ciphers they spread English over
  18–25 distinct symbols, never the message's 13 (R35); this excludes the randomly keyed constructions tested, under the
  tested plaintext, not every possible key.
- **A purpose-built four-square can match the cipher's symbol usage and flatness** — a key optimized for each
  passage reached 13 symbols with the specified frequency flatness in 13 of 100 passages; 10 of those 13 were not
  flagged by the tested family-wise order statistic at the 5% threshold, which is not evidence that they contain no
  order (O34). A feasibility demonstration with keys optimized using the plaintext, not evidence that D'Agapeyeff
  used four-square; it has not been searched.

With the methods tested, the grille hypothesis cannot be decided from the cipher's own text. For the tested
objectives, higher-scoring incorrect tables frequently exist even when the true order and table are supplied, so more
optimization of the same objective cannot be assumed to help; longer budgets were not studied, and a differently
designed search or model is not ruled out (report, Section 7). No decipherment is claimed. The full argument, prior work and limitations are in
the report.

## Start here

| File | What it is |
|---|---|
| `report/DAgapeyeff-Report-VoodooMods.pdf` | **The report** — findings, figures, prior work, limitations, the team, budget and timeline |
| `report/FACTCHECK-LOG.md` | Every correction made while checking the report against its sources |
| `evidence/case/dagapeyeff.json` | The case file: every result with its evidence and review history (codes such as F78, R29 — explained in the report's Appendix D) |
| `MANIFEST.sha256` | SHA-256 of every file in this repository |

## Contents

| Path | Contents |
|---|---|
| `report/` | The PDF; its Markdown sources (`front.md`, `body_final.md`, `back.md`, `codes.md`, `appendix-e.md`); figures (`figs/`); `make_figures.py` and `build_report.py`; the fact-check log, QA report and source pack |
| `lab/cipher/grille/` | The search engines (`grille_engine.py`, `poly_engine.py`), the grille benchmarks (`bench2.py`, `bench_ngram.py`, `bench_tolerance.py`) with their results, and the English model texts |
| `lab/cipher/round11/` | The table-repair (`table_test.py`) and identifiability (`identifiability.py`) experiments, the cipher as cells, and their results |
| `docs/sources.json`, `lab/cipher/lm/CORPUS.md` | Provenance of every language source: Project Gutenberg eBook numbers, catalog details, retrieval date and processing, fingerprints, wordfreq version and licensing (the report's Appendix F) |
| `lab/cipher/provenance/` | The Latin comparison of case F80 (`latin_flatness.py`, needs the PegasusDMZ agent tools) and its result |
| `lab/cipher/lib/` | For future experiments: `label_distance.py` — exact (optimal one-to-one) group-label distance as the default, the published greedy matching under a legacy name, and raw letterwise distance — with unit tests (`test_label_distance.py`). Not used by the published results |
| `docs/validation-2026-10-17/`, `validation/original/` | The R29 and F4 clarifications of October 17: the original commands for both, recovered from the session record and rerun unchanged, the two F4 events computed side by side (`validation/f4_events.py`), and `R29-F4-RESPONSE.md` |
| `validation/` and `docs/validation-2026-10-16/` | The release-candidate validation of October 16: full-size reruns of the published experiments from a fresh clone (`run_all.sh`), predeclared criteria (`CRITERIA.md`), the expected-output comparison (`compare.py`), standalone recomputations that need no PegasusDMZ code (`flatness_standalone.py`, `recompute_extra.py`, `run_f66.sh`), and the results: `REVIEW-RESPONSE.md`, `validation-results.json`, logs and the QA report |
| `lab/cipher/audit/` and `docs/audit-2026-10-15/` | The internal audit of October 15 (written within the project, not by an unaffiliated party): separately written checks of the four-square reconstruction, flatness and order tests, the n-gram score and ten truth-start runs, and greedy versus exact label matching on all 2,000 robustness runs; scripts and outputs, with the audit report and the patch it led to |
| `lab/cipher/round12/repro/` | A clean-room reproduction of the headline experiments from a fresh copy of this repository (`run_repro.sh`), and its run-by-run comparison with the published results (`compare_repro.py`, `repro-compare.json`) |
| `lab/cipher/round12/` | The checks made after review of the draft: robustness of the identifiability result and purpose-built four-square keys (`review_checks.py`), the four-square order test (`fsq_order.py`), and their results |
| `lab/cipher/lm/` | `corpus/`: 11 of the 13 public-domain novels the English models are built from; `CORPUS.md` lists all 13 with fingerprints |
| `evidence/` | The case file, lab job records, the report's Appendix C (`APPENDIX-C.md`), the budget totals (`accounting-2026-10-14.json`) and the evidence collector |
| `docs/` | The novelty check and literature search, Gariazzo's report (CC BY 4.0), the team's findings write-up and the round-10 briefing |
| `data/ciphertext.txt` | The 395 digits as published |
| `tools/` | `build_release.py` (assembles and verifies this repository) and `accounting.py` (recomputes the budget from the raw records) |

Some material is listed by fingerprint only and not included, because it is not the project's to redistribute: Hendrick's
manuscript (all rights reserved — doi:10.5281/zenodo.23241303), extracts from D'Agapeyeff's book, the literature search
with its abstracts (the metadata is included), and two corpus novels by Agatha Christie that are public domain in the
USA but not in the UK and EU — together with `model_text_big.txt`, which contains their text. See `NOTICE`.

## Verify

```
sha256sum -c MANIFEST.sha256
```

Every fingerprint in the report's Appendix C appears in `MANIFEST.sha256`.

## Reproduce

First obtain the two Christie novels from Project Gutenberg into `lab/cipher/lm/corpus/` (file names and fingerprints
in `lab/cipher/lm/CORPUS.md`) and rebuild the model text — this reproduces its published fingerprint exactly:

```
python tools/build_model_text.py lab/cipher/lm/corpus lab/cipher/grille/model_text_big.txt
```

The scripts read and write absolute paths under `/lab/cipher/`, exactly as they ran. Mount this repository's `lab/`
directory at `/lab` in a container with Python 3.12, PyTorch, SciPy and a CUDA GPU (CPU works, slowly). The PyTorch
image has no SciPy, which four of the scripts import, so build a small image first (the published runs used Python
3.12.13, NumPy 2.5.2, SciPy 1.18.1 and PyTorch 2.11.0 with CUDA 12.8):

```
printf 'FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime
RUN pip install "scipy>=1.11" "matplotlib>=3.8"
' | docker build -t dagapeyeff-env -
run() { docker run --rm --gpus all -v "$PWD/lab:/lab" -w /lab/cipher dagapeyeff-env "$@"; }
run python grille/bench_ngram.py                                              # Figure 4 (F78)
run python grille/bench_tolerance.py                                          # Figure 5 (F74)
run python round11/table_test.py validate                                     # Section 6.3 (I47)
run python round11/identifiability.py A 100 182,273,364,455,546,728,1092 -big   # Figure 6 (F76)
run python round11/identifiability.py B 100 182,273,364,455,546,728,1092 -big
run python round12/review_checks.py ident 50 182,273,364,546 -full                # Section 6.5 (F77)
run python round12/review_checks.py fsq 100 10 -full 50000                         # Section 7 (O34)
run python round12/fsq_order.py 2000
run python round12/comparability.py                                              # Section 6.5, comparability (F79)
run sh -c "cd lib && python test_label_distance.py"                           # exact vs legacy label distance (unit tests, ~1 min)
run python audit/test_label_distance.py                                           # audit: greedy vs exact label matching (unit test)
run python audit/audit_fsq.py                                                     # audit: four-square rebuild, flatness, order test
run python audit/ngram_indep.py                                                   # audit: independent n-gram scorer, 10 truth-start runs
run python audit/label_full.py                                                    # audit: all 2,000 robustness runs, greedy vs exact
```

**One entry point.** `validation/run_all.sh` runs every experiment above at full size (`gpu`: about 9 hours on a
laptop RTX 5060; `cpu`: under an hour), logging each command, its output, exit code and elapsed time;
`validation/compare.py` then checks every printed number against the rerun and the published files. Run it in a
container whose `/lab` is a working copy of `lab/` (the scripts overwrite their result files) and whose `/val` holds
the logs; keep a second, untouched clone for `--ref`:

```
docker run --rm --gpus all --network none -v "$PWD/work/lab:/lab" -v "$PWD/val:/val"     -v "$PWD/validation/run_all.sh:/val/run_all.sh:ro" dagapeyeff-env sh /val/run_all.sh gpu
python validation/compare.py --ref lab/cipher --new work/lab/cipher --steps val/logs --out compare.json
pip install wordfreq==3.1.1 scipy && python validation/flatness_standalone.py --lang en    # F31: 364/1000
```

Seeds are fixed; GPU annealing is not bit-for-bit deterministic, so individual runs vary slightly while the aggregate
results hold. `grille_engine.py` is the final version and is backward compatible with the earlier benchmarks.
`report/make_figures.py` redraws every figure from the result files; `report/build_report.py` rebuilds the PDF.

## Credit and method

Conceived and directed by **Nicolas Houghtaling** (VoodooMods LLC), who designed the research platform it ran on, chose the problem,
and made the decisions that shaped it. Software, search engines, analyses and writing: Anthropic's Claude (Opus 5.5)
under the author's direction. Supporting investigation: a team of AI agents on DeepSeek, Kimi and Qwen models (Section
11 of the report introduces each). Draft review: ChatGPT (OpenAI), through ChatGPT Plus, at the author's
request, over several rounds — an AI review, not human peer review. Language-model cost for the agent team: about US$68 (`evidence/accounting-2026-10-14.json`).

**Review status.** The repository includes the original experiment records, project-internal reproduction results
(`lab/cipher/round12/repro/`), separately implemented numerical checks written by the developer, outside the
experiment code (`lab/cipher/audit/`), and a full-size rerun of the published experiments from a fresh clone of this
repository, in containers with no network (`docs/validation-2026-10-16/`). All of it was done within the project by
the developer; none of it is replication by an unaffiliated party, and the AI review is not human peer review.
Independent replication is welcome — that is what this repository is for.

## Cite as

Houghtaling, N. (2026). *The D'Agapeyeff Cipher (1939): grille recovery and polyphonic-table identifiability under n-gram scoring.* VoodooMods LLC. doi:10.5281/zenodo.23306263

## Copyright and licensing

© 2026 VoodooMods LLC. The author, Nicolas Houghtaling, carried out this work at VoodooMods LLC, which holds the
copyright to the extent it owns the applicable rights. The report, its figures and the accompanying research materials
are released under the Creative Commons Attribution 4.0 International License (CC BY 4.0), and the source code under
the Apache License 2.0. Copyright is asserted only in material eligible for protection under applicable law;
third-party materials keep their own rights and licenses, as set out in the repository's LICENSE and NOTICE files.
