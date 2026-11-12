"""Independent LP and exhaustive exact-grid tests for directional dual budget.

The grid oracle enumerates actual directed flows and signed measurement errors,
without invoking the pairwise formula or the fast dominance algorithm.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import random
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experimental"))
from directional_dual_budget import (
    topk_dual_budget_margin, pairwise_dual_bound,
    witness_for_pair, adjusted_scores,
)


def direct_flow_enumeration(scores, arcs, error_caps, B, E, k, step=1):
    n = len(scores)
    insiders = sorted(range(n), key=lambda v: (-scores[v], v))[:k]
    outsiders = [j for j in range(n) if j not in insiders]
    options_f = [
        [step * x for x in range(int(c / step) + 1)]
        for _, _, c in arcs]
    options_e = [
        [step * x for x in range(-int(c / step), int(c / step) + 1)]
        for c in error_caps]
    best = None
    for f in product(*options_f):
        if sum(f) > B:
            continue
        for e in product(*options_e):
            if sum(abs(v) for v in e) > E:
                continue
            s = adjusted_scores(scores, arcs, f, e)
            margin = min(s[i] - s[j] for i in insiders for j in outsiders)
            if best is None or margin < best:
                best = margin
    return best


def independent_lp_pair(i, j, arcs, error_caps, B, E):
    """Independent LP over nonnegative flows and split +/- errors."""
    from scipy.optimize import linprog
    n = len(error_caps)
    m = len(arcs)
    coeff = [
        int(u == i) + int(v == j) - int(v == i) - int(u == j)
        for u, v, c in arcs]
    objective = [-z for z in coeff]
    objective += [-int(v == j) + int(v == i) for v in range(n)]
    objective += [int(v == j) - int(v == i) for v in range(n)]
    rows, rhs = [], []
    row = [0] * (m + 2 * n)
    for t in range(m):
        row[t] = 1
    rows.append(row)
    rhs.append(B)
    row = [0] * (m + 2 * n)
    for t in range(m, m + 2 * n):
        row[t] = 1
    rows.append(row)
    rhs.append(E)
    for v in range(n):
        row = [0] * (m + 2 * n)
        row[m + v] = 1
        row[m + n + v] = 1
        rows.append(row)
        rhs.append(error_caps[v])
    bounds = [(0, c) for _, _, c in arcs] + [(0, None)] * (2 * n)
    result = linprog(
        objective, A_ub=rows, b_ub=rhs, bounds=bounds, method="highs")
    assert result.success, result.message
    return -result.fun


class ExactDualBudgetTests(unittest.TestCase):
    def test_deterministic(self):
        cases = [
            ([10, 7], [(0, 1, 2)], [0, 0], 2, 0, 1, -1),
            ([10, 7], [(1, 0, 2)], [0, 0], 2, 0, 1, 3),
            ([10, 7], [], [2, 2], 0, 3, 1, 0),
            ([10, 7], [(0, 1, 2)], [2, 2], 2, 3, 1, -4),
            ([10, 7], [(0, 1, 2)], [2, 2], 0, 0, 1, 3),
            ([10, 6], [(0, 1, 2)], [0, 0], 2, 0, 1, 0),
            ([10, 6], [(1, 0, 2)], [0, 0], 2, 0, 1, 4),
            ([10**100 + 1, 10**100], [], [0, 0], 0, 0, 1, 1),
        ]
        for scores, arcs, a, B, E, k, expected in cases:
            got = topk_dual_budget_margin(scores, arcs, a, B, E, k)
            self.assertEqual(got[0], expected)

    def test_all_pairs_1000_random_graphs(self):
        rng = random.Random(20261112)
        for trial in range(1000):
            n = rng.randint(2, 12)
            arcs = []
            for u in range(n):
                for v in range(n):
                    if u != v and rng.random() < 0.22:
                        arcs.append((u, v, rng.randint(0, 6)))
            scores = [rng.randint(-20, 30) for _ in range(n)]
            a = [rng.randint(0, 5) for _ in range(n)]
            B, E = rng.randint(0, 15), rng.randint(0, 12)
            k = rng.randint(1, n - 1)
            top = sorted(range(n), key=lambda v: (-scores[v], v))[:k]
            rest = [j for j in range(n) if j not in top]
            exact = min(
                scores[i] - scores[j] - pairwise_dual_bound(
                    i, j, arcs, a, B, E)
                for i in top for j in rest)
            margin, pair, source = topk_dual_budget_margin(
                scores, arcs, a, B, E, k)
            self.assertEqual(margin, exact, (trial, source))
            f, err = witness_for_pair(n, *pair, arcs, a, B, E)
            updated = adjusted_scores(scores, arcs, f, err)
            self.assertEqual(updated[pair[0]] - updated[pair[1]], margin)
            self.assertLessEqual(sum(f), B)
            self.assertLessEqual(sum(abs(x) for x in err), E)

    def test_exact_rational_flow_enumeration_115(self):
        rng = random.Random(11022026)
        half = Fraction(1, 2)
        for trial in range(115):
            n = rng.randint(2, 4)
            arcs = []
            for u in range(n):
                for v in range(n):
                    if u != v and len(arcs) < 3 and rng.random() < 0.3:
                        arcs.append((u, v, half * rng.randint(0, 2)))
            a = [half * rng.randint(0, 2) for _ in range(n)]
            scores = [half * rng.randint(-3, 14) for _ in range(n)]
            B = half * rng.randint(0, 3)
            E = half * rng.randint(0, 3)
            k = rng.randint(1, n - 1)
            expected = direct_flow_enumeration(
                scores, arcs, a, B, E, k, half)
            got = topk_dual_budget_margin(scores, arcs, a, B, E, k)[0]
            self.assertEqual(got, expected, trial)

    def test_independent_lp_390_pairs(self):
        rng = random.Random(20261114)
        checked = 0
        for trial in range(85):
            n = rng.randint(2, 7)
            arcs = []
            for u in range(n):
                for v in range(n):
                    if u != v and rng.random() < 0.3:
                        arcs.append((u, v, rng.randint(0, 5)))
            scores = [rng.randint(0, 20) for _ in range(n)]
            a = [rng.randint(0, 5) for _ in range(n)]
            B, E = rng.randint(0, 12), rng.randint(0, 12)
            k = rng.randint(1, n - 1)
            top = sorted(range(n), key=lambda v: (-scores[v], v))[:k]
            rest = [j for j in range(n) if j not in top]
            margins = []
            for i in top:
                for j in rest:
                    optimum = independent_lp_pair(i, j, arcs, a, B, E)
                    margins.append(scores[i] - scores[j] - optimum)
                    self.assertAlmostEqual(
                        optimum, pairwise_dual_bound(
                            i, j, arcs, a, B, E), places=7)
                    checked += 1
            got = topk_dual_budget_margin(scores, arcs, a, B, E, k)[0]
            self.assertAlmostEqual(got, min(margins), places=7)
        self.assertEqual(checked, 390)


if __name__ == "__main__":
    unittest.main(verbosity=2)
