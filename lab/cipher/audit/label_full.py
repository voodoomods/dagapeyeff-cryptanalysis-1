"""Audit D (2026-10-15) — greedy vs exact group-label matching on ALL 2,000 robustness runs (ident-full.json).

ident-full.json stores 'wrong_found' (greedy distance) but not the recovered tables, so every run is regenerated
deterministically: same code path as review_checks.ident (original functions review_checks.Model / repair / wrong,
same seeds 12000+p / 12500+p, same passages). ident-full.json is read, never written.

For every run: the recovered table; distances raw (letterwise, no relabelling), greedy (review_checks.wrong) and
exact (maximum-weight one-to-one assignment of the 13 labels, scipy.optimize.linear_sum_assignment); exact /
truth_beaten under each distance; the fresh-passage and other-corpus score differences; and agreement of every
regenerated field with the published record.

    python label_full.py   ->  /lab/cipher/audit/label_full.json
"""
import json, random, sys, time
sys.path.insert(0, "/lab/cipher/round12")
import numpy as np
from scipy.optimize import linear_sum_assignment
import review_checks as rc


def exact_distance(t, truth):
    m = np.zeros((13, 13))
    for a, b in zip(t, truth):
        m[a, b] += 1
    r, c = linear_sum_assignment(m, maximize=True)
    return 26 - int(m[r, c].sum())


def raw_distance(t, truth):
    return sum(a != b for a, b in zip(t, truth))


pub = {(r["exp"], r["model"], r["source"], r["plant"], r["L"]): r for r in json.load(open("/lab/cipher/round12/ident-full.json"))["runs"]}
configs = [("E1", ("A", "joint", 6), "pool", ("B", "joint", 6)), ("E1", ("A", "joint", 6), "prose", ("B", "joint", 6)),
           ("E1", ("B", "joint", 6), "pool", ("A", "joint", 6)), ("E1", ("B", "joint", 6), "prose", ("A", "joint", 6)),
           ("E1c", ("A", "cond", 6), "prose", ("B", "cond", 6)), ("E1c", ("B", "cond", 6), "prose", ("A", "cond", 6)),
           ("E3", ("C", "joint", 6), "prose", None), ("E3", ("C", "cond", 4), "prose", None),
           ("E3", ("C", "cond", 5), "prose", None), ("E3", ("C", "cond", 6), "prose", None)]
assert len(configs) == 10
models = {}
M = lambda k: models.setdefault(k, rc.Model(*k))  # noqa: E731
out = {"runs": []}
t0 = time.time()
for p in range(50):
    for exp, mk, src, ck in configs:
        corpus = mk[0]
        truth = rc.pe.balanced_table(rc.TXT[corpus], 13, random.Random(12000 + p))
        text = rc.PROSE if src == "prose" else rc.POOL
        st = random.Random(12500 + p).randrange(0, len(text) - 6000)
        model = M(mk)
        for L in (182, 273, 364, 546):
            enc = lambda s: np.array([truth[ord(c) - 65] for c in s], dtype=np.int64)  # noqa: E731
            stream, fresh = enc(text[st:st + L]), enc(text[st + 3000:st + 3000 + L])
            s_true = model.score(truth, stream)
            found, s_found = rc.repair(model, stream, truth)
            g, x, r = rc.wrong(found, truth), exact_distance(found, truth), raw_distance(found, truth)
            rec = {"exp": exp, "model": model.name, "source": src, "plant": p, "L": L, "table": found,
                   "greedy": g, "exact": x, "raw": r, "margin": round(s_found - s_true, 5),
                   "beaten_greedy": g > 0 and s_found > s_true + 1e-6, "beaten_exact": x > 0 and s_found > s_true + 1e-6}
            if g > 0 or x > 0:
                rec["fresh"] = round(model.score(found, fresh) - model.score(truth, fresh), 5)
                if ck:
                    cm = M(ck)
                    rec["other"] = round(cm.score(found, stream) - cm.score(truth, stream), 5)
            P = pub[(exp, model.name, src, p, L)]
            rec["matches_published"] = (P["wrong_found"] == g and P["exact"] == (g == 0) and P["truth_beaten"] == rec["beaten_greedy"]
                                        and P["margin"] == rec["margin"] and P.get("fresh_found_minus_truth") == rec.get("fresh")
                                        and P.get("other_found_minus_truth") == rec.get("other"))
            out["runs"].append(rec)
        print(json.dumps({"p": p, "exp": exp, "model": model.name, "src": src, "runs": len(out["runs"]),
                          "elapsed_min": round((time.time() - t0) / 60, 1)}), flush=True)
    json.dump(out, open("/lab/cipher/audit/label_full.json", "w"))

R = out["runs"]
by = {}
for r in R:
    k = f"{r['exp']} {r['model']} {r['source']} L{r['L']}"
    s = by.setdefault(k, {"runs": 0, "greedy_ne_exact": 0, "mean_wrong_greedy": 0.0, "mean_wrong_exact": 0.0, "mean_wrong_raw": 0.0,
                          "exact_flag_changes": 0, "beaten_flag_changes": 0})
    s["runs"] += 1; s["greedy_ne_exact"] += r["greedy"] != r["exact"]
    s["mean_wrong_greedy"] += r["greedy"]; s["mean_wrong_exact"] += r["exact"]; s["mean_wrong_raw"] += r["raw"]
    s["exact_flag_changes"] += (r["greedy"] == 0) != (r["exact"] == 0)
    s["beaten_flag_changes"] += r["beaten_greedy"] != r["beaten_exact"]
for s in by.values():
    for k in ("mean_wrong_greedy", "mean_wrong_exact", "mean_wrong_raw"):
        s[k] = round(s[k] / s["runs"], 2)
out["by_setup"] = by
out["summary"] = {"runs": len(R), "matches_published_all_fields": sum(r["matches_published"] for r in R),
                  "greedy_ne_exact": sum(r["greedy"] != r["exact"] for r in R),
                  "greedy_minus_exact_values": sorted({r["greedy"] - r["exact"] for r in R}),
                  "exact_flag_changes": sum((r["greedy"] == 0) != (r["exact"] == 0) for r in R),
                  "truth_beaten_flag_changes": sum(r["beaten_greedy"] != r["beaten_exact"] for r in R),
                  "pure_relabellings": sum(r["raw"] > 0 and r["exact"] == 0 for r in R),
                  "raw_ne_exact": sum(r["raw"] != r["exact"] for r in R)}
json.dump(out, open("/lab/cipher/audit/label_full.json", "w"))
print(json.dumps(out["summary"], indent=1))
