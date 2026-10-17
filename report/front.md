## 1. Executive summary

**Publication status.** Research preprint. This manuscript has undergone internal verification and AI-assisted critical review but has not been formally peer-reviewed by an independent academic journal.

In 1939 Alexander D'Agapeyeff closed his book *Codes and Ciphers* with a short challenge cipher: 196 two-digit
numbers, and invited readers to solve it. In more than eighty years nobody has.

This report sets out what an AI-assisted cryptanalysis program, conceived and directed by Nicolas Houghtaling over
seven days, October 8 to 14, 2026, established about the cipher, with further checks on October 15 to 17 prompted by
reviews of the draft by a separate AI system, ChatGPT (OpenAI). It is careful to separate this study's findings from what others published first, and what was
measured in practice ciphers from what can be said about the real one.

**The question addressed.** Recent work (Hendrick 2026) showed that no one-to-one letter key, combined with any
transposition, can produce the cipher's symbol counts, and that if the cipher carries a message at all, its order was
scrambled by a system as thorough as a *turning grille* (other families, such as keyed four-square, also remain open).
One construction consistent with every observed property is a 14 × 14 turning grille laid over a table in which each
of 13 symbols stands for a group of letters (a *polyphonic* table). Hendrick left the turning grille open because no
search could find its key. We asked whether, under this hypothesis, it could be found at all.

**What we found.** All rates below are measured on practice ciphers we made in the hypothesized form, with known keys.

- **With the true table supplied, practice-cipher grilles were recovered.** Scoring candidate grilles by six-symbol
  patterns recovered at least 45 of 49 orbits in six of six practice ciphers (five exactly; 95% interval 61–100%);
  four-symbol scoring, the usual choice, managed 2 of 6. A preliminary demonstration on six synthetic ciphers with
  the table given — not a general success rate, and not recovery of the historical grille.
- **A nearly right table is not enough.** With 6 or more letters in the wrong group the search never found the grille
  (0 of 12); with the true table it did 4 of 4. A preliminary result, the polyphonic counterpart of Hendrick's for
  one-to-one keys.
- **Under the scores tested, 182 symbols rarely single out the table.** Handed the true symbol order and started *at
  the true table*, a search that climbs the n-gram score usually moves to a *different table that scores higher*. The
  true table stayed best among its neighbors in only 11% of 200 practice ciphers at the cipher's 182 symbols, and in
  8% to 26% under every alternative tested after review: natural prose instead of sampled words, three English
  corpora and four scoring methods. It reaches one in two only at several hundred symbols.
- **The higher-scoring tables fit the passage, not English.** They usually still win under an independent corpus, but
  on a fresh passage enciphered with the true table they lose four times in five: they are fitted to the particular
  182 symbols. A higher score shows the true table is not optimal under the score, not that another table is more
  probable under English itself. Checks of the scoring itself found no sign that it favors particular tables: on
  10,000 and 100,000 held-out symbols, no tested neighbor outscored the true table.
- **D'Agapeyeff's own book teaches no table of this kind.** Every construction in it puts one letter in each cell.
- **A second construction can also fit.** Four-square and two-square with *random* keys spread English over 18 to 25
  symbols: in 10,000 practice ciphers none reached the cipher's 13, which excludes randomly keyed squares for the
  plaintext tested, not every key. But a four-square whose key is built
  on purpose around the message reached 13 symbols, as flat as the cipher's, in 13 of 100 passages; 10 of those 13
  were not flagged by the family-wise order test used in this study at the 5% level, which does not show that they contain no order.
  That shows such a construction is possible, not that D'Agapeyeff used it; it has not been searched.

**What it means.** Under the grille-plus-polyphonic hypothesis and the n-gram scores we tested, 182 symbols are not
enough to single out the table, so with these methods the hypothesis can be neither confirmed nor refuted from the
ciphertext alone. This is a measurement under stated methods, not a proof that no method could succeed. For the
tested scoring objectives, higher-scoring incorrect tables frequently exist even when the true symbol order and table
are supplied, so additional optimization of the same objective cannot be assumed to improve true-table recovery; we
have not established how success rates change with longer search budgets. A differently designed search or a
stronger model of the language is not ruled out. What would settle it is the table
from a source outside the ciphertext, or a longer message in the same system. We claim no decipherment.

**What this study adds, within the literature reviewed.** Two results extend earlier work to polyphonic tables:
recovery of the grille when the table is known, and the requirement that the table be essentially exact (Hendrick
showed both for one-to-one keys). Three are new findings within the literature reviewed: the truth-start measurement
and its robustness checks, the exclusion of randomly keyed four-square and two-square by symbol usage, and the
feasibility of a purpose-built four-square. They are measurements and applications made with standard search and
statistical tools, not new algorithms (Appendix A), and the literature check of October 14, 2026 behind them does not
establish priority (Section 9). The flatness of the symbol counts, the count bound, the grille search with a known key
and the one-to-one key tolerance are prior work, credited in Section 9.

Every number in this report comes from a recorded result: the files behind the key results are in the accompanying
repository, listed with their SHA-256 fingerprints in Appendix C, and every other figure comes from an entry in the
project's case file (Appendix D) that records its evidence. Appendix A describes the techniques built or adapted in
this study, Appendix B the approaches that did not work, and Appendix E every setup of the robustness checks.

Codes in brackets, such as [F78] or [R29], refer to entries in the project's case file of checked results; each
is explained in one line in Appendix D, and in the PDF each code links to its entry.
