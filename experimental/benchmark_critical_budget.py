"""Single-run synthetic scaling illustration for first-failure transfer budget.

Not a controlled performance benchmark or a guarantee about wall-clock time.
Run: python experimental/benchmark_critical_budget.py
"""
import random
import sys
from pathlib import Path
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experimental.critical_flow_budget import critical_flow_budget


def synthetic_instance(n):
    rng = random.Random(20261112+n)
    arcs, seen = [], set()
    while len(arcs) < 4*n:
        u, v = rng.randrange(n), rng.randrange(n)
        if u == v or (u,v) in seen:
            continue
        seen.add((u,v))
        arcs.append((u,v,rng.randrange(1,5)))
    scores = (
        [1000+rng.randrange(50) for _ in range(n//2)]
        + [rng.randrange(50) for _ in range(n-n//2)]
    )
    errors = [rng.randrange(1,5) for _ in range(n)]
    return scores, arcs, errors, 3, n//2


if __name__ == "__main__":
    print("n,m,seconds,threshold,reason")
    for n in (1000, 10000, 50000):
        scores, arcs, errors, H, k = synthetic_instance(n)
        start = perf_counter()
        budget, pair, reason = critical_flow_budget(scores, arcs, errors, H, k)
        print(f"{n},{len(arcs)},{perf_counter()-start:.6f},{budget},{reason}")
