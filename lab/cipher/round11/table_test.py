"""Round 11 — test candidate polyphonic tables against the grille hypothesis (no model calls; lab GPU).

    python table_test.py validate                      repair check on plants (2 and 4 letters wrong, random table)
    python table_test.py real CANDIDATES.json OUT.json  every candidate on the real cipher + a shuffled-cipher control

Pipeline per table: group 6-gram grille search (80k steps x 512 chains) -> repair the table on the top orders
(letter moves / swaps scored by likelihood with the order fixed) -> grille search again with the repaired table.
The shuffled control runs the SAME pipeline on the cipher's 182 message symbols in random positions: a real break must
score clearly above it (a planted break does by ~0.4 per 6-gram, F73 / bench-tolerance).
"""
import json, random, sys, time
sys.path.insert(0, "/lab/cipher/grille")
import numpy as np, torch
import grille_engine as ge, poly_engine as pe

dev = ge.device()
MT = open("/lab/cipher/grille/model_text_big.txt").read()
LET = ge.letter_ids(MT)
POOL = open("/lab/cipher/grille/plain_pool.txt").read()
STEPS, CHAINS, N, BASE = 80000, 512, 6, 14
KEEP = np.array([p for p in range(196) if p % 14 != 13])


def search(cells, tab, seed):
    Q = torch.tensor(ge.group_ngrams_ids(LET, tab, N, BASE), device=dev)
    top = ge.anneal(Q, cells, CHAINS, 0, seed, True, key=np.arange(30), steps=STEPS, n=N, base=BASE)
    streams = [cells[ge.order_for(np.array(t["shifts"]), True)] for t in top[:3]]
    return top, streams


def pipeline(cells, tab, seed, proposals=300):
    t0 = time.time()
    top1, streams = search(cells, tab, seed)
    rep, rep_score, acc = ge.repair_table(LET, streams, tab, 13, n=N, base=BASE)
    top2, _ = search(cells, rep, seed + 1)
    return {"score_initial": top1[0]["score"], "shifts_initial": top1[0]["shifts"],
            "repair_moves": acc, "table_repaired": rep,
            "score_final": top2[0]["score"], "shifts_final": top2[0]["shifts"], "seconds": round(time.time() - t0, 1)}


def shuffled(cells, seed):
    c = cells.copy()
    vals = c[KEEP].copy()
    np.random.default_rng(seed).shuffle(vals)
    c[KEEP] = vals
    return c


def corrupt(tab, k, rnd):
    t = list(tab)
    while sum(1 for x in range(26) if t[x] != tab[x]) < k:
        a, b = rnd.sample(range(26), 2)
        if t[a] != t[b]:
            t[a], t[b] = t[b], t[a]
    return t


def wrong(t, truth):
    return sum(1 for x in range(26) if t[x] != truth[x])


def validate(out_path):
    out = {"runs": []}
    for p in range(2):
        rnd = random.Random(500 + p)
        truth = pe.balanced_table(MT, 13, rnd)
        cells, sh = ge.plant_poly(POOL[3001 * (p + 1):], truth, True, rnd)
        cases = [("wrong2", corrupt(truth, 2, random.Random(p))), ("wrong4", corrupt(truth, 4, random.Random(p + 9))),
                 ("random", pe.balanced_table(MT, 13, random.Random(900 + p)))]
        if p == 0:
            cases.append(("true_table_on_shuffled_cipher", truth))
        for name, tab in cases:
            c = shuffled(cells, 7) if "shuffled" in name else cells
            r = pipeline(c, tab, 11 * p + len(out["runs"]))
            r.update(case=name, plant=p, wrong_before=wrong(tab, truth), wrong_after=wrong(r["table_repaired"], truth),
                     orbits_initial=ge.match_up_to_rotation(r["shifts_initial"], sh)[0],
                     orbits_final=ge.match_up_to_rotation(r["shifts_final"], sh)[0])
            for k in ("shifts_initial", "shifts_final", "table_repaired"):
                r.pop(k)
            out["runs"].append(r)
            print(json.dumps(r), flush=True)
            json.dump(out, open(out_path, "w"), indent=1)


def real(cand_path, out_path):
    cands = json.load(open(cand_path))
    cells = np.array(json.load(open("/lab/cipher/round11/real_cells.json")), dtype=np.int64)
    out = {"runs": []}
    for i, c in enumerate(cands):
        tab = c["table"]
        r = pipeline(cells, tab, 100 + i)
        null = pipeline(shuffled(cells, 1000 + i), tab, 200 + i)
        r.update(name=c["name"], page=c.get("page"), freq_chi2_p=c.get("freq_chi2_p"),
                 null_score_final=null["score_final"], margin=round(r["score_final"] - null["score_final"], 4))
        order = ge.order_for(np.array(r["shifts_final"]), True)
        r["symbols_in_order"] = cells[order].tolist()
        out["runs"].append(r)
        print(json.dumps({k: v for k, v in r.items() if k not in ("symbols_in_order", "shifts_initial", "shifts_final")}),
              flush=True)
        json.dump(out, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    if sys.argv[1] == "validate":
        validate("/lab/cipher/round11/validate.json")
    else:
        real(sys.argv[2], sys.argv[3])
