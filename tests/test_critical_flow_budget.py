"""Independent validation of critical budget: analytical pair thresholds and real flows.

The exhaustive oracle enumerates actual half-unit directed flows and integer
measurement errors; it does not use the near-linear algorithm or Gamma bound.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experimental.critical_flow_budget import critical_flow_budget
from experimental.directional_dual_budget import (
    topk_dual_budget_margin, adjusted_scores, witness_for_pair,
)


def all_pairs_threshold(scores, arcs, error_caps, H, k):
    n = len(scores)
    top = sorted(range(n), key=lambda i: (-scores[i], i))[:k]
    outsiders = [j for j in range(n) if j not in top]
    out = [sum(c for u,v,c in arcs if u == i) for i in range(n)]
    incoming = [sum(c for u,v,c in arcs if v == j) for j in range(n)]
    cap = {(u,v):c for u,v,c in arcs}
    result = None
    for i in top:
        for j in outsiders:
            deficit = scores[i] - scores[j] - min(
                H, error_caps[i] + error_caps[j])
            c = cap.get((i,j), 0)
            max_damage = out[i] + incoming[j]
            if deficit <= 0:
                threshold = Fraction(0)
            elif deficit > max_damage:
                continue
            elif deficit <= 2*c:
                threshold = Fraction(deficit, 2)
            else:
                threshold = Fraction(deficit - c)
            if result is None or threshold < result:
                result = threshold
    return result


def brute_force_threshold(scores, arcs, error_caps, H, k):
    """Enumerate all half-unit flows and integer error vectors for small cases."""
    n = len(scores)
    top = sorted(range(n), key=lambda i: (-scores[i], i))[:k]
    outsiders = [j for j in range(n) if j not in top]
    legal_errors = [
        e for e in product(*(range(-a, a+1) for a in error_caps))
        if sum(abs(v) for v in e) <= H]
    earliest = None
    for half_flow in product(*(range(2*c+1) for _,_,c in arcs)):
        units = sum(half_flow)
        if earliest is not None and units >= earliest:
            continue
        f = [Fraction(x,2) for x in half_flow]
        for errors in legal_errors:
            new = adjusted_scores(scores, arcs, f, errors)
            if any(new[i] <= new[j] for i in top for j in outsiders):
                earliest = units if earliest is None else min(earliest, units)
                break
    return None if earliest is None else Fraction(earliest, 2)


class CriticalFlowBudgetTests(unittest.TestCase):
    def test_deterministic_and_huge_integer_cases(self):
        examples = [
            ([3,0], [(0,1,1)], [1,1], 0, 1, None),
            ([3,0], [(0,1,1)], [1,1], 1, 1, Fraction(1)),
            ([3,0], [(0,1,1)], [1,1], 2, 1, Fraction(1,2)),
            ([3,0], [(0,1,1)], [1,1], 3, 1, Fraction(1,2)),
            ([3,0], [(0,1,1)], [0,0], 0, 1, None),
            ([2,0], [(0,1,1)], [0,0], 0, 1, Fraction(1)),
            ([1,0], [(0,1,1)], [0,0], 0, 1, Fraction(1,2)),
            ([5,5], [], [0,0], 0, 1, Fraction(0)),
            ([10**100+1, 10**100], [], [0,0], 0, 1, None),
        ]
        for scores, arcs, a, H, k, expected in examples:
            observed, pair, reason = critical_flow_budget(
                scores, arcs, a, H, k)
            self.assertEqual(observed, expected)

    def test_2000_random_graphs_independent_pair_formula(self):
        rng = random.Random(20261112)
        for iteration in range(2000):
            n = rng.randrange(2,10)
            arcs = [
                (i,j,rng.randrange(4))
                for i in range(n) for j in range(n)
                if i != j and rng.random() < 0.22]
            scores = [rng.randrange(-5,16) for _ in range(n)]
            a = [rng.randrange(4) for _ in range(n)]
            H = rng.randrange(10)
            k = rng.randrange(1,n)
            expected = all_pairs_threshold(scores, arcs, a, H, k)
            result, pair, reason = critical_flow_budget(
                scores, arcs, a, H, k)
            self.assertEqual(result, expected, (
                iteration, scores, arcs, a, H, k))
            if result is not None and result > 0:
                # The exact grid immediately below threshold is still safe.
                previous = topk_dual_budget_margin(
                    scores, arcs, a, result - Fraction(1,2), H, k)[0]
                at_budget = topk_dual_budget_margin(
                    scores, arcs, a, result, H, k)[0]
                self.assertGreater(previous, 0)
                self.assertLessEqual(at_budget, 0)
                f,e = witness_for_pair(
                    n, *pair, arcs, a, result, H)
                updated = adjusted_scores(scores, arcs, f, e)
                self.assertLessEqual(updated[pair[0]], updated[pair[1]])

    def test_120_independent_exhaustive_perturbation_cases(self):
        rng = random.Random(12062026)
        for iteration in range(120):
            n = rng.randrange(2,5)
            arcs = []
            for i in range(n):
                for j in range(n):
                    if i != j and len(arcs) < 3 and rng.random() < 0.3:
                        arcs.append((i,j,rng.randrange(3)))
            scores = [rng.randrange(-2,7) for _ in range(n)]
            a = [rng.randrange(2) for _ in range(n)]
            H = rng.randrange(3)
            k = rng.randrange(1,n)
            expected = brute_force_threshold(scores, arcs, a, H, k)
            observed = critical_flow_budget(scores, arcs, a, H, k)[0]
            self.assertEqual(observed, expected, (
                iteration, scores, arcs, a, H, k))

    def test_safe_budget_region_need_not_be_convex(self):
        scores, arcs, a = [3,0], [(0,1,1)], [1,1]
        self.assertGreater(
            topk_dual_budget_margin(scores, arcs, a, 2, 0, 1)[0], 0)
        self.assertGreater(
            topk_dual_budget_margin(scores, arcs, a, 0, 2, 1)[0], 0)
        self.assertEqual(
            topk_dual_budget_margin(scores, arcs, a, 1, 1, 1)[0], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
