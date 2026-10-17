# Fact-check log — report body

Draft: `draft_body.md` (turing, task t-fd52afd1). Checked against `SOURCE-PACK.md` (case entries in full, Figure 6
data, novelty check) by the developer (Claude), 2026-10-14, after the editor's run (strunk, t-40c803f4) timed out
having written only this file's header. Result: `body_final.md`.

| # | Claim as drafted | Verdict | Source | Correction |
|---|---|---|---|---|
| 1 | "395 digits … 392 digit-pairs … or 196 pairs if the 04 is counted" | CORRECTED | F1, F4 | 395 digits; the first 392 give 196 two-digit symbols = 14 × 14. |
| 2 | "four cells 71, 92, 93, 94 … appear only once or twice" | CORRECTED | F4 | Eight occurrences of the rare symbols (71, 92, 93, 94 and the 04), all in column 14; p < 1/20,000 over row lengths 2–20. |
| 3 | "Natural English at this length uses 17–22 distinct letters" | OK | F31 | As stated in F31. |
| 4 | "Hendrick … made the first rigorous contribution" | CUT | C9 | No priority claim; contributions described as recorded. |
| 5 | "recovering the bound in Latin as the closest language" | CORRECTED | C9 | If a one-to-one key were used, the counts would point to Latin. |
| 6 | Gariazzo "recovering planted grilles when the letter key was already known but not when both were unknown" | CORRECTED | C12, C13 | That is Hendrick's result (4/4 known key, 0/4 both unknown). Gariazzo: four families incl. a Fleissner grille over a one-letter-per-cell square, shuffled controls, none beat them. |
| 7 | "Of 304 enciphering families … reduced 17-letter alphabet … [F27, retired]" as support for the polyphonic hypothesis | CORRECTED | O16, F31, R29, F34 | F27 is retired and describes a different construction. Hypothesis argued from F31, R29, F34; O16 cited only for column 14 as padding. |
| 8 | Illustrative table {E,T,A} … {Q,Z} … digraph groups (CH, TH …) | CORRECTED | — | Not balanced; digraphs in a 26-letter table. Replaced by a computed balanced table (2M letters of English, poly_engine.balanced_table), shares 6.7–12.2 %. |
| 9 | "passed through a preregistration ledger and a multi-reviewer gate" | CORRECTED | — | Second-reviewer confirmation in the case file + programmatic claim gate; no preregistration ledger was used. |
| 10 | Padding crib (148,398 keyword squares; R26 figures) in §6.3 | CUT | R26 | Concerns one-to-one keyword squares, not polyphonic tables. |
| 11 | "roughly 500–700 symbols, at which the identifiability rate crosses 50 %" | CORRECTED | F76 | 41 % at 364, 57 % at 455 → crosses 50 % at ≈ 420 symbols. |
| 12 | Balanced-table fits by language "[F31, refined]" | OK | F31 | English 364, Latin 368 per 1,000 quoted in §2. |
| 13 | §6.4 percentages 11/27/41/57/63/75/84 % and 14/8 %, 94/74 % | OK | F76, fig6_data.json | Verified; per-corpus rows added as a table. |
| 14 | §6.1 "6/6 … 5-gram 6/6 … 4-gram 2/6"; §6.2 "4/4, 1/4, 2/4, 0/12" | OK | F73, F74 | Verified. |
| 15 | §6.3 "-5.74 to -5.44 … 2 to 5 wrong letters" | OK | I47 | Direction kept; raw scores dropped as unexplained jargon. |
| 16 | §8 "89 % … lower bound on non-identifiability" | OK | F76 | Kept, explained. |
| 17 | (missing) the no-message alternative | ADDED | F66, C9 | Hendrick's conclusion and our replication (family-wise p = 0.29) stated in §3 and §7. |
| 18 | F64 (proposed) and F67 (100th-percentile statistic) | NOT USED | F64, F67 | Unconfirmed / of the kind the claim gate now refuses. |
| 19 | Gariazzo's model described (developer's first edit) as "a large language model" | CORRECTED | C12 | A statistical quadgram model of English. |
| 20 | Exec summary: D'Agapeyeff "is reported to have said" he could no longer read the cipher | CUT | — | Not sourced in the case file. |
| 21 | Reference: Barker 1978, *Cryptologia* "2(2)" | CORRECTED | — | Volume/issue not verifiable; DOI kept. |
| 22 | Glossary: symbols as coordinates "of a 5 × 5 square" | CORRECTED | O16, F4 | Row digit 6–9 (once 0), column digit 1–5. |
| 23 | Appendix A.2: without rotation-invariant judging "correct recoveries can be scored as failures" | CORRECTED | F71 | F71 states only that a quarter-turned grille is the same solution; reworded. |
| 24 | Appendices A and B (new): every number and entry | OK | F73, F74, I47, F76, O32, R27, R21, R32, F68, R26, F65 | All cited entries confirmed; O23 confirmed against Hendrick's full text. |
| 25 | Study dates "7 to October 14" | CORRECTED | ledger, tasks, files | D'Agapeyeff work began on Oct 8, local date (first task and the ciphertext/sources files that day). Oct 7 was the earlier Enigma/Beale work. |
| 26 | §11.1 budget table and by-model / by-day figures (new) | OK | evidence/accounting-2026-10-14.json | Recomputed by tools/accounting.py from the proxy ledger (task-attributed rows), the session transcript (deduplicated by message id, from the first D'Agapeyeff task) and lab job records. |
| 27 | §11.1 "a billion input tokens cost less than US$70" | CORRECTED | accounting | Mixed billed agent tokens with subscription developer tokens; now "the agents' 423 million input tokens cost about US$67". |
| 28 | §11.2 who found what (new) | OK | case file `by` / `confirmed_by` + evidence fields; ledger models per agent | Agent→model taken from the ledger rows of that agent during the study. |
| 29 | §11.3 timeline: full-text novelty check placed on Tue Oct 14 | CORRECTED | C12, C13 timestamps | That falls on Mon Oct 13, local date; moved to Mon. All other timeline items checked against entry timestamps, briefing files and commits. |
| 30 | §11.2 the team (new): role, model, contribution, calls and cost per agent | OK | team registry (roles); dagapeyeff task list per assignee; case entries naming the agent (by / evidence); ledger rows per agent (models); accounting-2026-10-14.json (calls, cost) | Agents stated to be AI models, not the historical namesakes. |
| 31 | §11.4 timeline weekdays (Wed Oct 8 … Tue Oct 14) | CORRECTED | calendar | Oct 8, 2026 is a Thursday; all seven labels shifted (Thu 8 … Wed 14). |
| 32 | §10, §11.3, §11.4: the author's decisions and their dates (new) | OK | the author's instructions in the session record (local dates) | Each decision matched to the record that followed it: the case file, Kasiski, F31, the Hendrick check (C9) and, from "aim at the key", F71–F76. |
| 33 | §11.2: Strunk and Juran entries | CUT | — | Their contribution to the report was negligible; counted with the other teammates (ten, US$2.09). |
| 34 | Appendix D (new): one-line statement for each of the 31 codes cited | OK | full text of each entry in the case file | Every statement checked against its entry; all 31 confirmed; result files listed only where the file is in the repository. 142 in-text references link to their entries (no dangling links). |
| 35 | §5, §10, Appendix D: entries recorded "only after a second reviewer" checked them | CORRECTED | case file `by` / `confirmed_by` | Most cited entries were recorded and confirmed by the same hand (developer; Turing for the team's). Now stated as such; §8 adds a "Review" limitation: not yet reviewed outside the project. |
| 36 | Exec summary and Appendix C: "every number is traced to the run / every result comes from a file below" | CORRECTED | Appendix C, Appendix D | Key results have files in the repository; other figures come from case-file entries with recorded evidence. |
| 37 | §7: von zur Gathen's unicity estimate "helped to confirm" the Zodiac-340 solution | CORRECTED | doi:10.3384/ecp188395 abstract | The paper offers "a further argument in its favor"; now "argued that this supports the accepted solution". |
| 38 | F16 shown "at risk" (cites retired F14, F15) | CORRECTED (record) | F14/F15 logs | F16 is the check that retired them; linked as supersedes. All 31 cited codes confirmed, none at risk. |
| 39 | README: Hendrick "left one family open: a turning grille"; reproduce commands | CORRECTED | C9, O23 | Several families remain open; reproduce block rewritten as a shell function (syntax-checked). |
| 40 | DOI 10.5281/zenodo.23306263 (supplied by the author) | ADDED | — | On the cover, "Cite as", PDF metadata, README and CITATION.cff. Not yet resolvable-checked (Zenodo unreachable after the VM restart). |
| 41 | Rights claimed (COPYRIGHT, NOTICE, report §10, README) | CORRECTED | rights audit 2026-10-14 | Claims narrowed to the project's own contribution "to the extent copyright subsists", with an AI-assistance clause; quotations, facts, the ciphertext and agent namesakes expressly not claimed (no endorsement implied). |
| 42 | Third-party content in the repository | CORRECTED | rights audit | Removed: 31 publisher abstracts (metadata-only file shipped instead); two Christie novels (public domain in the USA only) and model_text_big.txt, which contains them (byte-exact rebuild script added). Gariazzo (CC BY 4.0) given an attribution file; wordfreq-derived files and bench-2.json plaintexts marked CC BY-SA 4.0. |
| 43 | Personal data in tools/accounting.py | CORRECTED | — | Home path and session id replaced by environment variables. gitleaks: no leaks. |
| 44 | R34 (new): four-square and two-square excluded by symbol usage — exec summary, §7, §9, Appendices A, B, D | OK | micro-digraph-cells.json (5×5 four/two-square: 22–25 distinct, 0/4,000 ≤ 13), micro-digraph-cells-4x5.json (4×5: 18–20; 13-letter text: 4×5 18–20, 5×5 20–25; 0/6,000 ≤ 13) | Total 10,000 practice ciphers, none at 13 or fewer. Caveat (random keyed squares) stated. Novelty not checked beyond Hendrick and Gariazzo. |
| 45 | §7 "22 to 25 … even when the message is restricted" | CORRECTED | micro-digraph-cells-4x5.json | The 5×5 restricted-text case went down to 20; now "20 to 25 even when restricted". |
| 46 | §7 "Is it a question of computing time?" (new) and docs/FINDINGS-ADDENDUM.md | OK | F68, F76, C9, R21, R27, R34 | Answers the reading that "untestable at 1200s" meant a compute limit: every listed family is closed by the data or by identifiability. |
| 47 | §10: the literature review "placed the work against Hendrick's" | CORRECTED | — | Now "set this study alongside the work of others on the cipher — above all Hendrick's and Gariazzo's"; Acknowledgements section added crediting earlier researchers. |
| 48 | Times of day in the report and records | CUT | — | Clock times and time-of-day words removed from the report, this log and the accounting file (dates kept). Machine timestamps inside the raw evidence (case file, lab job records) are unchanged. |
| 49 | Title and subtitle: "the hypothesis lies below its unicity distance" | CORRECTED | external review; F76, F77 | Shannon's unicity distance assumes perfect knowledge of the language; we measured recovery under stated models. Now "A turning grille is recoverable, but 182 symbols do not determine its polyphonic table". |
| 50 | Exec summary / §7: "neither this search nor any other can confirm it", "more computing time would not change any of this" | CORRECTED | external review; F77 | Limited to the methods tested; a better model of the language is not ruled out (§8). |
| 51 | §6.4: "explains the text better", 11% as a probability of identifiability | CORRECTED | external review; F76 | "Scores better"; rates are recovery rates under the procedure, not probabilities that the table is identifiable by every method. |
| 52 | Practice plaintexts drawn from a word-frequency sample (no grammar) | CHECKED | ident-full.json (F77) | Repeated on held-out natural prose (two Wells novels): 12–18% exact at 182 symbols, against 20–26% for the word sample under the same models. Conclusion unchanged; disclosed in §5 and §6.5. |
| 53 | Dependence on corpus and score | CHECKED | ident-full.json (F77) | Ten setups (three corpora; joint 6-gram and chain-rule 4/5/6-gram scores): 8–26% exact at 182 symbols, 28–60% at 546; pooled 15%, 26%, 29%, 41% at 182/273/364/546. |
| 54 | Are the better-scoring tables genuine competitors? | CHECKED | ident-full.json (F77) | At 182 symbols they still beat the truth under the other corpus in 171 of 248 cases (69%), but on a fresh passage in only 82 of 427 (19%): they fit the passage, not English. |
| 55 | §7 / exec summary: "keyed four-square and two-square are excluded outright" | CORRECTED | fsq-full.json, fsq-order.json (O33); R35 supersedes R34 | Holds for random keys only. A purpose-built key reaches 13 cells in 13 of 100 passages (14 in 59, 15 in 27, 16 in 1), all 13 flat (chi-square p 0.85–1.0); order test flags 12 of 100 (3 of the 13) against 52 of 100 with random keys; the real message family-wise p = 0.999. |
| 56 | §4: "flat in a way only a deliberately balanced many-to-one table reproduces" | CORRECTED | F31, O33 | A purpose-built four-square also reproduces it; §4 now says no ordinary table does and a balanced one does, and names the second construction. |
| 57 | Exec summary: "three English corpora, and five scoring methods" | CORRECTED | review_checks.py | Four scoring methods (joint 6-gram; chain-rule 4-, 5- and 6-gram). |
| 58 | §7: a longer text "more than twice as long" | CORRECTED | F76, F77 | Pooled recovery is 41% at 546 symbols (3×); now "at least twice as long, and under some of the models we tried three times or more". |
| 59 | Pronouns for Hendrick and the author | CORRECTED | — | Replaced with names ("Hendrick", "the author"). |

Entries 49 onward: revision of October 15, 2026 after an external review of the draft; checks in `lab/cipher/round12/`.

Entries 60 onward: second external review (October 15, 2026).

| # | Claim as drafted | Verdict | Source | Correction |
|---|---|---|---|---|
| 60 | Subtitle "A turning grille is recoverable, but 182 symbols do not determine its polyphonic table" | CORRECTED | second review | Universal reading removed: now "Grille recovery and polyphonic-table identifiability under n-gram scoring". |
| 61 | §8 "finding a better table proves the true one is not the most likely" | CORRECTED | second review | Now: not optimal under the tested scoring function; says nothing about which table is more probable under the true language distribution. Carried through §1, §6.4, §7, §8, §9. |
| 62 | §7 longer searches would not help | CORRECTED | second review | Algorithm and objective stated (simulated annealing / steepest ascent on n-gram scores); a differently designed search or objective is not ruled out. |
| 63 | §6.1 "For the real cipher, the remaining unknown is therefore the table" | CORRECTED | second review | Limited to practice ciphers with known table and model; the real cipher's grille, table and construction remain unconfirmed. |
| 64 | §4 "Three established facts narrow the field" | CORRECTED | second review; F4, F31, F32, F65, R29, R31, F34, O16 | Split into what is observed in the ciphertext and what is inferred from simulations of particular families (with their scope). |
| 65 | §6.4 "exact recovery" undefined | CORRECTED | identifiability.py, review_checks.py | Defined: the search starts at the true table and climbs; "truth kept" = no swap raises the score = the true table is a local maximum of the score. Not blind recovery. |
| 66 | §6.4/§8 89% as a lower bound on how often the table is undetermined | CORRECTED | second review; F76 | Now an empirical lower bound on how often a higher-scoring alternative exists under this score and procedure; not information-theoretic ambiguity. |
| 67 | Small-sample results presented as rates (6/6, 4 per condition) | CORRECTED | bench-ngram.json, bench-tolerance.json | 95% Wilson intervals added (6/6: 61–100%; 2/6: 10–70%; 4/4: 51–100%; 1/4: 5–70%; 2/4: 15–85%; 0/12: 0–24%) and labeled preliminary demonstrations. |
| 68 | §6.5 robustness given as ranges only | ADDED | ident-full.json | Appendix E: all 40 setup × length rows with counts, intervals, other-corpus and fresh-passage results; data splits and seeds (generated by make_appendix_e.py). |
| 69 | §6.5 cross-model and fresh-passage procedure | CLARIFIED | review_checks.py | Table selected by one search under one model on one passage; rescored unchanged under the other corpus on the same passage, and under the same model on a passage 3,000 letters on that played no part in selection; neither passage in any model corpus. |
| 70 | §7 purpose-built four-square | CLARIFIED | fsq-full.json, fsq-order.json | A feasibility result using knowledge of the plaintext; 13 of 100 (8–21%); not evidence that D'Agapeyeff used it; "most promising lead" stated as judgment. |
| 71 | Appendix D "catalogd historical tables" | CORRECTED | — | "cataloged" — an artifact of the American-spelling sweep (catalogue→catalog applied inside "catalogued"). |
| 72 | §6.1 / F73: "all 49 holes … on 6 of 6, and the true grille was always the top-scoring candidate" | CORRECTED | bench-ngram.json (F78 supersedes F73) | Recovered by the benchmark's criterion (≥ 45 of 49 orbits) on 6 of 6; exactly on 5, 48/49 on the sixth, where the near-miss scored above the truth. Five-symbol: 47–49 orbits, exact on 3 (F73 said 48–49). Found while preparing the reproducibility audit; the case file corrected by F78, and F74, I47, C12, C13 re-pointed. |

Entries 73 onward: third external review (October 15, 2026).

| # | Claim as drafted | Verdict | Source | Correction |
|---|---|---|---|---|
| 73 | Request 1: are scores comparable across candidate tables? | CHECKED | comparability.json (F79) | Model rebuilt per table; floored mass 2.10 (A′) / 1.45 (B), spread 0.002 log10 across 306 tables; 0 of 9,150 neighbor comparisons beat the truth at 10,000 and 100,000 held-out symbols; renormalized truth-start keeps the truth in the same 200/200 runs. No rerun needed; added to §6.5, §8, A.12, Appendix D. |
| 74 | §7 "a longer run … would find a wrong answer more reliably" | CORRECTED | third review | Replaced with the reviewer's wording: higher-scoring incorrect tables frequently exist, so more optimization of the same objective cannot be assumed to help; longer budgets not studied. Same in §1, Appendix B, README, findings addendum. |
| 75 | "With the table given, the grille can be found" (§1, §6.1 heading, §9, README) | CORRECTED | F78 | "Recovered at least 45 of 49 orbits in six of six practice ciphers (five exactly)", true table supplied, preliminary, not the historical grille. |
| 76 | §10 reproduction compared outcomes only | EXTENDED | repro-compare.json | Every regenerated record identical to the published one in every field except elapsed time; order-test file byte-identical; other fingerprints differ only through recorded run times. Labeled internal reproduction. |

Entries 77 onward: final review (October 15, 2026).

| # | Claim as drafted | Verdict | Source | Correction |
|---|---|---|---|---|
| 77 | §6.5 "the true table must beat every neighbor once the held-out text is long enough" | CORRECTED | final review; F79 | Now: under a sufficiently accurate model the true table should outperform neighbors on long held-out text; the finite-sample tests check this for the models and neighbors examined. Measurements unchanged (0 of 9,150 at 10,000 and 100,000 symbols; 200/200 paired outcomes). Same softening in §1, A.12 and Appendix D. |
| 78 | §6.5 "a property of short texts, not of the way tables are scored" | CORRECTED | final review | Now: supports short-passage effects rather than the tested normalization; does not exclude every possible model or scoring bias. |
| 79 | §6.1 "the table is the only obstacle to finding the grille" | CORRECTED | final review; F78 | Now: in these practice ciphers, supplying the true table enabled grille recovery under five- and six-symbol scoring; generalization untested. |
| 80 | Cover date October 14 while §1 reports October 15 checks | CORRECTED | — | Cover and metadata dated October 15, 2026 (first edition; not labeled revised). October 14 kept only for the literature check and the budget snapshot, which were made that day. |
| 81 | §8 "Section 6.5 shows the scores are comparable across tables" | CORRECTED | final review; F79 | Now "provides empirical evidence that": the tests cover selected models, tables and lengths, not every candidate. |

Entries 82 onward: internal audit follow-up (October 15, 2026); details in audit-2026-10-15/AUDIT-REPORT.md.

| # | Claim as drafted | Verdict | Source | Correction |
|---|---|---|---|---|
| 82 | README / §1: purpose-built four-square "13 flat symbols with little detectable order in 13 of 100" / "mostly without detectable order" | CORRECTED | internal audit 2026-10-15; fsq-full.json, fsq-order.json; O34 | Separated: 13 of 100 reach 13 flat symbols; 10 of those 13 are not flagged by the tested family-wise order statistic at the 5% level (flagged: passages 34, 77, 95). Non-detection is not absence of order. |
| 83 | §7 "removes most of the dependence between the two symbols of each pair" | CORRECTED | audit_fsq.py | Not shown: 7 of the 13 flat passages have uncorrected pair dependence at p < 0.05. Replaced with a description of the test and its result. |
| 84 | §4, §7, §9, Appendix D, §11.3: four-square "reproduces … lack of (detectable) order" / "fits the clues" | CORRECTED | O34 | Narrowed to usage and flatness (13 of 100) and, for 10 of 100, non-detection by one order test. Citations moved from O33 to O34 (O33 kept as a record). |
| 85 | Greedy label matching in round-12 distances | CHECKED | label_audit.py | 220 regenerated runs: truth-kept flag identical under raw, greedy and optimal matching; no pure relabellings; greedy overstated error size by 1 in 6 of 200 runs, none cited in the report. No change. |
| 86 | §10 "A follow-up internal audit … using independently written code" | CLARIFIED | audit follow-up; label_full.json | Now states the audit ran within the project, with checking code written separately from the experiment code, not by an unaffiliated researcher; adds the all-runs label comparison; cites where its scripts and outputs are (now shipped in lab/cipher/audit/ and docs/audit-2026-10-15/). |
| 87 | Round-12 distances use greedy label matching (review_checks.wrong, docstring says 'best label matching') | CHECKED | label_full.json, test_label_distance.py | All 2,000 robustness runs regenerated: every field matches the published record (2,000/2,000); greedy ≠ exact in 80 runs, by one letter; 0 truth-kept and 0 higher-scoring flag changes; no relabellings. No reported figure uses these distances. Appendix E now notes it. The executed script is left unchanged. |
| 88 | §11.4 Sat Oct 10 "an independent review of round 1" | CORRECTED | REVIEW-2026-10-10.md ("Reviewer: Claude (developer), for the operator") | Now "a review of round 1 by the developer (Claude), separate from the agent team"; independent of the agent team, not of the project. |
| 89 | §8: no plaintext-distribution limitation | ADDED | final wording review | New 'Plaintext' limitation: tested on a frequency-weighted English word sample and held-out Wells prose; not on telegram style, abbreviations, unusual vocabulary or misspellings; rates may differ. §6.5 findings unchanged. |
| 90 | §9 novelty assessments | QUALIFIED | final wording review | Added: provisional, based on the literature examined; no claim of priority over unpublished or unfound work. |
| 91 | §1, §7, README: random-key four-square/two-square "excluded" | NARROWED | R35; micro-digraph-cells*.json (plaintext: plain_pool.txt) | Now: the randomly keyed constructions tested did not reproduce 13-symbol usage in 10,000 practice ciphers; excludes those constructions under the tested plaintext, not every key. |
| 92 | README "Review status" | REWRITTEN | lab/cipher/round12/repro, lab/cipher/audit | Lists original records, internal reproduction and separately implemented checks; states none is a complete clean-environment rerun or unaffiliated replication. The reviewer's suggested 'checked outside the project's agent system' was not used: not substantiated by project records. |
| 93 | "external reviewers" / "external readers" (§1, §5, §6.5, §8, §10, §11.3, §11.4, Acknowledgements, README) | CORRECTED | author, October 15, 2026 | The draft reviews were by ChatGPT-6 sol (OpenAI), an AI model, at the author's request. Every mention now names it and says it is an AI review, not human peer review; credited in §10 ('Review of the drafts'), the Acknowledgements and the README. |
| 94 | Cover label "Research report" | CHANGED | preprint labeling request | Cover now "Research preprint"; PDF keywords add "research preprint". |
| 95 | No publication-status statement | ADDED | preprint labeling request | §1 opens with "Publication status. Research preprint …not been formally peer-reviewed by an independent academic journal"; README states the same. Consistent with §10 (AI review, not human peer review). |
| 96 | CITATION.cff: invalid top-level `type: report`; date-released from build clock (read 2026-10-16) | CORRECTED | CFF 1.2.0 schema (type: software | dataset) | Top-level entry now describes the repository; the paper is a preferred-citation (type report, status preprint, October 2026); date-released fixed at 2026-10-15. |
| 97 | Reviewer named "ChatGPT-6 sol" (entry 93) | CORRECTED | author, October 16, 2026 | The reviewer was OpenAI's GPT-6 (through ChatGPT Plus); all mentions renamed. |
| 98 | §10 Cost and §11.1 omitted the reviewer's subscription | ADDED | author | ChatGPT Plus subscription listed in §10 Cost and as a row in §11.1 (usage not recorded; no per-token charge). |
| 99 | §11.3 Contributions omitted the reviewer | ADDED | author | OpenAI's GPT-6 listed as draft reviewer, with what it did and did not do. |
| 100 | Reviewer named "GPT-6" (entries 97–99) | CORRECTED | author, October 16, 2026 | The reviewer's name is GPT-6.1 Sol (OpenAI); all mentions renamed. |
| 101 | Reviewer named "GPT-6.1 Sol" | CORRECTED | final corrections, October 16, 2026 | No contemporaneous record proves which model performed each review session; attribution is now "ChatGPT (OpenAI)", through ChatGPT Plus where the subscription matters. Substance and the AI-review disclosure unchanged. |

Entries 102 onward: language-source provenance audit (October 16, 2026).

| # | Claim as drafted | Verdict | Source | Correction |
|---|---|---|---|---|
| 102 | §2 "about a third of trials … for Latin (368 of 1,000)" | CORRECTED | latin_flatness.json (F80); Gutenberg records | 368 came from an ad-hoc run before the F31 tool was committed; the committed tool gives 345–374 across seeds and call orders on the same ten-edition Latin corpus (within that variation), but 167–182 for the six editions without English notes. Now reports the range and the dependence on the texts sampled. English 364/1000 reproduces exactly. |
| 103 | §4 inference bullet "in about a third of trials" | CORRECTED | F80 | Now "about a third of English trials and one in six to one in three Latin trials depending on the texts sampled". |
| 104 | §6.1 "7-million-letter English corpus" without sources | ADDED | sources.json; build_model_text.py | Identified as 13 Project Gutenberg novels (Appendix F); plaintext source named (word-frequency sample). |
| 105 | §6.4 corpora A/B composition and Wells role | CLARIFIED | identifiability.py (files[0::2] / [1::2]) | Notes that the Wells novels are in corpus A in §6.4 (held out only in §6.5); Appendix F lists each corpus. |
| 106 | §4 example table "two million letters of English" | CHECKED | model_text_big.txt[:2,000,000] | Reproduced exactly from the first 2,000,000 letters of the model text (Adventures, Great Expectations, Hound, The Man Who Was Thursday, part of Memoirs); source now in Appendix F. |
| 107 | References lacked the language sources | ADDED | Gutenberg catalog records; wordfreq 3.1.1 README | Project Gutenberg editions (23 eBook numbers), Speer 2022 (wordfreq), Brysbaert & New 2009 and van Heuven et al. 2014 (SUBTLEX, as wordfreq's terms require); new Appendix F with per-source provenance and roles; acknowledgements name wordfreq, SUBTLEX, Google Books Ngrams and OpenSubtitles. |
| 108 | CORPUS.md "War and Peace (Project Gutenberg English translation)" | CORRECTED | Gutenberg record #2600 | Translators Louise and Aylmer Maude; eBook numbers, record dates and retrieval added for all 13 novels; 10 Latin editions added. |

Entries 109 onward: release-candidate validation (October 16, 2026). Evidence in `docs/validation-2026-10-16/`.

| # | Claim as drafted | Verdict | Source | Correction |
|---|---|---|---|---|
| 109 | §2 "natural passages use 17 to 22 different letters" | CORRECTED | flatness_standalone.py (identical counts to the platform tool); F81 | 182-letter windows use 18–25 letters in English (median 22) and 14–25 in Latin (median 20). The origin of "17 to 22" is not recorded. Never 13, so the point stands. |
| 110 | §7 "family-wise p = 0.29" for the replication of Hendrick's test | CLARIFIED | 20 reruns of hendrick_familywise.py (unseeded), from a copy writing elsewhere | 0.29 is one Monte Carlo draw; 20 reruns give 0.25–0.59 (median 0.38), always info lag 3 smallest. Range added; conclusion (not significant) unchanged. |
| 111 | §2 / §4 "odds below 1 in 20,000 after allowing for every row length from 2 to 20" | CHECKED | recompute_extra.py (new code) | With the platform's statistic (excess concentration over 1/p): exact bound 1.8 × 10⁻⁹, 0 of 200,000 shuffles. A cruder "any period, all in one residue" statistic gives about 0.7% because of period 2; the printed odds rest on the former. No change. |
| 112 | §4 "in 40 of 40 planted texts" (R29) | CHECKED | recompute_extra.py (new code, new seeds) | 39 of 40 at p < 0.05 (38 at p < 0.01); real message p = 0.72. Conclusion reproduced; the exact count is seed-dependent. No change. |
| 113 | §2 F32 component p-values (rows 0.08, columns 0.30, halves 0.10 / 0.60, lag family 0.91) | CHECKED | recompute_extra.py (new code) | 0.087, 0.304, 0.094, 0.494 (left/right split assumed: columns 1–6 vs 8–13), lag family 0.902. No change. |

Entries 114 onward: R29 and F4 clarifications (October 17, 2026). Evidence in `docs/validation-2026-10-17/`.

| # | Claim as drafted | Verdict | Source | Correction |
|---|---|---|---|---|
| 114 | §4 "left detectable order in 40 of 40 planted texts" (R29) | CLARIFIED | original command (session record, October 11), rerun unchanged at PegasusDMZ commit c908608: identical (40/40 at p < 0.05, 39/40 at p < 0.01, real p 0.698); recompute_extra.json | 40 of 40 kept as the result for the original plants and seeds; the separately written check (39 of 40, new seeds, different practice texts and tables) reported beside it, not pooled; test named; real-message result kept separate. Case F82. |
| 115 | Appendix D R29 "always leaves order" / "so its order was scrambled" | CORRECTED | as 114 | "always" overstated a 40-text sample; now "in all 40 of the original practice texts" and "if such a table was used its order was scrambled". |
| 116 | §2 "odds below 1 in 20,000 after allowing for every row length from 2 to 20" (F4) | CLARIFIED | original command (session record, October 11), rerun unchanged: 0 of 20,000, (0+1)/(20,001) = 5.0 × 10⁻⁵; f4_events.py | Statistic now defined in the text (largest column share less 1/p, best over row lengths 2–20); "below 1 in 20,000" identified as the simulation floor; exact bound 1.8 × 10⁻⁹ added; §5 note separates the looser any-row-length event (0.71%, 95% from row length 2) and says the scan covers only the choice of row length. The printed claim stands. Case F83. |
| 117 | Validation note (October 16) "same parity, 1 in 64" for row length 2 | CORRECTED | f4_events.py (exact count) | Exactly 0.0067, about 1 in 149 (eight positions drawn without replacement). Corrected in `validation/recompute_extra.py`; the October 16 output file keeps the original wording as a record. |
| 118 | §9 table "A polyphonic table without transposition is excluded (R29)" | CLARIFIED | R29, F82 | Qualified "under the tested conditions". |
| 119 | Figure 1 caption "Every one of the five rare symbols falls in the last column" | CLARIFIED | F4 | "All eight occurrences of the five rare symbols fall in the last column" (counts occurrences, as the test does). |

Entries 120 onward: external AI review of the release candidate (October 17, 2026; ChatGPT (OpenAI), not peer review).

| # | Claim as drafted | Verdict | Source | Correction |
|---|---|---|---|---|
| 120 | §6.3 "On two practice ciphers whose grille had already been recovered exactly … from 2 wrong letters to 5" (I47) | CORRECTED | `lab/cipher/round11/validate.json`; case I47 (whose own text was right) | Only plant 0 had its grille recovered (49/49 orbits; 2 → 5 wrong). Plant 1's grille was not recovered (19/49) and its table went 2 → 8. Text, Appendix D, §8 sample sizes and the contributions table now say so. |
| 121 | §2 "Ordinary text is never this even … Nor does any table that people ordinarily make … produce it"; §4 "other ordinary tables … never"; Appendix D F31 / F65; Appendix B; contributions and timeline (F65) | CORRECTED | standalone flatness runs (`docs/validation-2026-10-16/flatness/`) | Random merges matched in 1/1,000 English windows (2/2,000) and 1–14 per 1,000 Latin; fixed-pattern pairs and the book's sign system 0. "Never" kept only where the count is 0; elsewhere "rarely" with the rate. Case F84. The contrast with balanced tables (364/1,000) is unchanged; the inference is stated less absolutely. |
| 122 | `validation/compare.py` I47 check | CORRECTED | as 120 | It examined only the first record; it now checks both 2-wrong-letter records and their starting grilles. |
| 123 | `validation/compare.py` S2 letter-range check | CORRECTED | F81 | The predeclared check of the old "17 to 22" claim is kept (it fails, as expected) and marked superseded; a versioned check of the corrected range (S2-letters-v2) and of F84 added; the script now exits 1 on any unexpected FAIL. |

Entries 124 onward: editorial pass on ownership and novelty wording (October 17, 2026). No result changed.

| # | Claim as drafted | Verdict | Source | Correction |
|---|---|---|---|---|
| 124 | Possessive "our / ours" for tests, simulations, judgment and drafts (§1, §4, §5, §6.5, §6.6, §7, Appendix A, Appendix D C9, acknowledgements, README) | REWORDED | — | "This study", "the present analysis", "the order test of Section 7", or the finding itself. |
| 125 | §1 "separate what is new", "What is new … not previously published"; §9 "What is new and what is not" with Prior art / **New** / Probably new | REWORDED | §9 literature check | Labels now Prior work / Replicated in this study / Extended in this study (F78, F74: Hendrick's one-to-one results applied to polyphonic tables) / New finding, within the literature reviewed ("less certain" where it was "Probably new"); "the main contribution" → "the study's main result"; §1 says these are measurements and applications of standard tools, not new algorithms, and that the check does not establish priority. |
| 126 | Appendix A "Techniques introduced in this work" | REWORDED | — | "Techniques built or adapted in this study"; "None is claimed as a new algorithm". |
| 127 | Appendix D F66 "independently replicated"; §7 "our replication … confirms"; history "an independent check of the team's first round" | REWORDED | — | "replicated within this study by the team's statistics specialist (not an independent replication)"; "the replication … in this study is consistent with it"; "a separate check" — keeps project-internal checks distinct from independent replication. |
| 128 | §7 bullet ending "uses exactly / 13." | LAYOUT | rendered PDF (page 14 of 41) | A wrapped line beginning "13." was read by pandoc as a numbered list, printing a stray "13." at the top of the page; rewrapped. No source line in the report now begins with a number and a period. |
