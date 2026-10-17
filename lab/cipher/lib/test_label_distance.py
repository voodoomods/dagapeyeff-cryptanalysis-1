"""Unit tests for label_distance.py.   python test_label_distance.py   (or pytest)

(a) label-permutation invariance; (b) the known counterexample (greedy 4, exact 3); (c) random balanced tables;
(d) exact distance never exceeds greedy distance; (e) the legacy function reproduces round12/review_checks.wrong on the
2,000 saved robustness tables (lab/cipher/audit/label_full.json), if that file is present.
"""
import json
import os
import random

import numpy as np

from label_distance import exact_label_distance, legacy_greedy_label_distance, raw_label_distance

HERE = os.path.dirname(os.path.abspath(__file__))


def balanced_random_table(rnd, k=13, n=26):
    t = [i % k for i in range(n)]          # every group has n/k letters
    rnd.shuffle(t)
    return t


def test_a_permutation_invariance():
    rnd = random.Random(1)
    for _ in range(500):
        truth = balanced_random_table(rnd)
        perm = list(range(13)); rnd.shuffle(perm)
        relab = [perm[x] for x in truth]
        assert exact_label_distance(relab, truth) == 0
        other = balanced_random_table(rnd)
        assert exact_label_distance([perm[x] for x in other], truth) == exact_label_distance(other, truth)


def test_b_counterexample():
    found = [0, 0, 0, 0, 0, 1, 1] + [2 + i % 11 for i in range(19)]
    truth = [0, 0, 0, 1, 1, 0, 0] + [2 + i % 11 for i in range(19)]
    assert legacy_greedy_label_distance(found, truth) == 4
    assert exact_label_distance(found, truth) == 3
    assert raw_label_distance(found, truth) == 4


def test_c_random_balanced_tables():
    rnd = random.Random(2)
    for _ in range(2000):
        a, b = balanced_random_table(rnd), balanced_random_table(rnd)
        d = exact_label_distance(a, b)
        assert 0 <= d <= 26 - 2               # at least one group's two letters can always be matched
        assert d <= raw_label_distance(a, b)


def test_d_exact_never_exceeds_greedy():
    rng = np.random.default_rng(3)
    for _ in range(5000):
        truth = list(rng.integers(0, 13, 26)); t = list(truth)
        for _ in range(int(rng.integers(1, 9))):
            i, j = rng.integers(0, 26, 2); t[i], t[j] = t[j], t[i]
        assert exact_label_distance(t, truth) <= legacy_greedy_label_distance(t, truth)


def test_e_legacy_reproduces_published():
    """Recompute both distances for all 2,000 saved robustness tables against their regenerated true tables."""
    path = os.path.join(HERE, "..", "audit", "label_full.json")
    if not os.path.exists(path):
        return
    import sys
    sys.path.insert(0, os.path.join(HERE, "..", "grille"))
    import re
    import poly_engine as pe
    lm = os.path.join(HERE, "..", "lm", "corpus")
    files = sorted(f for f in os.listdir(lm) if f.endswith(".txt"))
    if len(files) != 13:   # the two Christie novels are not redistributed; see lab/cipher/lm/CORPUS.md
        print("skip test_e: corpus incomplete (%d of 13 novels) - add the two Christie novels per CORPUS.md" % len(files))
        return
    held = {"time-machine.txt", "war-of-the-worlds.txt"}
    read = lambda fs: re.sub("[^A-Z]", "", "".join(open(os.path.join(lm, f), encoding="utf-8", errors="ignore").read() for f in fs).upper())  # noqa: E731
    A = read([f for f in files[0::2] if f not in held]); B = read(files[1::2])
    text = {"A": A, "B": B, "C": A + B}
    runs = json.load(open(path))["runs"]
    g_ok = x_ok = 0
    truths = {}
    for r in runs:
        key = (r["model"][0], r["plant"])
        if key not in truths:
            truths[key] = pe.balanced_table(text[key[0]], 13, random.Random(12000 + key[1]))
        truth = truths[key]
        g_ok += legacy_greedy_label_distance(r["table"], truth) == r["greedy"]
        x_ok += exact_label_distance(r["table"], truth) == r["exact"]
    assert (g_ok, x_ok) == (len(runs), len(runs)) == (2000, 2000)
    assert sum(r["greedy"] != r["exact"] for r in runs) == 80
    assert sum((r["greedy"] == 0) != (r["exact"] == 0) for r in runs) == 0


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn(); print("pass", name)
