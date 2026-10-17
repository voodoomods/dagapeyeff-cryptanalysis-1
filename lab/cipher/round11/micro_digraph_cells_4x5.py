"""Micro test (companion to micro_digraph_cells.py): four-square on 4x5 squares (20-letter alphabet, matching the
cipher's 4x5 coordinate grid), and on 4x5 and 5x5 squares with plaintext restricted to its 13 commonest letters.
Counts distinct cipher cells in 182-symbol windows; the D'Agapeyeff message uses 13."""
import json, random, re
import numpy as np
pool = re.sub("[^A-Z]", "", open("/lab/cipher/grille/plain_pool.txt").read())


def run(alphabet, rows, cols, keep_only=None, n=2000):
    size = rows * cols; mins = []; le13 = 0
    for k in range(n):
        rnd = random.Random(k + (777 if keep_only else 0))
        s = rnd.randrange(0, len(pool) - 3000)
        txt = [c for c in pool[s:s + 3000] if c in alphabet]
        if keep_only:
            txt = [c for c in txt if c in keep_only]
        txt = txt[:182]
        P1 = rnd.sample(alphabet, size); P2 = rnd.sample(alphabet, size)
        C1 = rnd.sample(range(size), size); C2 = rnd.sample(range(size), size)
        p1 = {ch: i for i, ch in enumerate(P1)}; p2 = {ch: i for i, ch in enumerate(P2)}
        out = []
        for i in range(0, len(txt) - 1, 2):
            r1, c1 = divmod(p1[txt[i]], cols); r2, c2 = divmod(p2[txt[i + 1]], cols)
            out += [C1[r1 * cols + c2], C2[r2 * cols + c1]]
        d = len(set(out)); mins.append(d); le13 += d <= 13
    m = np.array(mins)
    return {"distinct_cells_min": int(m.min()), "distinct_cells_median": float(np.median(m)),
            "plants_with_13_or_fewer": le13, "plants": n}


a20 = list("ETAOINSHRDLCUMWFGYPB")
a25 = list("ABCDEFGHIKLMNOPQRSTUVWXYZ")
top13 = set("ETAOINSHRDLCU")
out = {"real_distinct_cells": 13,
       "four_square_4x5_20_letters": run(a20, 4, 5),
       "four_square_4x5_text_13_letters": run(a20, 4, 5, keep_only=top13),
       "four_square_5x5_text_13_letters": run(a25, 5, 5, keep_only=top13)}
json.dump(out, open("/lab/cipher/round11/micro-digraph-cells-4x5.json", "w"), indent=1)
print(json.dumps(out, indent=1))
