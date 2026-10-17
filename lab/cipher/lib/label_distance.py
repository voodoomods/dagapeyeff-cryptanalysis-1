"""Group-label distance between two polyphonic tables (letter -> group id), for FUTURE experiments.

Default: `exact_label_distance` — letters that disagree after the best one-to-one relabelling of the group ids,
found by maximum-weight bipartite assignment (scipy.optimize.linear_sum_assignment, maximize=True). This is the
minimum over all label permutations.

`legacy_greedy_label_distance` reproduces round12/review_checks.wrong exactly (greedy pick of the largest cells of the
label contingency table). It is kept only to reproduce the published results; it can exceed the exact distance.
`raw_label_distance` counts letters whose group id differs with no relabelling — the right measure when the group ids
are observed cipher symbols (as in the truth-start test).

Every result record written with these functions should name the metric, e.g. {"distance_metric": "exact_assignment"}.
"""
from collections import Counter

import numpy as np
from scipy.optimize import linear_sum_assignment

METRIC_EXACT = "exact_assignment"
METRIC_GREEDY = "legacy_greedy"
METRIC_RAW = "raw_letterwise"


def _contingency(t, truth, k):
    m = np.zeros((k, k))
    for a, b in zip(t, truth):
        m[a, b] += 1
    return m


def exact_label_distance(t, truth, k=13):
    """Letters in disagreement after the optimal one-to-one relabelling of t's group ids onto truth's."""
    if len(t) != len(truth):
        raise ValueError("tables must have the same length")
    m = _contingency(t, truth, k)
    r, c = linear_sum_assignment(m, maximize=True)
    return len(t) - int(m[r, c].sum())


def legacy_greedy_label_distance(t, truth):
    """The greedy matching used by round12/review_checks.wrong (published results). Not optimal in general."""
    pairs = Counter(zip(t, truth))
    used_a, used_b, agree = set(), set(), 0
    for (x, y), n in pairs.most_common():
        if x not in used_a and y not in used_b:
            used_a.add(x); used_b.add(y); agree += n
    return len(t) - agree


def raw_label_distance(t, truth):
    """Letters whose group id differs, without relabelling."""
    if len(t) != len(truth):
        raise ValueError("tables must have the same length")
    return sum(a != b for a, b in zip(t, truth))


DISTANCES = {METRIC_EXACT: exact_label_distance, METRIC_GREEDY: legacy_greedy_label_distance, METRIC_RAW: raw_label_distance}
