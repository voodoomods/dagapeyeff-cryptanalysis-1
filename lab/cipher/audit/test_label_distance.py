"""Reproducible test (audit, 2026-10-15): greedy label matching (round12/review_checks.wrong) vs an exact maximum-weight
one-to-one assignment of the 13 group labels. Run:  python test_label_distance.py   (needs numpy, scipy)

review_checks.wrong is a greedy approximation: it takes the largest cells of the 13 x 13 label contingency table first.
It never under-counts agreement for a pure relabelling (distance 0 stays 0) but can over-count distance in general.
"""
from collections import Counter
import numpy as np
from scipy.optimize import linear_sum_assignment


def greedy_distance(t, truth):                       # same algorithm as review_checks.wrong (executed code, unchanged)
    pairs = Counter(zip(t, truth))
    used_a, used_b, agree = set(), set(), 0
    for (x, y), k in pairs.most_common():
        if x not in used_a and y not in used_b:
            used_a.add(x); used_b.add(y); agree += k
    return 26 - agree


def exact_distance(t, truth):
    m = np.zeros((13, 13))
    for a, b in zip(t, truth):
        m[a, b] += 1
    r, c = linear_sum_assignment(m, maximize=True)
    return 26 - int(m[r, c].sum())


def test_counterexample():
    # found groups 0/1 vs true groups 0/1 on 7 letters: (0,0)=3, (0,1)=2, (1,0)=2, (1,1)=0; the other 19 letters agree
    found = [0, 0, 0, 0, 0, 1, 1] + [2 + i % 11 for i in range(19)]
    truth = [0, 0, 0, 1, 1, 0, 0] + [2 + i % 11 for i in range(19)]
    assert greedy_distance(found, truth) == 4      # takes (0,0)=3, then only (1,1)=0 is left
    assert exact_distance(found, truth) == 3       # (0,1)+(1,0) = 4 agreements


def test_relabelling_is_zero_for_both():
    rng = np.random.default_rng(1)
    truth = list(rng.integers(0, 13, 26))
    perm = rng.permutation(13)
    relab = [int(perm[x]) for x in truth]
    assert greedy_distance(relab, truth) == 0 and exact_distance(relab, truth) == 0


def test_greedy_never_below_exact():
    rng = np.random.default_rng(2)
    for _ in range(5000):
        truth = list(rng.integers(0, 13, 26)); t = list(truth)
        for _ in range(int(rng.integers(1, 8))):
            i, j = rng.integers(0, 26, 2); t[i], t[j] = t[j], t[i]
        assert greedy_distance(t, truth) >= exact_distance(t, truth)


if __name__ == "__main__":
    test_counterexample(); test_relabelling_is_zero_for_both(); test_greedy_never_below_exact()
    print("ok: counterexample greedy 4 / exact 3; relabelling 0 / 0; greedy >= exact on 5,000 random swap tables")
