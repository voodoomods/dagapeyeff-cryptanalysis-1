"""Audit A (2026-10-15) — independent reconstruction of the purpose-built four-square results (O33).

Independent of the experiment code: does NOT import review_checks.py or fsq_order.py. Re-derives, from the two held-out
Wells texts, the recorded window seeds and the stored P1/P2 keys in fsq-full.json:
  1. the four-square symbol streams, S1/S2 cell counts, merged cell counts (documented alignment rule: S1 pairs in
     ascending count order and S2 pairs in descending count order share cell ids), compared with the stored records;
  2. the chi-square flatness p-values from the 13-cell count vectors, via the regularized upper incomplete gamma
     function (not scipy.stats.chisquare);
  3. the order test with its own mutual-information code and FRESH shuffles (numpy PCG64, seed 20261015, 5,000
     shuffles), under two family-wise min-p conventions:
        'orig'  — shuffle p-values (1 + #{all shuffles >= it, itself included}) / (B + 1), as in fsq_order.py;
        'loo'   — shuffle p-values (1 + #{other shuffles >= it}) / B, the exchangeable leave-one-out convention.
     Classification at alpha = 0.05 is compared with fsq-order.json.

    python audit_fsq.py   ->  /lab/cipher/audit/audit_fsq.json
"""
import json, math, random, re
from collections import Counter
import numpy as np
from scipy.special import gammaincc

LM = "/lab/cipher/lm/corpus/"
HELD = ["time-machine.txt", "war-of-the-worlds.txt"]
PROSE = re.sub("[^A-Z]", "", "".join(open(LM + f, encoding="utf-8", errors="ignore").read() for f in HELD).upper())
A25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
FULL = json.load(open("/lab/cipher/round12/fsq-full.json"))
ORDER = json.load(open("/lab/cipher/round12/fsq-order.json"))
B = 5000
ALPHA = 0.05
rng = np.random.Generator(np.random.PCG64(20261015))


def window(w):
    st = random.Random(31000 + w).randrange(0, len(PROSE) - 400)
    return [c if c != "J" else "I" for c in PROSE[st:st + 182]]


def four_square(text, P1, P2):
    pos1 = {ch: divmod(i, 5) for i, ch in enumerate(P1)}
    pos2 = {ch: divmod(i, 5) for i, ch in enumerate(P2)}
    s1, s2 = [], []
    for a, b in zip(text[0::2], text[1::2]):
        s1.append((pos1[a][0], pos2[b][1]))       # row of a in P1, column of b in P2
        s2.append((pos2[b][0], pos1[a][1]))       # row of b in P2, column of a in P1
    return s1, s2


def aligned_stream(s1, s2):
    c1, c2 = Counter(s1), Counter(s2)
    ids1 = {k: i for i, k in enumerate(sorted(c1, key=lambda k: (c1[k], s1.index(k))))}
    ids2 = {k: i for i, k in enumerate(sorted(c2, key=lambda k: (-c2[k], s2.index(k))))}
    out = []
    for x, y in zip(s1, s2):
        out += [ids1[x], ids2[y]]
    return np.array(out, dtype=np.int64)


def chisq_p(counts):
    n, k = sum(counts), len(counts)
    e = n / k
    chi2 = sum((o - e) ** 2 / e for o in counts)
    return float(gammaincc((k - 1) / 2, chi2 / 2))


def mutual_info(x, y):
    k = int(max(x.max(), y.max())) + 1
    j = np.zeros((k, k))
    np.add.at(j, (x, y), 1)
    j /= j.sum()
    px, py = j.sum(1), j.sum(0)
    m = j > 0
    return float((j[m] * np.log2(j[m] / np.outer(px, py)[m])).sum())


def stats(s):
    return np.array([mutual_info(s[0:-1:2], s[1::2]), mutual_info(s[1:-1:2], s[2::2]),
                     max(mutual_info(s[:-L], s[L:]) for L in range(1, 27))])


def order_test(s):
    obs = stats(s)
    sh = np.array([stats(rng.permutation(s)) for _ in range(B)])
    p_obs = (1 + (sh >= obs).sum(0)) / (B + 1)
    ge = sh[None, :, :] >= sh[:, None, :]                      # ge[b, b', i] : T_b'i >= T_bi
    cnt_all = ge.sum(1)                                          # includes b itself
    p_orig = (1 + cnt_all) / (B + 1)
    p_loo = (1 + cnt_all - 1) / B
    fam = {name: float((1 + (p.min(1) <= p_obs.min()).sum()) / (B + 1)) for name, p in (("orig", p_orig), ("loo", p_loo))}
    return {"p": [round(float(x), 4) for x in p_obs], "family_orig": round(fam["orig"], 4), "family_loo": round(fam["loo"], 4)}


out = {"prose_letters": len(PROSE), "shuffles": B, "seed": 20261015, "alpha": ALPHA, "windows": [], "random_key": []}
stored_order = {x["window"]: x for x in ORDER["purpose_built"]}
stored_rand = {x["window"]: x for x in ORDER["random_key"]}
for r in FULL["runs"]:
    w = r["window"]
    text = window(w)
    s1, s2 = four_square(text, r["P1"], r["P2"])
    merged = sorted([a + b for a, b in zip(sorted(Counter(s1).values()) + [0] * max(0, len(set(s2)) - len(set(s1))),
                                           sorted(Counter(s2).values(), reverse=True) + [0] * max(0, len(set(s1)) - len(set(s2))))
                     if a + b > 0], reverse=True)
    rec = {"window": w, "s1_cells": len(set(s1)), "s2_cells": len(set(s2)), "merged_counts": merged,
           "matches_stored": (len(set(s1)), len(set(s2)), merged) == (r["s1_cells"], r["s2_cells"], r["merged_counts"])}
    if len(merged) == 13:
        rec["chisq_p"] = round(chisq_p(merged), 6)
        rec["chisq_matches_stored"] = abs(rec["chisq_p"] - r["flat_p_if_13"]) < 5e-5
    stream = aligned_stream(s1, s2)
    t = order_test(stream)
    rec.update(order=t, stored_family_p=stored_order[w]["family_p"])
    out["windows"].append(rec)
    kr = random.Random(55000 + w)
    k1, k2 = kr.sample(A25, 25), kr.sample(A25, 25)
    rs1, rs2 = four_square(text, k1, k2)
    t2 = order_test(aligned_stream(rs1, rs2))
    out["random_key"].append({"window": w, "order": t2, "stored_family_p": stored_rand[w]["family_p"]})
    print(json.dumps({"w": w, "match": rec["matches_stored"], "fam": t["family_orig"], "stored": stored_order[w]["family_p"]}), flush=True)
    json.dump(out, open("/lab/cipher/audit/audit_fsq.json", "w"), indent=1)

flat = [x for x in out["windows"] if len(x["merged_counts"]) == 13 and x.get("chisq_p", 0) >= ALPHA]
def flagged(rows, key): return sorted(x["window"] for x in rows if x["order"][key] < ALPHA)
out["summary"] = {
    "streams_matching_stored": sum(x["matches_stored"] for x in out["windows"]),
    "chisq_matching_stored": sum(x.get("chisq_matches_stored", False) for x in out["windows"]),
    "flat_13_windows": sorted(x["window"] for x in flat),
    "flat_13_flagged_orig": flagged(flat, "family_orig"),
    "flat_13_flagged_loo": flagged(flat, "family_loo"),
    "flat_13_pair_stat_p_below_alpha": sorted(x["window"] for x in flat if min(x["order"]["p"][:2]) < ALPHA),
    "purpose_built_flagged_orig": len(flagged(out["windows"], "family_orig")),
    "purpose_built_flagged_loo": len(flagged(out["windows"], "family_loo")),
    "random_key_flagged_orig": len(flagged(out["random_key"], "family_orig")),
    "random_key_flagged_loo": len(flagged(out["random_key"], "family_loo")),
    "stored": {"flat_13_flagged": sorted(w for w in (x["window"] for x in flat) if stored_order[w]["family_p"] < ALPHA),
               "purpose_built_flagged": sum(x["family_p"] < ALPHA for x in ORDER["purpose_built"]),
               "random_key_flagged": sum(x["family_p"] < ALPHA for x in ORDER["random_key"])},
}
json.dump(out, open("/lab/cipher/audit/audit_fsq.json", "w"), indent=1)
print(json.dumps(out["summary"], indent=1))
