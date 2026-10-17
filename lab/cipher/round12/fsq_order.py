"""Round 12, check 4b — does a four-square built on purpose (fsq-full.json) leave order the cipher does not have?

The real message (182 symbols, column 14 removed) shows no order (F32, F66). A four-square writes each plaintext digraph
(a, b) as two symbols, (row a, col b) and (row b, col a), so the two symbols of a digraph share information. Statistics,
each against SHUFFLES of the same symbols (order destroyed, counts kept), computed identically for every text:

  mi_even   mutual information between positions 2k and 2k+1 (digraph phase 0)
  mi_odd    the same for positions 2k+1 and 2k+2 (phase 1; the cipher's phase is unknown)
  mi_max    the largest lag-1..26 mutual information over the whole stream
Family-wise p = how often a shuffle's smallest single p is as small as the text's (min-p permutation correction).

Texts: the real message; the 100 purpose-built four-square ciphertexts of fsq-full.json (rebuilt from their keys and
windows, with the cipher squares aligned exactly as there); 100 randomly keyed four-square ciphertexts of the same
windows. Also for the purpose-built keys: MI is unchanged by relabelling either symbol of a digraph, so the alignment
of the cipher squares does not matter for mi_even.

    python fsq_order.py [SHUFFLES]
"""
import json, random, sys
from collections import Counter
sys.path.insert(0, "/lab/cipher/round12")
import numpy as np
import review_checks as rc

SH = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
LAGS = 26


def mi(x, y):
    k = int(max(x.max(), y.max())) + 1
    j = np.bincount(x * k + y, minlength=k * k).reshape(k, k).astype(float)
    j /= j.sum()
    px, py = j.sum(1, keepdims=True), j.sum(0, keepdims=True)
    nz = j > 0
    return float((j[nz] * np.log2(j[nz] / (px @ py)[nz])).sum())


def stats(s):
    e = mi(s[0:-1:2], s[1::2])
    o = mi(s[1:-1:2], s[2::2])
    m = max(mi(s[:-L], s[L:]) for L in range(1, LAGS + 1))
    return np.array([e, o, m])


def test(s, rnd):
    s = np.asarray(s, dtype=np.int64)
    real = stats(s)
    sh = np.array([stats(np.array(rnd.sample(list(s), len(s)))) for _ in range(SH)])
    p = (1 + (sh >= real).sum(0)) / (SH + 1)
    # min-p family-wise: rank of each shuffle's own min p
    ranks = np.array([(1 + (sh[:, i][None, :] >= sh[:, i][:, None]).sum(1)) / (SH + 1) for i in range(3)]).T
    fam = (1 + (ranks.min(1) <= p.min()).sum()) / (SH + 1)
    return {"mi_even_p": round(float(p[0]), 4), "mi_odd_p": round(float(p[1]), 4), "mi_max_p": round(float(p[2]), 4),
            "family_p": round(float(fam), 4)}


def encipher(text, P1, P2, align=True):
    q1, q2 = rc.square_from(P1), rc.square_from(P2)
    s1 = [(q1[a][0], q2[b][1]) for a, b in zip(text[0::2], text[1::2])]
    s2 = [(q2[b][0], q1[a][1]) for a, b in zip(text[0::2], text[1::2])]
    c1, c2 = Counter(s1), Counter(s2)
    # cells: S1 pairs ascending by count get ids 0..; S2 pairs descending by count land on the same ids (best_flat_merge)
    id1 = {k: i for i, (k, _) in enumerate(sorted(c1.items(), key=lambda kv: kv[1]))}
    order2 = sorted(c2.items(), key=lambda kv: -kv[1])
    id2 = {k: i for i, (k, _) in enumerate(order2)} if align else {k: i + len(id1) for i, (k, _) in enumerate(order2)}
    out = []
    for x, y in zip(s1, s2):
        out += [id1[x], id2[y]]
    return out


def main():
    rnd = random.Random(4242)
    real = json.load(open("/lab/cipher/round11/real_cells.json"))
    msg = [v for i, v in enumerate(real) if i % 14 != 13]
    out = {"shuffles": SH, "real_message": test(msg, rnd), "purpose_built": [], "random_key": []}
    print("real", out["real_message"], flush=True)
    fsq = json.load(open("/lab/cipher/round12/fsq-full.json"))
    for r in fsq["runs"]:
        w = r["window"]
        st = random.Random(31000 + w).randrange(0, len(rc.PROSE) - 400)
        text = [c if c != "J" else "I" for c in rc.PROSE[st:st + 182]]
        cells = encipher(text, list(r["P1"]), list(r["P2"]))
        assert len(set(cells)) == r["merged_cells"], (w, len(set(cells)), r["merged_cells"])
        t = test(cells, rnd); t.update(window=w, cells=r["merged_cells"], flat_p=r["flat_p_if_13"])
        out["purpose_built"].append(t)
        kr = random.Random(55000 + w)
        t2 = test(encipher(text, kr.sample(rc.A25, 25), kr.sample(rc.A25, 25)), rnd); t2.update(window=w)
        out["random_key"].append(t2)
        print(json.dumps(t), json.dumps(t2), flush=True)
        json.dump(out, open("/lab/cipher/round12/fsq-order.json", "w"), indent=1)

    def summ(rows):
        return {"texts": len(rows), "family_p_below_0.05": sum(x["family_p"] < 0.05 for x in rows),
                "family_p_below_0.01": sum(x["family_p"] < 0.01 for x in rows),
                "mi_even_or_odd_p_below_0.05": sum(min(x["mi_even_p"], x["mi_odd_p"]) < 0.05 for x in rows),
                "median_family_p": float(np.median([x["family_p"] for x in rows]))}
    out["summary"] = {"real_message": out["real_message"], "purpose_built_all": summ(out["purpose_built"]),
                      "purpose_built_13_flat": summ([x for x in out["purpose_built"] if (x["flat_p"] or 0) >= 0.05]),
                      "random_key": summ(out["random_key"])}
    json.dump(out, open("/lab/cipher/round12/fsq-order.json", "w"), indent=1)
    print(json.dumps(out["summary"], indent=1))


if __name__ == "__main__":
    main()
