"""Table given, grille searched: group n-gram order 4 / 5 / 6 over 13 symbols. Judged up to rotation.
Also reports the TRUE order's score under each model (identifiability: found > true means the model, not the search, fails)."""
import json, random, sys, time
sys.path.insert(0, "/lab/cipher/grille")
import numpy as np, torch
import grille_engine as ge, poly_engine as pe

dev = ge.device()
mt = open("/lab/cipher/grille/model_text_big.txt").read()
pool = open("/lab/cipher/grille/plain_pool.txt").read()
STEPS, CHAINS, PLANTS = 80000, 512, 6
out = {"steps": STEPS, "chains": CHAINS, "runs": []}
for t in range(PLANTS):
    rnd = random.Random(300 + t)
    tab = pe.balanced_table(mt, 13, rnd)
    cells, sh = ge.plant_poly(pool[5003 * (t + 1):], tab, True, rnd)
    for n in (4, 5, 6):
        Q = torch.tensor(ge.group_ngrams(mt, tab, n=n, base=13), device=dev)
        t0 = time.time()
        top = ge.anneal(Q, cells, CHAINS, 0, t, True, key=np.arange(30), steps=STEPS, n=n, base=13)
        order = ge.order_for(sh, True)
        g = torch.tensor(cells[order], device=dev)[None, :]
        L = g.shape[1] - n + 1
        q = g[:, :L].clone()
        for j in range(1, n):
            q = q * 13 + g[:, j:j + L]
        true_score = float(Q[q].mean())
        orb, k = ge.match_up_to_rotation(top[0]["shifts"], sh)
        r = {"plant": t, "n": n, "orbits_up_to_rotation": orb, "found_score": top[0]["score"],
             "true_score": round(true_score, 4), "model_fails": top[0]["score"] > true_score and orb < 45,
             "seconds": round(time.time() - t0, 1)}
        out["runs"].append(r)
        print(json.dumps(r), flush=True)
        json.dump(out, open("/lab/cipher/grille/bench-ngram.json", "w"), indent=1)
for n in (4, 5, 6):
    rs = [r for r in out["runs"] if r["n"] == n]
    out[f"solved_n{n}"] = sum(r["orbits_up_to_rotation"] >= 45 for r in rs)
    out[f"model_fails_n{n}"] = sum(r["model_fails"] for r in rs)
json.dump(out, open("/lab/cipher/grille/bench-ngram.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "runs"}))
