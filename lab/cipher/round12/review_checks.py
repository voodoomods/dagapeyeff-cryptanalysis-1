"""Round 12 — checks requested by external review of the identifiability claim (F76) and the four-square exclusion (R34).

    python review_checks.py ident PLANTS LENGTHS TAG      experiments 1-3 (table identifiability)
    python review_checks.py fsq   WINDOWS RESTARTS TAG     experiment 4 (purpose-built four-square key)

1. Natural prose. F76 drew practice plaintexts from plain_pool.txt (words sampled by frequency: no grammar). Here the
   same truth-start test is run on held-out NATURAL prose (two Wells novels, removed from every model) and, paired on
   the same plants, on the word-frequency pool.
2. Calibration. Every table that beats the truth under one model is re-scored (a) under the other, disjoint model and
   (b) on a fresh passage of the same source enciphered with the true table. A genuine competing explanation should
   still win; an artefact of one model's sparse counts should not.
3. Model quality. Combined corpus (all 11 non-held-out books); joint 6-gram score as in F76 vs proper chain-rule
   conditional n-gram scores (add-one smoothed, n = 4, 5, 6).
4. Four-square with a key built on purpose: hill-climb the plaintext squares (and align the cipher squares) to make a
   given 182-letter text use as few cells as possible, then test whether 13 cells can also be as flat as the cipher's.

Writes /lab/cipher/round12/<mode><TAG>.json after every run; prints one JSON line per run (timing included).
"""
import glob, json, random, re, sys, time
from collections import Counter
sys.path.insert(0, "/lab/cipher/grille")
import numpy as np
import torch
import grille_engine as ge, poly_engine as pe

DEV = ge.device()
OUTDIR = "/lab/cipher/round12"
LM = "/lab/cipher/lm/corpus/"
HELD = ["time-machine.txt", "war-of-the-worlds.txt"]          # natural prose, kept out of every model
files = sorted(glob.glob(LM + "*.txt"))
names = [f.rsplit("/", 1)[1] for f in files]
A = [f for f, n in zip(files[0::2], names[0::2]) if n not in HELD]  # F76 corpus A minus the held-out books
B = files[1::2]                                                       # F76 corpus B (contains neither)
clean = lambda fs: re.sub("[^A-Z]", "", "".join(open(f, encoding="utf-8", errors="ignore").read() for f in fs).upper())  # noqa: E731
TXT = {"A": clean(A), "B": clean(B)}
TXT["C"] = TXT["A"] + TXT["B"]
PROSE = clean([LM + h for h in HELD])
POOL = re.sub("[^A-Z]", "", open("/lab/cipher/grille/plain_pool.txt").read())
BASE = 14


# ---------------------------------------------------------------------------------------------- scoring models
class Model:
    """kind 'joint': mean log10 joint n-gram frequency over windows (F76's score, floor count 0.3).
       kind 'cond' : mean log10 P(x_i | previous n-1), add-one smoothed over the 13 symbols (a proper likelihood)."""

    def __init__(self, corpus: str, kind: str, n: int):
        self.L = torch.tensor(ge.letter_ids(TXT[corpus]), device=DEV)
        self.kind, self.n, self.name = kind, n, f"{corpus}:{kind}{n}"
        self.pw = torch.tensor([BASE ** (n - 1 - j) for j in range(n)], device=DEV)

    def _codes(self, g, n):
        m = len(g) - n + 1
        q = g[:m].clone()
        for j in range(1, n):
            q = q * BASE + g[j:j + m]
        return q

    def table(self, tab):
        g = torch.tensor(tab, device=DEV)[self.L]
        c = torch.bincount(self._codes(g, self.n), minlength=BASE ** self.n).float()
        if self.kind == "joint":
            return torch.log10(torch.clamp(c, min=0.3) / c.sum())
        ctx = torch.bincount(self._codes(g, self.n - 1)[: len(g) - self.n + 1], minlength=BASE ** (self.n - 1)).float()
        return torch.log10((c + 1.0) / (ctx.repeat_interleave(BASE) + 13.0))

    def score(self, tab, stream):
        s = torch.tensor(stream, device=DEV)
        return float(self.table(tab)[self._codes(s, self.n)].mean())


def repair(model: Model, stream, init, max_sweeps=8):
    """Steepest ascent over every swap of two letters in different groups (balance kept), as F76."""
    tab = list(init)
    cur = model.score(tab, stream)
    for _ in range(max_sweeps):
        best, best_t = cur, None
        for a in range(26):
            for b in range(a + 1, 26):
                if tab[a] == tab[b]:
                    continue
                t = list(tab); t[a], t[b] = t[b], t[a]
                v = model.score(t, stream)
                if v > best:
                    best, best_t = v, t
        if best_t is None:
            break
        tab, cur = best_t, best
    return tab, cur


def wrong(t, truth):
    """letters whose group differs from the truth, up to relabelling of groups (best label matching)."""
    pairs = Counter(zip(t, truth))
    used_a, used_b, agree = set(), set(), 0
    for (x, y), k in pairs.most_common():
        if x not in used_a and y not in used_b:
            used_a.add(x); used_b.add(y); agree += k
    return 26 - agree


def ident(plants, lengths, tag):
    out = {"held_out_books": HELD, "A": [f.rsplit('/', 1)[1] for f in A], "B": [f.rsplit('/', 1)[1] for f in B],
           "letters": {k: len(v) for k, v in TXT.items()}, "prose_letters": len(PROSE), "runs": []}
    path = f"{OUTDIR}/ident{tag}.json"
    models = {k: Model(*k.split("|")) for k in []}
    def M(corpus, kind, n):
        key = f"{corpus}|{kind}|{n}"
        if key not in models:
            models[key] = Model(corpus, kind, n)
        return models[key]
    # (experiment, model, source, calibration model)
    configs = [("E1", ("A", "joint", 6), "pool", ("B", "joint", 6)), ("E1", ("A", "joint", 6), "prose", ("B", "joint", 6)),
               ("E1", ("B", "joint", 6), "pool", ("A", "joint", 6)), ("E1", ("B", "joint", 6), "prose", ("A", "joint", 6)),
               ("E1c", ("A", "cond", 6), "prose", ("B", "cond", 6)), ("E1c", ("B", "cond", 6), "prose", ("A", "cond", 6)),
               ("E3", ("C", "joint", 6), "prose", None), ("E3", ("C", "cond", 4), "prose", None),
               ("E3", ("C", "cond", 5), "prose", None), ("E3", ("C", "cond", 6), "prose", None)]
    for p in range(plants):
        rnd = random.Random(12000 + p)
        lab = list(range(13)); rnd.shuffle(lab)
        for exp, mk, src, ck in configs:
            corpus = mk[0]
            truth = pe.balanced_table(TXT[corpus], 13, random.Random(12000 + p))
            text = PROSE if src == "prose" else POOL
            st = random.Random(12500 + p).randrange(0, len(text) - 6000)
            model = M(*mk)
            for L in lengths:
                enc = lambda s: np.array([truth[ord(c) - 65] for c in s], dtype=np.int64)  # noqa: E731
                stream, fresh = enc(text[st:st + L]), enc(text[st + 3000:st + 3000 + L])
                t0 = time.time()
                s_true = model.score(truth, stream)
                found, s_found = repair(model, stream, truth)
                w = wrong(found, truth)
                r = {"exp": exp, "plant": p, "L": L, "model": model.name, "source": src, "wrong_found": w,
                     "exact": w == 0, "truth_beaten": w > 0 and s_found > s_true + 1e-6,
                     "margin": round(s_found - s_true, 5)}
                if w > 0:
                    r["fresh_found_minus_truth"] = round(model.score(found, fresh) - model.score(truth, fresh), 5)
                    if ck:
                        cm = M(*ck)
                        r["other_model"] = cm.name
                        r["other_found_minus_truth"] = round(cm.score(found, stream) - cm.score(truth, stream), 5)
                r["seconds"] = round(time.time() - t0, 1)
                out["runs"].append(r)
                print(json.dumps(r), flush=True)
                json.dump(out, open(path, "w"), indent=1)
    summ = {}
    for r in out["runs"]:
        k = f"{r['exp']} {r['model']} {r['source']} L{r['L']}"
        s = summ.setdefault(k, {"plants": 0, "exact": 0, "truth_beaten": 0, "beaten_also_other_model": 0,
                                "beaten_also_fresh_text": 0, "mean_wrong": 0.0, "mean_seconds": 0.0})
        s["plants"] += 1; s["exact"] += r["exact"]; s["truth_beaten"] += r["truth_beaten"]
        s["mean_wrong"] += r["wrong_found"]; s["mean_seconds"] += r["seconds"]
        if r["truth_beaten"]:
            s["beaten_also_other_model"] += r.get("other_found_minus_truth", -1) > 0
            s["beaten_also_fresh_text"] += r.get("fresh_found_minus_truth", -1) > 0
    for s in summ.values():
        s["mean_wrong"] = round(s["mean_wrong"] / s["plants"], 2); s["mean_seconds"] = round(s["mean_seconds"] / s["plants"], 1)
    out["summary"] = summ
    json.dump(out, open(path, "w"), indent=1)
    print(json.dumps(summ, indent=1))


# ---------------------------------------------------------------------------------------------- experiment 4
A25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def fsq_cells(text, rowP1, colP2, rowP2, colP1):
    """cells used by a four-square: symbol 1 from (row of a in P1, col of b in P2), symbol 2 from (row of b in P2,
    col of a in P1). Cipher squares are bijections the encipherer may align freely, so only these pairs matter."""
    s1 = [(rowP1[a], colP2[b]) for a, b in zip(text[0::2], text[1::2])]
    s2 = [(rowP2[b], colP1[a]) for a, b in zip(text[0::2], text[1::2])]
    return Counter(s1), Counter(s2)


def square_from(perm):
    return {ch: divmod(i, 5) for i, ch in enumerate(perm)}


def objective(text, P1, P2):
    q1, q2 = square_from(P1), square_from(P2)
    c1, c2 = fsq_cells(text, {k: v[0] for k, v in q1.items()}, {k: v[1] for k, v in q2.items()},
                       {k: v[0] for k, v in q2.items()}, {k: v[1] for k, v in q1.items()})
    return max(len(c1), len(c2)), c1, c2


def best_flat_merge(c1, c2, k=13):
    """Align the two cipher squares (S2's pairs onto S1's cells) to make the merged counts as flat as possible:
    greedy, largest S2 counts onto smallest S1 counts. Returns merged counts (len = distinct cells used)."""
    a = sorted(c1.values()) + [0] * max(0, len(c2) - len(c1))
    b = sorted(c2.values(), reverse=True) + [0] * max(0, len(a) - len(c2))
    return [x + y for x, y in zip(a, b) if x + y > 0]


def fsq(windows, restarts, tag, iters=20000):
    from scipy.stats import chisquare
    path = f"{OUTDIR}/fsq{tag}.json"
    out = {"windows": windows, "restarts": restarts, "iters": iters, "runs": []}
    src = PROSE
    for w in range(windows):
        rnd = random.Random(31000 + w)
        st = rnd.randrange(0, len(src) - 400)
        text = [c if c != "J" else "I" for c in src[st:st + 182]]
        t0, best = time.time(), None
        for rs in range(restarts):
            P1, P2 = rnd.sample(A25, 25), rnd.sample(A25, 25)
            cur, _, _ = objective(text, P1, P2)
            temp = 2.0
            for it in range(iters):
                which = rnd.random() < 0.5
                P = list(P1 if which else P2)
                i, j = rnd.sample(range(25), 2); P[i], P[j] = P[j], P[i]
                v, _, _ = objective(text, P if which else P1, P2 if which else P)
                if v <= cur or rnd.random() < np.exp((cur - v) / temp):
                    cur = v
                    P1, P2 = (P, P2) if which else (P1, P)
                temp = max(0.05, temp * 0.9997 ** (20000 / iters))
            v, c1, c2 = objective(text, P1, P2)
            if best is None or v < best[0]:
                best = (v, c1, c2, "".join(P1), "".join(P2))
        v, c1, c2, p1, p2 = best
        merged = best_flat_merge(c1, c2)
        r = {"window": w, "min_cells": v, "s1_cells": len(c1), "s2_cells": len(c2), "merged_cells": len(merged),
             "merged_counts": sorted(merged, reverse=True),
             "flat_p_if_13": round(float(chisquare(merged).pvalue), 4) if len(merged) == 13 else None,
             "P1": p1, "P2": p2, "seconds": round(time.time() - t0, 1)}
        out["runs"].append(r)
        print(json.dumps(r), flush=True)
        json.dump(out, open(path, "w"), indent=1)
    m = [r["min_cells"] for r in out["runs"]]
    out["summary"] = {"min_cells_min": min(m), "min_cells_median": float(np.median(m)), "min_cells_max": max(m),
                      "windows_with_13_or_fewer": sum(x <= 13 for x in m),
                      "windows_13_and_flat": sum(1 for r in out["runs"] if (r["flat_p_if_13"] or 0) >= 0.05)}
    json.dump(out, open(path, "w"), indent=1)
    print(json.dumps(out["summary"], indent=1))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "ident":
        ident(int(sys.argv[2]), tuple(int(x) for x in sys.argv[3].split(",")), sys.argv[4] if len(sys.argv) > 4 else "")
    else:
        fsq(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else "",
            int(sys.argv[5]) if len(sys.argv) > 5 else 20000)
