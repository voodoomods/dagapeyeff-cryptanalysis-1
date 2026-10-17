"""Overnight identifiability study (I47 follow-up) — is a balanced 13-group polyphonic table determined by a symbol
stream of length L when the ORDER is known (grille already solved)?

    python identifiability.py A|B      model corpus half A or B (disjoint Gutenberg books)

For each of 20 plants and L in (182, 364, 728, 1456): stream = true_table[plaintext[:L]] (plaintext from the
wordfreq-sampled pool — a different source from the model corpus). Steepest-ascent repair (grille_engine.repair_table)
from (a) the TRUE table and (b) the true table with 2 letters swapped, swaps only (balance kept, as the hypothesis
requires); at L=182 also with letter moves allowed. Recorded per run: score of the truth, score and distance-to-truth
of the table found, and whether a wrong table outscores the truth (= the truth is not the maximum-likelihood table).
Writes /lab/cipher/round11/identifiability-<corpus>.json after every run.
"""
import glob, json, random, re, sys, time
sys.path.insert(0, "/lab/cipher/grille")
import numpy as np
import grille_engine as ge, poly_engine as pe

CORPUS = sys.argv[1]
files = sorted(glob.glob("/lab/cipher/lm/corpus/*.txt"))
half = files[0::2] if CORPUS == "A" else files[1::2]
text = re.sub("[^A-Z]", "", "".join(open(f, encoding="utf-8", errors="ignore").read() for f in half).upper())
LET = ge.letter_ids(text)
POOL = re.sub("[^A-Z]", "", open("/lab/cipher/grille/plain_pool.txt").read())
PLANTS = int(sys.argv[2]) if len(sys.argv) > 2 else 20
LENGTHS = tuple(int(x) for x in sys.argv[3].split(",")) if len(sys.argv) > 3 else (182, 364, 728, 1456)
TAG = sys.argv[4] if len(sys.argv) > 4 else ""
OUT = f"/lab/cipher/round11/identifiability-{CORPUS}{TAG}.json"
N, BASE = 6, 14
out = {"corpus": CORPUS, "books": [f.rsplit("/", 1)[1] for f in half], "model_letters": len(text),
       "n": N, "runs": []}


def wrong(t, truth):
    return sum(1 for i in range(26) if t[i] != truth[i])


def score_of(tab, stream):
    return ge.stream_score(ge.group_ngrams_ids(LET, tab, N, BASE), stream, N, BASE)


for p in range(PLANTS):
    rnd = random.Random((9000 if TAG else 7000) + p)
    truth = pe.balanced_table(text, 13, rnd)
    start = rnd.randrange(0, len(POOL) - 1500)
    near = list(truth)
    a, b = next((x, y) for x in rnd.sample(range(26), 26) for y in range(26) if truth[x] != truth[y])
    near[a], near[b] = near[b], near[a]
    for L in LENGTHS:
        stream = np.array([truth[ord(c) - 65] for c in POOL[start:start + L]], dtype=np.int64)
        s_true = score_of(truth, stream)
        configs = [("truth", truth, False), ("near2", near, False)]
        if L == 182 and not TAG:
            configs += [("truth+moves", truth, True)]
        for name, init, moves in configs:
            t0 = time.time()
            found, s_found, changes = ge.repair_table(LET, [stream], init, 13, max_sweeps=8, n=N, base=BASE, moves=moves)
            r = {"plant": p, "L": L, "start": name, "moves": moves, "score_truth": round(s_true, 5),
                 "score_found": round(s_found, 5), "wrong_found": wrong(found, truth), "changes": changes,
                 "truth_beaten": s_found > s_true + 1e-6 and wrong(found, truth) > 0,
                 "exact": wrong(found, truth) == 0, "seconds": round(time.time() - t0, 1)}
            out["runs"].append(r)
            print(json.dumps(r), flush=True)
            json.dump(out, open(OUT, "w"), indent=1)

summary = {}
for L in LENGTHS:
    for name in ("truth", "near2", "truth+moves"):
        rs = [r for r in out["runs"] if r["L"] == L and r["start"] == name]
        if rs:
            summary[f"L{L}:{name}"] = {"plants": len(rs), "truth_beaten": sum(r["truth_beaten"] for r in rs),
                                      "exact": sum(r["exact"] for r in rs),
                                      "mean_wrong": round(sum(r["wrong_found"] for r in rs) / len(rs), 2)}
out["summary"] = summary
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps(summary, indent=1))
