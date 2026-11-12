"""Exact separation-margin tests, including two independent oracles.

The all-pairs oracle tests the new O(m+n log n) margin reduction.
The exhaustive-grid oracle computes minimum separations by enumerating
feasible signed edge flows, without using the pairwise Gamma formula.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from edge_transfer_topk import (
    topk_robustness_margin,
    pair_gamma,
    degrees,
    constructive_witness,
    witness_value,
)


def top_and_outsiders(scores, k):
    top = sorted(range(len(scores)), key=lambda i: (-scores[i], i))[:k]
    return top, [j for j in range(len(scores)) if j not in top]


def pair_oracle(scores, edges, B, k):
    d = degrees(len(scores), edges)
    cap = {(min(u, v), max(u, v)): c for u, v, c in edges}
    top, outsiders = top_and_outsiders(scores, k)
    return min(
        scores[i] - scores[j] - pair_gamma(i, j, d, cap, B)
        for i in top for j in outsiders
    )


def flow_oracle(scores, edges, B, k, step=Fraction(1, 2)):
    """Exact exhaustive signed flow enumeration on the specified grid."""
    top, outsiders = top_and_outsiders(scores, k)
    options = []
    for _, _, capacity in edges:
        count = int(capacity / step)
        assert count * step == capacity
        options.append([z * step for z in range(-count, count + 1)])
    best = None
    for f in product(*options):
        if sum(abs(x) for x in f) > B:
            continue
        updated = list(scores)
        for (u, v, _), amount in zip(edges, f):
            updated[u] -= amount
            updated[v] += amount
        value = min(updated[i] - updated[j] for i in top for j in outsiders)
        if best is None or value < best:
            best = value
    return best


class MarginCertificateTests(unittest.TestCase):
    def test_large_integer_exactness(self):
        for exponent in (30, 100, 500):
            h = 10 ** exponent
            self.assertEqual(
                topk_robustness_margin([h + 1, h], [], 0, 1)[0], 1
            )
        self.assertEqual(
            topk_robustness_margin([10, 7, 0], [(0, 1, 2)], 2, 1)[0],
            -1,
        )
        self.assertEqual(
            topk_robustness_margin([10, 6, 0], [(0, 1, 2)], 2, 1)[0],
            0,
        )
        self.assertEqual(
            topk_robustness_margin([10, 1, 0], [(0, 1, 2)], 2, 1)[0],
            5,
        )

    def test_all_pairs_oracle_2600_integer_graphs(self):
        rng = random.Random(20261112)
        for case in range(2600):
            n = rng.randrange(2, 12)
            edges = []
            for i in range(n):
                for j in range(i + 1, n):
                    if rng.random() < 0.4:
                        edges.append((i, j, rng.randrange(4)))
            scores = [rng.randrange(-10, 20) for _ in range(n)]
            B = rng.randrange(15)
            k = rng.randrange(1, n)
            margin, pair, source = topk_robustness_margin(
                scores, edges, B, k
            )
            self.assertEqual(
                margin, pair_oracle(scores, edges, B, k),
                (case, scores, edges, B, k),
            )
            i, j = pair
            f = constructive_witness(i, j, n, edges, B)
            actual_margin = scores[i] - scores[j] - witness_value(
                i, j, edges, f)
            self.assertEqual(actual_margin, margin)
            self.assertLessEqual(sum(abs(x) for x in f), B)
            self.assertTrue(all(
                abs(x) <= c for x, (_, _, c) in zip(f, edges)
            ))

    def test_independent_signed_flow_oracle_420_fraction_graphs(self):
        rng = random.Random(11022026)
        step = Fraction(1, 2)
        for case in range(420):
            n = rng.randrange(2, 6)
            edges = []
            for i in range(n):
                for j in range(i + 1, n):
                    if len(edges) < 4 and rng.random() < 0.42:
                        edges.append((i, j, Fraction(rng.randrange(4), 2)))
            scores = [Fraction(rng.randrange(-4, 14), 2)
                      for _ in range(n)]
            B = Fraction(rng.randrange(9), 2)
            k = rng.randrange(1, n)
            observed = topk_robustness_margin(scores, edges, B, k)[0]
            expected = flow_oracle(scores, edges, B, k, step)
            self.assertEqual(
                observed, expected, (case, scores, edges, B, k)
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
