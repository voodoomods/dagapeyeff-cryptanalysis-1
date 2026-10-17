"""
Keyed four-square and two-square on the GPU — the digraphic systems the 2026 literature leaves open (Hendrick 2026:
not excluded by letter counts; his all-squares search recovered 0 of 6 planted texts at 196 letters, so nobody has
searched the cells with power).

The ciphertext symbols here are Polybius CELLS (rows 6-9 and 0, columns 1-5: 25 symbols), not letters. A final
letter->cell substitution after a digraphic cipher is absorbed into the cipher squares, so a four-square is searched as

    cipher digraph (x, y):  (r1, c2) = position of cell x in cipher square C1
                            (r2, c1) = position of cell y in cipher square C2
    plaintext:              a = P1[r1, c1],  b = P2[r2, c2]

with C1, C2 arrangements of the 25 cells and P1, P2 keyed letter squares (I/J together). Two-square (horizontal) ties
them: one letter square L, one R, and one letter->cell map f:  C1 = f(R), C2 = f(L), P1 = L, P2 = R.

Thousands of chains anneal all squares at once (moves: swap two entries of one square), scored by the quadgram fit of
the whole decryption. Same discipline as every engine here: real text, shuffled cells (same search), and a planted
answer of the same system; a power curve for power_check. Standalone (numpy + torch); compound_engine runs it.
"""

from __future__ import annotations

import random
import time

import numpy as np
import torch

LET25 = [i for i in range(26) if i != 9]              # A..Z without J (J -> I)


def device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _rand_perms(B: int, n: int, g, dev) -> torch.Tensor:
    return torch.argsort(torch.rand(B, n, device=dev, generator=g), 1)


class State:
    """B chains of square arrangements. All squares are stored as index permutations of 0..24:
    four: posC1, posC2 (cell -> position), P1, P2 (position -> letter slot 0..24)
    two:  L, R (position -> letter slot), g (cell -> letter slot)  [f^-1]"""

    def __init__(self, variant: str, B: int, g, dev):
        self.variant, self.B, self.dev = variant, B, dev
        names = ("posC1", "posC2", "P1", "P2") if variant == "four" else ("L", "R", "g")
        self.t = {k: _rand_perms(B, 25, g, dev) for k in names}

    def names(self):
        return list(self.t)

    def clone(self):
        s = State.__new__(State)
        s.variant, s.B, s.dev = self.variant, self.B, self.dev
        s.t = {k: v.clone() for k, v in self.t.items()}
        return s


LETTER = torch.tensor(LET25)                          # letter slot -> A..Z index


def decrypt(st: State, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """x, y: (D,) first and second cells of the D digraphs -> (B, 2D) letters (0..25)."""
    B = st.B
    L25 = LETTER.to(st.dev)
    if st.variant == "four":
        p1 = st.t["posC1"][:, x]                        # (B, D) positions of x in C1
        p2 = st.t["posC2"][:, y]
        r1, c2 = p1 // 5, p1 % 5
        r2, c1 = p2 // 5, p2 % 5
        a = torch.gather(st.t["P1"], 1, r1 * 5 + c1)
        b = torch.gather(st.t["P2"], 1, r2 * 5 + c2)
    else:
        # positions of letters in L and R: inverse permutations
        posL = torch.argsort(st.t["L"], 1)
        posR = torch.argsort(st.t["R"], 1)
        u = st.t["g"][:, x]                             # letter slot behind cell x (C1 = f(R))
        v = st.t["g"][:, y]                             # (C2 = f(L))
        p1 = torch.gather(posR, 1, u)
        p2 = torch.gather(posL, 1, v)
        r1, c2 = p1 // 5, p1 % 5
        r2, c1 = p2 // 5, p2 % 5
        a = torch.gather(st.t["L"], 1, r1 * 5 + c1)
        b = torch.gather(st.t["R"], 1, r2 * 5 + c2)
    out = torch.stack([a, b], 2).reshape(B, -1)
    return L25[out]


def score(Q: torch.Tensor, letters: torch.Tensor) -> torch.Tensor:
    q = letters[:, :-3] * 17576 + letters[:, 1:-2] * 676 + letters[:, 2:-1] * 26 + letters[:, 3:]
    return Q[q].mean(1)


def anneal(Q: torch.Tensor, cells: np.ndarray, variant: str, chains: int, seconds: float, seed: int,
           t_hi: float = 0.05, t_lo: float = 0.002, restarts: int = 1) -> list[dict]:
    dev = Q.device
    g = torch.Generator(device=dev).manual_seed(seed)
    c = torch.tensor(cells[: len(cells) // 2 * 2], device=dev)
    x, y = c[0::2], c[1::2]
    best_all = []
    for rs in range(max(1, restarts)):
        st = State(variant, chains, g, dev)
        cur = score(Q, decrypt(st, x, y))
        best, best_st = cur.clone(), st.clone()
        names = st.names()
        ar = torch.arange(chains, device=dev)
        t0, it = time.monotonic(), 0
        span = seconds / max(1, restarts)
        while True:
            frac = min(1.0, (time.monotonic() - t0) / span)
            if frac >= 1.0 and it > 0:
                break
            T = t_hi * (t_lo / t_hi) ** frac
            k = names[it % len(names)]
            a = torch.randint(0, 25, (chains,), device=dev, generator=g)
            b = torch.randint(0, 25, (chains,), device=dev, generator=g)
            old = st.t[k]
            new = old.clone()
            va, vb = new[ar, a].clone(), new[ar, b].clone()
            new[ar, a], new[ar, b] = vb, va
            st.t[k] = new
            s = score(Q, decrypt(st, x, y))
            acc = (s >= cur) | (torch.rand(chains, device=dev, generator=g) < torch.exp((s - cur) / T))
            st.t[k] = torch.where(acc[:, None], new, old)
            cur = torch.where(acc, s, cur)
            better = cur > best
            if better.any():
                best = torch.where(better, cur, best)
                for kk in names:
                    best_st.t[kk] = torch.where(better[:, None], st.t[kk], best_st.t[kk])
            it += 1
        order = torch.argsort(best, descending=True)[:5]
        dec = decrypt(best_st, x, y)
        for b_ in order.tolist():
            best_all.append({"variant": variant, "score": round(float(best[b_]), 4), "steps": it,
                             "plaintext": "".join(chr(65 + int(v)) for v in dec[b_].tolist())})
    best_all.sort(key=lambda r: -r["score"])
    return best_all


def plant(plain: str, variant: str, rnd: random.Random, with_truth: bool = False):
    """Encipher letters (J->I, even length) with random keyed squares of the variant -> cell ids 0..24."""
    letters = [ch for ch in plain.upper().replace("J", "I") if "A" <= ch <= "Z"]
    letters = letters[: len(letters) // 2 * 2]
    slot = {chr(65 + LET25[i]): i for i in range(25)}
    if variant == "four":
        P1, P2 = rnd.sample(range(25), 25), rnd.sample(range(25), 25)   # position -> letter slot
        C1, C2 = rnd.sample(range(25), 25), rnd.sample(range(25), 25)   # position -> cell
    else:
        L, R = rnd.sample(range(25), 25), rnd.sample(range(25), 25)
        f = rnd.sample(range(25), 25)                                    # letter slot -> cell
        P1, P2 = L, R
        C1 = [f[R[p]] for p in range(25)]
        C2 = [f[L[p]] for p in range(25)]
    pos1 = {P1[p]: p for p in range(25)}
    pos2 = {P2[p]: p for p in range(25)}
    out = []
    for i in range(0, len(letters), 2):
        r1, c1 = divmod(pos1[slot[letters[i]]], 5)
        r2, c2 = divmod(pos2[slot[letters[i + 1]]], 5)
        out += [C1[r1 * 5 + c2], C2[r2 * 5 + c1]]
    arr = np.array(out, dtype=np.int64)
    if not with_truth:
        return arr
    if variant == "four":
        truth = {"posC1": [C1.index(c) for c in range(25)], "posC2": [C2.index(c) for c in range(25)], "P1": P1, "P2": P2}
    else:
        truth = {"L": L, "R": R, "g": [f.index(c) for c in range(25)]}
    return arr, truth


def run(Qnp: np.ndarray, cfg: dict, progress=print, partial_path=None, plant_only: bool = False) -> dict:
    """cfg: symbols (cells 0..24), variant (four|two), phase (0|1: which symbol starts a digraph), chains,
    max_seconds, restarts, seed, self_check_plain."""
    dev = device()
    Q = torch.tensor(Qnp, device=dev, dtype=torch.float32)
    variant = cfg.get("variant", "four")
    chains = int(cfg.get("chains", 4096))
    secs = float(cfg["max_seconds"])
    restarts = int(cfg.get("restarts", 2))
    seed = int(cfg.get("seed", 0))
    phases = cfg.get("phases", [0, 1])
    sym = np.array(cfg["symbols"], dtype=np.int64)
    rnd = random.Random(seed + 99)
    plain = "".join(ch for ch in cfg.get("self_check_plain", "").upper().replace("J", "I") if "A" <= ch <= "Z")
    L = len(sym) // 2 * 2
    pc = plant(plain[:L], variant, rnd)
    truth = plain[:L]

    def judge(top):
        agree = sum(a == b for a, b in zip(top[0]["plaintext"], truth)) / L
        return {"char_agreement": round(agree, 3), "recovered": agree >= 0.8}

    if plant_only:
        return judge(anneal(Q, pc, variant, chains, secs, seed, restarts=restarts))

    def search(c, label):
        found = []
        for ph in phases:
            cc = c[ph:]
            r = anneal(Q, cc, variant, chains, secs / len(phases), seed + 7 * ph, restarts=restarts)
            for x in r:
                x["phase"] = ph
            found += r
        found.sort(key=lambda r: -r["score"])
        progress(f"{label}: best {found[0]['score']} ({variant}, phase {found[0]['phase']}, {found[0]['steps']} steps "
                 f"x {chains} chains on {dev.type})")
        return found

    progress(f"digraph {variant}: phase 1/3 real cells ({len(sym)} symbols, phases {phases}, {secs:.0f}s, {chains} chains)")
    real = search(sym, "phase 1 done")
    if partial_path:
        import json
        json.dump({"phase": 1, "real": {"top": real[:10]}}, open(partial_path, "w"), indent=1)
    sh = np.array(rnd.sample([int(v) for v in sym], len(sym)), dtype=np.int64)
    null = search(sh, "phase 2 done (null)")
    chk = judge(anneal(Q, pc, variant, chains, secs, seed + 3, restarts=restarts))
    tq = np.array([ord(ch) - 65 for ch in truth])
    truth_score = float(Qnp[tq[:-3] * 17576 + tq[1:-2] * 676 + tq[2:-1] * 26 + tq[3:]].mean())
    chk["true_plaintext_score"] = round(truth_score, 4)
    out = {"mode": f"gpu-digraph-{variant}", "real": {"top": real[:10]},
           "null_control": {"best_score": null[0]["score"], "top_plaintext": null[0]["plaintext"][:120],
                            "top": [{"score": r["score"], "plaintext": r["plaintext"]} for r in null[:10]]},
           "self_check": chk, "margin_over_null": round(real[0]["score"] - null[0]["score"], 4), "device": dev.type}
    progress(f"done: margin over null {out['margin_over_null']}, plant {chk['char_agreement']}")
    return out
