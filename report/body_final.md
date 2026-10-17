## 2. The cipher

In 1939 Alexander D'Agapeyeff closed *Codes and Ciphers*, a popular introduction to cryptography, with a challenge
cipher printed without key or method. As transcribed in every standard source, it is 395 digits: 78 groups of five plus
a closing "92000" [F1]. Read as two-digit numbers, the first 392 digits give 196 symbols, and 196 is exactly 14 × 14.

Laid out 14 symbols to a row (Figure 1), the text shows its one clear structural feature. The eight occurrences of the
rare symbols (71, 92, 93, 94 and the single 04) all fall in the last column. To judge how unusual that is without
fixing the row length in advance, we scored every row length from 2 to 20 by the largest share of the eight in any
one column, less the share chance alone would put there (one in the number of columns), and kept the best score.
None of 20,000 random placements of eight symbols among the 196 positions scored as high as the cipher, so the odds
are below 1 in 20,000; counted exactly, the chance is at most about 2 in a billion [F4, F83]. Section 5 says what this
does and does not measure. The other thirteen columns, 182 symbols in all, use
exactly 13 distinct symbols, and those occur almost equally often: from 9 to 20 times each, statistically
indistinguishable from uniform (chi-square p = 0.73) [F31].

{{fig1}}

That flatness is the cipher's central puzzle (Figure 2). Ordinary text is never this even: in 2,000 English passages of
the same length, the thirteen commonest letters were this flat only once, and 182-letter passages of natural text use 18 to
25 different letters in English (median 22) and 14 to 25 in Latin (median 20), not 13 [F31, F81]. Nor does any table that people ordinarily make — letters merged at random, or two letters to a
symbol in a fixed pattern — produce it. What does reproduce it is a table built *on purpose* to balance the
frequencies, in which each symbol stands for a group of letters chosen so that every symbol occurs about equally often:
such tables match the cipher's flatness in about a third of trials for English (364 of 1,000). For Latin the rate
depends on which texts are sampled: 345 to 374 of 1,000 for the ten-edition Latin corpus used, about one in six (167
to 182) for its six editions without English notes [F31, F80]. The English and Latin sources are listed in Appendix F. (A second purpose-built construction, a four-square with a key designed around the message, can also
reproduce it; Section 7.) Beyond its flat counts the message carries no detectable order: rows, columns, halves and
symbol-to-symbol dependence all look like a random shuffle (family-wise p = 0.91) [F32].

{{fig2}}

## 3. Where the problem stood

The cipher has been discussed for decades. Wayne Barker described it for *Cryptologia* in 1978. Robert Matthews
noted its flatness around 2003, and Erik van Eykelen first observed that its rare symbols fill one column [F4, C9].

Two substantial studies appeared in 2026. **Hendrick** showed that no one-to-one letter key, with any transposition,
can produce the cipher's counts (the closest of 479,051 English passages needs 8 errors); that searches with measured
power for columnar transposition, four-square with standard squares, coordinate shifts, homophonic keys, the book's own
dummy rule and enciphering errors all come up empty; and that if a one-to-one key were used, the counts would point to
Latin rather than English [C9]. Hendrick tested the cipher against a "no message" recipe and found it consistent (family-wise
p = 0.28), with the caveat that the test barely detects a turning grille, and left the turning grille open: the search
recovers planted grilles when the letter key is known (4 of 4) but not when grille and key are both unknown (0 of 4),
and in Hendrick's tests under a Latin model it fails with keys only 65–69% right [C13, F34, O23]. **Gariazzo** rebuilt a solver scored by a statistical
(quadgram) model of English and searched four cipher families — including a 14 × 14 Fleissner (turning) grille over an ordinary
one-letter-per-cell square — with shuffled-cipher controls; none beat the controls [C12].

Two further 2026 preprints (doi:10.5281/zenodo.18639389 and doi:10.5281/zenodo.20565170) claim solutions, using a
homophonic columnar transposition and a rail-fence-with-nulls construction respectively. They are noted here for
completeness and have not been assessed.

## 4. The hypothesis

**What is observed.** Three properties of the ciphertext itself:

- All eight occurrences of the rare symbols fall in column 14 of the 14 × 14 layout (odds below 1 in 20,000 on the
  row-length scan of Section 2) [F4, F83].
- The other 182 symbols use exactly 13 distinct symbols, almost equally often (chi-square against uniform, p = 0.73)
  [F31].
- No test we applied finds order among those 182 symbols: rows, columns, halves and symbol-to-symbol dependence all
  look like a random shuffle (family-wise p = 0.91) [F32].

**What we infer, and how firmly.** Each inference below rests on simulations of particular cipher families, and holds
only for the families simulated:

- *The flatness points to a deliberate table.* In our simulations, a one-to-one key on English was this flat once in
  2,000 passages, and other ordinary tables — letters merged at random, letters paired in a fixed pattern, the book's
  own sign system — never; a table built on purpose to balance the frequencies was, in about a third of English trials
  and in one in six to one in three Latin trials depending on the texts sampled [F31, F80, F65, R31].
- *Such a table would need its order scrambled.* In the original 40 planted texts, a balanced table used without a
  transposition left detectable order (dependence between neighboring symbols beyond 400 shuffles, p < 0.05) in all
  40 [R29]. A separately written check within the project, with new seeds and differently drawn practice texts, found
  it in 39 of 40, so the exact count depends on the texts sampled; both show strong detectability under the tested
  conditions [F82]. The cipher's own message shows no such dependence (p = 0.70).
- *A turning grille is one system that scrambles order thoroughly enough.* Of the systems Hendrick's order test
  examined, only a turning grille hides order this well [F34]; systems that test did not examine are not covered.
- *Column 14 is padding.* A simulation of the enciphering procedure supports reading column 14 as dummies added at
  the last step, with the message in the other 182 symbols [O16].

D'Agapeyeff's book shows he knew both ingredients: it mentions the grille (as Cardano's invention) and describes a
sign system in which one sign serves for a pair of letters — g and j, f and v/y, s and z [F34, F42].

The hypothesis tested in depth in this report is therefore **a 14 × 14 turning grille over a balanced polyphonic
table**. It is one construction consistent with the observations, not the only one: a four-square whose key is built
on purpose around the message is also consistent with the frequency observations, and in some passages was not
flagged by our order test (Section 7) [O34], and so is a cipher with no message at
all [F66]. The message is written out in letters, each letter is replaced by the symbol of its group, the symbols are
placed through the holes of a square card turned a quarter at a time (Figure 3), and column 14 is filled with dummies.

{{fig3}}

A balanced table pools rare letters and leaves common ones alone, so that each of the 13 symbols occurs close to the
ideal 1/13 (7.7%) of the time. The table below was computed from two million letters of English with the same
balancing used in our experiments; it is an illustration, not the cipher's key:

| Symbol | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Letters | E | T | A | O | C·G·U | B·R | K·S | M·P·W | I | L·V·Y | H·Q·X | D·F·J·Z | N |
| Share | 12.2% | 9.1% | 8.2% | 7.8% | 7.3% | 7.1% | 7.1% | 7.0% | 7.0% | 7.0% | 6.8% | 6.7% | 6.7% |

E alone exceeds 1/13 and cannot be split, which is why even the best table is not perfectly flat. Reading such a
cipher means choosing, for every symbol, which letter of its group was meant — with the true table and the true order,
a standard decoding recovers 85–90% of the letters in practice ciphers [R29].

## 5. How we tested it

**Practice ciphers.** Every method was first run on ciphers we made ourselves in exactly the hypothesized form — a
14 × 14 grille, a balanced 13-symbol table, English text, dummies in column 14 — with the answer known. A method that
cannot recover a practice cipher at this length tells us nothing when it fails on the real one [F68]. The plaintexts
of the practice ciphers were drawn from a sample of English words weighted by frequency; because such text has no
grammar, the identifiability measurements were repeated on natural prose (Section 6.5). Unless a sentence says
otherwise, every success rate in Section 6 is a rate *in practice ciphers*, under the hypothesis; none is a statement
about the real cipher's grille or table, which remain unknown.

**Shuffled controls.** A search can always find *something*; the question is whether it finds more in the real cipher
than in the same symbols shuffled into random order. Our comparisons use the same search, with the same effort, on
shuffled copies.

**The column-14 odds.** The score of Section 2 rewards concentration *beyond chance*: with p columns, chance puts
about one in p of the occurrences in any given column, so all eight in one column scores 1 − 1/p — 0.93 at row length
14, but only 0.5 at row length 2. Only eight in one column at a row length of 14 or more reaches the cipher's score,
and the exact chance of that is at most about 2 in a billion; the published "below 1 in 20,000" is the floor that
20,000 random placements can show [F83]. A looser question — are all eight in one column at *some* row length from 2
to 20? — has a chance of about 0.7%, almost all of it from row length 2 (all eight in odd positions or all in even
ones). That is a different question, and it is not the source of the odds in Section 2. The scan allows for choosing
the row length; it does not allow for the choice to look at the rare symbols' columns in the first place, which was
made after the alignment had been noticed (by van Eykelen) [F4, C9]. The wider search for structure, corrected for
everything it examined, finds this one feature and no other [F16].

**Judging a grille.** A grille turned a quarter is the same grille, so a recovered grille was counted as correct if it
matched the true one in any of its four orientations [F71].

**Uncertainty.** Rates are given with 95% Wilson intervals where the sample is small enough for the interval to
matter. Results resting on fewer than ten practice ciphers per condition are preliminary demonstrations, not
general success rates.

**Recording claims.** Every finding was recorded in the project's case file with its evidence. A claim proposed by an
agent had to pass a programmatic claim gate — which refused claims that cited missing results, uncorrected p-values or statistics
that shuffling cannot change — and be confirmed by a designated reviewer. Results produced by the developer were
recorded directly, each with its evidence. Uncertain results are kept and labeled as such. A separate AI
system, ChatGPT (OpenAI), reviewed several drafts of this report at the author's request; the checks it prompted are in
Sections 6.5 and 7 and Appendix E, and its points on wording are taken up throughout. That is an AI review, not human
peer review, and the case file itself has not been independently reviewed (Section 8).
Section 10 describes the safeguards.

## 6. Results

### 6.1 With the true table supplied, practice-cipher grilles were recovered

If the polyphonic table is known, can the grille be found? Candidate grilles were scored by how English-like the
resulting stream of *group* symbols is, using counts of symbol patterns from a 7-million-letter English corpus — 13 Project Gutenberg
novels (Appendix F) — while the practice texts came from a different source, a sample of English words weighted by
frequency. A grille counts as recovered when at least 45 of its 49 orbits are
right, up to rotation. Scoring by six-symbol patterns recovered the grille on 6 of 6 practice ciphers (95% interval
61–100%): exactly — all 49 orbits — on 5, and with one orbit wrong on the sixth, where that near-miss scored slightly
above the true grille. Five-symbol patterns also recovered 6 of 6 (47 to 49 orbits right, exactly on 3); four-symbol
patterns, the usual choice in such searches, only 2 of 6 (10–70%) (Figure 4) [F78]. At five and six symbols the score
never preferred a grille with fewer than 45 orbits right. Each search takes about two minutes on a laptop GPU. With
six practice ciphers this is a demonstration that the method works, not a measured success rate.

In these practice ciphers, supplying the true table enabled successful grille recovery under five- and six-symbol
scoring. Whether this generalizes to other keys, plaintexts and constructions remains untested. For the real cipher,
the grille, the table and the construction itself all remain unconfirmed.

{{fig4}}

### 6.2 The table must be essentially exact

How close must the table be? The same search was given tables with some letters moved to the wrong group (keeping the
groups balanced), four practice ciphers per condition. With the true table it found 4 of 4 grilles (51–100%); with 2
letters misplaced, 1 of 4; with 4 misplaced, 2 of 4; with 6, 8 or 12 misplaced, none of 12 (0–24%) (Figure 5) [F74].
With four trials, the 2- and 4-letter results cannot be told apart (intervals 5–70% and 15–85%); the clear contrast is
between the true table and six or more misplaced letters. A table that is not nearly exact scores like a random one,
so in these trials there is no gradual path toward the correct table. Hendrick found the same cliff for one-to-one
keys [C13]; this result extends it, in a preliminary way, to polyphonic tables.

{{fig5}}

### 6.3 Neither the cipher nor the book supplies the table

A natural next step is to repair a nearly-right table using the cipher itself. On two practice ciphers whose grille
had already been recovered exactly, a search that changed the table to raise the score of the symbol stream moved the
table *further* from the truth — from 2 wrong letters to 5 [I47]. Section 6.4 measures this systematically.

Nor does the author's book help. Every table construction it describes or prints puts one letter in each cell of a
5 × 5 square. A message on 13 cells of such a square could use only 13 different letters, which the cipher's counts
already exclude [F75].

### 6.4 The truth-start test: how well 182 symbols pin down the table

The decisive measurement asks: *if the grille were already solved*, does the text single out the true table under
the score? For each of 100 practice ciphers per English model corpus (two corpora built from different books; here
the two Wells novels belong to corpus A — Appendix F lists each corpus), the
search is handed the true symbol order and **starts at the true table**. It then climbs by steepest ascent: every swap
of two letters between groups is scored with the six-symbol score of Section 6.1, the best swap is taken, and this
repeats until no swap raises the score. Two outcomes are possible:

- **Truth kept** — no swap raises the score, so the search ends at the true table: the true table is a local maximum
  of the score.
- **Higher-scoring table found** — the search moves away to a table that scores the text better.

In 3 of the more than 2,000 truth-start runs in this report the search moved to a table scoring higher by less than
one part in a million — a numerical tie, where the passage cannot tell the two tables apart. These count as the truth
*not* kept (and not as a higher-scoring table found); counting them as kept would change no figure by more than
2 points (corpus A at 364 symbols: 48% instead of 46%).

This is not blind recovery of an unknown key. The search is given both the true order and the true table, which is
the most favorable case possible; a search for grille and table starting from nothing did worse (0 of 3 practice
ciphers at every budget tried) [F68]. The table below and Figure 6 give how often the truth was kept [F76]:

| Text length (symbols) | 182 | 273 | 364 | 455 | 546 | 728 | 1,092 |
|---|---|---|---|---|---|---|---|
| Corpus A | 14% | 31% | 46% | 65% | 72% | 84% | 94% |
| Corpus B | 8% | 22% | 36% | 49% | 54% | 65% | 74% |
| Both | 11% | 26.5% | 41% | 57% | 63% | 74.5% | 84% |

At the cipher's own length the search found a higher-scoring table in 178 of 200 practice ciphers (89%; 95% interval
84–93%), and kept the truth in 22 (11%; 7–16%). When letters were also allowed to move between groups, it found a
higher-scoring table every time [F76]. The rate of keeping the truth rises steadily with length and passes one in two
at roughly 420 symbols — more than twice the cipher's 182.

What these numbers measure is narrow, and it matters. They are rates for this search and this score. A higher-scoring
table shows that the true table is *not optimal under the tested score*; it does not establish which table is more
probable under the true distribution of English. And because the search only looks at single swaps from the truth,
89% is a lower bound on how often a higher-scoring table exists under this score — not a measure of ambiguity in any
information-theoretic sense. Section 6.5 tests how much the numbers depend on the procedure.

{{fig6}}

### 6.5 Robustness checks after review

The first review by ChatGPT asked three questions of Section 6.4: whether the results depend on the practice plaintexts,
whether they depend on the language model and score, and whether the higher-scoring tables are genuine competing
explanations or artifacts of the model. We reran the truth-start test with 50 practice ciphers for each of ten
setups and four lengths (2,000 runs) [F77]:

- **Plaintext.** Natural prose — two novels by H. G. Wells, removed from every language model — instead of the
  word-frequency sample.
- **Corpus.** The two corpora of Section 6.4 (with the Wells novels taken out of corpus A) and both combined
  (6.6 million letters).
- **Score.** The six-symbol score used throughout, and a chain-rule score in which each symbol is predicted from the
  three, four or five before it.

| Truth kept | 182 symbols | 273 | 364 | 546 |
|---|---|---|---|---|
| Lowest of the ten setups | 8% | 10% | 16% | 28% |
| Highest of the ten setups | 26% | 42% | 44% | 60% |
| All 500 runs at each length | 15% | 26% | 29% | 41% |

Each setup's rate rests on 50 practice ciphers, so individual rates carry intervals of roughly ±10 points (for
example 8%: 3–19%; 26%: 16–40%); the pooled 15% at 182 symbols has 12–18%. Appendix E gives every setup and length
with its counts and interval, the data splits and the seeds.

No setup changes the conclusion. Natural prose did not make the truth easier to keep (12–18% at 182 symbols, against
20–26% for the word sample under the same models), and neither the combined corpus nor the chain-rule scores raised
it (8–16% on prose at 182 symbols, against 12–18% for the original score).

**What are the higher-scoring tables?** Each table found at 182 symbols was scored two more ways, and the procedure
matters for reading the result. The table was chosen by one search only: under one model, on one passage. It was then
scored, unchanged, (a) on the *same passage* under the model of the *other, disjoint corpus*, with the same kind of
score; and (b) on a *fresh passage* — 3,000 letters further on in the same source, enciphered with the same true table
— under the *same model*. The fresh passage played no part in the search, and neither passage is in any model's
corpus. Under the other corpus the table found still beat the true table in 69% of cases (171 of 248; 63–74%), so it
is not an artifact of one corpus's sparse counts. On the fresh passage it beat the true table in only 19% (82 of 427;
16–23%). The higher-scoring tables are therefore fitted to the particular 182 symbols — passage-specific overfitting —
rather than better descriptions of English. This explains the result of Section 6.4; it does not by itself establish
non-identifiability in an information-theoretic sense.

**Are scores comparable across tables?** A later review by ChatGPT asked whether these comparisons are fair. Each candidate table
is scored with a language model *rebuilt for that table*: the corpus is mapped through the candidate and its group
patterns are counted. That is the right quantity in principle — it estimates how probable the symbol stream is if that
table was used — but it could still favor some tables for reasons unrelated to the text, through the floor given to
unseen patterns, smoothing, or the sizes of the groups. We checked three things [F79]:

- **Normalization.** The six-symbol model, with its floor for unseen patterns, does not sum to one (2.10 for
  corpus A′, 1.45 for corpus B), but its total varies by only 0.002 in log10 across the true table and its 305
  single-swap neighbors.
- **Consistency.** Under a sufficiently accurate model of the true symbol distribution, the true table should
  outperform competing neighbors on sufficiently long held-out text. Our finite-sample tests assess whether that
  expectation holds for the models and neighbors examined here. On Wells prose held out of every model, no tested
  neighbor outscored the true table at 10,000 or 100,000 symbols — 0 of 9,150 comparisons over two corpora, three
  scores (six-symbol, six-symbol renormalized to sum to one, chain-rule) and five different true tables — against 1–3%
  of neighbors at 182 symbols and at most 1 in 1,525 at 1,092.
- **Renormalized rerun.** The truth-start test on prose with the renormalized six-symbol score kept the truth in
  exactly the same practice ciphers as the original score (200 of 200 runs: 9 and 6 of 50 at 182 symbols, 25 and 22
  of 50 at 546).

These checks support the interpretation that the higher-scoring alternatives arise primarily from short-passage
effects rather than the tested normalization procedure. They do not exclude every possible model or scoring bias.

## 7. What it means

Shannon defined the *unicity distance* of a cipher system as the length of ciphertext beyond which only one key is
expected to give a meaningful reading; below it, several keys fit equally well. Von zur Gathen (2022) estimated it at
80–152 symbols for the Zodiac-340 cipher, and argued that this supports the accepted solution. Shannon's quantity is
defined by the true probabilities of the language. Ours is an empirical measurement under n-gram scores, the practical
analog for the grille-plus-polyphonic system: in practice ciphers of the cipher's length, with the grille already
solved, the true table was not the best under the score in three or more cases out of four, under every model and
score we tested [F76, F77].

The hypothesis is therefore neither confirmed nor refuted by these methods: with them, the cipher is **too short to
be decided from its own text**. A proposed solution of this kind would be one choice among several tables that score
as well or better, and these scores could not show that it is D'Agapeyeff's. A much better model of the language
might narrow the field; none we tried did. Two kinds of evidence would change the picture: the table itself, from a
source outside the ciphertext (a notebook, a letter, a worked example), or a longer text enciphered the same way — on
our measurements at least twice as long, and under some of the models we tried three times or more.

**Is it a question of computing time?** Several searches, in this study and in earlier work, are recorded as
having "no power" within a time budget — for the joint grille-and-table search, 1,200 seconds per phase [F68]. It is
natural to read that as a shortage of computing power. What we can say is narrower:

- **Grille and table together.** The objective in every search here is an n-gram score of the symbol stream; the
  searches are simulated annealing over grille and table together (F68) and steepest ascent over table swaps
  (Section 6.4). For the tested scoring objectives, higher-scoring incorrect tables frequently exist even when the
  true symbol order and table are supplied — in 89% of practice ciphers [F76], and in 74% to 92% under every model and
  score of Section 6.5 [F77]. Consequently, additional optimization of the same objective cannot be assumed to improve
  true-table recovery. We have not established how success rates change with longer search budgets; the joint search
  found none of 3 practice grilles at every budget tried [F68], but that is not a budget study. A differently designed
  search or objective is not ruled out.
- **Any other transposition under a polyphonic table** (columnar, double): the same — the curve of Section 6.4
  assumes the order is already known, and the true table is still usually not the best under the score.
- **Columnar or double transposition with an ordinary one-to-one key**: excluded by the symbol counts whatever the
  transposition [C9], and columnar was in any case searched with demonstrated power [R21, R27].
- **Four-square and two-square with random keys**: the randomly keyed constructions tested did not reproduce the
  observed 13-symbol usage in 10,000 practice ciphers [R35]. That excludes those sampled constructions under the tested
  plaintext (the English word sample), not every possible key or plaintext. In these systems each cipher
  symbol is set by the row of one plaintext letter and the column of another, so English spreads over nearly every
  symbol: 22 to 25 distinct symbols in 182 with 5 × 5 squares (20 to 25 even when the message is restricted to its 13
  commonest letters) and 18 to 20 with 4 × 5 squares — none used 13 or fewer. The cipher's message uses exactly
  13.

**A second construction that fits.** The four-square exclusion holds only for keys chosen at random. An encipherer who
knows the message can arrange the plaintext squares so that its frequent letters share a few rows and columns. A
hill-climb doing exactly that — which, like the encipherer, uses the plaintext — reached 13 symbols in 13 of 100
passages of 182 letters (95% interval 8–21%) and 14 or 15 in most of the rest; all 13 were as flat as the cipher's
counts (chi-square p from 0.85 to 1.0, against the cipher's 0.73). We then applied an order test — three
mutual-information statistics (between the two symbols of each pair, in both phases, and the largest at lags 1 to
26), each against 2,000 shuffles of the same symbols, with a family-wise min-p correction, at the 5% level.
Purpose-built keys were flagged less often than random keys: 12 of 100 (7–20%) against 52 of 100 (42–62%). Of the 13
passages that match the cipher's usage and flatness, 3 were flagged (passages 34, 77 and 95), leaving 10 of 100 that
match the usage and flatness and were not flagged; the real message is not flagged (family-wise p = 0.999) [O34].
Not being flagged is not evidence that no order is present: the test examines three statistics only, and on the
uncorrected pair statistics 7 of the 13 show dependence at p < 0.05.

This is a feasibility result. It shows that an intentionally constructed four-square *can* reproduce the cipher's
13 symbols and its flatness (13 of 100 passages) and, in 10 of 100, also go undetected by the order test we applied —
the same kinds of observation that led to the grille hypothesis.
It does not show that D'Agapeyeff used a four-square. The construction has not been searched: an ordinary
four-square search cannot climb to the key [R32], and a key built this way has a structure that a new search would
have to exploit. In our judgment — not a measured probability — it is the most promising lead this study leaves open.

The alternative that the cipher carries no message remains open, as Hendrick concluded and our replication of Hendrick's
order test confirms (family-wise p = 0.29; 0.25 to 0.59 across 20 reruns of the same test) [F66].

## 8. Limitations

**Sample sizes.** The truth-start curve rests on 100 practice ciphers per corpus at each length and the checks of
Section 6.5 on 50 per setup and length; the purpose-built four-square result on 100 passages. The grille-recovery and
table-error results rest on 6 and 4 practice ciphers per condition, and the repair experiment of Section 6.3 on 2
[F78, F74, I47]: they are preliminary demonstrations, with the wide intervals given in Section 6. The truth-start
result (Sections 6.4 and 6.5) is the best supported.

**Language model.** Only English was tested. The two corpora agree on the shape of the curve but differ in level
(14% against 8% at 182 symbols; 94% against 74% at 1,092), so the exact figures depend on the model. The checks of
Section 6.5 — natural prose, a combined corpus, chain-rule scores — kept the truth at 182 symbols in 8% to 26% of
practice ciphers, but they are all n-gram models; a stronger model of English (for example a neural one) was not
tried.

**Plaintext.** The practice messages were drawn from a frequency-weighted sample of English words and, in Section
6.5, from held-out literary prose (two novels by H. G. Wells); the language models were built from novels. The results
have not been tested on telegram-style messages, abbreviations, unusual vocabulary, deliberate misspellings or other
kinds of plaintext that may be relevant to the historical cipher, and recovery and identifiability rates may differ
for them. This does not affect the robustness findings of Section 6.5, which hold for the plaintexts tested.

**Search method and what it measures.** The truth-start search climbs from the true table to any higher-scoring
neighbor. Finding a higher-scoring table shows that the true table is not optimal under the tested scoring function;
it does not establish which table is more probable under the true language distribution. Failing to find one does
not show that the true table is the global best under the score. The 89% is therefore an empirical lower bound on
how often a higher-scoring alternative exists under this score and procedure, and the rates of keeping the truth are
rates for this procedure — neither is a probability that the table is identifiable by every possible method.

**Review.** The results have been checked within the project — against their evidence, by the claim gate, by
fact-checking every number in this report, by reproducing the budget from the raw records, and by rerunning the
headline experiments from a fresh copy of the repository (Section 10). ChatGPT (OpenAI) reviewed several drafts at the author's
request, which led to Section 6.5, Appendix E, the four-square finding and more careful wording; that is an AI review,
not human peer review or replication. Most case-file entries were
recorded and confirmed by the same hand (the developer, or Turing for the team's results). Replication outside the
project, which the repository is built to make easy, is the natural next step.

**Score comparability.** Section 6.5 provides empirical evidence that the scores are comparable across tables and consistent as the text grows,
for the n-gram scores used; it does not cover other kinds of model.

**Assumptions.** The experiments assume a 14 × 14 turning grille, column 14 as dummies, exactly 13 balanced groups and
English. A different layout, an unbalanced table or another language is not covered. The purpose-built four-square
test (Section 7) used one simple hill-climb and 5 × 5 squares, and judged order by three dependence statistics.

## 9. What is new and what is not

| Finding | Status |
|---|---|
| The counts are flat; the message has no detectable order (F31, F32) | Prior art — Matthews c. 2003; Hendrick 2026. Replicated here with quantified rates. |
| No one-to-one key with any transposition fits the counts (C9) | Prior art — Hendrick 2026. |
| A turning grille is recovered in practice ciphers when the letter key is known (F71) | Prior art — Hendrick 2026; Gariazzo 2026. Replicated. |
| The grille needs a nearly exact one-to-one key | Prior art — Hendrick 2026. |
| With the true **polyphonic** table supplied, six-symbol scoring recovered at least 45 of 49 grille orbits in six of six practice ciphers, five exactly (F78) | **New** as far as checked; a preliminary demonstration (95% interval 61–100%), not recovery of the historical grille. |
| A polyphonic table must be essentially exact (F74) | **New** for polyphonic tables, preliminary (4 practice ciphers per condition); extends Hendrick's result. |
| Under the n-gram scores tested, 182 symbols rarely single out the true polyphonic table, even with the grille known; measured curve to 1,092 symbols, robust across plaintexts, corpora and scores; the higher-scoring tables are fitted to the passage; scores comparable across tables (F76, F77, F79) | **New** as far as checked — the main contribution. |
| A polyphonic table without transposition is excluded, under the tested conditions (R29) | Probably new; not found in the works checked. |
| The book teaches no table that fits the hypothesis (F75) | Probably new; narrow. |
| Four-square and two-square with random keys excluded by symbol usage (R35) | Probably new — not in Hendrick or Gariazzo; not checked against the wider literature. |
| A purpose-built four-square can reproduce the cipher's symbol usage and flatness (13 of 100 passages; 10 of 100 also not flagged by the tested order statistic) (O34) | **New** as far as checked — a feasibility result and an open lead. |

"As far as checked" means not found in Hendrick (2026) or Gariazzo (2026), read in full, nor in the abstracts returned
by searches of OpenAlex, Semantic Scholar and arXiv on October 14, 2026. These novelty assessments are provisional:
they rest on the literature examined for this report and do not establish priority over unpublished work, historical
investigations or literature the search did not find. Specialist review may identify earlier equivalent methods or
results.
