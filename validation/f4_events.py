"""F4: the two different questions about the rare symbols' column, computed side by side (October 17, 2026).

The eight occurrences of the rare symbols (71, 92, 93, 94 and the single 04) sit at 0-based positions
41, 55, 97, 111, 125, 139, 167, 195 of the 196 symbols. Null hypothesis for both: the eight positions are a uniformly
random 8-subset of the 196 (equivalently, the symbol sequence is shuffled; the symbol counts are held fixed).

  A  the report's statistic (F4): for each row length p = 2..20, the largest share of the eight occurrences in one
     column (residue mod p) minus 1/p, the share chance alone would put there; S = max over p. The cipher scores
     1 - 1/14 = 0.929. With eight occurrences, S >= 0.929 only if all eight share one residue at some p >= 14
     (seven of eight scores at most 7/8 - 1/20 = 0.825), so P(S >= 0.929) <= sum over p = 14..20 of
     P(all eight on one residue mod p) - an exact union bound.
  B  a looser question, NOT the report's: are all eight on one residue for ANY p in 2..20? Period 2 dominates
     (all eight odd or all even).

    python validation/f4_events.py [OUT.json]        (numpy)
"""
import json, sys
from math import comb
from pathlib import Path

import numpy as np

N_POS, K = 196, 8
REAL = [41, 55, 97, 111, 125, 139, 167, 195]


def one_residue(p):                 # exact P(all K positions on one residue mod p)
    return sum(comb(len(range(r, N_POS, p)), K) for r in range(p)) / comb(N_POS, K)


exact = {p: one_residue(p) for p in range(2, 21)}
real_S = max(max(np.bincount(np.array(REAL) % p, minlength=p)) / K - 1 / p for p in range(2, 21))

rng = np.random.default_rng(20261017)
M, B = 1_000_000, 50_000
hit_A = hit_B = hit_B_p2 = 0
for _ in range(M // B):
    idx = np.argsort(rng.random((B, N_POS)), axis=1)[:, :K]
    S = np.zeros(B)
    anyp = np.zeros(B, dtype=bool)
    for p in range(2, 21):
        r = idx % p
        top = np.stack([(r == v).sum(1) for v in range(p)], 1).max(1)
        S = np.maximum(S, top / K - 1 / p)
        allone = top == K
        anyp |= allone
        if p == 2:
            p2 = allone
    hit_A += int((S >= real_S - 1e-12).sum())
    hit_B += int(anyp.sum())
    hit_B_p2 += int(p2.sum())

out = {
    "positions": REAL, "null": "uniform random 8-subset of 196 positions (symbol counts fixed)",
    "A_report_statistic": {"definition": "max over p=2..20 of (largest column share - 1/p)", "real_value": round(real_S, 4),
                           "exact_upper_bound": sum(exact[p] for p in range(14, 21)),
                           "per_period_terms_14_20": {p: exact[p] for p in range(14, 21)},
                           "monte_carlo": {"placements": M, "reaching_real": hit_A, "seed": 20261017},
                           "original_run": "0 of 20,000 (random.Random(t), t = 0..19,999) -> (0+1)/(20,000+1) = 5.0e-5; validation/original/f4_original.py"},
    "B_any_period_one_column": {"definition": "all eight on one residue for at least one p in 2..20",
                                "real_meets_it_at": [p for p in range(2, 21) if len({i % p for i in REAL}) == 1],
                                "exact_p2_term": exact[2], "exact_sum_of_terms_2_20": sum(exact.values()),
                                "monte_carlo": {"placements": M, "hits": hit_B, "rate": hit_B / M,
                                                "hits_with_p2": hit_B_p2, "share_from_p2": round(hit_B_p2 / max(hit_B, 1), 4)}},
}
Path(sys.argv[1] if len(sys.argv) > 1 else "f4_events.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
