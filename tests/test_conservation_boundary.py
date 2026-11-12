"""Conservation-model counterexample: distinguish exactness from lower bound.

This is NOT a test of a defect in EdgeFlow's independent-arc theorem.
It checks the limits of applying that theorem to a different flow model.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experimental"))
from directional_dual_budget import topk_dual_budget_margin, adjusted_scores


class ConservationBoundaryTests(unittest.TestCase):
    def test_independent_vs_routed_global_margin(self):
        scores = [4, 0, 0, 0]
        arcs = [(0, 1, 1), (1, 2, 1), (2, 3, 1)]
        independent, pair, _ = topk_dual_budget_margin(
            scores, arcs, [0] * 4, 1, 0, 1
        )
        self.assertEqual(independent, 2)
        self.assertEqual(pair, (0, 1))

        # For a conserved routed path, all flows equal t, 0 <= t <= 1/3.
        t = Fraction(1, 3)
        routed = adjusted_scores(
            scores, arcs, [t, t, t], [0] * 4
        )
        routed_margin = min(routed[0] - routed[j] for j in (1, 2, 3))
        self.assertEqual(routed_margin, Fraction(10, 3))
        self.assertLess(independent, routed_margin)

        # Independent-arc witness f=(1,0,0) is NOT conserved at node 1.
        independent_witness = adjusted_scores(
            scores, arcs, [1, 0, 0], [0] * 4
        )
        self.assertEqual(independent_witness[0] - independent_witness[1], 2)
        self.assertNotEqual(1, 0)

    def test_exact_grid_enumeration_of_conserved_flows(self):
        scores = [4, 0, 0, 0]
        arcs = [(0, 1, 1), (1, 2, 1), (2, 3, 1)]
        step = Fraction(1, 12)
        feasible_margins = []
        for grid in product(range(13), repeat=3):
            f = [step * x for x in grid]
            if sum(f) > 1:
                continue
            # Conservation at both intermediate nodes.
            if f[0] != f[1] or f[1] != f[2]:
                continue
            updated = adjusted_scores(scores, arcs, f, [0] * 4)
            feasible_margins.append(
                min(updated[0] - updated[j] for j in (1, 2, 3))
            )
        self.assertEqual(min(feasible_margins), Fraction(10, 3))

    def test_conservative_guarantee_is_one_way(self):
        # Strictly positive independent-arc margin implies strict robustness
        # for any subset of its feasible flows, including conserved flows.
        scores = [10, 0, 0, 0]
        arcs = [(0, 1, 1), (1, 2, 1), (2, 3, 1)]
        independent = topk_dual_budget_margin(
            scores, arcs, [0] * 4, 1, 0, 1
        )[0]
        self.assertGreater(independent, 0)
        self.assertEqual(independent, 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
