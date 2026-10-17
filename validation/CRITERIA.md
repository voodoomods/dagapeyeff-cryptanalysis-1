# Validation criteria (fixed October 16, 2026, before the full-size reruns finished)

Release candidate: GitHub commit `44f7b233d76744e98b5ed164d4144a93f6f0cd0d`, cloned fresh; reruns run in containers
with no network, from a working copy of that clone. Published files are read from a separate clone and never written.

**Reruns of the published scripts** (`run_all.sh`; same scripts, arguments and seeds; full size):

1. *Record identity.* Every record equals the published record in every field except elapsed time (and, added when
   F79 was compared, the `tag` field, which only echoes the output-file suffix given on the command line). An earlier
   reduced-size clean-room run (`lab/cipher/round12/repro/`) was identical, so identity is expected. GPU annealing is
   not guaranteed bit-for-bit; a difference is reported with the records that differ, never explained away.
2. *Paper numbers.* Every number the report prints is recomputed from the rerun's records (`compare.py`) and must equal
   the printed value at the printed precision. The same extractor is applied to the published file first ("source
   inspection").

PASS = both met; PARTIAL = paper numbers met, some records differ; FAIL = a printed number differs (in the rerun or in
the published file); NOT RUN = the step did not finish with exit code 0 (reason given).

**Independent recomputations** (new code by the developer, from the definitions in the report and case file — not
reruns of the original analysis code, which is part of the PegasusDMZ platform and not in this repository):

| Claim | Expected |
|---|---|
| F31 / F80 flatness (`flatness_standalone.py`) | English 364 / 1,000 (exact); Latin ten editions within 345–374; six editions within 167–182 |
| §2 letter range | every window within the printed 17–22 |
| F4 rare symbols in one column (`recompute_extra.py`) | p below 1 / 20,000 with the platform's period-scan statistic |
| F32 no order (`recompute_extra.py`) | every component p > 0.05; lag family near 0.91 |
| R29 (`recompute_extra.py`, new seeds) | at least 38 of 40 planted texts at p < 0.05 and the real message p > 0.05; 40 of 40 for PASS, otherwise PARTIAL |
| F66 (`run_f66.sh`, 20 reruns of the original unseeded script) | family-wise p > 0.05 in every rerun; the published 0.291 inside the rerun range |

**F68** (joint grille-and-table search has no power at this length): rerun of the original lab job
`20261012-230606-edb3` — same config file, and the engine `compound_engine.py` whose SHA-256 (`9b8fe0fb…`) equals the
last committed version (PegasusDMZ commit `0cd257a`, October 11, before the original run), with `grille_engine.py` and
`poly_engine.py` from that same commit (the lab's copies were refreshed on October 13, so the exact files present at
the original run were not preserved; `0cd257a` is the last committed version before it) — after the GPU suite, never
alongside it (its budgets are wall-clock seconds, so a shared GPU would bias it toward failure). Expected: 0 of 3
planted answers recovered at each budget (60, 300 and 1,200 s per phase). The engine is part of the PegasusDMZ
platform, not this repository, so outsiders cannot rerun this one.
