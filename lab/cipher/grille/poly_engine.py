"""
Polyphonic tables: one cipher symbol stands for a GROUP of letters (the reverse of homophones).

Why: the 13 message columns use 13 cells with flat counts (case F31). No natural text under a one-to-one key does that
(Hendrick 2026 proves the count bound), but a table that groups letters to balance their frequencies does (our merge
tests: ~36% of English windows). Hendrick's searches decode every cell to ONE letter, so this class is untested.

Decoding a polyphonic text is like predictive text (T9): each symbol allows a few letters and the language picks one.
Given a grouping, the best reading is exact by Viterbi over a bigram letter model (26 states). A search anneals the
grouping (moves: move one letter to another symbol, or swap two letters' symbols), scoring each grouping by its Viterbi
log-probability per letter. Optionally the symbol ORDER comes from a turning grille (grille_engine), annealed jointly.

Standalone (numpy + torch). Bigram model: built from the same running-text stream the quadgrams come from.
"""

from __future__ import annotations

import heapq
import random
import time
from collections import Counter

import numpy as np
import torch


def device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def bigram_model(text: str) -> tuple[np.ndarray, np.ndarray]:
    """log P(letter) and log P(next | prev) from running text (add-one smoothed)."""
    ids = np.array([ord(ch) - 65 for ch in text if "A" <= ch <= "Z"], dtype=np.int64)
    uni = np.bincount(ids, minlength=26) + 1.0
    bi = np.ones((26, 26))
    np.add.at(bi, (ids[:-1], ids[1:]), 1)
    return np.log(uni / uni.sum()), np.log(bi / bi.sum(1, keepdims=True))


def balanced_table(text: str, k: int, rnd: random.Random) -> list[int]:
    """letter -> symbol: letters packed by frequency into k groups as evenly as possible (labels shuffled)."""
    freq = Counter(ch for ch in text if "A" <= ch <= "Z")
    h = [(0, i) for i in range(k)]
    table = [0] * 26
    for letter in sorted(range(26), key=lambda x: -freq.get(chr(65 + x), 0)):
        s, i = heapq.heappop(h)
        table[letter] = i
        heapq.heappush(h, (s + freq.get(chr(65 + letter), 0), i))
    lab = list(range(k))
    rnd.shuffle(lab)
    return [lab[t] for t in table]


def viterbi(logU: torch.Tensor, logB: torch.Tensor, allowed: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """allowed: (B, L, 26) bool — letters each position may be. Returns (best log-prob per chain, best paths (B, L))."""
    B, L, _ = allowed.shape
    neg = torch.tensor(-1e9, device=allowed.device)
    v = torch.where(allowed[:, 0], logU[None, :], neg)
    back = []
    for i in range(1, L):
        cand = v[:, :, None] + logB[None, :, :]               # (B, prev, next)
        best, arg = cand.max(1)
        v = torch.where(allowed[:, i], best, neg)
        back.append(arg)
    score, last = v.max(1)
    path = [last]
    for arg in reversed(back):
        last = torch.gather(arg, 1, last[:, None])[:, 0]
        path.append(last)
    return score, torch.stack(path[::-1], 1)


def anneal(logU, logB, symbols: np.ndarray, k: int, chains: int, seconds: float, seed: int,
           t_hi: float = 0.08, t_lo: float = 0.004, init: list[int] | None = None) -> list[dict]:
    """Anneal the grouping letter->symbol (B, 26) for a fixed symbol order."""
    dev = logB.device
    g = torch.Generator(device=dev).manual_seed(seed)
    B, L = chains, len(symbols)
    sym = torch.tensor(symbols, device=dev)
    if init is not None:
        table = torch.tensor(init, device=dev).repeat(B, 1)
    else:
        table = torch.randint(0, k, (B, 26), device=dev, generator=g)
        table[:, :k] = torch.arange(k, device=dev)[None, :].expand(B, k)[:, torch.randperm(k, generator=g, device=dev)]

    def score(tb):
        allowed = (tb[:, None, :] == sym[None, :, None])         # (B, L, 26): letter's group is this symbol
        sc, _ = viterbi(logU, logB, allowed)
        return sc / L

    cur = score(table)
    best, btab = cur.clone(), table.clone()
    ar = torch.arange(B, device=dev)
    t0, it = time.monotonic(), 0
    while True:
        frac = min(1.0, (time.monotonic() - t0) / seconds)
        if frac >= 1.0 and it > 0:
            break
        T = t_hi * (t_lo / t_hi) ** frac
        nt = table.clone()
        a = torch.randint(0, 26, (B,), device=dev, generator=g)
        if it % 2:
            b = torch.randint(0, 26, (B,), device=dev, generator=g)          # swap two letters' symbols
            va, vb = nt[ar, a].clone(), nt[ar, b].clone()
            nt[ar, a], nt[ar, b] = vb, va
        else:
            nt[ar, a] = torch.randint(0, k, (B,), device=dev, generator=g)  # move a letter to another symbol
        s = score(nt)
        acc = (s >= cur) | (torch.rand(B, device=dev, generator=g) < torch.exp((s - cur) / T))
        table = torch.where(acc[:, None], nt, table)
        cur = torch.where(acc, s, cur)
        better = cur > best
        if better.any():
            best = torch.where(better, cur, best)
            btab = torch.where(better[:, None], table, btab)
        it += 1
    top = torch.argsort(best, descending=True)[:5]
    allowed = (btab[:, None, :] == sym[None, :, None])
    _, paths = viterbi(logU, logB, allowed)
    return [{"score": round(float(best[b]), 4), "steps": it, "table": btab[b].tolist(),
             "plaintext": "".join(chr(65 + int(x)) for x in paths[b].tolist())} for b in top.tolist()]


def decode_with(logU, logB, symbols: np.ndarray, table: list[int]) -> str:
    dev = logB.device
    tb = torch.tensor(table, device=dev)[None, :]
    allowed = (tb[:, None, :] == torch.tensor(symbols, device=dev)[None, :, None])
    _, p = viterbi(logU, logB, allowed)
    return "".join(chr(65 + int(x)) for x in p[0].tolist())
