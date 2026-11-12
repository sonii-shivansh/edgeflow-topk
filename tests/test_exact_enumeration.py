"""Independent exact oracle: enumerate feasible signed flows on small grids.

Does not use Gamma or the LP solver. Integral/half-integral capacities and
budget suffice for extremal optimal flows in this separable budgeted model.
"""
from fractions import Fraction
from pathlib import Path
from itertools import product
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from edge_transfer_topk import certifies_strict_topk


def oracle(scores, edges, budget, k, step=1):
    n = len(scores)
    top = sorted(range(n), key=lambda i: (-scores[i], i))[:k]
    out = [j for j in range(n) if j not in top]
    ranges = []
    for _, _, capacity in edges:
        bound = int(capacity / step)
        assert bound * step == capacity
        ranges.append([x * step for x in range(-bound, bound + 1)])
    for flows in product(*ranges):
        if sum(abs(f) for f in flows) > budget:
            continue
        updated = list(scores)
        for (u, v, _), f in zip(edges, flows):
            updated[u] -= f
            updated[v] += f
        if any(updated[i] <= updated[j] for i in top for j in out):
            return False
    return True


class ExactEnumerationTests(unittest.TestCase):
    def test_very_large_integer_scores(self):
        h = 10**100
        self.assertTrue(certifies_strict_topk([h+1,h], [], 0, 1)[0])
        self.assertTrue(certifies_strict_topk([h+1,h], [(0,1,0)], 0, 1)[0])
        self.assertTrue(certifies_strict_topk([3*h,0], [(0,1,h)], h, 1)[0])
        self.assertFalse(certifies_strict_topk([2*h,0], [(0,1,h)], h, 1)[0])

    def test_exhaustive_integer_flows(self):
        rng = random.Random(20261112)
        for case in range(260):
            n = rng.randint(2, 6)
            edges = []
            for i in range(n):
                for j in range(i+1, n):
                    if rng.random() < 0.34 and len(edges) < 5:
                        c = rng.randint(0, 2)
                        edges.append((i,j,c) if rng.randrange(2) else (j,i,c))
            scores = [rng.randint(-3,9) for _ in range(n)]
            budget = rng.randint(0,4)
            k = rng.randint(1,n-1)
            expected = oracle(scores,edges,budget,k)
            observed = certifies_strict_topk(scores,edges,budget,k)[0]
            self.assertEqual(observed,expected,(case,scores,edges,budget,k))

    def test_exhaustive_half_unit_flows(self):
        rng = random.Random(20261113)
        half = Fraction(1,2)
        for case in range(90):
            n = rng.randint(2,5)
            edges = []
            for i in range(n):
                for j in range(i+1,n):
                    if rng.random() < 0.35 and len(edges) < 4:
                        c = Fraction(rng.randint(0,4),2)
                        edges.append((i,j,c) if rng.randrange(2) else (j,i,c))
            scores = [Fraction(rng.randint(-4,10),2) for _ in range(n)]
            budget = Fraction(rng.randint(0,6),2)
            k = rng.randint(1,n-1)
            expected = oracle(scores,edges,budget,k,step=half)
            observed = certifies_strict_topk(scores,edges,budget,k)[0]
            self.assertEqual(observed,expected,(case,scores,edges,budget,k))


if __name__ == "__main__":
    unittest.main(verbosity=2)
