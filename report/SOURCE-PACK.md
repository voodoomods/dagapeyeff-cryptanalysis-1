# Source pack for the report body (generated from the case file — the ONLY source besides the files named at the end)

## F1 — fact · confirmed
Transcription: 395 digits = 78 five-digit groups + '92000'; identical in Wikipedia, Schmeh, Dunin and the Cipher Foundation, and in the 1974 Gale reprint's text.

Evidence: navigator 2026-10-10; book_snippets on the reprint

## F4 — fact · confirmed
With the 04 counted, the text is 196 pairs = 14x14. All 8 rare symbols (cells 71, 92, 93, 94 — 7 occurrences — and the 04) sit at positions 41, 55, 97, 111, 125, 139, 167, 195: column 14 of the 14x14 layout (p < 1/20,000 after scanning periods 2-20). Column 14's other 6 entries are ordinary cells (84, 62, 85, 64, 74, 83), including rows 1-2.

Evidence: grid_profile(width=14); first noted by Erik van Eykelen

## F27 — fact · retired
Procedure simulation confirms only reduced alphabet (r17) + 4x5 square + dummy every 14th symbol can reproduce all cipher clues (17 cells, coordinates intact, all rare in column 14). With 300 trials and seed=9999, joint probability = 0.017.

Evidence: simulate_procedures(ciphertext='dagapeyeff', families='square=4x5,reduction=r17,dummies=p14', trials=300, seed=9999) shows top family (r17/4x5/p14/after) joint=0.017. Comparable results with families='all' (seed=8888) show only 6/304 families reproduce all clues, all sharing r17/4x5/p14.

## O16 — open · confirmed
Procedure simulation: of 304 enciphering families, only reduced-alphabet + 4x5 square + a dummy every 14th symbol added as the last step ever reproduce all clues (17 cells, intact coordinates, every rare symbol in column 14); every other family tried scored 0 joint matches in 80 trials. Lead: column 14 is final-step padding; the message is in dagapeyeff:no-col14.

Evidence: simulate_procedures(families='all', trials=80, seed=0) run by the operator 2026-10-11; families limited to the simulator's list

## F31 — fact · confirmed
The 13 message columns (182 symbols, column 14 excluded) use exactly 13 distinct cells, and their counts (20,17,17,16,16,15,14,13,12,12,11,10,9) are statistically indistinguishable from UNIFORM (chi-square vs uniform p 0.73). Natural text is almost never this flat: in 2000 windows of 182 letters each, the top-13 letters were as flat in 1/2000 (English), 0/2000 (17-letter English, French, German, French-style Russian, numbers spelled out), 6/2000 (Latin) - and natural windows use 17-22 letters, not 13. Every rare cell (71 92 93 94 04) occurs ONLY in column 14; column 14 draws its 8 rare entries REFINED (operator): naturally made tables never reach this flatness either - many-to-one merges with rare letters scattered 0-5/1000, two letters per symbol (Porta A-M/N-Z, random pairs, keyword 2x13 tables) 0/1000 - but a DELIBERATELY frequency-balanced many-to-one table does (English 364/1000, Latin 368/1000, German 54, French 4). So the message is not natural text through a naturally made table; it is consistent with a frequency-balanced table, fractionation, a key stream, a numeric code, or no message.

Evidence: operator computation 2026-10-11 (scipy chisquare; windows from the en/en-r17/fr/de/ru-latfr/la/numbers streams)

## F32 — fact · confirmed
Beyond F31 the 13 message columns show NO structure in any view tested against 1500-5000 shuffles: rows do not differ (chi2 p 0.08), columns do not (0.30), top vs bottom half do not (0.10), left vs right do not (0.60); no lagged dependence at lags 1-26 in reading or column order (max mutual information, family-wise p 0.91); adjacent repeats and short gaps at or slightly above chance (no repeat-avoidance, so no sign of a human-invented sequence); row digits and column digits alone show nothing. Column 14 is the only structure in the text; the message itself is statistically indistinguishable fr

Evidence: operator assumption audit 2026-10-11 (permutation tests; flatness_tools.message + scipy/numpy)

## C9 — convention · confirmed
PRIOR ART (literature check 2026-10-11): F31/F32 were reached independently but are NOT new. Flatness noted qualitatively by Wikipedia and R. Matthews (c. 2003, read as unusual English). C. Hendrick, Zenodo 10.5281/zenodo.23241303, published 2026-10-08: proves the count bound for any one-to-one key with any transposition (479,051 English windows, closest needs 8 errors); planted-power searches with shuffled cells (columnar width 14, four-square with standard squares, coordinate shifts 2-14, homophonic, the book dummy rule, enciphering errors) all negative; a 98-language count screen puts LATIN

Evidence: Zenodo / OpenAlex records read 2026-10-11 by the operator

## C12 — convention · confirmed
PRIOR ART (novelty check 2026-10-14): a 2026 Zenodo report (10.5281/zenodo.22011904, code/data 10.5281/zenodo.21970477) already ran a Fleissner/turning-grille search on this cipher with a quadgram model, simulated annealing and null-baseline calibration - so F71 is a replication, not new; its abstract covers one-to-one substitution only, so polyphonic-table results (F73, F74, I47) are not covered as far as the abstract shows. Frame I47 as a unicity-distance measurement (von zur Gathen 2022, 10.3384/ecp188395).

Evidence: /workspace/research/cipher/dagapeyeff/literature/NOVELTY-CHECK-2026-10-14.md

## C13 — convention · confirmed
PRIOR ART / PRECEDENT (full-text check 2026-10-14): Hendrick 2026 already measured the one-to-one-key version of F74 - grille search with the key held fixed recovers 4/4 grilles with the true key, 1/4 with keys 77-82% right, 0/4 at 65-69% - and the key-given grille search (4/4) that F71 replicates. Cite Hendrick as the precedent for F74; ours is the polyphonic-table version. Neither Hendrick nor Gariazzo 2026 treats polyphonic tables, unicity distance or table identifiability, so F73 and I47 (+ the identifiability curve) are ours as far as checked.

Evidence: /workspace/research/cipher/dagapeyeff/literature/NOVELTY-CHECK-2026-10-14.md (full-text section); hendrick2026/paper; gariazzo2026/report.txt

## R26 — ruled_out · confirmed
Padding crib: no dictionary keyword square (148,398 squares: 30k words x fills rows/cols4/cols5 x rest alpha/after) makes the 13 message columns' cell counts fit English letter frequencies better than shuffled cell labels do - full English p 0.89, 17-letter p 0.79, 19-letter p 0.87, German p 0.88 - while planted ciphers put the true square at rank 1 in 100% of plants. Count-based, so it holds for ANY transposition of those 13 columns. French p 0.16 (not significant; English keywords only).

Evidence: padding_crib / null_crib.rank_squares run by the operator 2026-10-11 (nulls 100, plants 30-40, seeds 0-1)

## R29 — ruled_out · confirmed
A polyphonic table (each symbol = a group of letters, e.g. frequency-balanced) WITHOUT a transposition: planted English through balanced 13-symbol tables shows lag-1 mutual information beyond shuffles in 40/40 texts (p<0.01 in 39/40), the real 13 message columns show none (p 0.70). Any message must have its order scrambled (grille or transposition). Polyphonic decoding itself has power: with the true table a bigram Viterbi recovers 85-90% of letters; an annealed search from scratch reached 70% on CPU.

Evidence: operator test 2026-10-11 (poly_engine.balanced_table + lag-1 MI vs 400 shuffles; decode_with / anneal)

## R31 — ruled_out · confirmed
English written in the book's own sign system (ch, sh, th as single signs; g/j, f/v/y, s/z merged), with vowels kept or dropped as in shorthand, never gives the message's 13 flat symbols: 16-22 distinct signs in 182-sign windows, 0/400 flat (chi2 p>=0.5).

Evidence: operator test 2026-10-12 (wordfreq-sampled English, 400 windows per variant)

## F34 — fact · confirmed
The book mentions the grille: book_snippets(codesciphers0000daga) finds one passage referring to the grille cipher as the invention of Jerome Cardan (an anecdotal/historical context); no hits for turning grille, four square, two square, Playfair or stencil (full-text search, so absence is weak evidence). Hendrick 2026 (sec. Starting from no message): of five message systems, the order test leaves only NO MESSAGE or a system that destroys order as completely as a TURNING GRILLE (his test flags 19/20 keyed-square and 14-column messages, 3/20 grilles); van Eykelen's recipe = the cells dealt onto 

Evidence: book_snippets 2026-10-11 operator; Hendrick 2026 manuscript section nomessage

## F42 — fact · confirmed
The book (codesciphers0000daga, near p.123) describes a sign system in which signs are provided for ch, sh, th while g/j, f/vy and s/z have one sign for each pair - the author wrote about merged-letter (many-to-one) sign systems. Also p.115: the grille as Jerome Cardan's invention, historical only; no turning grille, four-square, two-square or Playfair found.

Evidence: book_snippets verified by operator 2026-10-12 (phrases: one sign, s and z, i and j); kahn R8 B/LEAD-7

## F64 — fact · proposed
When testing ALL statistics simultaneously (cells=13, flatness, IC, digraph IC), uniform13 (no message) and keystream13 outperform balanced13: uniform13 matches 75%, keystream13 58%, balanced13 only 33%.

Evidence: simulate_second_layer(layers=uniform13,keystream13,balanced13,trials=100) results: uniform13.all=0.75, keystream13.all=0.58, balanced13.all=0.33; simulate_second_layer documentation states 'all' = share of trials matching every statistic at once

## F66 — fact · confirmed
Hendrick's 30-order-statistic no-message test has been independently replicated: family-wise p=0.291 (Hendrick: 0.2814), smallest p=0.0120 for info lag 3 (Hendrick: 0.0138). The test correctly flags 19/20 keyed-square and 14-columnar messages but only 3/20 turning-grille plants, consistent with a grille destroying sufficient order to be indistinguishable from no message by these statistics.

Evidence: Hendrick 2026 (internal copy) section 'Starting from no message', family_p=0.2814, smallest_p=0.0138 (info lag 3). Our replication (friedman, 1000 dealings): family_p=0.2910, smallest_p=0.0120 for info lag 3. Replication passed. Power check on grille+polyphonic plants: 0/3 at all budgets.

## F67 — fact · confirmed
The 13 message columns show MORE non-random structure than expected for casually dealt symbols on every human-invention test tested: rows are more imbalanced, pair choices more concentrated, and consecutive repeats more frequent than shuffled controls (all at percentile 1.0). Casual 'random dealing by hand' is contradicted; if there is no message, the symbols were arranged by a deliberate procedure.

Evidence: batey human_patterns_simple.json and mercator.md: Row balance CV=0.755 (percentile 1.0 vs shuffles, MORE imbalanced than random), pair concentration HHI=0.0789 vs expected 0.0667 (percentile 1.0, MORE concentrated), consecutive repeats 10.4% vs 7.9% (percentile 1.0, MORE repeats). Uniform counts in message columns suggest systematic tallying, not random dealing.

## F68 — fact · confirmed
The gpu-grille-polyphonic engine (turning grille over polyphonic text, dummies in column 14) is UNTESTABLE at this length: even at 1200s per phase, 0 of 3 planted answers were recovered by the joint search (annealing grille orbits + polyphonic table simultaneously). A negative on the real text would mean nothing without a recovered plant.

Evidence: gpu-grille-poly power check job 20261012-230606-edb3: 0/3 plants recovered at budgets 60s, 300s, and 1200s (all failed). Lab log: 'UNTESTABLE AT THIS LENGTH - no budget tried recovers a planted answer reliably; a negative on the real text would mean nothing.'

## F71 — fact · confirmed
The grille search HAS POWER WITH THE KEY GIVEN: GPU benchmark 20261014-002920-eb8a recovers every planted 14x14 null-column grille exactly (49/49 orbits up to rotation, 100% of letters, 3/3), as do CPU runs (256 chains, 60-90s). Key unknown it does not (14-19/49 orbits, chance ~12). A grille turned a quarter is the same solution - judge plants up to rotation (grille_engine.match_up_to_rotation).

Evidence: /lab/cipher/grille/bench-2.json; operator CPU runs 2026-10-14

## F73 — fact · confirmed
With the polyphonic TABLE GIVEN, the turning-grille search is solved: scoring orders by group-symbol 6-grams (grille_engine.group_ngrams(text, table, n=6, base=13), English from a 7M-letter Gutenberg corpus, plants from a different source) recovers the grille on 6/6 plants (49/49 orbits up to rotation; 5-grams 6/6 at 48-49; 4-grams 2/6), and the true order is the top score, so the I46 identifiability failure is gone. The remaining unknown for the real cipher is the table.

Evidence: /lab/cipher/grille/bench-ngram.json (lab job 20261014-013414-0e0e, 80k steps x 512 chains, ~2 min GPU per run)

## F74 — fact · confirmed
The table-given grille search needs an essentially EXACT polyphonic table: with group 6-grams it recovers the grille on 4/4 plants with the true table, 1/4 with 2 letters misplaced, 2/4 with 4, and 0/12 with 6, 8 or 12 - a near-right table scores like a random one, so there is no gradient toward the table from the grille search alone.

Evidence: /lab/cipher/grille/bench-tolerance.json (lab job 20261014-023519-9bce, 4 plants x 6 levels, 80k steps x 512 chains, balance-preserving swaps)

## F75 — fact · confirmed
The book teaches no table that fits the lead hypothesis: every construction found (CLIQUE square with I/J merged, keyword + remaining alphabet with J omitted, MANCHESTR example) is a 5x5 square with ONE letter per cell, so a message on 13 cells would use only 13 letters - excluded by the counts (C9, F31); the merged-letter sign list is never flat (R31).

Evidence: 148 book_snippets results retrieved by kahn (task t-eacb4ddf), stored /workspace/.pegasus/kahn_snippets.json; pp.~120-123

## F76 — fact · confirmed
Under the turning-grille + balanced 13-group polyphonic hypothesis the table is NOT determined at the cipher length: with the symbol order known (grille solved), steepest-ascent search from the true table finds a different, higher-likelihood table in 178/200 practice ciphers at 182 symbols (89%; 100% when letters may also move between groups), and recovers the true table exactly in 11% - rising gradually to 27% at 273, 41% at 364, 57% at 455, 63% at 546, 75% at 728 and 84% at 1,092 symbols (two disjoint Gutenberg model corpora: 14/8% at 182, 94/74% at 1,092; same shape, level depends on the la

Evidence: /lab/cipher/round11/identifiability-A-big.json, identifiability-B-big.json (lab jobs 20261014-042944-11e7, -5d7d; 100 plants x 7 lengths per corpus, 6-gram group model, repair_table swaps-only) + identifiability-A/B.json (20 plants, 182-1456)

## I46 — inconclusive · confirmed
Grille + polyphonic table with the TABLE GIVEN: Viterbi-bigram scoring has no power (15-23/49 orbits, GPU job d99d); scoring the order by GROUP-SYMBOL quadgrams (grille_engine.group_quadgrams, English mapped through the table) solves some plants (48/49 at 80k steps x 512 chains) but not all - on another the found order scores ABOVE the true one (-4.009 vs -4.026): 4-symbol statistics over 13 groups are not always discriminating. Higher-order group n-grams are the next step.

Evidence: operator CPU runs 2026-10-14 (plants seeds 300, 302)

## I47 — inconclusive · confirmed
The table cannot be recovered from the cipher by likelihood under the grille + polyphonic hypothesis: with the grille ALREADY CORRECT (49/49) and only 2 letters wrong, steepest-ascent repair raised the 6-gram score (-5.74 to -5.44) while moving the table further from the truth (2 to 5 wrong; other plants 2 to 8, 4 to 9-10) - 182 symbols admit many tables that explain them better than the true one. Detection still works: a true lock scores about -5.4 to -5.7, shuffled ciphers and random tables about -6.1 to -6.2.

Evidence: /lab/cipher/round11/validate.json (lab job 20261014-032058-a3e9; grille_engine.repair_table, 2 plants)

## O23 — open · proposed
STATE-OF-THE-ART FRONTIER (Hendrick 2026, sec. Open): (1) 14x14 TURNING GRILLE - not closed; searches have no power without a nearly right letter key (0/4 with grille and key unknown); (2) KEYED FOUR-SQUARE / TWO-SQUARE - not excluded by counts; an all-squares search recovered 0/6 plants at 196 letters (no power); (3) a general LETTER-PAIR TABLE (e.g. 2x2 Hill over a keyed square) - not excluded; (4) width-14 transposition in languages other than English/Latin; (5) double transposition above width 6 (divide-and-conquer, Lasry 2014); (6) NO MESSAGE (van Eykelen tally-and-deal) - consistent with

Evidence: Hendrick 2026 manuscript (paper/dagapeyeff-exclusions.tex, numbers.tex) read 2026-10-11; operator merge tests (F31 refined)

## Figure 6 data (exact percentages, true table recovered exactly, grille order known)
{"A": [[182, 273, 364, 455, 546, 728, 1092], [14.0, 31.0, 46.0, 65.0, 72.0, 84.0, 94.0]], "B": [[182, 273, 364, 455, 546, 728, 1092], [8.0, 22.0, 36.0, 49.0, 54.0, 65.0, 74.0]], "combined": [11.0, 26.5, 41.0, 57.0, 63.0, 74.5, 84.0], "plants_per_corpus": [100, 100]}

## Novelty check (verbatim)
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
- Latin model, key held fixed: true key 4/4, keys 77–82 % right 1/4, 65–69 % right 0/4 — "the grille can be found only from a nearly right key"; key-only methods reach ~59 % → **F74 has a one-to-one-key analog in Hendrick; ours is the polyphonic-table version — cite Hendrick as the precedent.**
- "Homophonic keys" = many symbols to one letter (capped); no polyphonic (one symbol → several letters) tables; no unicity distance, no table identifiability. The turning grille is left open *because* the key can't be found.

**Gariazzo 2026** (`gariazzo2026/Report_Agapeyeff.pdf`, CC-BY-4.0, text in `report.txt`): families A–D incl. C Fleissner 14×14 (4 rotations), letters via a one-letter-per-cell Polybius square, shuffled-cell null; no polyphonic / homophonic tables, no unicity, no identifiability.

**Semantic Scholar / arXiv retry**: arXiv nothing on point; Semantic Scholar background only — "Cryptanalytic Properties of Short Substitution Ciphers" (1989), "A framework for the study of homophonic ciphers" (1993), "Revisiting the Unicity Distance through a Channel Transmission Perspective" (arXiv 2410.14816, 2024). One query ("polyphonic cipher cryptanalysis") still rate-limited; OpenAlex covered it.

## Attribution after the full-text check

| Finding | Status |
|---|---|
| F31 / F32 flatness, no order | PRIOR ART (Matthews; Hendrick) — ours replicate |
| F71 grille search, key given | PRIOR ART (Hendrick 4/4; Gariazzo) — replication |
| F74 exact-table requirement | **OURS for polyphonic tables**; one-to-one analog is Hendrick's (cite) |
| F73 grille recovered with a polyphonic table given (group 6-grams) | **OURS** — not in Hendrick, Gariazzo or any abstract found |
| I47 + identifiability curve (182 → 1,456 symbols) | **OURS** — the main contribution; frame as unicity distance (von zur Gathen 2022; Shannon) |
| R29 polyphonic without transposition excluded by lag-1 MI | **probably ours** — not in the two full texts |
| F75 the book teaches no fitting table | probably ours (narrow) |
