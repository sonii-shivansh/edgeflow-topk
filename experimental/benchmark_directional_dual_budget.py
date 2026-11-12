"""Synthetic single-run scaling illustration for directional dual-budget ranking.

Not a representative real workload, scientific benchmark, or proof of an
asymptotic lower bound. Use several warmups/repeats on fixed hardware before
making performance claims.
"""
from pathlib import Path
from random import Random
from time import perf_counter
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from directional_dual_budget import topk_dual_budget_margin


def instance(n):
    rng = Random(20261112 + n)
    arcs, seen = [], set()
    while len(arcs) < min(n * (n - 1), 4 * n):
        u, v = rng.randrange(n), rng.randrange(n)
        if u == v or (u, v) in seen:
            continue
        seen.add((u, v))
        arcs.append((u, v, rng.randint(1, 5)))
    error_caps = [rng.randint(0, 5) for _ in range(n)]
    scores = (
        [100000 + rng.randint(0, 1000) for _ in range(n // 2)]
        + [rng.randint(0, 1000) for _ in range(n - n // 2)]
    )
    return scores, arcs, error_caps, 20, 15, n // 2


if __name__ == "__main__":
    print("n,m,seconds,worst_margin,strictly_robust")
    for n in (1000, 5000, 20000):
        scores, arcs, error_caps, B, H, k = instance(n)
        start = perf_counter()
        value = topk_dual_budget_margin(scores, arcs, error_caps, B, H, k)
        elapsed = perf_counter() - start
        print(f"{n},{len(arcs)},{elapsed:.6f},{value[0]},{value[0]>0}")
