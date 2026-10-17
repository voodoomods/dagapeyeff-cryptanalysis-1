## Appendix E. Robustness breakdown

Every setup and length of Section 6.5, from `lab/cipher/round12/ident-full.json` [F77]. Each row is 50 practice ciphers (plants 0–49). *Truth kept*: the search, started at the true table, ended there — no swap of two letters between groups raises the score, so the true table is a local maximum of that score. *Higher-scoring found*: the search moved to a different table with a higher score. Of those, *other corpus*: the table found also beats the true table under the other corpus's model on the same passage (setups with a disjoint second corpus only); *fresh passage*: it also beats the true table under the same model on a passage 3,000 letters further on, which played no part in the search. Intervals are 95% Wilson intervals. One run (Wells prose, A′ + B, chain-rule 3 before, 273 symbols) ended in a numerical tie and counts in neither column (§6.4). The result file also records how many letters the table found differs from the truth, using a greedy match of group labels; an exact assignment gives identical truth-kept and higher-scoring outcomes in all 2,000 runs and differs from the greedy count by one letter in 80 (internal audit, `lab/cipher/audit/label_full.json`). Those letter counts are not used in this report.

| Plaintext | Corpus (letters) | Score | Length | Truth kept | 95% CI | Higher-scoring found | other corpus | fresh passage |
|---|---|---|---|---|---|---|---|---|
| word sample | A′ (5 books, 1.95 M) | 6-symbol (as §6.4) | 182 | 13 of 50 (26%) | 16–40% | 37 | 23 of 37 | 1 of 37 |
| word sample | A′ (5 books, 1.95 M) | 6-symbol (as §6.4) | 273 | 21 of 50 (42%) | 29–56% | 29 | 11 of 29 | 2 of 29 |
| word sample | A′ (5 books, 1.95 M) | 6-symbol (as §6.4) | 364 | 22 of 50 (44%) | 31–58% | 28 | 9 of 28 | 2 of 28 |
| word sample | A′ (5 books, 1.95 M) | 6-symbol (as §6.4) | 546 | 28 of 50 (56%) | 42–69% | 22 | 13 of 22 | 5 of 22 |
| word sample | B (6 books, 4.67 M) | 6-symbol (as §6.4) | 182 | 10 of 50 (20%) | 11–33% | 40 | 33 of 40 | 8 of 40 |
| word sample | B (6 books, 4.67 M) | 6-symbol (as §6.4) | 273 | 13 of 50 (26%) | 16–40% | 37 | 27 of 37 | 10 of 37 |
| word sample | B (6 books, 4.67 M) | 6-symbol (as §6.4) | 364 | 19 of 50 (38%) | 26–52% | 31 | 23 of 31 | 7 of 31 |
| word sample | B (6 books, 4.67 M) | 6-symbol (as §6.4) | 546 | 30 of 50 (60%) | 46–72% | 20 | 14 of 20 | 2 of 20 |
| Wells prose | A′ (5 books, 1.95 M) | 6-symbol (as §6.4) | 182 | 9 of 50 (18%) | 10–31% | 41 | 29 of 41 | 7 of 41 |
| Wells prose | A′ (5 books, 1.95 M) | 6-symbol (as §6.4) | 273 | 14 of 50 (28%) | 17–42% | 36 | 28 of 36 | 7 of 36 |
| Wells prose | A′ (5 books, 1.95 M) | 6-symbol (as §6.4) | 364 | 14 of 50 (28%) | 17–42% | 36 | 24 of 36 | 7 of 36 |
| Wells prose | A′ (5 books, 1.95 M) | 6-symbol (as §6.4) | 546 | 25 of 50 (50%) | 37–63% | 25 | 15 of 25 | 7 of 25 |
| Wells prose | B (6 books, 4.67 M) | 6-symbol (as §6.4) | 182 | 6 of 50 (12%) | 6–24% | 44 | 32 of 44 | 6 of 44 |
| Wells prose | B (6 books, 4.67 M) | 6-symbol (as §6.4) | 273 | 13 of 50 (26%) | 16–40% | 37 | 28 of 37 | 12 of 37 |
| Wells prose | B (6 books, 4.67 M) | 6-symbol (as §6.4) | 364 | 14 of 50 (28%) | 17–42% | 36 | 27 of 36 | 10 of 36 |
| Wells prose | B (6 books, 4.67 M) | 6-symbol (as §6.4) | 546 | 22 of 50 (44%) | 31–58% | 28 | 23 of 28 | 5 of 28 |
| Wells prose | A′ (5 books, 1.95 M) | chain-rule, 5 before | 182 | 6 of 50 (12%) | 6–24% | 44 | 26 of 44 | 8 of 44 |
| Wells prose | A′ (5 books, 1.95 M) | chain-rule, 5 before | 273 | 12 of 50 (24%) | 14–37% | 38 | 20 of 38 | 7 of 38 |
| Wells prose | A′ (5 books, 1.95 M) | chain-rule, 5 before | 364 | 14 of 50 (28%) | 17–42% | 36 | 21 of 36 | 4 of 36 |
| Wells prose | A′ (5 books, 1.95 M) | chain-rule, 5 before | 546 | 15 of 50 (30%) | 19–44% | 35 | 21 of 35 | 11 of 35 |
| Wells prose | B (6 books, 4.67 M) | chain-rule, 5 before | 182 | 8 of 50 (16%) | 8–29% | 42 | 28 of 42 | 7 of 42 |
| Wells prose | B (6 books, 4.67 M) | chain-rule, 5 before | 273 | 14 of 50 (28%) | 17–42% | 36 | 23 of 36 | 11 of 36 |
| Wells prose | B (6 books, 4.67 M) | chain-rule, 5 before | 364 | 16 of 50 (32%) | 21–46% | 34 | 19 of 34 | 6 of 34 |
| Wells prose | B (6 books, 4.67 M) | chain-rule, 5 before | 546 | 25 of 50 (50%) | 37–63% | 25 | 15 of 25 | 5 of 25 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 3 before | 182 | 4 of 50 (8%) | 3–19% | 46 | — | 4 of 46 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 3 before | 273 | 5 of 50 (10%) | 4–21% | 44 | — | 9 of 44 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 3 before | 364 | 8 of 50 (16%) | 8–29% | 42 | — | 11 of 42 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 3 before | 546 | 15 of 50 (30%) | 19–44% | 35 | — | 7 of 35 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 4 before | 182 | 4 of 50 (8%) | 3–19% | 46 | — | 11 of 46 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 4 before | 273 | 7 of 50 (14%) | 7–26% | 43 | — | 10 of 43 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 4 before | 364 | 10 of 50 (20%) | 11–33% | 40 | — | 9 of 40 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 4 before | 546 | 14 of 50 (28%) | 17–42% | 36 | — | 3 of 36 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 5 before | 182 | 5 of 50 (10%) | 4–21% | 45 | — | 16 of 45 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 5 before | 273 | 17 of 50 (34%) | 22–48% | 33 | — | 8 of 33 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 5 before | 364 | 16 of 50 (32%) | 21–46% | 34 | — | 8 of 34 |
| Wells prose | A′ + B (6.62 M) | chain-rule, 5 before | 546 | 18 of 50 (36%) | 24–50% | 32 | — | 6 of 32 |
| Wells prose | A′ + B (6.62 M) | 6-symbol (as §6.4) | 182 | 8 of 50 (16%) | 8–29% | 42 | — | 14 of 42 |
| Wells prose | A′ + B (6.62 M) | 6-symbol (as §6.4) | 273 | 12 of 50 (24%) | 14–37% | 38 | — | 13 of 38 |
| Wells prose | A′ + B (6.62 M) | 6-symbol (as §6.4) | 364 | 14 of 50 (28%) | 17–42% | 36 | — | 10 of 36 |
| Wells prose | A′ + B (6.62 M) | 6-symbol (as §6.4) | 546 | 15 of 50 (30%) | 19–44% | 35 | — | 6 of 35 |

**Data splits.** The 13 corpus novels, sorted by file name, are split alternately: corpus A takes the 1st, 3rd, … (7 books), corpus B the 2nd, 4th, … (6 books); Section 6.4 uses A and B in full. For Section 6.5 the two Wells novels (*The Time Machine*, *The War of the Worlds*, both in A) are removed from every model and used only as plaintext (407,678 letters): A′ is A without them. The word sample is `lab/cipher/grille/plain_pool.txt`.

**True tables.** For each practice cipher the true table is the balanced table of the model's own corpus (letters packed into 13 groups by frequency, `poly_engine.balanced_table`), with its 13 labels shuffled by the plant's seed.

**Search and score.** Steepest ascent from the true table: every swap of two letters in different groups is scored, the best is taken, until none improves (at most 8 sweeps). The score is the mean log10 of the six-symbol pattern frequency over the passage (§6.4), or the mean log10 conditional probability of each symbol given the 3, 4 or 5 before it with add-one smoothing (chain-rule). A candidate table is scored by rebuilding the model from the corpus mapped through that table.

**Seeds.** Section 6.4: plant *p* uses `Random(9000 + p)` for its table labels and passage (the 20-plant runs `Random(7000 + p)`). Section 6.5: table labels `Random(12000 + p)`, passage start `Random(12500 + p)`, fresh passage 3,000 letters later. Four-square (§7): passage `Random(31000 + w)`, random-key controls `Random(55000 + w)`, order-test shuffles `Random(4242)`. GPU sums are not bit-for-bit deterministic, so individual runs can differ slightly on re-execution.
