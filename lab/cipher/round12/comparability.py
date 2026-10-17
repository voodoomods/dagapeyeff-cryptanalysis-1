"""Round 12, check 5 — are scores comparable across candidate tables? (third review, request 1)

Every candidate table is scored with a language model rebuilt from the corpus mapped through THAT table. This is the
right quantity in principle — the corpus mapped through table t estimates P(group-symbol sequence | t) — but two things
could still make scores incomparable across tables:

  (a) normalization: the six-symbol score floors unseen patterns at a count of 0.3 over a 14^6 grid, so each table's
      model carries a total mass sum(max(c, 0.3)) / sum(c) > 1 that differs from table to table;
  (b) systematic bias: the rebuilding could favor some tables whatever the text.

Tests (no search involved; all on Wells prose, held out of every model):

  1. Mass. For the true table and every single-swap neighbor, the total mass of the six-symbol model and how much it
     varies across tables, compared with the score margins seen in the truth-start test.
  2. Consistency (Gibbs). Score the true table and EVERY single-swap neighbor on held-out streams of 182, 1,092,
     10,000 and 100,000 symbols. For a comparable, unbiased score the fraction of neighbors that beat the truth must
     fall to zero as the text grows. Scores: 'joint' (as used in §6.4), 'jointn' (the same, normalized to mass 1),
     'cond' (chain-rule, 5 before; normalized by construction). Several true tables: the balanced table and 4 others
     made from it by random swaps.
  3. Truth-start rerun with the normalized six-symbol score (prose, corpora A' and B, 50 plants, 182 and 546 symbols),
     same seeds as ident-full.json, to compare with the published joint6 rows.

    python comparability.py [TAG]       -> /lab/cipher/round12/comparability<TAG>.json
"""
import json, random, sys, time
sys.path.insert(0, "/lab/cipher/round12")
import numpy as np
import torch
import review_checks as rc

TAG = sys.argv[1] if len(sys.argv) > 1 else ""
OUT = f"/lab/cipher/round12/comparability{TAG}.json"
BASE = rc.BASE


class NormModel(rc.Model):
    """'jointn': the six-symbol joint score renormalized so that the floored model sums to 1 over its grid."""

    def table(self, tab):
        g = torch.tensor(tab, device=rc.DEV)[self.L]
        c = torch.clamp(torch.bincount(self._codes(g, self.n), minlength=BASE ** self.n).float(), min=0.3)
        return torch.log10(c / c.sum())


def model(corpus, kind):
    return NormModel(corpus, "joint", 6) if kind == "jointn" else rc.Model(corpus, kind, 6)


def neighbors(tab):
    out = []
    for a in range(26):
        for b in range(a + 1, 26):
            if tab[a] != tab[b]:
                t = list(tab); t[a], t[b] = t[b], t[a]
                out.append(t)
    return out


def mass(m, tab):
    g = torch.tensor(tab, device=rc.DEV)[m.L]
    c = torch.bincount(m._codes(g, 6), minlength=BASE ** 6).float()
    return float(torch.clamp(c, min=0.3).sum() / c.sum())


out = {"tag": TAG, "prose_letters": len(rc.PROSE), "mass": {}, "consistency": [], "truth_start": []}
LENGTHS = (182, 1092, 10000, 100000)
enc = lambda tab, s: np.array([tab[ord(ch) - 65] for ch in s], dtype=np.int64)  # noqa: E731

# 1 + 2
for corpus in ("A", "B"):
    base_truth = rc.pe.balanced_table(rc.TXT[corpus], 13, random.Random(1))
    truths = [base_truth]
    rnd = random.Random(777)
    for _ in range(4):
        t = list(base_truth)
        for _ in range(3):
            nb = neighbors(t)
            t = nb[rnd.randrange(len(nb))]
        truths.append(t)
    mj = rc.Model(corpus, "joint", 6)
    ms = [mass(mj, t) for t in [base_truth] + neighbors(base_truth)]
    out["mass"][corpus] = {"tables": len(ms), "mass_min": round(min(ms), 6), "mass_max": round(max(ms), 6),
                           "log10_mass_spread": round(float(np.log10(max(ms)) - np.log10(min(ms))), 7)}
    print("mass", corpus, out["mass"][corpus], flush=True)
    for kind in ("joint", "jointn", "cond"):
        m = model(corpus, kind)
        for ti, truth in enumerate(truths):
            t0 = time.time()
            st = random.Random(4000 + ti).randrange(0, len(rc.PROSE) - max(LENGTHS) - 1)
            streams = {L: torch.tensor(enc(truth, rc.PROSE[st:st + L]), device=rc.DEV) for L in LENGTHS}
            codes = {L: m._codes(s, 6) for L, s in streams.items()}
            sc = lambda tab: {L: float(m.table(tab)[codes[L]].mean()) for L in LENGTHS}  # noqa: E731
            s_true = sc(truth)
            beat = {L: 0 for L in LENGTHS}
            best_margin = {L: -1e9 for L in LENGTHS}
            nbs = neighbors(truth)
            for t in nbs:
                s = sc(t)
                for L in LENGTHS:
                    d = s[L] - s_true[L]
                    beat[L] += d > 1e-6
                    best_margin[L] = max(best_margin[L], d)
            r = {"corpus": corpus, "score": kind, "truth": ti, "neighbors": len(nbs),
                 "beat_truth": {str(L): beat[L] for L in LENGTHS},
                 "best_neighbor_minus_truth": {str(L): round(best_margin[L], 6) for L in LENGTHS},
                 "seconds": round(time.time() - t0, 1)}
            out["consistency"].append(r)
            print(json.dumps(r), flush=True)
            json.dump(out, open(OUT, "w"), indent=1)

# 3: truth-start with the normalized score, same seeds and passages as ident-full.json (E1 prose rows)
for corpus in ("A", "B"):
    m = model(corpus, "jointn")
    for p in range(50):
        truth = rc.pe.balanced_table(rc.TXT[corpus], 13, random.Random(12000 + p))
        st = random.Random(12500 + p).randrange(0, len(rc.PROSE) - 6000)
        for L in (182, 546):
            stream = enc(truth, rc.PROSE[st:st + L])
            s_true = m.score(truth, stream)
            found, s_found = rc.repair(m, stream, truth)
            w = rc.wrong(found, truth)
            r = {"corpus": corpus, "score": "jointn", "plant": p, "L": L, "wrong_found": w, "exact": w == 0,
                 "truth_beaten": w > 0 and s_found > s_true + 1e-6}
            out["truth_start"].append(r)
            print(json.dumps(r), flush=True)
            json.dump(out, open(OUT, "w"), indent=1)

summ = {}
for r in out["truth_start"]:
    k = f"{r['corpus']}:jointn prose L{r['L']}"
    s = summ.setdefault(k, {"plants": 0, "exact": 0, "truth_beaten": 0})
    s["plants"] += 1; s["exact"] += r["exact"]; s["truth_beaten"] += r["truth_beaten"]
cons = {}
for r in out["consistency"]:
    k = f"{r['corpus']}:{r['score']}"
    c = cons.setdefault(k, {str(L): [0, 0] for L in LENGTHS})
    for L in LENGTHS:
        c[str(L)][0] += r["beat_truth"][str(L)]; c[str(L)][1] += r["neighbors"]
out["summary"] = {"truth_start_normalized": summ, "neighbors_beating_truth": cons}
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps(out["summary"], indent=1))
