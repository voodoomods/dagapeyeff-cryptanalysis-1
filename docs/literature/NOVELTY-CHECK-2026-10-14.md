# Novelty check — 2026-10-14 (Nic via Claude)

Generic scholarly searches (OpenAlex; Semantic Scholar / arXiv calls failed — not reachable through the proxy today),
no case details sent. Raw results: `novelty-search-2026-10-14.json`. **Nothing was published.**

Queries: turning grille cryptanalysis · Fleissner grille hill climbing · homophonic substitution unicity distance ·
polyphonic substitution cipher cryptanalysis · D'Agapeyeff cipher (+ failed: Semantic Scholar / arXiv variants).

## Directly relevant prior work found

| DOI | Year | What it is | Bearing on our findings |
|---|---|---|---|
| 10.5281/zenodo.23241303 | 2026 | Hendrick — key-free count exclusions; open items incl. turning grille | Already in the case file (C9, O23). F31/F32 prior art. |
| 10.5281/zenodo.22011904 (+ data/code 10.5281/zenodo.21970477) | 2026 | "Anatomy, Reconstruction of a Solver, and Statistical Assessment" — families A substitution, B columnar, **C Fleissner grille**, D double transposition, four-square; quadgram LM + simulated annealing; **null-baseline calibration**; English / French / Hebrew | **F71 (grille search, key given) is at most a replication**; null-baseline method is prior art. Abstract shows one-to-one substitution only — **no polyphonic table** found → F73 / F74 / I47 not covered *as far as the abstract shows*. Full text NOT yet read. |
| 10.3384/ecp188395 | 2022 | von zur Gathen — unicity distance of the Zodiac-340 system (80–152) | The theoretical frame for **I47**: our result is a measured statement that 182 symbols lie below the unicity distance of grille + 13-group polyphonic table. Cite it. |
| 10.5281/zenodo.18639389 | 2026 | "Dual-Block Homophonic Columnar Transposition" — claims a military-order plaintext | A competing solution claim; homophonic + columnar (not grille). Our C9 / R-entries on columnar bear on it; not examined. |
| 10.5281/zenodo.20565170 | 2026 | Polybius (MANCHESTR) + 5-rail rail fence + periodic nulls — claims a partial plaintext ("now out too you") | Competing partial claim; not examined. |
| 10.1080/0161-117891852901 | 1978 | Barker, Cryptologia — "The unsolved d'Agapeyeff cipher" | Historical background. |
| 10.5281/zenodo.17991353 | 2025 | Hobbyist upload (author disclaims expertise) | Not relevant. |

## Revised attribution (supersedes the OURS table in FINDINGS.md until the full texts are read)

- **F71** grille search power, key given → REPLICATION / prior art (zenodo.22011904, family C).
- **F73** table-given grille search over a 13-group polyphonic table with group 6-grams → **probably ours** (not in any abstract found).
- **F74** exact-table requirement → **probably ours**.
- **I47** table not determined by 182 symbols → **probably ours as a measurement**; frame and cite as a unicity-distance result (von zur Gathen 2022). Being strengthened by the overnight identifiability study.
- **R29**, **F75** → not found in abstracts; unverified.

## Still to do before any claim of novelty
1. Read the full texts of zenodo.22011904 and zenodo.23241303 sections on grilles and homophonic/polyphonic tables.
2. Retry Semantic Scholar / arXiv for "unicity distance homophonic", "polyphonic cipher key recovery", "Fleissner grille".
3. Check Cryptologia / HistoCrypt proceedings (Linköping ECP) for polyphonic-cipher identifiability.

---

## Full-text check (later 2026-10-14)

**Hendrick 2026** (local copy `hendrick2026/paper/`, LaTeX + PDF, grep of the full text):
- Key-given 14×14 grille search: 4/4 planted grilles; key and grille both unknown 0/4 (≤ 18/49 holes after 8M steps); the cells were *not* searched with it → **F71 is prior art (Hendrick, and Gariazzo).**
- Latin model, key held fixed: true key 4/4, keys 77–82 % right 1/4, 65–69 % right 0/4 — "the grille can be found only from a nearly right key"; key-only methods reach ~59 % → **F74 has a one-to-one-key analogue in Hendrick; ours is the polyphonic-table version — cite Hendrick as the precedent.**
- "Homophonic keys" = many symbols to one letter (capped); no polyphonic (one symbol → several letters) tables; no unicity distance, no table identifiability. The turning grille is left open *because* the key can't be found.

**Gariazzo 2026** (`gariazzo2026/Report_Agapeyeff.pdf`, CC-BY-4.0, text in `report.txt`): families A–D incl. C Fleissner 14×14 (4 rotations), letters via a one-letter-per-cell Polybius square, shuffled-cell null; no polyphonic / homophonic tables, no unicity, no identifiability.

**Semantic Scholar / arXiv retry**: arXiv nothing on point; Semantic Scholar background only — "Cryptanalytic Properties of Short Substitution Ciphers" (1989), "A framework for the study of homophonic ciphers" (1993), "Revisiting the Unicity Distance through a Channel Transmission Perspective" (arXiv 2410.14816, 2024). One query ("polyphonic cipher cryptanalysis") still rate-limited; OpenAlex covered it.

## Attribution after the full-text check

| Finding | Status |
|---|---|
| F31 / F32 flatness, no order | PRIOR ART (Matthews; Hendrick) — ours replicate |
| F71 grille search, key given | PRIOR ART (Hendrick 4/4; Gariazzo) — replication |
| F74 exact-table requirement | **OURS for polyphonic tables**; one-to-one analogue is Hendrick's (cite) |
| F73 grille recovered with a polyphonic table given (group 6-grams) | **OURS** — not in Hendrick, Gariazzo or any abstract found |
| I47 + identifiability curve (182 → 1,456 symbols) | **OURS** — the main contribution; frame as unicity distance (von zur Gathen 2022; Shannon) |
| R29 polyphonic without transposition excluded by lag-1 MI | **probably ours** — not in the two full texts |
| F75 the book teaches no fitting table | probably ours (narrow) |
