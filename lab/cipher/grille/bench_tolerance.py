"""How wrong may the polyphonic TABLE be before the table-given grille search (group 6-grams) fails?
Corrupt the true table by swapping letters between groups (k letters misplaced, balance kept), search the grille with
the corrupted table, judge orbits up to rotation. Also report the score of the true order under the corrupted model."""
import json, random, sys, time
sys.path.insert(0, "/lab/cipher/grille")
import numpy as np, torch
import grille_engine as ge, poly_engine as pe

dev = ge.device()
mt = open("/lab/cipher/grille/model_text_big.txt").read()
pool = open("/lab/cipher/grille/plain_pool.txt").read()
STEPS, CHAINS, N = 80000, 512, 6
LEVELS, PLANTS = (0, 2, 4, 6, 8, 12), 4
OUT = "/lab/cipher/grille/bench-tolerance.json"


def corrupt(tab, k, rnd):
    """Swap letters between different groups until k letters sit in a wrong group (k even; balance kept)."""
    t = list(tab)
    letters = list(range(26))
    rnd.shuffle(letters)
    moved = set()
    i = 0
    while len(moved) < k and i < len(letters) - 1:
        a = letters[i]
        b = next((x for x in letters[i + 1:] if x not in moved and t[x] != t[a] and x != a), None)
        i += 1
        if b is None or a in moved:
            continue
        t[a], t[b] = t[b], t[a]
        moved |= {a, b}
    wrong = sum(1 for x in range(26) if t[x] != tab[x])
    return t, wrong


out = {"steps": STEPS, "chains": CHAINS, "n": N, "runs": []}
for t in range(PLANTS):
    rnd = random.Random(400 + t)
    tab = pe.balanced_table(mt, 13, rnd)
    cells, sh = ge.plant_poly(pool[4001 * (t + 1):], tab, True, rnd)
    for k in LEVELS:
        ctab, wrong = corrupt(tab, k, random.Random(1000 * t + k))
        Q = torch.tensor(ge.group_ngrams(mt, ctab, n=N, base=13), device=dev)
        t0 = time.time()
        top = ge.anneal(Q, cells, CHAINS, 0, 7 * t + k, True, key=np.arange(30), steps=STEPS, n=N, base=13)
        orb, _ = ge.match_up_to_rotation(top[0]["shifts"], sh)
        r = {"plant": t, "misplaced": wrong, "orbits_up_to_rotation": orb, "solved": orb >= 45,
             "found_score": top[0]["score"], "seconds": round(time.time() - t0, 1)}
        out["runs"].append(r)
        print(json.dumps(r), flush=True)
        json.dump(out, open(OUT, "w"), indent=1)
summary = {}
for k in LEVELS:
    rs = [r for r in out["runs"] if r["misplaced"] == k]
    if rs:
        summary[k] = {"solved": sum(r["solved"] for r in rs), "of": len(rs),
                      "mean_orbits": round(sum(r["orbits_up_to_rotation"] for r in rs) / len(rs), 1)}
out["summary"] = summary
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps(summary))
