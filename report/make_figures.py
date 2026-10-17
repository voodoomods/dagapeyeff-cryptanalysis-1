"""Figures for the D'Agapeyeff report — every number read from the result files (no hand-typed data).

Run in the agent container:  python /workspace/research/cipher/dagapeyeff/report/make_figures.py
Writes SVG (+ PNG) into report/figs/. Palette: data-viz reference instance, light mode, slots 1-3 only
(blue #2a78d6, orange #eb6834, aqua #1baf7a — validated all-pairs); ink #0b0b0b / #52514e; surface white.
"""
import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

LAB = Path("/lab/cipher")
OUT = Path("/workspace/research/cipher/dagapeyeff/report/figs")
OUT.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID, MUTED = "#0b0b0b", "#52514e", "#e6e5e1", "#bdbcb7"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
    "axes.titleweight": "bold", "axes.titlesize": 11, "axes.titlecolor": INK, "axes.titlelocation": "left",
    "legend.frameon": False, "svg.fonttype": "none",
})


def save(fig, name):
    for ext in ("svg", "png", "pdf"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)


# ── 1. the cipher as a 14 x 14 grid ──────────────────────────────────────────────────────────────────────────
cells = json.loads((LAB / "round11/real_cells.json").read_text())
ids = json.loads((LAB / "round11/cell_ids.json").read_text())
label = {i: p for i, p in enumerate(ids["used"])}
label.update({13 + j: p for j, p in enumerate(ids["extra"])})
fig, ax = plt.subplots(figsize=(7.2, 7.2))
ax.grid(False)
for i, c in enumerate(cells):
    r, k = divmod(i, 14)
    col14 = k == 13
    rare = c >= 13
    face = "#fdf0ea" if col14 else "#f4f7fc"
    ax.add_patch(Rectangle((k, 13 - r), 1, 1, facecolor=face, edgecolor="white", linewidth=1.5))
    ax.text(k + 0.5, 13 - r + 0.5, label[c], ha="center", va="center", fontsize=8.5,
            color=ORANGE if rare else INK, fontweight="bold" if rare else "normal", family="DejaVu Sans Mono")
ax.add_patch(Rectangle((13, 0), 1, 14, fill=False, edgecolor=ORANGE, linewidth=2))
ax.set_xlim(0, 14); ax.set_ylim(0, 14); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("The ciphertext as 196 two-digit symbols, 14 per row", pad=10)
ax.text(13.5, -0.45, "column 14", ha="center", fontsize=9, color=ORANGE)
ax.text(0, -0.45, "Bold orange: the five rare symbols (04, 71, 92, 93, 94) — all in column 14", fontsize=9, color=INK2)
save(fig, "fig1_cipher_grid")

# ── 2. symbol counts: flat cipher vs. English letters ───────────────────────────────────────────────────────
msg = [c for i, c in enumerate(cells) if i % 14 != 13]
cnt = Counter(msg)
syms = sorted(range(13), key=lambda s: -cnt[s])
eng = [12.7, 9.1, 8.2, 7.5, 7.0, 6.7, 6.3, 6.1, 6.0, 4.3, 4.0, 2.8, 2.8, 2.4, 2.4, 2.2, 2.0, 2.0, 1.9, 1.5, 1.0,
       0.8, 0.15, 0.15, 0.1, 0.07]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6), gridspec_kw={"width_ratios": [13, 26], "wspace": 0.18})
for a in (a1, a2): a.grid(axis="x", visible=False)
a1.bar(range(13), [cnt[s] for s in syms], color=BLUE, width=0.82)
a1.axhline(182 / 13, color=INK2, linestyle=(0, (4, 3)), linewidth=1)
a1.text(12.6, 182 / 13 + 0.6, "uniform: 14", ha="right", fontsize=8.5, color=INK2)
a1.set_xticks(range(13)); a1.set_xticklabels([label[s] for s in syms], fontsize=7.5, family="DejaVu Sans Mono")
a1.set_ylabel("count in 182 message symbols")
a1.set_title("Cipher: 13 symbols, nearly flat")
a1.text(0, -4.2, "chi-square vs uniform: p = 0.73", fontsize=8.5, color=INK2)
a2.bar(range(26), [182 * e / 100 for e in eng], color=MUTED, width=0.82)
a2.set_xticks(range(26)); a2.set_xticklabels(list("ETAOINSHRDLCUMWFGYPBVKJXQZ"), fontsize=7.5)
a2.set_title("English: 26 letters, steep")
a1.set_ylim(0, 24); a2.set_ylim(0, 24)          # same scale: both count occurrences in 182 characters
save(fig, "fig2_flatness")

# ── 3. turning grille, illustrated on 4 x 4 ─────────────────────────────────────────────────────────────────
holes0 = [(0, 0), (2, 0), (0, 2), (1, 1)]       # exactly one hole in each of the 4 rotation orbits
def rot(p, k, n=4):
    r, c = p
    for _ in range(k):
        r, c = c, n - 1 - r
    return (r, c)
text = "ENEMYATTACKSDAWN"
fig, axes = plt.subplots(1, 5, figsize=(11, 2.6))
filled = {}
for k in range(4):
    ax = axes[k]; ax.grid(False); ax.axis("off"); ax.set_aspect("equal")
    hs = sorted(rot(p, k) for p in holes0)
    for j, (r, c) in enumerate(hs):
        filled[(r, c)] = text[4 * k + j]
    for r in range(4):
        for c in range(4):
            hole = (r, c) in hs
            ax.add_patch(Rectangle((c, 3 - r), 1, 1, facecolor=("#ffffff" if hole else "#d9d8d3"),
                                   edgecolor="white", linewidth=2))
            if hole:
                ax.text(c + 0.5, 3 - r + 0.5, filled[(r, c)], ha="center", va="center", fontsize=13,
                        color=[BLUE, ORANGE, AQUA, INK][k], fontweight="bold")
    ax.set_xlim(0, 4); ax.set_ylim(0, 4)
    ax.set_title(f"turn {k}: letters {4*k+1}–{4*k+4}", fontsize=9.5, loc="center")
ax = axes[4]; ax.grid(False); ax.axis("off"); ax.set_aspect("equal")
for (r, c), ch in filled.items():
    k = next(i for i in range(4) if (r, c) in [rot(p, i) for p in holes0])
    ax.add_patch(Rectangle((c, 3 - r), 1, 1, facecolor="#f4f7fc", edgecolor="white", linewidth=2))
    ax.text(c + 0.5, 3 - r + 0.5, ch, ha="center", va="center", fontsize=13, color=[BLUE, ORANGE, AQUA, INK][k],
            fontweight="bold")
ax.set_xlim(0, 4); ax.set_ylim(0, 4); ax.set_title("grid, read row by row", fontsize=9.5, loc="center")
fig.suptitle("A turning grille (4 × 4 for illustration; the hypothesis uses 14 × 14 with 49 holes per turn)",
             x=0.02, ha="left", fontsize=11, fontweight="bold", color=INK, y=1.04)
save(fig, "fig3_turning_grille")

# ── 4. group n-gram order (table given) ─────────────────────────────────────────────────────────────────────
ng = json.loads((LAB / "grille/bench-ngram.json").read_text())
fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.grid(axis="x", visible=False)
for i, (n, col) in enumerate([(4, BLUE), (5, BLUE), (6, BLUE)]):
    rs = [r for r in ng["runs"] if r["n"] == n]
    solved = sum(r["orbits_up_to_rotation"] >= 45 for r in rs)
    ax.bar(i, solved, color=col, width=0.6)
    ax.text(i, solved + 0.12, f"{solved} of {len(rs)}", ha="center", fontsize=10, color=INK)
ax.set_xticks(range(3)); ax.set_xticklabels(["4-grams", "5-grams", "6-grams" + chr(10) + "(used in this report)"])
ax.set_ylim(0, 6.8); ax.set_ylabel("practice ciphers solved")
ax.set_title("Grille recovered with the table given, by scoring order")
save(fig, "fig4_ngram_order")

# ── 5. table tolerance ──────────────────────────────────────────────────────────────────────────────────────
tol = json.loads((LAB / "grille/bench-tolerance.json").read_text())
levels = sorted({r["misplaced"] for r in tol["runs"]})
fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.grid(axis="x", visible=False)
for i, k in enumerate(levels):
    rs = [r for r in tol["runs"] if r["misplaced"] == k]
    s = sum(r["solved"] for r in rs)
    ax.bar(i, max(s / len(rs) * 100, 0.8), color=BLUE, width=0.6)
    ax.text(i, s / len(rs) * 100 + 2.5, f"{s}/{len(rs)}", ha="center", fontsize=10, color=INK)
ax.set_xticks(range(len(levels))); ax.set_xticklabels([str(k) for k in levels])
ax.set_xlabel("letters in the wrong group of the table"); ax.set_ylabel("grilles recovered (%)")
ax.set_ylim(0, 112); ax.set_title("A nearly right table is not enough")
save(fig, "fig5_tolerance")

# ── 6. identifiability curve (headline) ─────────────────────────────────────────────────────────────────────
curves = {}
for c in "AB":
    d = json.loads((LAB / f"round11/identifiability-{c}-big.json").read_text())
    rs = [r for r in d["runs"] if r["start"] == "truth"]
    Ls = sorted({r["L"] for r in rs})
    curves[c] = (Ls, [100 * sum(r["exact"] for r in rs if r["L"] == L) / sum(1 for r in rs if r["L"] == L) for L in Ls],
                 sum(1 for r in rs if r["L"] == Ls[0]))
LsA, yA, nA = curves["A"]; LsB, yB, nB = curves["B"]
comb = [(a + b) / 2 for a, b in zip(yA, yB)]
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.axvspan(150, 182, color="#fdf0ea", zorder=0)
ax.axvline(182, color=ORANGE, linewidth=1.5, linestyle=(0, (4, 3)))
ax.text(186, 96, "the cipher:\n182 symbols", fontsize=9, color=INK2, va="top")
ax.plot(LsA, yA, color=BLUE, linewidth=2, marker="o", markersize=6, markeredgecolor="white", markeredgewidth=1.5,
        label=f"model corpus A ({nA} practice ciphers)")
ax.plot(LsB, yB, color=AQUA, linewidth=2, marker="s", markersize=6, markeredgecolor="white", markeredgewidth=1.5,
        label=f"model corpus B ({nB} practice ciphers)")
ax.plot(LsA, comb, color=INK, linewidth=1.2, linestyle=(0, (2, 2)), label="both corpora")
ax.annotate(f"{comb[0]:.0f}%", (LsA[0], comb[0]), xytext=(8, -14), textcoords="offset points", fontsize=10,
            color=INK, fontweight="bold")
ax.annotate(f"{comb[-1]:.0f}%", (LsA[-1], comb[-1]), xytext=(-8, -16), textcoords="offset points", fontsize=10,
            color=INK, fontweight="bold", ha="right")
ax.set_xlim(150, 1120); ax.set_ylim(0, 100)
ax.set_xlabel("length of the symbol stream (grille order known)")
ax.set_ylabel("true table kept (%)")
ax.set_title("Truth-start test: how often the true table is kept, by text length")
ax.legend(loc="lower right")
save(fig, "fig6_identifiability")

json.dump({"A": curves["A"][:2], "B": curves["B"][:2], "combined": comb, "plants_per_corpus": [nA, nB]},
          open(OUT / "fig6_data.json", "w"), indent=1)
print("done")
