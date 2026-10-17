"""Audit C (2026-10-15) — independent implementation of the six-symbol group n-gram score and the truth-start test.

Written from the report's description (Appendix E, 'Search and score'), in numpy on the CPU, float64, without importing
grille_engine, poly_engine or review_checks for the scoring or the search:

  score(table, stream) = mean over the stream's 6-symbol windows w of log10( max(count_t(w), 0.3) / N_t ),
  where count_t counts 6-symbol windows of the model corpus mapped through table t (symbols coded in base 14) and
  N_t is the number of windows. Steepest ascent from the true table over every swap of two letters in different
  groups, best swap first, at most 8 sweeps, accept only strict improvement > 1e-6 ... see note below.

  1. Hand-checked toy cases (tiny corpus, 2-symbol tables) with values computed on paper.
  2. Agreement with the experiment's scorer (review_checks.Model 'joint', 6) on 50 random (table, passage) pairs —
     imported ONLY for this comparison, after the independent values are computed.
  3. Truth-start reruns, independent search: the first 10 plants of the 'Wells prose, corpus A′, six-symbol' setup of
     ident-full.json at 182 symbols, same seeds and passages; final table, kept / higher-scoring, compared with the
     published record. The true tables come from the documented rule (letters packed into 13 groups by frequency,
     labels shuffled by Random(12000 + p)) implemented here independently.

Note on acceptance: the original takes the best swap whenever it beats the current score by any amount (float32 on
GPU); this implementation does the same in float64, so near-ties (< 1e-6) may resolve differently — reported, not hidden.

    python ngram_indep.py   ->  /lab/cipher/audit/ngram_indep.json
"""
import glob, heapq, json, random, re
from collections import Counter
import numpy as np

LM = "/lab/cipher/lm/corpus/"
BASE, N = 14, 6
HELD = ["time-machine.txt", "war-of-the-worlds.txt"]


def clean(fs):
    return re.sub("[^A-Z]", "", "".join(open(f, encoding="utf-8", errors="ignore").read() for f in fs).upper())


def codes(sym, n=N):
    m = len(sym) - n + 1
    q = sym[:m].astype(np.int64).copy()
    for j in range(1, n):
        q = q * BASE + sym[j:j + m]
    return q


def model(letters, table, n=N):
    c = np.bincount(codes(np.asarray(table, dtype=np.int64)[letters], n), minlength=BASE ** n).astype(np.float64)
    return np.log10(np.maximum(c, 0.3) / c.sum())


def score(letters, table, stream, n=N):
    return float(model(letters, table, n)[codes(stream, n)].mean())


def balanced(text, k, rnd):
    freq = Counter(text)
    h = [(0, i) for i in range(k)]
    tab = [0] * 26
    for letter in sorted(range(26), key=lambda x: -freq.get(chr(65 + x), 0)):
        s, i = heapq.heappop(h)
        tab[letter] = i
        heapq.heappush(h, (s + freq.get(chr(65 + letter), 0), i))
    lab = list(range(k)); rnd.shuffle(lab)
    return [lab[t] for t in tab]


def climb(letters, stream, start, sweeps=8):
    tab, cur = list(start), score(letters, start, stream)
    for _ in range(sweeps):
        best, bt = cur, None
        for a in range(26):
            for b in range(a + 1, 26):
                if tab[a] != tab[b]:
                    t = list(tab); t[a], t[b] = t[b], t[a]
                    v = score(letters, t, stream)
                    if v > best:
                        best, bt = v, t
        if bt is None:
            break
        tab, cur = bt, best
    return tab, cur


out = {}
# 1. toy: corpus "ABAB", n = 2, table A->0, B->1: windows (0,1),(1,0),(0,1) -> codes 1, 14, 1 ; N = 3
lt = np.array([0, 1, 0, 1]); tab = [0, 1] + [2] * 24
q = model(lt, tab, 2)
toy = {"P(01)": round(float(10 ** q[1]), 6), "P(10)": round(float(10 ** q[14]), 6), "P(unseen 00)": round(float(10 ** q[0]), 6),
       "expected": {"P(01)": round(2 / 3, 6), "P(10)": round(1 / 3, 6), "P(unseen 00)": round(0.3 / 3, 6)},
       "score_stream_0101": round(score(lt, tab, np.array([0, 1, 0, 1]), 2), 6),
       "expected_score": round(float((2 * np.log10(2 / 3) + np.log10(1 / 3)) / 3), 6)}
toy["ok"] = bool(toy["P(01)"] == toy["expected"]["P(01)"] and toy["P(10)"] == toy["expected"]["P(10)"]
             and toy["P(unseen 00)"] == toy["expected"]["P(unseen 00)"] and toy["score_stream_0101"] == toy["expected_score"])
out["toy"] = toy
print("toy", toy, flush=True)

files = sorted(glob.glob(LM + "*.txt"))
Afiles = [f for f in files[0::2] if f.rsplit("/", 1)[1] not in HELD]
textA = clean(Afiles)
LA = np.frombuffer(textA.encode(), dtype=np.uint8).astype(np.int64) - 65
PROSE = clean([LM + h for h in HELD])

# 2. agreement with the experiment's scorer (imported only now)
import sys
sys.path.insert(0, "/lab/cipher/round12")
import review_checks as rc
mexp = rc.Model("A", "joint", 6)
rnd = random.Random(424242)
diffs = []
for i in range(50):
    t = [rnd.randrange(13) for _ in range(26)]
    st = rnd.randrange(0, len(PROSE) - 600)
    s = np.array([t[ord(c) - 65] for c in PROSE[st:st + 182]], dtype=np.int64)
    diffs.append(abs(score(LA, t, s) - mexp.score(t, s)))
out["agreement"] = {"pairs": 50, "max_abs_diff": float(max(diffs)), "mean_abs_diff": float(np.mean(diffs))}
print("agreement", out["agreement"], flush=True)

# 3. independent truth-start reruns
pub = {(r["plant"], r["L"]): r for r in json.load(open("/lab/cipher/round12/ident-full.json"))["runs"]
       if r["exp"] == "E1" and r["model"] == "A:joint6" and r["source"] == "prose"}
reruns = []
for p in range(10):
    truth = balanced(textA, 13, random.Random(12000 + p))
    assert truth == rc.pe.balanced_table(rc.TXT["A"], 13, random.Random(12000 + p))   # documented rule matches
    st = random.Random(12500 + p).randrange(0, len(PROSE) - 6000)
    stream = np.array([truth[ord(c) - 65] for c in PROSE[st:st + 182]], dtype=np.int64)
    s_true = score(LA, truth, stream)
    found, s_found = climb(LA, stream, truth)
    wrong = sum(a != b for a, b in zip(found, truth))
    r = {"plant": p, "L": 182, "wrong_raw": wrong, "kept": wrong == 0, "margin": round(s_found - s_true, 7),
         "published_wrong_found": pub[(p, 182)]["wrong_found"], "published_exact": pub[(p, 182)]["exact"]}
    r["same_outcome"] = (r["kept"] == r["published_exact"])
    reruns.append(r)
    print(json.dumps(r), flush=True)
    out["truth_start"] = reruns
    json.dump(out, open("/lab/cipher/audit/ngram_indep.json", "w"), indent=1)
out["summary"] = {"toy_ok": toy["ok"], "max_abs_score_diff_vs_experiment": out["agreement"]["max_abs_diff"],
                  "truth_start_same_kept_flag": sum(r["same_outcome"] for r in reruns),
                  "truth_start_same_wrong_count": sum(r["wrong_raw"] == r["published_wrong_found"] for r in reruns),
                  "runs": len(reruns)}
json.dump(out, open("/lab/cipher/audit/ngram_indep.json", "w"), indent=1)
print(json.dumps(out["summary"], indent=1))
