"""
Turning grille (14x14, 4 quarter turns) on the GPU — the one message system that survives the 2026 order test
(Hendrick: of the systems tested, only 'no message' or a system destroying order as completely as a turning grille
remain; his searches recover 0/4 planted grilles when grille and key are both unknown).

Geometry. A 14x14 grid splits into 49 orbits of 4 cells under a quarter turn, (r, c) -> (c, 13 - r). A grille opens
one cell of every orbit; turning it 3 times opens the other 3, so the grille is 49 choices s[o] in {0, 1, 2, 3}
(which member of orbit o is open at turn 0). Member m of orbit o is open at turn (m - s[o]) mod 4. Letters are written
turn by turn, each turn's open cells in reading order, and the grid is read row by row. So decryption is: label every
cell with its turn, and read the cells sorted by (turn, row, column).

Null-column rule (option): the cipher's only structure is column 14, which a rotating grille cannot make by itself.
The one grille procedure that does: when an open cell falls in column 14, write a dummy there instead of a letter.
Then the message is the other 182 cells, read in (turn, row, column) order, and column 14 is padding.

Search: thousands of chains anneal the 49 turn choices and (unless given) the letter key at once — moves change one
orbit's choice or swap two letters of the key — scored by quadgram fit of the decryption. Same discipline as every
engine here: real cells, shuffled cells, and a planted grille message; a power curve for power_check.
"""

from __future__ import annotations

import random
import time

import numpy as np
import torch

N = 14


def device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def orbits(n: int = N) -> tuple[np.ndarray, np.ndarray]:
    """orbit id and member index (0..3) of every cell (row-major index)."""
    oid = -np.ones(n * n, dtype=np.int64)
    mem = np.zeros(n * n, dtype=np.int64)
    k = 0
    for r in range(n // 2):
        for c in range(n // 2):
            rc = (r, c)
            for m in range(4):
                oid[rc[0] * n + rc[1]] = k
                mem[rc[0] * n + rc[1]] = m
                rc = (rc[1], n - 1 - rc[0])
            k += 1
    return oid, mem


OID, MEM = orbits()


def order_for(shifts: np.ndarray, null_col: bool) -> np.ndarray:
    """Plaintext order of the cells (indices into the row-major grid) for one grille."""
    turn = (MEM - shifts[OID]) % 4
    cells = [p for p in range(N * N) if not (null_col and p % N == N - 1)]
    return np.array(sorted(cells, key=lambda p: (turn[p], p)), dtype=np.int64)


def encipher(plain_ids: np.ndarray, shifts: np.ndarray, null_col: bool, null_symbols: list[int],
             rnd: random.Random) -> np.ndarray:
    """plain_ids: symbols in plaintext order (182 with the null column, else 196) -> grid read row by row."""
    order = order_for(shifts, null_col)
    grid = np.full(N * N, -1, dtype=np.int64)
    grid[order] = plain_ids[: len(order)]
    for p in range(N * N):
        if grid[p] < 0:
            grid[p] = rnd.choice(null_symbols)
    return grid



def match_up_to_rotation(found_shifts, true_shifts) -> tuple[int, int]:
    """(orbits right, offset k): a grille turned a quarter before writing reads the same four streams starting from
    another one — the same solution. found == (true + k) mod 4 on every orbit for one k means solved."""
    f = np.asarray(found_shifts) % 4
    t = np.asarray(true_shifts) % 4
    best = max(range(4), key=lambda k: int(((t + k) % 4 == f).sum()))
    return int(((t + best) % 4 == f).sum()), best


def unrotate(found_shifts, k: int) -> np.ndarray:
    return (np.asarray(found_shifts) - k) % 4

def anneal(Q: torch.Tensor, cells: np.ndarray, chains: int, seconds: float, seed: int, null_col: bool,
           key: np.ndarray | None = None, t_hi: float = 0.06, t_lo: float = 0.003,
           steps: int | None = None, n: int = 4, base: int = 26) -> list[dict]:
    """cells: the 196 grid symbols (ids 0..k-1). key: fixed symbol->letter map (k,) or None to anneal it too.
    Q is a flat log table of n-grams over `base` symbols (default: English quadgrams, 26^4); group_ngrams builds
    higher orders over the 13 group symbols."""
    dev = Q.device
    g = torch.Generator(device=dev).manual_seed(seed)
    B = chains
    oid = torch.tensor(OID, device=dev)
    mem = torch.tensor(MEM, device=dev)
    keep = torch.tensor([p for p in range(N * N) if not (null_col and p % N == N - 1)], device=dev)
    sym = torch.tensor(cells, device=dev)
    k = int(cells.max()) + 1
    shifts = torch.randint(0, 4, (B, 49), device=dev, generator=g)
    if key is None:
        # frequency-order start (commonest symbol -> E ...) for two thirds, random for the rest
        order = np.argsort(-np.bincount(cells[keep.cpu().numpy()], minlength=k), kind="stable")
        freq_key = np.zeros(max(k, 26), dtype=np.int64)
        en = [ord(ch) - 65 for ch in "ETAOINSHRDLCUMWFGYPBVKJXQZ"]
        rest = list(range(26))
        for s, ch in zip(order, en):
            freq_key[s] = ch
        keys = torch.tensor(freq_key[:max(k, 26)], device=dev).repeat(B, 1)
        nr = B // 3
        keys[:nr] = torch.argsort(torch.rand(nr, max(k, 26), device=dev, generator=g), 1) % 26
    else:
        keys = torch.tensor(key, device=dev).repeat(B, 1)
    anneal_key = key is None

    def decode(sh, ky):
        turn = (mem[None, :] - torch.gather(sh, 1, oid[None, :].expand(B, -1))) % 4      # (B, 196)
        sortkey = turn[:, keep] * 1000 + keep[None, :]
        order = torch.gather(keep[None, :].expand(B, -1), 1, torch.argsort(sortkey, 1))
        return torch.gather(ky, 1, sym[order])

    def score(letters):
        L = letters.shape[1] - n + 1
        q = letters[:, :L].clone()
        for j in range(1, n):
            q = q * base + letters[:, j:j + L]
        return Q[q].mean(1)

    cur = score(decode(shifts, keys))
    best, bsh, bky = cur.clone(), shifts.clone(), keys.clone()
    ar = torch.arange(B, device=dev)
    t0, it = time.monotonic(), 0
    while True:
        frac = min(1.0, it / steps) if steps else min(1.0, (time.monotonic() - t0) / seconds)
        if frac >= 1.0 and it > 0:
            break
        T = t_hi * (t_lo / t_hi) ** frac
        if anneal_key and it % 2 == 1:
            a = torch.randint(0, k, (B,), device=dev, generator=g)
            b = torch.randint(0, 26, (B,), device=dev, generator=g)
            nk = keys.clone()
            # swap the letters of symbol a and of whichever symbol currently maps to letter b (keeps it one-to-one)
            la = nk[ar, a].clone()
            holder = (nk[:, :k] == b[:, None]).float().argmax(1)
            has = (nk[:, :k] == b[:, None]).any(1)
            nk[ar, a] = b
            nk[ar[has], holder[has]] = la[has]
            s = score(decode(shifts, nk))
            acc = (s >= cur) | (torch.rand(B, device=dev, generator=g) < torch.exp((s - cur) / T))
            keys = torch.where(acc[:, None], nk, keys)
        else:
            o = torch.randint(0, 49, (B,), device=dev, generator=g)
            v = torch.randint(0, 4, (B,), device=dev, generator=g)
            ns = shifts.clone()
            ns[ar, o] = v
            s = score(decode(ns, keys))
            acc = (s >= cur) | (torch.rand(B, device=dev, generator=g) < torch.exp((s - cur) / T))
            shifts = torch.where(acc[:, None], ns, shifts)
        cur = torch.where(acc, s, cur)
        better = cur > best
        if better.any():
            best = torch.where(better, cur, best)
            bsh = torch.where(better[:, None], shifts, bsh)
            bky = torch.where(better[:, None], keys, bky)
        it += 1
    top = torch.argsort(best, descending=True)[:5]
    dec = decode(bsh, bky)
    return [{"score": round(float(best[b]), 4), "steps": it, "shifts": bsh[b].tolist(), "key": bky[b].tolist(),
             "plaintext": "".join(chr(65 + int(x)) for x in dec[b].tolist())} for b in top.tolist()]


def plant(plain: str, null_col: bool, rnd: random.Random, n_symbols: int = 26) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """A planted grille message: (cells, true shifts, true key symbol->letter)."""
    L = N * (N - 1) if null_col else N * N
    letters = np.array([ord(ch) - 65 for ch in plain[:L]], dtype=np.int64)
    perm = list(range(26))
    rnd.shuffle(perm)                                   # letter -> symbol
    syms = np.array([perm[x] for x in letters], dtype=np.int64)
    shifts = np.array([rnd.randrange(4) for _ in range(49)], dtype=np.int64)
    nulls = [26 + i for i in range(4)] if null_col else [0]
    cells = encipher(syms, shifts, null_col, nulls, rnd)
    key = np.zeros(30, dtype=np.int64)
    for letter, s in enumerate(perm):
        key[s] = letter
    return cells, shifts, key


def run(Qnp: np.ndarray, cfg: dict, progress=print, partial_path=None, plant_only: bool = False) -> dict:
    """cfg: symbols (196 grid cells, ids), null_col (bool), chains, max_seconds, seed, self_check_plain,
    key_given (plants only: give the true key — the field's 'with key' benchmark)."""
    dev = device()
    Q = torch.tensor(Qnp, device=dev, dtype=torch.float32)
    null_col = bool(cfg.get("null_col", True))
    chains = int(cfg.get("chains", 8192))
    secs = float(cfg["max_seconds"])
    seed = int(cfg.get("seed", 0))
    rnd = random.Random(seed + 99)
    plain = "".join(ch for ch in cfg.get("self_check_plain", "").upper() if "A" <= ch <= "Z")
    L = N * (N - 1) if null_col else N * N
    pc, psh, pkey = plant(plain, null_col, rnd)
    truth = plain[:L]

    def judge(top):
        orbits, k = match_up_to_rotation(top[0]["shifts"], psh)
        order = order_for(unrotate(top[0]["shifts"], k), null_col)
        key = top[0].get("key") or pkey             # the found key (key unknown) or the given one
        text = "".join(chr(65 + int(key[pc[i]])) for i in order)
        agree = sum(a == b for a, b in zip(text, truth)) / L
        return {"char_agreement": round(agree, 3), "orbits_right_up_to_rotation": orbits, "rotation": k,
                "recovered": agree >= 0.8 or orbits >= 45}

    kg = pkey if cfg.get("key_given") else None
    if plant_only:
        return judge(anneal(Q, pc, chains, secs, seed, null_col, key=kg))
    sym = np.array(cfg["symbols"], dtype=np.int64)
    progress(f"grille: phase 1/3 real cells (null_col={null_col}, {chains} chains, {secs:.0f}s, {dev.type})")
    real = anneal(Q, sym, chains, secs, seed, null_col)
    if partial_path:
        import json
        json.dump({"phase": 1, "real": {"top": real}}, open(partial_path, "w"), indent=1)
    keep = [p for p in range(N * N) if not (null_col and p % N == N - 1)]
    sh = sym.copy()
    vals = [int(sym[p]) for p in keep]
    rnd.shuffle(vals)
    for p, v in zip(keep, vals):
        sh[p] = v
    null = anneal(Q, sh, chains, secs, seed + 1, null_col)
    progress(f"phase 2 done (null): best {null[0]['score']}")
    chk = judge(anneal(Q, pc, chains, secs, seed + 2, null_col))
    out = {"mode": "gpu-grille", "null_col": null_col, "real": {"top": real},
           "null_control": {"best_score": null[0]["score"], "top_plaintext": null[0]["plaintext"][:120],
                            "top": [{"score": r["score"], "plaintext": r["plaintext"]} for r in null]},
           "self_check": chk, "margin_over_null": round(real[0]["score"] - null[0]["score"], 4), "device": dev.type}
    progress(f"done: margin over null {out['margin_over_null']}, plant {chk['char_agreement']}")
    return out


# ── grille + polyphonic table (one symbol = a group of letters) ─────────────────────────────────────────────────────

def anneal_poly(logU: torch.Tensor, logB: torch.Tensor, cells: np.ndarray, k: int, chains: int, seconds: float,
                seed: int, null_col: bool = True, t_hi: float = 0.08, t_lo: float = 0.004,
                shifts_given: np.ndarray | None = None, table_given: list[int] | None = None) -> list[dict]:
    """Jointly anneal the grille (49 orbit choices) and the letter->symbol grouping; score = Viterbi bigram
    log-probability per letter of the grille's reading order (poly_engine.viterbi). shifts_given / table_given fix
    one part (power benchmarks)."""
    import poly_engine as pe  # noqa: PLC0415 — standalone in the lab, sibling module
    dev = logB.device
    g = torch.Generator(device=dev).manual_seed(seed)
    B = chains
    oid = torch.tensor(OID, device=dev)
    mem = torch.tensor(MEM, device=dev)
    keep = torch.tensor([p for p in range(N * N) if not (null_col and p % N == N - 1)], device=dev)
    sym = torch.tensor(cells, device=dev)
    shifts = (torch.tensor(shifts_given, device=dev).repeat(B, 1) if shifts_given is not None
              else torch.randint(0, 4, (B, 49), device=dev, generator=g))
    if table_given is not None:
        table = torch.tensor(table_given, device=dev).repeat(B, 1)
    else:
        table = torch.randint(0, k, (B, 26), device=dev, generator=g)

    def ordered(sh):
        turn = (mem[None, :] - torch.gather(sh, 1, oid[None, :].expand(B, -1))) % 4
        sk = turn[:, keep] * 1000 + keep[None, :]
        order = torch.gather(keep[None, :].expand(B, -1), 1, torch.argsort(sk, 1))
        return sym[order]                                                   # (B, L) symbols in reading order

    def score(sh, tb):
        s = ordered(sh)
        allowed = tb[:, None, :] == s[:, :, None]                          # (B, L, 26): letter in symbol's group
        sc, _ = pe.viterbi(logU, logB, allowed)
        return sc / s.shape[1]

    cur = score(shifts, table)
    best, bsh, btb = cur.clone(), shifts.clone(), table.clone()
    ar = torch.arange(B, device=dev)
    t0, it = time.monotonic(), 0
    move_grille = shifts_given is None
    move_table = table_given is None
    while True:
        frac = min(1.0, (time.monotonic() - t0) / seconds)
        if frac >= 1.0 and it > 0:
            break
        T = t_hi * (t_lo / t_hi) ** frac
        if move_grille and (not move_table or it % 2 == 0):
            o = torch.randint(0, 49, (B,), device=dev, generator=g)
            ns = shifts.clone()
            ns[ar, o] = torch.randint(0, 4, (B,), device=dev, generator=g)
            nt = table
        else:
            nt = table.clone()
            a = torch.randint(0, 26, (B,), device=dev, generator=g)
            if it % 4 == 1:
                b = torch.randint(0, 26, (B,), device=dev, generator=g)
                va, vb = nt[ar, a].clone(), nt[ar, b].clone()
                nt[ar, a], nt[ar, b] = vb, va
            else:
                nt[ar, a] = torch.randint(0, k, (B,), device=dev, generator=g)
            ns = shifts
        s = score(ns, nt)
        acc = (s >= cur) | (torch.rand(B, device=dev, generator=g) < torch.exp((s - cur) / T))
        shifts = torch.where(acc[:, None], ns, shifts)
        table = torch.where(acc[:, None], nt, table)
        cur = torch.where(acc, s, cur)
        better = cur > best
        if better.any():
            best = torch.where(better, cur, best)
            bsh = torch.where(better[:, None], shifts, bsh)
            btb = torch.where(better[:, None], table, btb)
        it += 1
    top = torch.argsort(best, descending=True)[:5]
    s = ordered(bsh)
    allowed = btb[:, None, :] == s[:, :, None]
    _, paths = pe.viterbi(logU, logB, allowed)
    return [{"score": round(float(best[b]), 4), "steps": it, "shifts": bsh[b].tolist(), "table": btb[b].tolist(),
             "plaintext": "".join(chr(65 + int(x)) for x in paths[b].tolist())} for b in top.tolist()]


def plant_poly(plain: str, table: list[int], null_col: bool, rnd: random.Random) -> tuple[np.ndarray, np.ndarray]:
    """Grille + polyphonic table plant: (cells, true shifts). Dummies in column 14 use symbols >= 13."""
    L = N * (N - 1) if null_col else N * N
    syms = np.array([table[ord(ch) - 65] for ch in plain[:L]], dtype=np.int64)
    shifts = np.array([rnd.randrange(4) for _ in range(49)], dtype=np.int64)
    k = max(table) + 1
    return encipher(syms, shifts, null_col, [k + i for i in range(4)] if null_col else [0], rnd), shifts



def run_poly(cfg: dict, progress=print, partial_path=None, plant_only: bool = False) -> dict:
    """cfg: symbols (196 cells), bigram {U: [26], B: [[26]*26]}, table_text (letters to build a balanced plant table),
    k (symbols in the message, 13), null_col, chains, max_seconds, seed, self_check_plain."""
    import poly_engine as pe  # noqa: PLC0415
    dev = device()
    U = torch.tensor(cfg["bigram"]["U"], device=dev, dtype=torch.float32)
    Bm = torch.tensor(cfg["bigram"]["B"], device=dev, dtype=torch.float32)
    null_col = bool(cfg.get("null_col", True))
    k = int(cfg.get("k", 13))
    chains = int(cfg.get("chains", 2048))
    secs = float(cfg["max_seconds"])
    seed = int(cfg.get("seed", 0))
    rnd = random.Random(seed + 99)
    plain = "".join(ch for ch in cfg.get("self_check_plain", "").upper() if "A" <= ch <= "Z")
    L = N * (N - 1) if null_col else N * N
    tab = pe.balanced_table(cfg.get("table_text", plain), k, rnd)
    pc, psh = plant_poly(plain, tab, null_col, rnd)
    truth = plain[:L]

    def judge(top):
        orbits, k = match_up_to_rotation(top[0]["shifts"], psh)
        agree = sum(a == b for a, b in zip(top[0]["plaintext"], truth)) / L
        return {"char_agreement_raw": round(agree, 3), "orbits_right_up_to_rotation": orbits, "rotation": k,
                "char_agreement": round(agree, 3) if k == 0 else None,
                "recovered": orbits >= 40 or (k == 0 and agree >= 0.6),
                "note": "a quarter-turned grille is the same solution; recovered = 40+/49 orbits up to rotation "
                        "(polyphonic text ceiling with the TRUE table ~0.85 of letters)"}

    if plant_only:
        return judge(anneal_poly(U, Bm, pc, k, chains, secs, seed, null_col))
    sym = np.array(cfg["symbols"], dtype=np.int64)
    progress(f"grille+poly: phase 1/3 real cells ({chains} chains, {secs:.0f}s, {dev.type})")
    real = anneal_poly(U, Bm, sym, k, chains, secs, seed, null_col)
    if partial_path:
        import json
        json.dump({"phase": 1, "real": {"top": real}}, open(partial_path, "w"), indent=1)
    keep = [p for p in range(N * N) if not (null_col and p % N == N - 1)]
    sh = sym.copy()
    vals = [int(sym[p]) for p in keep]
    rnd.shuffle(vals)
    for p_, v in zip(keep, vals):
        sh[p_] = v
    null = anneal_poly(U, Bm, sh, k, chains, secs, seed + 1, null_col)
    progress(f"phase 2 done (null): best {null[0]['score']}")
    chk = judge(anneal_poly(U, Bm, pc, k, chains, secs, seed + 2, null_col))
    out = {"mode": "gpu-grille-poly", "null_col": null_col, "real": {"top": real},
           "null_control": {"best_score": null[0]["score"], "top_plaintext": null[0]["plaintext"][:120],
                            "top": [{"score": r["score"], "plaintext": r["plaintext"]} for r in null]},
           "self_check": chk, "margin_over_null": round(real[0]["score"] - null[0]["score"], 4), "device": dev.type}
    progress(f"done: margin over null {out['margin_over_null']}, plant {chk['char_agreement']}")
    return out


# ── constructive search: beam decoding of the grille (key given) ────────────────────────────────────────────────────
#
# Annealing the 49 orbit choices fails even with the key given (operator benchmark 0/3; painvin: the landscape is so
# flat that 3 wrong moves erase 93% of the signal). A turning grille has a structure annealing ignores: read the grid
# in row order and each cell's letter goes to ONE of four plaintext streams (the four turns), in order. So decode
# constructively: scan the cells in reading order; at the first cell of an undecided orbit branch on its 4 choices;
# append each cell's letter to its turn's stream and score that stream's newest quadgram; keep the best `width`
# partial grilles. Every orbit is decided by its first cell in reading order, so 49 branchings in all.

def beam_decode(Qnp: np.ndarray, cells: np.ndarray, key: np.ndarray, null_col: bool = True, width: int = 16384,
                device_=None) -> list[dict]:
    """Every letter is scored by its conditional log-probability given up to 3 letters before it in its stream, so
    all partial grilles have scored the same letters. (Scoring only full quadgrams made the beam prefer paths that
    delayed scoring — it pruned the true grille: true -750 vs found -864.)"""
    dev = device_ or device()
    Q = torch.tensor(Qnp, device=dev, dtype=torch.float32)
    # conditional log-probabilities for 1st, 2nd, 3rd and later letters of a stream (from the joint quadgram table):
    # every letter of every stream is scored from the start, so no path gains by leaving streams short and the first
    # row's orbit choices aren't made blind.
    P4 = np.power(10.0, Qnp.astype(np.float64)).reshape(26, 26, 26, 26)
    P4 /= P4.sum()
    P3, P2 = P4.sum(3), P4.sum((2, 3))
    P1 = P2.sum(1)
    lg = lambda a: torch.tensor(np.log10(np.maximum(a, 1e-12)), device=dev, dtype=torch.float32)  # noqa: E731
    c1 = lg(P1)                                                     # (26,)
    c2 = lg(P2 / P1[:, None])                                       # (26, 26)  P(b | a)
    c3 = lg(P3 / P2[:, :, None])                                    # (26, 26, 26)
    c4 = lg(P4 / P3[:, :, :, None]).reshape(-1)                     # (26^4,)  P(d | abc)
    letters = torch.tensor(np.asarray(key)[cells], device=dev)                 # letter of every grid cell
    W = 1
    shifts = torch.full((1, 49), -1, dtype=torch.long, device=dev)
    ctx = torch.full((1, 4, 3), -1, dtype=torch.long, device=dev)              # last 3 letters of each turn's stream
    score = torch.zeros(1, device=dev)
    for p in range(N * N):
        if null_col and p % N == N - 1:
            continue
        o, m = int(OID[p]), int(MEM[p])
        if bool((shifts[:, o] < 0).any()):                                     # first cell of orbit o: branch 4 ways
            shifts = shifts.repeat_interleave(4, 0)
            ctx = ctx.repeat_interleave(4, 0)
            score = score.repeat_interleave(4, 0)
            shifts[:, o] = torch.arange(4, device=dev).repeat(W)
        q = (m - shifts[:, o]) % 4                                             # the turn this cell's letter belongs to
        ar = torch.arange(len(q), device=dev)
        c = ctx[ar, q]                                                         # (B, 3)
        ltr = letters[p]
        have = (c >= 0).sum(1)                                                  # letters already in this stream
        a, b_, d = c[:, 0].clamp(min=0), c[:, 1].clamp(min=0), c[:, 2].clamp(min=0)
        add = torch.where(have == 0, c1[ltr].expand(len(q)),
              torch.where(have == 1, c2[d, ltr],
              torch.where(have == 2, c3[b_, d, ltr], c4[a * 17576 + b_ * 676 + d * 26 + ltr])))
        score = score + add
        newc = torch.cat([c[:, 1:], ltr.expand(len(q))[:, None]], 1)
        ctx[ar, q] = newc
        if len(score) > width:
            keep = torch.topk(score, width).indices
            shifts, ctx, score = shifts[keep], ctx[keep], score[keep]
        W = len(score)
    order = torch.argsort(score, descending=True)[:5]
    out = []
    for b in order.tolist():
        sh = shifts[b].cpu().numpy()
        perm = order_for(sh, null_col)
        out.append({"score_sum": round(float(score[b]), 3), "shifts": sh.tolist(),
                    "plaintext": "".join(chr(65 + int(np.asarray(key)[cells[i]])) for i in perm)})
    return out


# ── a polyphonic table GIVEN: score the grille order by group-symbol quadgrams ───────────────────────────────────────
#
# With the table known, each cipher symbol simply IS a letter group: map English through the table and count the
# quadgrams of group symbols. Then the ordinary grille search (anneal with key = identity) scores orders directly —
# no Viterbi inside the loop; Viterbi only reads the letters at the end. Operator test 2026-10-14: plant solved 48/49
# orbits at 80k steps x 512 chains (CPU); another stalled with the found order scoring above the true one — the
# 4-symbol statistics over 13 groups are not always discriminating enough (identifiability), so higher orders help.

def group_quadgrams(text: str, table, floor: float = -9.0) -> np.ndarray:
    """log10 quadgram table (26^4 layout, group ids 0..k-1 in the low slots) of English mapped through `table`
    (letter index -> group id). Use with anneal(Q, cells, ..., key=np.arange(30))."""
    g = np.array([table[ord(c) - 65] for c in text if "A" <= c <= "Z"], dtype=np.int64)
    q = g[:-3] * 17576 + g[1:-2] * 676 + g[2:-1] * 26 + g[3:]
    cnt = np.bincount(q, minlength=26 ** 4).astype(np.float64)
    Q = np.full(26 ** 4, floor, dtype=np.float32)
    nz = cnt > 0
    Q[nz] = np.log10(cnt[nz] / cnt.sum())
    return Q


def group_ngrams(text: str, table, n: int = 5, base: int = 13, floor_count: float = 0.3) -> np.ndarray:
    """log10 n-gram table over group ids (base^n, flat) of English mapped through `table` (letter -> group id < base).
    Unseen n-grams get floor_count/total. Use with anneal(Q, cells, ..., key=np.arange(30), n=n, base=base)."""
    g = np.array([table[ord(c) - 65] for c in text if "A" <= c <= "Z"], dtype=np.int64)
    if g.max() >= base:
        raise ValueError(f"group id {int(g.max())} >= base {base}")
    L = len(g) - n + 1
    q = g[:L].copy()
    for j in range(1, n):
        q = q * base + g[j:j + L]
    cnt = np.bincount(q, minlength=base ** n).astype(np.float64)
    tot = cnt.sum()
    return np.log10(np.maximum(cnt, floor_count) / tot).astype(np.float32)


# ── table repair (round 11): a near-right polyphonic table, a grille order held fixed ────────────────────────────
# F74: the grille search locks on only with an (almost) exact table. When it does lock with a near-miss table, the
# order is (nearly) right, so the table can be repaired by likelihood: move / swap letters between groups and keep a
# change when the fixed order's symbol stream becomes more probable under the group n-gram model it implies.

def letter_ids(text: str) -> np.ndarray:
    return np.frombuffer(text.encode("ascii", "ignore"), dtype=np.uint8).astype(np.int64) - 65


def group_ngrams_ids(letters: np.ndarray, table, n: int = 6, base: int = 14, floor_count: float = 0.3) -> np.ndarray:
    """group_ngrams for a pre-encoded letter array (letter_ids) — fast enough to rebuild per table move."""
    g = np.asarray(table, dtype=np.int64)[letters]
    L = len(g) - n + 1
    q = g[:L].copy()
    for j in range(1, n):
        q = q * base + g[j:j + L]
    cnt = np.bincount(q, minlength=base ** n).astype(np.float64)
    return np.log10(np.maximum(cnt, floor_count) / cnt.sum()).astype(np.float32)


def stream_score(Q: np.ndarray, stream: np.ndarray, n: int = 6, base: int = 14) -> float:
    L = len(stream) - n + 1
    q = stream[:L].astype(np.int64).copy()
    for j in range(1, n):
        q = q * base + stream[j:j + L]
    return float(Q[q].mean())


def repair_table(letters: np.ndarray, streams: list[np.ndarray], table, movable_groups: int, max_sweeps: int = 6,
                 n: int = 6, base: int = 14, moves: bool = True) -> tuple[list[int], float, int]:
    """Steepest-ascent repair of a table (letter -> group) for the given symbol streams (decoded orders): every swap of
    two letters in different groups (and, with moves=True, every move of a letter to another group < movable_groups)
    is scored, the best is taken, until none improves. Group n-gram models are rebuilt on the GPU per candidate.
    Returns (table, mean score, accepted changes)."""
    dev = device()
    L = torch.tensor(letters, device=dev)
    nn = len(letters) - n + 1
    st = [torch.tensor(s.astype(np.int64), device=dev) for s in streams]
    pw = torch.tensor([base ** (n - 1 - j) for j in range(n)], device=dev)
    sq = [sum(s[j:j + len(s) - n + 1] * pw[j] for j in range(n)) for s in st]

    def score(t):
        g = torch.tensor(t, device=dev)[L]
        q = g[:nn].clone()
        for j in range(1, n):
            q = q * base + g[j:j + nn]
        cnt = torch.bincount(q, minlength=base ** n).float()
        Q = torch.log10(torch.clamp(cnt, min=0.3) / cnt.sum())
        return float(sum(Q[x].mean() for x in sq) / len(sq))

    tab, acc = list(table), 0
    cur = score(tab)
    for _ in range(max_sweeps):
        best, best_t = cur, None
        cands = [(a, b) for a in range(26) for b in range(a + 1, 26) if tab[a] != tab[b]]
        for a, b in cands:
            t = list(tab); t[a], t[b] = t[b], t[a]
            v = score(t)
            if v > best:
                best, best_t = v, t
        if moves:
            for a in range(26):
                for gid in range(movable_groups):
                    if gid == tab[a]:
                        continue
                    t = list(tab); t[a] = gid
                    v = score(t)
                    if v > best:
                        best, best_t = v, t
        if best_t is None:
            break
        tab, cur, acc = best_t, best, acc + 1
    return tab, cur, acc
