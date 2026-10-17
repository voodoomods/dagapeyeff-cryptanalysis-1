"""Write appendix-e.md: the full robustness breakdown of Section 6.5 (F77), every setup and length, from the result file.

Run in the agent container:  python /workspace/research/cipher/dagapeyeff/report/make_appendix_e.py
Input: /lab/cipher/round12/ident-full.json. Output: report/appendix-e.md (included by build_report.py).
"""
import json
import math
from pathlib import Path

R = Path(__file__).resolve().parent
d = json.load(open("/lab/cipher/round12/ident-full.json"))


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return f"{max(0, c - h) * 100:.0f}–{min(1, c + h) * 100:.0f}"


SRC = {"pool": "word sample", "prose": "Wells prose"}
CORP = {"A": "A′ (5 books, 1.95 M)", "B": "B (6 books, 4.67 M)", "C": "A′ + B (6.62 M)"}
SCORE = {"joint6": "6-symbol (as §6.4)", "cond4": "chain-rule, 3 before", "cond5": "chain-rule, 4 before",
         "cond6": "chain-rule, 5 before"}
rows = []
for k, s in d["summary"].items():
    exp, model, src, L = k.split()
    corpus, score = model.split(":")
    rows.append((exp, corpus, score, src, int(L[1:]), s))
rows.sort(key=lambda r: ({"E1": 0, "E1c": 1, "E3": 2}[r[0]], r[3], r[1], r[2], r[4]))

out = ["## Appendix E. Robustness breakdown", "",
       "Every setup and length of Section 6.5, from `lab/cipher/round12/ident-full.json` [F77]. Each row is 50 practice "
       "ciphers (plants 0–49). *Truth kept*: the search, started at the true table, ended there — no swap of two letters "
       "between groups raises the score, so the true table is a local maximum of that score. *Higher-scoring found*: the "
       "search moved to a different table with a higher score. Of those, *other corpus*: the table found also beats the "
       "true table under the other corpus's model on the same passage (setups with a disjoint second corpus only); "
       "*fresh passage*: it also beats the true table under the same model on a passage 3,000 letters further on, which "
       "played no part in the search. Intervals are 95% Wilson intervals. One run (Wells prose, A′ + B, chain-rule 3 before, "
       "273 symbols) ended in a numerical tie and counts in neither column (§6.4). The result file also records how many letters "
       "the table found differs from the truth, using a greedy match of group labels; an exact assignment gives identical "
       "truth-kept and higher-scoring outcomes in all 2,000 runs and differs from the greedy count by one letter in 80 "
       "(internal audit, `lab/cipher/audit/label_full.json`). Those letter counts are not used in this report.", "",
       "| Plaintext | Corpus (letters) | Score | Length | Truth kept | 95% CI | Higher-scoring found | other corpus | fresh passage |",
       "|---|---|---|---|---|---|---|---|---|"]
for exp, corpus, score, src, L, s in rows:
    n, k, b = s["plants"], s["exact"], s["truth_beaten"]
    other = f"{s['beaten_also_other_model']} of {b}" if exp in ("E1", "E1c") else "—"
    out.append(f"| {SRC[src]} | {CORP[corpus]} | {SCORE[score]} | {L} | {k} of {n} ({100 * k / n:.0f}%) | "
               f"{wilson(k, n)}% | {b} | {other} | {s['beaten_also_fresh_text']} of {b} |")
out += ["",
        "**Data splits.** The 13 corpus novels, sorted by file name, are split alternately: corpus A takes the 1st, 3rd, … "
        "(7 books), corpus B the 2nd, 4th, … (6 books); Section 6.4 uses A and B in full. For Section 6.5 the two Wells "
        "novels (*The Time Machine*, *The War of the Worlds*, both in A) are removed from every model and used only as "
        "plaintext (407,678 letters): A′ is A without them. The word sample is `lab/cipher/grille/plain_pool.txt`.", "",
        "**True tables.** For each practice cipher the true table is the balanced table of the model's own corpus "
        "(letters packed into 13 groups by frequency, `poly_engine.balanced_table`), with its 13 labels shuffled by the "
        "plant's seed.", "",
        "**Search and score.** Steepest ascent from the true table: every swap of two letters in different groups is "
        "scored, the best is taken, until none improves (at most 8 sweeps). The score is the mean log10 of the "
        "six-symbol pattern frequency over the passage (§6.4), or the mean log10 conditional probability of each symbol "
        "given the 3, 4 or 5 before it with add-one smoothing (chain-rule). A candidate table is scored by rebuilding the "
        "model from the corpus mapped through that table.", "",
        "**Seeds.** Section 6.4: plant *p* uses `Random(9000 + p)` for its table labels and passage (the 20-plant runs "
        "`Random(7000 + p)`). Section 6.5: table labels `Random(12000 + p)`, passage start `Random(12500 + p)`, fresh "
        "passage 3,000 letters later. Four-square (§7): passage `Random(31000 + w)`, random-key controls "
        "`Random(55000 + w)`, order-test shuffles `Random(4242)`. GPU sums are not bit-for-bit deterministic, so "
        "individual runs can differ slightly on re-execution.", ""]
(R / "appendix-e.md").write_text("\n".join(out), encoding="utf-8")
print(len(rows), "rows")
