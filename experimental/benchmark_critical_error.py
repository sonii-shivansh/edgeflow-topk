"""Single-run synthetic illustration; NOT a controlled performance benchmark."""
import random
from time import perf_counter
from experimental.critical_error_budget import critical_error_budget


def sample(n):
    rng=random.Random(191126+n)
    arcs=[];seen=set()
    while len(arcs)<4*n:
        u,v=rng.randrange(n),rng.randrange(n)
        if u==v or (u,v) in seen:continue
        seen.add((u,v))
        arcs.append((u,v,rng.randrange(1,5)))
    caps=[rng.randrange(16) for _ in range(n)]
    scores=([22+rng.randrange(4) for _ in range(n//2)]
            +[rng.randrange(3) for _ in range(n-n//2)])
    return scores,arcs,caps,8,n//2


if __name__=="__main__":
    print("n,m,seconds,critical_H")
    for n in (1000,10000,50000):
        scores,arcs,caps,F,k=sample(n)
        start=perf_counter()
        H,pair,source=critical_error_budget(scores,arcs,caps,F,k)
        elapsed=perf_counter()-start
        print(f"{n},{len(arcs)},{elapsed:.6f},{H}")
        assert H==8
