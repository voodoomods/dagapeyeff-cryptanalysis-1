# D'Agapeyeff Cipher — Findings

*Compiled by TURING, Chief Cryptanalyst, 2026-10-14. Source: the D'Agapeyeff case file only. Citations by entry id.*

---

## 1. Summary

The D'Agapeyeff cipher (1939, *Codes and Ciphers*) is 395 digits = 196 coordinate pairs from a 4×5 Polybius grid using 17 of 20 cells. Column 14 of the 14×14 layout contains every rare symbol (F4, p ≈ 0.0005) and the remaining 13 message columns use exactly 13 cells with counts indistinguishable from uniform (F31, χ² p = 0.73). No order structure survives in the message columns beyond chance (F32). We reached the frontier Hendrick 2026 had already described — a turning grille over polyphonic text with column-14 dummies, the procedure that reproduces every clue (O16, F27) — and went one step further: we found that the table needed by the grille search (F71, F73, F74) is unrecoverable from 182 symbols under its own hypothesis (I47), and that the book teaches no table that fits (F75). The grille search *with* the correct key and table works perfectly; without the table it is untestable. The Hendrick 2026 manuscript reached the same frontier independently and is the principal prior art (C9, O23).

## 2. What Is Established

### Flatness and absence of order structure

**F31** — The 13 message columns (182 symbols, column 14 excluded) use exactly 13 distinct cells. Their counts (20, 17, 17, 16, 16, 15, 14, 13, 12, 12, 11, 10, 9) are indistinguishable from uniform (χ² vs uniform p = 0.73). Natural text is almost never this flat: English, 17-letter English, French, German, and numbers-spelled-out windows match in ≤ 1/2000 cases; Latin reaches 24/2000. Only deliberately frequency-balanced many-to-one tables (English 364/1000, Latin 368/1000), fractionation, a running key, a numeric code, or no message produce counts this flat (F31).

**F32** — Beyond the column-14 anomaly, the 13 message columns show no structure against 1500–5000 shuffles: rows, columns, top/bottom, and left/right halves are ordinary; lagged mutual information at lags 1–26 in reading and column order yields family-wise p = 0.91; adjacent repeats are at or slightly above chance. Column 14 is the only detectable structure in the text.

### The count bound and what it excludes

**C9 (PRIOR ART)** — The flatness and the count bound have prior literature. Flatness was noted qualitatively by Robert Matthews (c. 2003). C. Hendrick, Zenodo [10.5281/zenodo.23241303](https://doi.org/10.5281/zenodo.23241303), published 2026-10-08, proved the count bound: 479,051 English windows, the closest needing 8 errors, exclude *any* one-to-one letter key with *any* transposition. Hendrick's planted-power searches including columnar width 14, four-square with standard squares, coordinate shifts 2–14, homophonic, the book's dummy rule, and enciphering errors were all negative. A 98-language count screen flagged Latin as closest but still excluded. Hendrick's open items are in O23.

**R26** — Reinforcing C9: no dictionary keyword square (148,398 squares: 30k words × fills) makes the 13 message columns' cell counts fit English letter frequencies better than shuffled cell labels (p = 0.89 full English, p = 0.79 17-letter English, p = 0.87 German, p = 0.88 Latin; French p = 0.16 not significant). Hold for *any* transposition — purely count-based.

### Polyphonic table without transposition excluded

**R29** — A polyphonic table (each symbol = a group of letters) without a transposition is ruled out: planted English through balanced 13-symbol tables shows lag-1 mutual information beyond shuffles in 40/40 texts (p < 0.01 in 39/40); the real 13 message columns show none (p = 0.70). Any message must have its order scrambled. Polyphonic decoding has power — when the table is known, Viterbi recovers 85–90% of letters; from scratch, annealing reaches 70% on CPU.

### The grille search: what works and what doesn't

**F71** — The grille search HAS POWER WITH THE KEY GIVEN: the GPU benchmark recovers every planted 14×14 null-column grille exactly (49/49 orbits up to rotation, 100% of letters, 3/3 plants). Key unknown, it does not (14–19/49 orbits, chance ≈ 12).

**F73** — With the polyphonic TABLE GIVEN, the turning-grille search is solved: scoring orders by group-symbol 6-grams recovers the grille on 6/6 plants (49/49 orbits up to rotation; 5-grams 6/6 at 48–49). The true order is always top score, so identifiability is no longer an issue *when the table is known*.

**F74** — The table-given grille search needs an essentially EXACT polyphonic table: it recovers the grille on 4/4 plants with the true table, 1/4 with 2 letters misplaced, 2/4 with 4 wrong, and 0/12 with 6, 8, or 12 wrong. A near-right table scores like a random one — there is no gradient toward the table from the grille search alone.

### Identifiability limit

**I47** — The table cannot be recovered from the cipher by likelihood under the grille+polyphonic hypothesis. With the grille ALREADY CORRECT (49/49) and only 2 letters wrong, steepest-ascent repair raised the 6-gram score while moving the table *further* from the truth (2 → 5 wrong; other plant 4 → 9–10 wrong). 182 symbols admit many tables that explain them better than the true one. Detection still has some signal: true-lock scores ≈ −5.4 to −5.7 (mean log₁₀ per 6-gram), shuffled ciphers and random tables ≈ −6.1 to −6.2.

### The book's tables

**F75** — The book teaches no table that fits the lead hypothesis. Every construction found (CLIQUE square with I/J merged, keyword + remaining alphabet with J omitted, MANCHESTR example) is a 5×5 square with ONE letter per cell → a message on 13 cells would use only 13 distinct letters, excluded by the counts (C9, F31). The merged-letter sign list (g/j, f/vy, s/z; ch/sh/th separate) is never flat (R31).

### Other engines

- **Gpu-grille-polyphonic** (grille + polyphonic table joint search): UNTESTABLE at this length — 0/3 plants recovered at budgets up to 1200s per phase (F68/I44).
- **Four-square / Two-square**: closed — scoring basin too shallow; ~12 random swaps from truth, annealing cannot climb (R32/F50).
- **Columnar width 14 + substitution, 04 kept** (aligned 14×14 grid): plant recovered, real below null; margin −0.0148 at 885 s/phase GPU (R27/R24).
- **Columnar widths 13–14 + substitution on :no-col14**: plants recovered, real at or below null (R21/R22/R23).
- **Double transposition**: UNTESTABLE — 0/3 plants at 1200s GPU (R20/I28).

## 3. Attribution of Findings

### PRIOR ART (published before us)

| Entry | Topic | Prior |
|-------|-------|-------|
| F4 | Rare symbols cluster in column 14 | Erik van Eykelen (first noted) |
| C9 | Flatness, count bound, extensive exclusions | C. Hendrick 2026, Zenodo; R. Matthews c. 2003 re flatness |
| O23 | Turning grille, keyed four-square, no-message as open frontier | Hendrick 2026 |
| F34 | Book mentions grille historically; Hendrick's no-message test | Book is primary; Hendrick's test reported by Hendrick |
| F66 | Replication of Hendrick's 30-order-statistic test | Hendrick 2026 |
| F1/F23 | Transcription | Wikipedia, Schmeh, Dunin, Gale reprint — identical |
| F31/F32 | Flatness and absence of order structure | Matthews c. 2003 (qualitative), Hendrick 2026 (counts, order tests) — our quantitative versions replicate and extend (C9) |

### REPLICATION (we reproduced a published result)

| Entry | Topic | Reproduction |
|-------|-------|---------------|
| F66 | Hendrick's 30-order-statistic no-message test (family p ≈ 0.29) | Confirmed independently (F61/F59) |
| R31 | Book's merged-letter sign system excluded for 13 flat symbols | Independent implementation against published system |

### OURS (not found in the literature we checked)

| Entry | Topic |
|-------|-------|
| R29 | Polyphonic table without transposition excluded by lag-1 MI |
| F71 | Grille search power with key given (49/49 orbits, 100% letters, 3/3 plants) |
| F73 | Table-given grille search solved with group 6-grams |
| F74 | Exact-table requirement: 0/12 plants recovered with ≥ 6 letters wrong |
| I47 | Table unrecoverable from 182 symbols under grille+polyphonic hypothesis |
| F75 | Book teaches no table fitting the lead hypothesis |
| F67 | Human-invention tests contradict casual dealing — symbols MORE patterned than random |
| R26 | Padding crib: 148k squares, no dictionary square fits counts |
| F65 | Only deliberately balanced tables match flatness; all historical/natural constructions fail |

*Note: where the literature search was incomplete for a specific finding, it carries no attribution label in the text above. The "ours" label means we did not find it in Hendrick 2026, Matthews, the Wikipedia article, or published D'Agapeyeff literature available to us — a more exhaustive search was not part of this compilation's scope.*

## 4. Methods and Their Power

| Method | Task | Plants | Budget | Recovery | Verdict |
|--------|------|--------|--------|----------|---------|
| Grille key-given (GPU, quadgrams) | 14×14 null-col grille | 3 | 60–90 s | 49/49 orbits, 100% letters | HAS POWER (F71) |
| Grille key-unknown (GPU, quadgrams) | Same | 3 | 60–90 s | 14–19/49 orbits (chance ~12) | NO POWER (F71) |
| Grille + table given (GPU, 6-grams) | Grille orbits over polyphonic | 6 | ~2 min GPU | 49/49 orbits all 6 | SOLVED (F73) |
| Grille + table given (GPU, 4-grams) | Same | 6 | ~2 min GPU | 49/49 on 2/6 only | INADEQUATE (F73) |
| Table tolerance (6-grams) | Exactness needed | 4 × 6 levels | ~2 min GPU | 4/4 true, 1/4 (2 wrong), 0/12 (≥6) | NEEDS EXACT TABLE (F74) |
| Table repair (grille correct) | Steepest-ascent from near-truth | 2 | — | Moves AWAY from truth (−5.74 → −5.44 but 2 → 5 wrong) | UNRECOVERABLE (I47) |
| Grille+poly joint (Gpu-grille-poly) | Both unknown | 3 | 60/300/1200 s | 0/3 at all budgets | UNTESTABLE (F68) |
| Columnar w14 + sub, 04 kept | GPU, 2048 chains | 3+ | 885 s/phase | 100% recovered, real below null | RULED OUT (R27) |
| Padding crib | 148k squares | 30–40 | ~seconds | True square rank 1 in all | RULED OUT (R26) |

**Caveats**: All grille and table recovery results rest on 3–6 plants (6-gram and tolerance tests on 4–6). The table repair result (I47) rests on 2 plants — treat as preliminary direction, not a closure-by-itself.

## 5. Open Questions

1. **The table, from an outside source.** The cipher needs an essentially exact 13-group polyphonic table (F74); it cannot be recovered from the ciphertext under the grille hypothesis (I47); the book teaches no table that fits (F75). If there *is* a message, the author must have had the table from somewhere not in the book — or the procedure is not grille+polyphonic.

2. **No message.** The no-message hypothesis (uniform13, van Eykelen tally-and-deal) matches 74–77% of cipher statistics (F64, F38). Hendrick's 30-statistic test yields family p ≈ 0.29 — not an exclusion (F66). Against no message: the symbols are MORE patterned than random dealing produces (F67), suggesting deliberate procedure even if message-free.

3. **Running key (keystream13).** Matches 68% of cipher statistics, second only to uniform13 (O29). No periodic or repeated-key trace found (keystream_test negative). Untested: a power check against English plaintext through a running-key over 13 symbol classes.

4. **Hendrick's other open items:** keyed four-square/two-square (closed by basin failure R32 unless a new move operator is devised); letter-pair tables; width-14 transposition in untried languages; double transposition above width 6; and no message (listed above, O23). The turning grille remains open in principle but closed in practice at current power levels — without the table, searches are untestable (F68).

**To settle the table question** — evidence from outside the cipher: a notebook, a published table of letter groups, or any 1930s source D'Agapeyeff could have known that defines exactly 13 frequency-balanced symbol-to-letters groups.

**To settle the no-message question** — a strong positive test (all 30 Hendrick statistics together at p < 0.01) on either direction would be decisive; our replication gives p ≈ 0.29, Hendrick's gives p ≈ 0.28 — both inconclusive.

**To settle the running-key question** — a power check (can a planted keystream13 message be recovered at this length?) would say whether the hypothesis is even testable.

---

*Developer's corrections (Nic via Claude, 2026-10-14), checked against the case file: the summary no longer claims we were "first" (Hendrick 2026 reached this frontier earlier — C9, O23); F31/F32 moved from OURS to PRIOR ART per C9; F71 is 3/3 plants (6/6 is F73); detection scores are mean log₁₀ per 6-gram, not bits. "OURS" means not found in the sources checked (Hendrick 2026, Matthews, Wikipedia, the D'Agapeyeff literature on hand) — no systematic literature search has been done yet.*
