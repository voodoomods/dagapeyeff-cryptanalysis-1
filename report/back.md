## 10. How this research was done

This is an AI-assisted study, and the method is disclosed in full so that readers can weigh it.

**The author.** Nicolas Houghtaling (ORCID 0009-0001-3192-544X) conceived the study and directed it throughout, and is responsible for its
conclusions. The author chose the D'Agapeyeff cipher and the question of whether it can be solved; designed and owns the
PegasusDMZ research platform the work ran on, built with AI assistance; and made the decisions that shaped the
research — insisting the team keep a record of established facts so that nothing was rediscovered (the origin of the
case file), asking for an independent check of the team's first round, pressing for methods that had not been tried
and for the weaknesses others had overlooked (the question that led to the flatness result of Section 2), approving
the literature review that set this study alongside the work of others on the cipher — above all Hendrick's and
Gariazzo's — aiming the final phase at the key itself (which led to
the results of Section 6), stopping work that was not productive, and requiring that every claim be checked against
the literature and stored with its evidence before anything is published, and, when AI reviews of the draft (ChatGPT) questioned the strength of its claims, holding publication until the checks they suggested had been run and the
headline experiments had been reproduced from a fresh copy of the repository. Section 11.3 lists these decisions with
their dates.

**The research platform.** The work ran on *PegasusDMZ*, a self-hosted platform built by the author. It hosts a team of
AI agents (language models given specialist roles such as statistician, historian and cryptanalyst) whose internet
access passes through a governed proxy; Section 11.2 introduces each of them. The agents ran on DeepSeek, Kimi and Qwen models through DeepInfra. Software
engineering, the search engines, the benchmark design and the final verification were done by Anthropic's Claude
(Opus 5.5) working with the author as developer.

**Safeguards against fooling ourselves.** Language-model agents make confident mistakes, and several did during this
work (an invented number in a consultation, a wrong statistic, a mislabeled claim of novelty). The platform therefore
enforces: a *case file* in which every claim is recorded with its evidence, and an agent's claim stands only once a
designated reviewer confirms it; a
*claim gate* that refuses claims citing missing results, uncorrected p-values or failed controls; known-answer
*practice ciphers* for every method before it touches the real cipher; *shuffled-cipher controls*; and a linked record
in which a disputed claim automatically flags every claim that rests on it. The figures in this report are drawn
directly from the result files, not retyped.

**Review of the drafts.** At the author's request, drafts of this report were reviewed by ChatGPT (OpenAI), an AI system
separate from both the developer and the agent team, over several rounds. Its reviews prompted the robustness checks of
Section 6.5, the score-comparability check, Appendix E, the internal audit and many narrower claims. Each suggestion was
checked against the evidence before it was adopted, and a few were not adopted where the project's records did not
support them. This is an AI review, not human peer review, and no one outside the project has yet replicated the
results.

**Cost.** About US$68 of language-model usage for the agent team, a Claude subscription for the developer work, a
ChatGPT Plus subscription for the ChatGPT reviews of the drafts, and a laptop GPU. Section 11 gives the full accounting.

**Code and data.** Every engine, experiment script, result file and figure behind this report is in the accompanying
repository `dagapeyeff-cryptanalysis-1` (<https://github.com/voodoomods/dagapeyeff-cryptanalysis-1>), laid out so the scripts run unchanged; Appendix C lists them with their fingerprints.

**Internal reproduction.** Before publication the headline experiments were rerun from a fresh copy of the repository,
following its README exactly — including rebuilding the language-model text, which reproduced its published
fingerprint — inside a container with no network access, on the same laptop. Every rerun matched the published
result run for run: the grille benchmark of Section 6.1 (18 of 18 runs), the truth-start test of Section 6.4 (the
first 20 practice ciphers per corpus at 182 and 546 symbols, 80 of 80), the robustness checks of Section 6.5 (the
first 10 practice ciphers of every setup at 182 and 546 symbols, 200 of 200), the purpose-built four-square search
(the first 30 passages, 30 of 30) and the order test of Section 7 (identical summary). Beyond the outcomes, every
regenerated record is identical to the published one in every field — scores included — except its elapsed time; the
order-test file is byte-for-byte identical, and the other files' SHA-256 fingerprints differ only because they record
run times. The scripts and the comparison are in `lab/cipher/round12/repro/`. This is an *internal reproduction*: it
shows the repository reproduces its own results on the same hardware; it is not independent external replication. On October 16–17 every published experiment was then rerun at full size
from a fresh clone of the release candidate, again with no network: of 4,959 published records compared, 4,956 are
identical apart from elapsed time (the other 3 are search controls bounded by wall-clock time), and every number
printed in this report was recomputed from the reruns; the record, with the one correction it led to (F81), is in
`docs/validation-2026-10-16/`. Separately, Proof — the team's replication reviewer, running on DeepSeek-V4-Pro — recomputed
about 120 numbers in Sections 1, 6, 7 and Appendix E from the result files without seeing the developer's working.
Its final verdict: every number matches the result files, apart from two rounded values (now shown exactly) and the
overstated grille result also found while preparing the reproduction (corrected by F78). A first pass had also
flagged two counts; they traced to an unstated convention — three runs in all ended in a numerical tie, which the
report counts as the truth *not* kept — and the convention is now stated (Section 6.4). A follow-up internal audit — run within
the project by the developer, with checking code written separately from the experiment code, and not a replication
by an unaffiliated researcher — rebuilt all 100 four-square passages and their flatness tests, repeated the order test
with fresh shuffles, re-derived the n-gram score, reran ten truth-start cases with its own search, and regenerated all
2,000 robustness runs to compare the greedy label matching recorded in `ident-full.json` with an exact assignment.
Everything matched the published records; greedy and exact matching differ by one letter in 80 of the 2,000 runs,
which changes no truth-kept or higher-scoring outcome and no figure in this report.
It found one reporting issue — the four-square summary had merged the frequency result (13 of 100) with the order
result (10 of 100 not flagged) — now separated (O34). The audit's scripts and outputs are in `lab/cipher/audit/`, its report in
`docs/audit-2026-10-15/`. The audit and that adjudication are in `report/AUDIT-proof.md`.

**Copyright and licensing.** © 2026 VoodooMods LLC. The author, Nicolas Houghtaling, carried out this work at VoodooMods LLC, which holds the
copyright to the extent it owns the applicable rights. The report, its figures and the accompanying research materials
are released under the Creative Commons Attribution 4.0 International License (CC BY 4.0), and the source code under
the Apache License 2.0. Copyright is asserted only in material eligible for protection under applicable law;
third-party materials keep their own rights and licenses, as set out in the repository's LICENSE and NOTICE files. In
particular, the files derived from the wordfreq word-frequency data are shared under CC BY-SA 4.0 rather than CC BY 4.0,
and the Project Gutenberg texts are public-domain works that this license does not cover.

**Cite as.** Houghtaling, N. (ORCID 0009-0001-3192-544X) (2026). *The D'Agapeyeff Cipher (1939): grille recovery and polyphonic-table identifiability under n-gram scoring.* VoodooMods LLC. doi:10.5281/zenodo.23306263


## 11. Budget, models and timeline

### 11.1 What it took

Every agent model call passes through the platform's proxy, which records the tokens and prices each call; the
developer's usage comes from its session records. Figures cover the D'Agapeyeff study from October 8 to a snapshot taken on October 14, 2026; `evidence/accounting-2026-10-14.json` in the
repository holds the aggregates and `tools/accounting.py` recomputes them from the raw records.

| Resource | Calls / jobs | Input tokens | of which from cache | Output tokens | Cost |
|---|---|---|---|---|---|
| AI agent team (DeepInfra), on D'Agapeyeff tasks | 10,570 calls | 422.6 M | 390.5 M (92%) | 3.68 M | US$67.35 |
| Planning chat with the chief-of-staff agent | 30 calls | 0.58 M | 0.48 M (82%) | 0.01 M | US$0.16 |
| Developer: Claude Opus 5.5 (Claude Code) | 1,234 calls | 607.5 M | 599.2 M (99%) | 1.52 M | Claude Pro subscription — no per-token charge |
| Draft review: ChatGPT (OpenAI) | not recorded | — | — | — | ChatGPT Plus subscription — no per-token charge |
| Lab computer (laptop, NVIDIA RTX 5060) | 89 jobs (54 on the GPU) | — | — | — | 72 GPU-hours, 27.5 CPU-job hours; no charge |

Most input tokens are re-sent context served from the providers' prompt caches, which is why the agents' 423 million
input tokens cost about US$67. The developer's figure is the whole working session over the study and includes some work on
the research platform itself done during it. The study built on tools first written for the team's earlier cipher work
(an Enigma message and the Beale ciphers, from October 7), which is not counted here. The checks of October 15
(Sections 6.5 and 7) are not in the table either: they used no agent model calls and six lab jobs, about 3 GPU-hours
and 0.7 CPU-job hours, plus about one GPU-hour for the reproduction run described in Section 10. The
second review's numbers audit by Proof, the team's replication reviewer, used a small number of agent model calls
(Section 10).

**Agent spend by model** (D'Agapeyeff tasks; each agent is introduced in Section 11.2):

| Model | Role | Calls | Cost |
|---|---|---|---|
| DeepSeek-V3.2 | the cipher specialists (Friedman, Welchman, Rejewski, Kahn, Kasiski, Painvin, Ventris and others) | 8,608 | US$48.99 |
| DeepSeek-V4-Pro | review board (Fisher, Skeptic), chief of staff; the cipher room from October 14 | 1,287 | US$9.93 |
| Kimi-K2.6 | Turing, chief cryptanalyst (to October 14) | 616 | US$8.20 |
| Qwen3-235B-A22B | fallback when another model was busy | 59 | US$0.23 |

By day (UTC): Oct 9 US$1.43 · Oct 10 US$1.99 · Oct 11 US$39.83 · Oct 12 US$11.36 · Oct 13 US$7.84 · Oct 14 US$4.90.

### 11.2 The team

The agents are AI models (language models given a role, instructions and tools), **not people**. Most are named in
tribute to figures from the history of codebreaking, statistics and scholarship; the names describe the role, and
nothing in this report should be read as the work or opinion of the historical person, or as implying any
association with or endorsement by them or their estates. Each ran on the model shown, at
the cost shown (D'Agapeyeff tasks only).

::: {.team}
**Turing** — Chief cryptanalyst: plans the attack, divides the work, judges results
:   Kimi-K2.6 (DeepSeek-V4-Pro from Oct 14) · 593 calls · US$8.32 · named after Alan Turing, Bletchley Park

    Led every round and split it into parallel angles; reviewed and recorded the team's findings (F65, F66, F68, R27, R32); drafted the body of this report

**Friedman** — Statistical cryptanalyst
:   DeepSeek-V3.2 · 1,195 calls · US$7.31 · named after William F. Friedman, US Army cryptanalyst

    Statistics angles: what process gives 13 heavy and a few rare cells, what column 14 is, the book's dummy rules; replicated Hendrick's no-message test (F66)

**Welchman** — Search engineer: turns attacks into fast code, estimates run time first
:   DeepSeek-V3.2 · 1,089 calls · US$6.60 · named after Gordon Welchman, Bletchley Park

    GPU searches: coordinate seriation, double transposition, the book's transposition passes

**Rejewski** — Mathematical cryptanalyst: structure and key space
:   DeepSeek-V3.2 · 1,038 calls · US$6.40 · named after Marian Rejewski, who first broke Enigma

    Repeats, isomorphs and layouts; implemented the book's method; cataloged historical tables (F65)

**Kahn** — Historian: context, provenance, the author's methods
:   DeepSeek-V3.2 (V4-Pro on Oct 14) · 1,085 calls · US$5.20 · named after David Kahn, historian of cryptology

    Reconstructed the book's methods from searches of its text; found its merged-letter sign system (F42); its retrieved passages settled F75

**Kasiski** — Pattern analyst: structure nobody asked about, corrected for everything looked at
:   DeepSeek-V3.2 · 955 calls · US$5.08 · named after Friedrich Kasiski, 1863 method for repeated-key ciphers

    Pattern sweeps of the raw text (F16); what column 14 holds (F28)

**Painvin** — Compound-cipher specialist
:   DeepSeek-V3.2 · 740 calls · US$4.21 · named after Georges Painvin, who broke the ADFGVX cipher

    Layered attacks: two-block models, alternating alphabets, the 14 × 14 grid on the GPU

**Ventris** — Decipherment linguist
:   DeepSeek-V3.2 · 726 calls · US$4.08 · named after Michael Ventris, who deciphered Linear B

    Was the plaintext English at all (other languages, R28); readability scans of results; second-layer simulations (F65)

**Batey** — Error analyst: transcription and enciphering slips
:   DeepSeek-V3.2 · 483 calls · US$3.28 · named after Mavis Batey, Bletchley Park

    Compared published transcriptions; searched for single slips; built no-message models

**Navigator** — Researcher: outside sources through the governed proxy
:   DeepSeek-V3.2 · 515 calls · US$2.43

    Sourced and checked the exact transcription (F1); searched the 1939 book on the Internet Archive; found the 2026 preprints

**Knox** — Puzzle setter: thinks from the cipher author's side
:   DeepSeek-V3.2 · 331 calls · US$2.11 · named after Dilly Knox, Bletchley Park

    What D'Agapeyeff meant readers to do; keyword phrases from the book (F29)

**Mercator** — Author specialist: the author's life, books and map-making habits
:   DeepSeek-V3.2 · 252 calls · US$1.69 · named after Gerardus Mercator, cartographer

    Turned D'Agapeyeff's other books and map-grid habits into testable keywords

**Fisher** — Review board: statistics referee
:   DeepSeek-V4-Pro · 353 calls · US$3.09 · named after Ronald A. Fisher, statistician

    Refereed the statistics of round 4

**Skeptic** — Review board: red team, tries to break claims
:   DeepSeek-V4-Pro · 234 calls · US$1.98

    Red-teamed round 4

**Chief of staff** — The platform's main assistant: the author's point of contact
:   DeepSeek-V4-Pro · 512 calls · US$3.47

    Planning with the author; follow-up tests (e.g. the book's methods, decoding with given tables)

:::

Ten other teammates made occasional calls on these tasks (US$2.09 together). The **developer** is not an agent of the
platform: it is Anthropic's Claude (Opus 5.5), working with the author in Claude Code (Section 10).

### 11.3 Contributions

**Nicolas Houghtaling** (author): conceptualization, research direction and supervision, the research platform and
compute, decisions on scope, method and publication, and review of the report.

**Claude Opus 5.5** (developer): software and search engines, benchmarks and analyses, figures, and the writing and
editing of this report under the author's direction.

**OpenAI's ChatGPT** (draft reviewer, through ChatGPT Plus): critical review of the drafts at the author's request —
the questions behind the robustness checks, the score-comparability check, Appendix E, the internal audit and many
narrower claims. It did not run experiments or write the report; each suggestion was checked against the evidence
before it was adopted.

**The agent team**: supporting investigation, replications, exclusions and literature, as below.

Every finding in the case file records who entered it and who confirmed it. The new results of this report were
produced by the developer — Claude Opus 5.5 — writing the search engines and running the benchmarks on the lab GPU; the
agent team's work supplied replications, exclusions and the literature behind them.

| Finding | Produced by | Model |
|---|---|---|
| The research questions behind the flatness result ("what weakness have others overlooked") and behind the final phase ("aim it at the key"); the case file of established facts | Author — Nicolas Houghtaling | — |
| Grille recovered with a polyphonic table given (F73, corrected in F78); exact-table requirement (F74); identifiability curve (F76); table not recoverable (I47) | Developer — engines and GPU benchmarks | Claude Opus 5.5 |
| The decision to test the review's points before publishing | Author — Nicolas Houghtaling | — |
| Robustness checks (F77); random-key four-square excluded (R35); purpose-built four-square matches the symbol usage and flatness (O34) | Developer — checks prompted by the ChatGPT reviews | Claude Opus 5.5 |
| Flatness (F31), no order (F32), polyphonic tables need a transposition (R29), procedure simulation (O16), the book's tables (F75, from Kahn's book searches), novelty checks (C9, C12, C13) | Developer — analyses and literature checks | Claude Opus 5.5 |
| Natural tables are never this flat (F65) | Rejewski and Ventris; recorded by Turing | DeepSeek-V3.2 (Turing: Kimi-K2.6) |
| Replication of Hendrick's no-message test (F66) | Friedman; recorded by Turing | DeepSeek-V3.2 |
| Joint grille-and-table search has no power (F68); columnar + substitution excluded (R27); four-square basin too flat (R32) | The cipher team's GPU runs; recorded by Turing | DeepSeek-V3.2 / Kimi-K2.6 |

The agents also caught and corrected each other — and were corrected — through the review process described in
Section 10; several of their errors are recorded in the fact-check log in the repository.

### 11.4 Timeline

Dates are the author's local dates. Evidence: the case file, the round briefings, the lab job records and the platform's
version history.

| Day | What happened |
|---|---|
| **Thu&nbsp;Oct&nbsp;8** | **The author chooses the D'Agapeyeff cipher** and directs the team to attack it from several angles; the transcription is sourced and checked. |
| **Fri&nbsp;Oct&nbsp;9** | Round 1: the agent team's first attempts. |
| **Sat&nbsp;Oct&nbsp;10** | **At the author's request**, a review of round 1 by the developer (Claude), separate from the agent team, finds methodological errors (the book's example square assumed as the key; shuffles of raw digits used as controls). New tools with built-in shuffled controls and known-answer self-checks; rounds 2–4. The author also asks that the team keep its established facts — the case file follows. |
| **Sun&nbsp;Oct&nbsp;11** | The heaviest day (about 6,000 agent calls, US$40). The case file is created and the transcription confirmed; at the author's request a pattern specialist (Kasiski) joins; column 14 holds every rare symbol; columnar and substitution families excluded on the GPU; the author presses for untried methods and overlooked weaknesses, and the flatness (F31) and missing order (F32) follow; the author approves the literature check, which finds Hendrick's paper of October 8; polyphonic tables shown to need a transposition (R29); the turning-grille engine and polyphonic decoder are built. Rounds 5–8. |
| **Mon&nbsp;Oct&nbsp;12** | Round 9. The book's own merged-letter sign system is found and excluded (F42, R31); the joint grille-and-table search is shown to have no power at this length (F68). |
| **Tue&nbsp;Oct&nbsp;13** | Team results recorded: natural tables never this flat (F65), Hendrick's no-message test replicated (F66), four-square basin (R32). Then **the author aims the final phase at the key**; grille recovered with the key given (F71); the author stops an unproductive agent round and refocuses the work on the table; six-symbol scoring recovers the grille with the table given (F73); the exact-table requirement (F74); the book's tables (F75); table repair fails on practice ciphers (I47); the author asks whether the results are unpublished — full-text novelty check against Hendrick and Gariazzo (C12, C13) — and orders the evidence preserved; the identifiability study starts overnight on the GPU. |
| **Wed&nbsp;Oct&nbsp;14** | The identifiability curve completes (F76). The author commissions this report and the repository; both are drafted, fact-checked and assembled. |
| **Thu&nbsp;Oct&nbsp;15** | A review of the draft by ChatGPT (OpenAI), requested by the author, questions the strength of three claims. **The author holds publication** and has all four suggested checks run: natural prose, other corpora and scores, the nature of the higher-scoring tables (F77), and purpose-built four-square keys with an order test (R35, O34). A second review of a later draft asks for narrower wording, intervals, the full robustness breakdown (Appendix E) and a reproducibility audit; the headline experiments are rerun from a fresh copy of the repository. A third review asks whether scores are comparable across tables; the check passes (F79). An internal audit separates the four-square frequency and order counts (O34). |

## Acknowledgements

This study stands on the work of everyone who has taken the D'Agapeyeff challenge seriously. We thank Wayne Barker,
whose 1978 *Cryptologia* article set out the problem; Robert Matthews, who noticed the flatness of the counts; Erik van
Eykelen, who first saw that the rare symbols fill one column and proposed a construction with no message; Chase
Hendrick, whose 2026 paper turned decades of conjecture into measured exclusions and a clear list of what remained
open; Ruben Gariazzo, whose 2026 report and released code showed how carefully a solver must be checked against
chance; the transcribers and archivists who preserved the cipher and D'Agapeyeff's book; Project Gutenberg and its volunteers, whose
editions of the novels and Latin texts listed in Appendix F made the language models possible; and Robyn Speer's
wordfreq, whose English data draws on SUBTLEX (freely available word lists by Marc Brysbaert and colleagues), Google
Books Ngrams (http://books.google.com/ngrams), OpenSubtitles and other sources. We also credit ChatGPT (OpenAI), which reviewed our drafts at the author's
request and whose questions led to Section 6.5, Appendix E, the four-square finding of Section 7, the internal audit
and more careful claims throughout. Where
this report goes further, it does so on their foundations.

## References

- Barker, W. G. (1978). The unsolved D'Agapeyeff cipher. *Cryptologia*. doi:10.1080/0161-117891852901
- D'Agapeyeff, A. (1939). *Codes and Ciphers*. Oxford University Press.
- Gariazzo, R. (2026). *The D'Agapeyeff Cryptogram (1939): Anatomy, Reconstruction of a Solver, and Statistical
  Assessment*. Zenodo. doi:10.5281/zenodo.22011904 (data and code: doi:10.5281/zenodo.21970477)
- Hendrick, C. (2026). *Excluding Classical Cipher Families for the 1939 D'Agapeyeff Challenge: Key-Free Counts and
  Searches with Demonstrated Power*. Zenodo. doi:10.5281/zenodo.23241303
- Brysbaert, M. & New, B. (2009). Moving beyond Kucera and Francis: A critical evaluation of current word frequency
  norms and the introduction of a new and improved word frequency measure for American English. *Behavior Research
  Methods* 41(4), 977–990. (SUBTLEX-US, part of wordfreq's English data.)
- Matthews, R. (c. 2003). Remarks on the flatness of the D'Agapeyeff cipher, as cited by Hendrick (2026).
- Project Gutenberg (1994–2026). Plain-text editions retrieved October 11, 2026 from https://www.gutenberg.org — English
  eBooks 35, 36, 98, 108, 834, 863, 974, 1155, 1400, 1661, 1695, 2600 (tr. Louise and Aylmer Maude) and 2852; Latin
  eBooks 218, 226, 227, 23306, 25861, 28233, 33311, 33849, 39355 and 47001. Authors, titles, editors and the version
  of each are listed in Appendix F.
- Shannon, C. E. (1949). Communication theory of secrecy systems. *Bell System Technical Journal* 28(4).
- Speer, R. (2022). *rspeer/wordfreq: v3.0* (v3.0.2). Zenodo. doi:10.5281/zenodo.7199437 (package version 3.1.1 used;
  code Apache-2.0, data CC BY-SA 4.0).
- van Heuven, W. J., Mandera, P., Keuleers, E. & Brysbaert, M. (2014). SUBTLEX-UK: A new and improved word
  frequency database for British English. *The Quarterly Journal of Experimental Psychology* 67(6), 1176–1190.
  doi:10.1080/17470218.2013.850521 (part of wordfreq's English data.)
- von zur Gathen, J. (2022). Unicity distance of the Zodiac-340 cipher. *HistoCrypt 2022*, Linköping Electronic
  Conference Proceedings. doi:10.3384/ecp188395
- Solution claims noted but not assessed: doi:10.5281/zenodo.18639389; doi:10.5281/zenodo.20565170.

## Glossary

| Term | Meaning |
|---|---|
| **Cell / symbol** | One of the two-digit numbers in the cipher, read as a row digit (6–9, and once 0) and a column digit (1–5) of a coordinate grid. |
| **Polyphonic table** | A key in which one symbol stands for *several* letters (the reverse of a homophonic key, where one letter has several symbols). |
| **Turning grille** | A square card with holes. The message is written through the holes, the card turned a quarter, and so on four times; the filled grid is then read row by row. |
| **Orbit** | A set of four cells that a turning grille cycles through as it turns; a valid grille has exactly one hole in each orbit. |
| **Practice cipher (plant)** | A cipher we made ourselves with a known key, used to measure whether a method can find the answer. |
| **Shuffled control** | The same search run on the cipher's symbols in random order, to see what "finding something" looks like by chance. |
| **n-gram score** | How likely a text is, judged by how often each run of *n* consecutive symbols occurs in a large sample of English. |
| **Chain-rule score** | A likelihood that predicts each symbol from the few before it and multiplies those predictions, as opposed to scoring each run of symbols on its own. |
| **Identifiable** | The data single out one key as the best-scoring under a given model and score; when not identifiable in this sense, wrong keys score the text as well or better. |
| **Unicity distance** | The length of ciphertext beyond which only one key is expected to give a sensible reading (Shannon 1949). |

## Appendix A. Techniques introduced in this work

These are the methods this study built or adapted. "Introduced" means we did not find them in the D'Agapeyeff
literature checked (Section 9); they were not checked against the general cryptanalysis literature, and some are
adaptations of standard tools. Paths are relative to the repository root.

**A.1 Group-symbol n-gram scoring.** To search a transposition when each symbol stands for a group of letters, we score
candidate orders with an n-gram model over the 13 *group* symbols, built by passing a large English corpus through the
table. No letter has to be chosen for any symbol, so the transposition can be searched separately from the decoding.
Six-symbol patterns recover the grille on 6 of 6 practice ciphers (exactly on 5) where the usual four-symbol patterns recover 2 [F78].
Code: `lab/cipher/grille/grille_engine.py` (`group_ngrams`, `group_ngrams_ids`, `anneal(…, n, base)`).

**A.2 Rotation-invariant judging of grille recovery.** A turning grille turned a quarter is the same grille. A search
may return the right grille in any of its four orientations, so recovered grilles are compared with the planted one
in all four (`match_up_to_rotation`) [F71].

**A.3 GPU-batched annealing over grille orbits.** A 14 × 14 grille with a dummy column is 49 orbits of four cells, each
taking one of four turns. Hundreds of annealing chains (512 in our runs) move orbit turns in parallel on one GPU, with a
fixed step budget so results do not depend on machine load (`anneal`). This is an implementation of standard simulated
annealing, not a new algorithm.

**A.4 Balance-preserving table perturbation.** To measure how exact a table must be, letters are swapped between groups
so that every group keeps its size, then the grille search is rerun with the perturbed table [F74]. Code:
`lab/cipher/grille/bench_tolerance.py`.

**A.5 Likelihood repair of a table with the order fixed.** Given a symbol order, every swap of two letters between groups
(and every move of a letter to another group) is scored by the n-gram likelihood of the symbol stream, rebuilding the
group model on the GPU for each candidate; the best change is taken until none improves [I47]. Code: `repair_table` in
`grille_engine.py`; `lab/cipher/round11/table_test.py`.

**A.6 Truth-start test.** Starting the repair search *at the true table*
asks whether any nearby table scores the text better. Each time one does, the true table is shown not to be optimal under the score — so the rate is a lower bound on how
often a higher-scoring alternative exists under that score, not a measure of ambiguity under the true language. Repeating this over text lengths and two independent
language models gives the curve of Section 6.4 [F76]. Code: `lab/cipher/round11/identifiability.py`.

**A.7 Neighbor-pair key signal (exploratory).** Under a turning grille, cells that are horizontally adjacent in the
grid are often consecutive letters of the message (14–37% of message-column pairs in our practice ciphers), so a
likelihood built from neighboring pairs can rank keys without knowing the grille. A simple hill-climb using it beat
frequency-only key accuracy in 4 of 6 practice ciphers, too weakly to help [O32]. Exploratory: the code was run
interactively and is not preserved; nothing in the report relies on it.

**A.8 Symbol-usage test for digraphic systems.** Before searching a system, ask whether it can produce the cipher's
symbol usage at all: encipher English with random keys and count the distinct symbols in 182-symbol windows. Four-square
and two-square with random keys never come close to the cipher's 13 (0 of 10,000 practice ciphers) [R35]. Code:
`lab/cipher/round11/micro_digraph_cells.py`, `micro_digraph_cells_4x5.py`.

**A.9 Safeguards in the research process.** A claim gate refusing claims that cite missing results, uncorrected
p-values or statistics that shuffling cannot change; permutation tests that flag such invariant statistics and report a
family-wise p-value; and a linked case file in which disputing a claim flags every claim resting on it. These are part
of the PegasusDMZ platform (Section 10) and are not included in the repository.

**A.10 Calibration of better-scoring tables.** To tell a genuine competing table from one that merely fits the
passage, every table that beats the true one is scored again under an independent language model and on a fresh
passage enciphered with the true table [F77]. Code: `lab/cipher/round12/review_checks.py` (`ident`).

**A.11 Purpose-built key search and pair-dependence test.** For a given passage, a hill-climb rearranges the
plaintext squares of a four-square to use as few cipher symbols as possible, the two cipher squares are aligned to
make the counts as flat as possible, and the result is tested for order with mutual information between the two
symbols of each pair (both phases) and at lags 1 to 26, against shuffles with a family-wise correction [O34]. Code:
`lab/cipher/round12/review_checks.py` (`fsq`), `fsq_order.py`.

**A.12 Score-comparability check.** For a scoring model rebuilt per candidate table: measure the model's total mass
across the true table and its neighbors, score the true table against every single-swap neighbor on held-out text of
growing length (under a sufficiently accurate model, no neighbor should stay ahead on long text), and rerun the truth-start
test with a renormalized score [F79]. Code: `lab/cipher/round12/comparability.py`.

## Appendix B. Approaches that did not work

| Approach | Outcome | Entry |
|---|---|---|
| Columnar transposition (width 14) + one unknown substitution, with the 04 kept or removed | Practice ciphers recovered; the real cipher scored below its shuffled control | R27, R21 |
| Four-square / two-square with random keys | Excluded by symbol usage: they spread English over 18–25 distinct symbols, the message uses 13. A purpose-built key is not excluded (O34), but an ordinary four-square search cannot climb to the key (a key about 12 swaps from the truth) | R35, R32 |
| Grille and table searched together, nothing known | 0 of 3 practice ciphers at every budget tried. For the tested objectives the true table is usually not the best-scoring one even when supplied (F76), so more optimization of the same objective cannot be assumed to help; longer budgets were not studied | F68, F76 |
| Dictionary keyword squares ranked by how well cell counts fit English (148,398 squares) | None beats shuffled cell labels | R26 |
| Naturally made polyphonic tables (merges, letter pairs, keyword tables) | Never as flat as the cipher; only deliberately balanced tables are | F65 |
| Neighbor-pair key recovery (A.7) | Real but weak signal | O32 |
