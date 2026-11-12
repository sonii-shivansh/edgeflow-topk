"""Small synthetic scaling illustration (not a representative benchmark)."""
from pathlib import Path
from time import perf_counter
import random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from edge_transfer_topk import certifies_strict_topk


def make_case(n):
    rng = random.Random(20261112 + n)
    edges = [(i,i+1,rng.randrange(1,5)) for i in range(n-1)]
    existing = {(i,i+1) for i in range(n-1)}
    while len(edges) < 4*n:
        u,v = rng.randrange(n),rng.randrange(n)
        if u == v:
            continue
        u,v = sorted((u,v))
        if (u,v) in existing:
            continue
        existing.add((u,v))
        edges.append((u,v,rng.randrange(1,5)))
    return [10**9]*(n//2)+[0]*(n-n//2), edges


if __name__ == "__main__":
    print("n, m, seconds, robust")
    for n in [1000,10000,50000]:
        scores,edges = make_case(n)
        start = perf_counter()
        answer = certifies_strict_topk(scores,edges,1000,n//2)
        elapsed = perf_counter()-start
        print(f"{n}, {len(edges)}, {elapsed:.6f}, {answer[0]}")
        assert answer[0]
