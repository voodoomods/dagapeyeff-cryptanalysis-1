"""Audit B (2026-10-15) — group-label matching in the truth-start test.

Question: round12/review_checks.py measures distance from the true table with a GREEDY relabelling match; round11/
identifiability.py with a RAW letterwise comparison. Could either change the reported 'exact' / 'wrong_found' /
'truth_beaten' flags?

The stored records keep only 'wrong_found', not the final tables, so the tables are REGENERATED here by re-running the
original searches (original-script rerun: review_checks.repair / grille_engine.repair_table, same seeds) for a
representative subset, and each final table is compared with the truth three ways:
  raw      letters whose group id differs (no relabelling)
  greedy   review_checks.wrong (greedy pair-count matching)
  optimal  exact maximum-weight assignment of the 13 group ids (scipy.optimize.linear_sum_assignment)
Also: a constructed counterexample where greedy and optimal differ, and whether any final table is a pure relabelling
of the truth (raw > 0, optimal = 0).

Subset: round12 — plants 0-9, every setup, 182 and 546 symbols (200 runs); round11 F76 — plants 0-9, corpora A and B,
182 symbols, start = truth (20 runs).

    python label_audit.py   ->  /lab/cipher/audit/label_audit.json
"""
import glob, json, random, re, sys
sys.path.insert(0, "/lab/cipher/round12")
sys.path.insert(0, "/lab/cipher/grille")
import numpy as np
from scipy.optimize import linear_sum_assignment
import review_checks as rc
import grille_engine as ge, poly_engine as pe


def raw(t, truth):
    return sum(a != b for a, b in zip(t, truth))


def optimal(t, truth):
    m = np.zeros((13, 13))
    for a, b in zip(t, truth):
        m[a, b] += 1
    r, c = linear_sum_assignment(-m)
    return 26 - int(m[r, c].sum())


def compare(t, truth):
    return {"raw": raw(t, truth), "greedy": rc.wrong(t, truth), "optimal": optimal(t, truth)}


out = {}
# counterexample (7 letters, two found groups a/b, two true groups x/y): a&x=3, a&y=2, b&x=2, b&y=0
found = [0, 0, 0, 0, 0, 1, 1]
truth = [0, 0, 0, 1, 1, 0, 0]
pad_f, pad_t = found + list(range(2, 13)) * 2, truth + list(range(2, 13)) * 2
pad_f, pad_t = pad_f[:26], pad_t[:26]
out["counterexample"] = {"found": pad_f, "truth": pad_t, **compare(pad_f, pad_t),
                         "note": "greedy takes the largest cell (a,x)=3 first and is left with (b,y)=0; optimal pairs (a,y)+(b,x)=4"}
print("counterexample", out["counterexample"], flush=True)

# round12 subset: same seeds and passages as ident-full.json
full = {(r["exp"], r["model"], r["source"], r["plant"], r["L"]): r for r in json.load(open("/lab/cipher/round12/ident-full.json"))["runs"]}
configs = [("E1", ("A", "joint", 6), "pool"), ("E1", ("A", "joint", 6), "prose"), ("E1", ("B", "joint", 6), "pool"),
           ("E1", ("B", "joint", 6), "prose"), ("E1c", ("A", "cond", 6), "prose"), ("E1c", ("B", "cond", 6), "prose"),
           ("E3", ("C", "joint", 6), "prose"), ("E3", ("C", "cond", 4), "prose"), ("E3", ("C", "cond", 5), "prose"),
           ("E3", ("C", "cond", 6), "prose")]
models, rows = {}, []
for p in range(10):
    for exp, mk, src in configs:
        m = models.setdefault(mk, rc.Model(*mk))
        truth = pe.balanced_table(rc.TXT[mk[0]], 13, random.Random(12000 + p))
        text = rc.PROSE if src == "prose" else rc.POOL
        st = random.Random(12500 + p).randrange(0, len(text) - 6000)
        for L in (182, 546):
            stream = np.array([truth[ord(c) - 65] for c in text[st:st + L]], dtype=np.int64)
            found_t, s_found = rc.repair(m, stream, truth)
            d = compare(found_t, truth)
            pub = full[(exp, m.name, src, p, L)]
            rows.append({"exp": exp, "model": m.name, "source": src, "plant": p, "L": L, **d,
                         "published_wrong_found": pub["wrong_found"], "published_exact": pub["exact"],
                         "table": found_t, "truth": truth})
            print(json.dumps({k: rows[-1][k] for k in ("model", "source", "plant", "L", "raw", "greedy", "optimal", "published_wrong_found")}), flush=True)
            out["round12"] = rows
            json.dump(out, open("/lab/cipher/audit/label_audit.json", "w"), indent=1)

# round11 F76 subset: identifiability.py's corpus halves, seeds (tag '-big' -> 9000 + p) and repair call
files = sorted(glob.glob("/lab/cipher/lm/corpus/*.txt"))
POOL = re.sub("[^A-Z]", "", open("/lab/cipher/grille/plain_pool.txt").read())
pub11 = {}
rows11 = []
for c in "AB":
    half = files[0::2] if c == "A" else files[1::2]
    text = re.sub("[^A-Z]", "", "".join(open(f, encoding="utf-8", errors="ignore").read() for f in half).upper())
    LET = ge.letter_ids(text)
    pub11 = {(r["plant"], r["L"]): r for r in json.load(open(f"/lab/cipher/round11/identifiability-{c}-big.json"))["runs"] if r["start"] == "truth"}
    for p in range(10):
        rnd = random.Random(9000 + p)
        truth = pe.balanced_table(text, 13, rnd)
        start = rnd.randrange(0, len(POOL) - 1500)
        stream = np.array([truth[ord(ch) - 65] for ch in POOL[start:start + 182]], dtype=np.int64)
        found_t, s_found, changes = ge.repair_table(LET, [stream], truth, 13, max_sweeps=8, n=6, base=14, moves=False)
        d = compare(found_t, truth)
        rows11.append({"corpus": c, "plant": p, "L": 182, **d, "published_wrong_found": pub11[(p, 182)]["wrong_found"],
                       "published_exact": pub11[(p, 182)]["exact"], "table": found_t, "truth": truth})
        print(json.dumps({k: rows11[-1][k] for k in ("corpus", "plant", "raw", "greedy", "optimal", "published_wrong_found")}), flush=True)
        out["round11"] = rows11
        json.dump(out, open("/lab/cipher/audit/label_audit.json", "w"), indent=1)

allr = rows + rows11
out["summary"] = {
    "runs": len(allr),
    "greedy_equals_optimal": sum(r["greedy"] == r["optimal"] for r in allr),
    "raw_equals_optimal": sum(r["raw"] == r["optimal"] for r in allr),
    "pure_relabellings (raw>0, optimal=0)": sum(r["raw"] > 0 and r["optimal"] == 0 for r in allr),
    "exact_flag_same_under_all_three": sum((r["raw"] == 0) == (r["greedy"] == 0) == (r["optimal"] == 0) for r in allr),
    "round12_regenerated_greedy_equals_published": sum(r["greedy"] == r["published_wrong_found"] for r in rows),
    "round11_regenerated_raw_equals_published": sum(r["raw"] == r["published_wrong_found"] for r in rows11),
}
json.dump(out, open("/lab/cipher/audit/label_audit.json", "w"), indent=1)
print(json.dumps(out["summary"], indent=1))
