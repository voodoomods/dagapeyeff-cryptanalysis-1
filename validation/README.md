# Release-candidate validation (October 16, 2026)

Full-size reruns of the published experiments, from a fresh clone of the release candidate (GitHub commit
`44f7b233d76744e98b5ed164d4144a93f6f0cd0d`), with criteria fixed in advance (`CRITERIA.md`). Results are in
`docs/validation-2026-10-16/`: `REVIEW-RESPONSE.md` (the request-by-request matrix and the readiness statement),
`validation-results.json` (commands, exit codes, elapsed times, SHA-256 of every output), `compare.json`, the logs
and the QA report.

This is a rerun by the project's developer, in containers with no network. It is not replication by an unaffiliated
party.

| File | What it does | Needs |
|---|---|---|
| `run_all.sh` | Every published experiment at full size, the published scripts and seeds; logs each step's command, output, exit code and seconds | the repository's `lab/` (working copy) at `/lab`, a log directory at `/val`; GPU for `gpu` mode |
| `compare.py` | Checks each rerun against its published file (record by record) and recomputes every number the report prints. Exit status 1 on any unexpected FAIL; a predeclared check of a claim since corrected is kept, marked `superseded_by`, and its FAIL is expected (October 17 version: `docs/validation-2026-10-17/compare.json`) | Python 3.9+ |
| `CRITERIA.md` | The pass / fail rules, written before the reruns finished | — |
| `flatness_standalone.py` | F31 / F80 flatness and the letter-count range, without the PegasusDMZ platform; same counts as the platform tool | `wordfreq==3.1.1`, `scipy`; the ten Latin editions for `--lang la` (`lab/cipher/lm/CORPUS.md`) |
| `recompute_extra.py` | New code for F4 (rare symbols in one column), F32 (no order) and R29 (a polyphonic table leaves order) | `numpy`; R29 imports `lab/cipher/grille/poly_engine.py` |
| `collect_results.py` | Gathers the run into `docs/validation-2026-10-16/` and writes `validation-results.json` (commands, exit codes, seconds, SHA-256 of every file) | Python 3.9+ |
| `qa_checks.py` | Publication-integrity checks on a built release: manifest, labels, attribution, peer-review wording, dates, spelling, DOI and license notes, case codes | Python 3.9+, `pypdf` |
| `f4_events.py` | F4's statistic and the looser "all in one column at any row length" event, side by side: exact counts and 1,000,000 placements (October 17) | `numpy` |
| `original/f4_original.py` | The October 11 F4 computation, recovered from the session record and unchanged (reads `data/ciphertext.txt`): 0 of 20,000 placements | standard library |
| `original/r29_original.py` | The October 11 R29 computation, recovered from the session record and unchanged: 40 / 40 | PegasusDMZ agent code at commit `c908608` (not in this repository) |
| `run_f66.sh`, `f66/hendrick_familywise.py` | Reruns the team's unmodified, unseeded replication of Hendrick's no-message test (F66) N times, writing elsewhere | `numpy` |

```
sh validation/run_all.sh cpu        # inside the container described in the README, then gpu
python validation/compare.py --ref lab/cipher --new work/lab/cipher --steps val/logs \
    --extra val/recompute_extra.json --f66 val/F66/reps --flatness val/flatness --out compare.json
python validation/flatness_standalone.py --lang en            # 364/1000 as flat (balanced table)
python validation/flatness_standalone.py --lang la --latin-dir PATH --seed 0
python validation/recompute_extra.py val/recompute_extra.json
sh validation/run_f66.sh val/F66/reps 20
```

F68 (the joint grille-and-table search) was rerun from the original lab job's configuration with the platform's
engine; that engine is not in this repository, so it is reported but cannot be rerun from here.

**Reading the unit tests.** `lab/cipher/lib/test_label_distance.py` prints "pass" after every test function that
returns, including `test_e`, which only prints "skip …" and returns when the two Christie novels are missing. Without
the full 13-novel corpus, count `test_e` as skipped, not passed. The file is left unchanged because its fingerprint
is cited.
