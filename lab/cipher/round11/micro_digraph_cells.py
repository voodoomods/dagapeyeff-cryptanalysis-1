"""Micro test: can a keyed four-square or two-square produce the cipher's cell usage?

The 182 message symbols of the D'Agapeyeff cipher use exactly 13 distinct cells, almost equally often (F31). For each
system, encipher English with random keys (the engine's own plant(), which enciphers onto 25 Polybius cells), take
182-symbol windows, and count distinct cells and the flatness of their counts. If no plant comes close to 13 cells, the
system is excluded by the data, regardless of how much search time is spent.

    python micro_digraph_cells.py [plants]
"""
import json, random, sys
from collections import Counter
sys.path.insert(0, "/lab/cipher/grille")
sys.path.insert(0, "/app/app")
import numpy as np
from scipy.stats import chisquare
import digraph_engine as de

POOL = open("/lab/cipher/grille/plain_pool.txt").read()
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
out = {"plants_per_system": N, "real": {"distinct_cells": 13, "chi2_p_uniform": 0.73}}
for variant in ("four", "two"):
    distinct, flat, lowest = [], 0, None
    for k in range(N):
        rnd = random.Random(10_000 * (variant == "two") + k)
        start = rnd.randrange(0, len(POOL) - 400)
        cells = np.asarray(de.plant(POOL[start:start + 400], variant, rnd))[:182]
        c = Counter(cells.tolist())
        distinct.append(len(c))
        if len(c) == 13 and chisquare(list(c.values())).pvalue >= 0.05:
            flat += 1
    d = np.array(distinct)
    out[variant] = {"distinct_cells_min": int(d.min()), "distinct_cells_median": float(np.median(d)),
                    "distinct_cells_max": int(d.max()), "plants_with_13_or_fewer": int((d <= 13).sum()),
                    "plants_with_13_and_flat": flat}
    print(variant, out[variant], flush=True)
json.dump(out, open("/lab/cipher/round11/micro-digraph-cells.json", "w"), indent=1)
