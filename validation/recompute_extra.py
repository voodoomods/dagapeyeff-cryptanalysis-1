"""Independent recomputation of claims that rest on the platform's ad-hoc analyses (validation, October 16, 2026).

These are NEW implementations from the definitions stated in the report and case file, not reruns of the original
code (which is not in this repository); where a definition had to be made concrete it is stated in the output.

  F4   all eight rare-symbol occurrences (71, 92, 93, 94, 04) fall in one column when the 196 symbols are laid out 14
       per row; chance under random placement, with the period scan of the platform's grid_profile (exact bound plus
       200,000 shuffles).
  F32  the 182 message symbols show no order: rows, columns and halves (chi-square vs 5,000 shuffles) and maximum
       mutual information over lags 1..26 in reading and column order (family-wise over both orders, min-p).
  R29  a balanced 13-group table WITHOUT a transposition leaves lag-1 dependence: 40 planted 182-symbol texts from the
       word sample, each tested against 400 shuffles; and the real message on the same test.

    python recompute_extra.py   (numpy; R29 also imports lab/cipher/grille/poly_engine.py)
"""
import json, math, random, sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LAB = HERE.parent / "lab" / "cipher"
digits = "".join(ch for ch in (HERE.parent / "data" / "ciphertext.txt").read_text() if ch.isdigit())
PAIRS = [digits[i:i + 2] for i in range(0, 392, 2)]
RARE = {"71", "92", "93", "94", "04"}
out = {}

# ---- F4  (statistic of the platform tool grid_profile: max over periods p = 2..20 of [largest share of rare
#            occurrences on one residue mod p] - 1/p; the real text scores 1 - 1/14 = 0.929 at p = 14)
from math import comb
rare_pos = [i for i, p in enumerate(PAIRS) if p in RARE]
k = len(rare_pos)
def align(ps):
    return max(max(Counter(i % q for i in ps).values()) / len(ps) - 1 / q for q in range(2, 21))
a_real = align(rare_pos)
# Exact: with 8 occurrences a score >= 0.929 needs all 8 on one residue at some p >= 14 (7 of 8 gives at most 0.875),
# so P <= sum over p = 14..20 of P(all 8 on one residue mod p)  (union bound).
exact = {q: sum(comb(len(range(r, 196, q)), k) for r in range(q)) / comb(196, k) for q in range(14, 21)}
union = sum(exact.values())
rng = np.random.default_rng(20261016)
N, ge = 200_000, 0
for _ in range(N // 20_000):
    idx = np.argsort(rng.random((20_000, 196)), axis=1)[:, :k]
    best = np.zeros(20_000)
    for q in range(2, 21):
        r = idx % q
        top = np.stack([(r == v).sum(1) for v in range(q)], 1).max(1)
        best = np.maximum(best, top / k - 1 / q)
    ge += int((best >= a_real - 1e-12).sum())
naive_periods = [w for w in range(2, 21) if len({i % w for i in rare_pos}) == 1]
out["F4"] = {"rare_occurrences": k, "rare_positions_0based": rare_pos, "statistic": "max_p(top residue share - 1/p), p = 2..20",
             "real_statistic": round(a_real, 4), "exact_union_bound_p": union, "exact_one_in": round(1 / union),
             "shuffles": N, "shuffles_reaching_real": ge,
             "note": ("A cruder statistic - 'all eight on one residue for ANY p in 2..20' - is reached by chance in about 0.7% "
                      "of shuffles, almost all at p = 2 (all eight odd or all even: exactly 0.0067, about 1 in 149; validation/f4_events.py); the real text meets it at p = "
                      + ", ".join(map(str, naive_periods)) + ". The published odds rest on the excess-over-1/p statistic."),
             "claim": "odds below 1 in 20,000 after allowing for every row length from 2 to 20",
             "pass": bool(union < 1 / 20000 and ge == 0)}
print("F4", out["F4"], flush=True)

# ---- F32
msg = [p for i, p in enumerate(PAIRS) if i % 14 != 13]           # 182 symbols, 14 rows x 13 columns
codes = {s: i for i, s in enumerate(sorted(set(msg)))}
m = np.array([codes[s] for s in msg])
col_order = np.array([i * 13 + c for c in range(13) for i in range(14)])

def mi(x, y, k):
    j = np.zeros((k, k)); np.add.at(j, (x, y), 1); j /= j.sum()
    px, py = j.sum(1), j.sum(0); nz = j > 0
    return float((j[nz] * np.log2(j[nz] / np.outer(px, py)[nz])).sum())

def max_mi(seq, k=13):
    return max(mi(seq[:-L], seq[L:], k) for L in range(1, 27))

def stats(seq):
    return np.array([max_mi(seq), max_mi(seq[col_order])])

def chi_table(rows_of_codes, k=13):
    t = np.zeros((len(rows_of_codes), k))
    for r, row in enumerate(rows_of_codes):
        np.add.at(t[r], row, 1)
    e = t.sum(1, keepdims=True) * t.sum(0, keepdims=True) / t.sum()
    nz = e > 0
    return float((((t - e) ** 2)[nz] / e[nz]).sum())

def layout_stats(seq):
    g = seq.reshape(14, 13)
    return np.array([chi_table(list(g)), chi_table(list(g.T)), chi_table([g[:7].ravel(), g[7:].ravel()]),
                     chi_table([g[:, :6].ravel(), g[:, 7:].ravel()])])

rs = random.Random(20261016)
obs = stats(m)
B = 5000
sh = np.array([stats(np.array(rs.sample(list(m), len(m)))) for _ in range(B)])
p_obs = (1 + (sh >= obs).sum(0)) / (B + 1)
p_sh = (1 + (sh[None, :, :] >= sh[:, None, :]).sum(1) - 1) / B
fam = (1 + (p_sh.min(1) <= p_obs.min()).sum()) / (B + 1)
lay_obs = layout_stats(m)
lay_sh = np.array([layout_stats(np.array(rs.sample(list(m), len(m)))) for _ in range(B)])
lay_p = (1 + (lay_sh >= lay_obs).sum(0)) / (B + 1)
out["F32_layout"] = {"rows_p": round(float(lay_p[0]), 3), "columns_p": round(float(lay_p[1]), 3),
                     "top_vs_bottom_p": round(float(lay_p[2]), 3), "left_vs_right_p": round(float(lay_p[3]), 3),
                     "published": {"rows": 0.08, "columns": 0.30, "top_vs_bottom": 0.10, "left_vs_right": 0.60},
                     "note": "left vs right = columns 1-6 vs 8-13 (the published split of 13 columns is not recorded)",
                     "pass": bool(min(lay_p) > 0.05)}
print("F32 layout", out["F32_layout"], flush=True)
out["F32_lag_component"] = {"reading_order_max_mi_p": round(float(p_obs[0]), 4), "column_order_max_mi_p": round(float(p_obs[1]), 4),
                            "family_p": round(float(fam), 4), "shuffles": B,
                            "claim": "no lagged dependence at lags 1-26 in reading or column order, family-wise p = 0.91",
                            "note": "case F32: the family-wise 0.91 is the lag-dependence family (lags 1-26, reading and column order); rows, columns and halves are reported separately in F32_layout",
                            "pass": bool(fam > 0.05)}
print("F32", out["F32_lag_component"], flush=True)

# ---- R29
sys.path.insert(0, str(LAB / "grille"))
import poly_engine as pe
pool = (LAB / "grille" / "plain_pool.txt").read_text()
model_text = (LAB / "grille" / "model_text_big.txt").read_text() if (LAB / "grille" / "model_text_big.txt").exists() else pool
rr = random.Random(29)

def lag1_p(seq, k, shuffles=400):
    seq = np.array(seq)
    real = mi(seq[:-1], seq[1:], k)
    c = sum(mi(s[:-1], s[1:], k) >= real for s in (np.array(rr.sample(list(seq), len(seq))) for _ in range(shuffles)))
    return (1 + c) / (shuffles + 1)

ps = []
for t in range(40):
    table = pe.balanced_table(model_text, 13, random.Random(2900 + t))
    st = rr.randrange(0, len(pool) - 200)
    ps.append(lag1_p([table[ord(ch) - 65] for ch in pool[st:st + 182]], 13))
real_p = lag1_p(list(m), 13)
out["R29"] = {"planted_texts": 40, "p_below_0.05": sum(p < 0.05 for p in ps), "p_below_0.01": sum(p < 0.01 for p in ps),
              "real_message_lag1_p": round(real_p, 3), "shuffles_each": 400,
              "claim": "40 of 40 planted texts show lag-1 dependence beyond shuffles (p < 0.01 in 39); real message p = 0.70",
              "pass": bool(sum(p < 0.05 for p in ps) >= 38 and real_p > 0.05)}
print("R29", out["R29"], flush=True)
(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "recompute_extra.json").write_text(json.dumps(out, indent=1))
