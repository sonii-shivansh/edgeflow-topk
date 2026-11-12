"""Exact strict top-k robustness for edge-transfer perturbations.

Research proof: research/PROOF.md
Numerical verification: experiments/RESULTS.md
Core algorithm uses the standard library; tests use SciPy and NumPy.
Novelty has NOT been established.
"""
from bisect import bisect_right
from math import isclose
import random


def degrees(n, edges):
    """Weighted capacity degree for each vertex."""
    d = [0] * n
    for u, v, c in edges:
        assert 0 <= u < n and 0 <= v < n and u != v and c >= 0
        d[u] += c
        d[v] += c
    return d


def pair_gamma(i, j, d, edge_capacity, B):
    """Exact worst-case increase of (updated_score[j] - updated_score[i])."""
    c = edge_capacity.get((min(i, j), max(i, j)), 0)
    other = d[i] + d[j] - 2 * c
    assert other >= -1e-9
    return 2 * min(c, B) + min(max(0, other), max(0, B - c))


def certifies_strict_topk(scores, edges, B, k):
    """Return (is_strictly_robust, violating_pair_or_None, reason).

    Time O(m+n log n), space O(m+n), for a finite simple undirected
    graph with signed independent edge transfers and shared L1 budget.
    A possible top-k boundary tie counts as not strictly robust.
    """
    n = len(scores)
    assert B >= 0 and 1 <= k < n
    seen, cap = set(), {}
    for u, v, c in edges:
        e = (min(u, v), max(u, v))
        assert e not in seen, "Graph must be simple"
        seen.add(e)
        cap[e] = c
    d = degrees(n, edges)
    T = sorted(range(n), key=lambda v: (-scores[v], v))[:k]
    in_top = set(T)
    out = sorted((v for v in range(n) if v not in in_top), key=lambda v: d[v])
    out_d = [d[v] for v in out]
    q = len(out)

    prefix = [None] * q  # max of score[j]+degree[j]
    suffix = [None] * q  # max of score[j]
    for t, j in enumerate(out):
        item = (scores[j] + d[j], j)
        prefix[t] = max(prefix[t - 1], item) if t else item
    for t in range(q - 1, -1, -1):
        j = out[t]
        item = (scores[j], j)
        suffix[t] = max(suffix[t + 1], item) if t < q - 1 else item

    for i in T:
        t = bisect_right(out_d, B - d[i])
        candidates = []
        if t:
            value, j = prefix[t - 1]
            candidates.append((d[i] + value, j))
        if t < q:
            value, j = suffix[t]
            candidates.append((B + value, j))
        worst, j = max(candidates)
        if scores[i] <= worst:
            return False, (i, j), "baseline"

    for u, v, c in edges:
        if (u in in_top) != (v in in_top):
            i, j = (u, v) if u in in_top else (v, u)
            if scores[i] - scores[j] <= pair_gamma(i, j, d, cap, B):
                return False, (i, j), "crossing-edge"
    return True, None, "certified"


def pair_lp_optimum(i, j, n, edges, B):
    """Independently solve the signed-flow pairwise LP using HiGHS."""
    from scipy.optimize import linprog
    m = len(edges)
    if not m:
        return 0.0
    a = [
        int(v == j) - int(u == j) - int(v == i) + int(u == i)
        for u, v, c in edges
    ]
    objective = [-x for x in a] + a
    A_ub, b_ub = [], []
    for t, (_, _, c) in enumerate(edges):
        row = [0.0] * (2 * m)
        row[t] = row[m + t] = 1.0
        A_ub.append(row)
        b_ub.append(c)
    A_ub.append([1.0] * (2 * m))
    b_ub.append(B)
    answer = linprog(
        objective, A_ub=A_ub, b_ub=b_ub,
        bounds=(0, None), method="highs"
    )
    assert answer.success, answer.message
    return float(-answer.fun)


def constructive_witness(i, j, n, edges, B):
    """Feasible signed edge-flow vector attaining the pairwise bound."""
    f = [0] * len(edges)
    remaining = B
    priorities = []
    for t, (u, v, c) in enumerate(edges):
        a = int(v == j) - int(u == j) - int(v == i) + int(u == i)
        if a:
            priorities.append((-abs(a), t, a))
    priorities.sort()
    for _, t, a in priorities:
        amount = min(edges[t][2], remaining)
        f[t] = (1 if a > 0 else -1) * amount
        remaining -= amount
    return f


def witness_value(i, j, edges, f):
    return sum(
        (int(v == j) - int(u == j) - int(v == i) + int(u == i)) * amount
        for (u, v, _), amount in zip(edges, f)
    )


def run_tests():
    rng = random.Random(20261111)
    deterministic = [
        ("empty graph", 3, [], 0, 1, 1),
        ("direct edge, small budget", 2, [(0, 1, 3)], 1, 0, 1),
        ("direct edge, saturated", 2, [(0, 1, 3)], 6, 0, 1),
        ("two-edge path", 3, [(0, 2, 2), (2, 1, 1)], 2.5, 0, 1),
        ("triangle", 3, [(0, 1, 1), (0, 2, 2), (2, 1, 4)], 4, 0, 1),
        ("disconnected", 4, [(0, 2, 2), (1, 3, 3)], 4, 0, 1),
        ("zero capacities", 3, [(0, 1, 0), (1, 2, 0)], 5, 0, 2),
        ("reverse orientation", 3, [(1, 0, 1), (2, 0, 2), (1, 2, 4)], 4, 0, 1),
    ]
    print("DETERMINISTIC PAIR CASES (formula, LP, constructive witness):")
    for title, n, edges, B, i, j in deterministic:
        d = degrees(n, edges)
        cap = {(min(u, v), max(u, v)): c for u, v, c in edges}
        gamma = pair_gamma(i, j, d, cap, B)
        lp = pair_lp_optimum(i, j, n, edges, B)
        f = constructive_witness(i, j, n, edges, B)
        attained = witness_value(i, j, edges, f)
        assert isclose(gamma, lp, abs_tol=1e-8)
        assert isclose(gamma, attained, abs_tol=1e-8)
        assert sum(abs(x) for x in f) <= B + 1e-9
        assert all(abs(x) <= e[2] + 1e-9 for x, e in zip(f, edges))
        print(f"  {title:27s}: {gamma:5.2f}, {lp:5.2f}, {attained:5.2f}")

    total_pairs = robust = nonrobust = 0
    failures = []
    max_error = 0.0
    for iteration in range(350):
        n = rng.randint(2, 8)
        edges = []
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < 0.43:
                    c = rng.randint(0, 5)
                    edges.append(
                        (u, v, c) if rng.randrange(2) == 0 else (v, u, c)
                    )
        B = rng.randint(0, 24) / 2
        scores = [rng.randint(-4, 15) for _ in range(n)]
        k = rng.randint(1, n - 1)
        d = degrees(n, edges)
        cap = {(min(u, v), max(u, v)): c for u, v, c in edges}
        T = sorted(range(n), key=lambda v: (-scores[v], v))[:k]
        outsiders = [j for j in range(n) if j not in T]
        exhaustive_lp = True

        for i in T:
            for j in outsiders:
                total_pairs += 1
                gamma = pair_gamma(i, j, d, cap, B)
                lp = pair_lp_optimum(i, j, n, edges, B)
                max_error = max(max_error, abs(gamma - lp))
                if not isclose(gamma, lp, abs_tol=1e-8):
                    failures.append(("pair", iteration, i, j, gamma, lp))
                f = constructive_witness(i, j, n, edges, B)
                if not isclose(witness_value(i, j, edges, f), gamma, abs_tol=1e-8):
                    failures.append(("witness", iteration, i, j))
                if sum(abs(x) for x in f) > B + 1e-8:
                    failures.append(("budget", iteration, i, j))
                if scores[i] - scores[j] <= lp + 1e-8:
                    exhaustive_lp = False

        fast, pair, reason = certifies_strict_topk(scores, edges, B, k)
        if fast != exhaustive_lp:
            failures.append(("decision", iteration, fast, exhaustive_lp))
        if not fast and pair is not None:
            i, j = pair
            f = constructive_witness(i, j, n, edges, B)
            assert scores[i] - scores[j] <= witness_value(i, j, edges, f) + 1e-8
        robust += int(fast)
        nonrobust += int(not fast)

    print(f"\nRANDOMIZED: seed=20261111, graphs=350, pair-LPs={total_pairs}")
    print(f"  exact algorithm vs independently solved LPs: {350-len([x for x in failures if x[0]=='decision'])}/350 agreements")
    print(f"  certified strict robust: {robust}; not robust: {nonrobust}")
    print(f"  maximum pair |formula - LP|: {max_error:.3g}")
    print(f"  failures: {len(failures)}")
    if failures:
        raise AssertionError(failures[:5])

    explicit = [
        ("rank boundary tie at B=0", [5, 5, 2], [], 0, 1),
        ("direct-edge correction detects failure", [10, 7, 0], [(0, 1, 2)], 2, 1),
        ("robust despite possible redistribution", [10, 1, 0], [(0, 1, 2)], 2, 1),
        ("nonedge baseline detects failure", [7, 5, 0, 0], [(0, 2, 3), (1, 3, 3)], 2, 1),
    ]
    print("\nEXPLICIT RANK CASES:")
    for title, s, e, B, k in explicit:
        answer, pair, reason = certifies_strict_topk(s, e, B, k)
        print(f"  {title:44s}: robust={answer}, reason={reason}, witness_pair={pair}")


if __name__ == "__main__":
    run_tests()



def topk_robustness_margin(scores, edges, B, k):
    """Return the exact worst-case top-k separation margin.

    Returns (margin, (insider, outsider), source) in O(m+n log n) time
    and O(m+n) space. The margin equals
      min_{feasible flows} min_{i in original top-k, j outside} (s'_i-s'_j).
    Positive means strictly robust; zero means a tie is attainable;
    negative means some outsider can overtake an original insider.
    Witness flows can be constructed with constructive_witness.
    For exact arithmetic use Python int or fractions.Fraction inputs.
    """
    n = len(scores)
    assert B >= 0 and 1 <= k < n
    capacity = {}
    for u, v, c in edges:
        assert 0 <= u < n and 0 <= v < n and u != v and c >= 0
        e = (min(u, v), max(u, v))
        assert e not in capacity, "Graph must be simple"
        capacity[e] = c
    d = degrees(n, edges)
    top = sorted(range(n), key=lambda v: (-scores[v], v))[:k]
    in_top = set(top)
    outsiders = sorted((j for j in range(n) if j not in in_top),
                       key=lambda j: d[j])
    outsider_degrees = [d[j] for j in outsiders]
    q = len(outsiders)
    prefix = [None] * q
    suffix = [None] * q
    for t, j in enumerate(outsiders):
        candidate = (scores[j] + d[j], j)
        prefix[t] = max(prefix[t - 1], candidate) if t else candidate
    for t in range(q - 1, -1, -1):
        j = outsiders[t]
        candidate = (scores[j], j)
        suffix[t] = max(suffix[t + 1], candidate) if t < q - 1 else candidate

    best = None
    for i in top:
        r = bisect_right(outsider_degrees, B - d[i])
        candidates = []
        if r:
            value, j = prefix[r - 1]
            candidates.append((scores[i] - d[i] - value,
                               (i, j), "baseline"))
        if r < q:
            value, j = suffix[r]
            candidates.append((scores[i] - B - value,
                               (i, j), "baseline"))
        for candidate in candidates:
            if best is None or candidate[0] < best[0]:
                best = candidate

    for u, v, _ in edges:
        if (u in in_top) != (v in in_top):
            i, j = (u, v) if u in in_top else (v, u)
            exact = scores[i] - scores[j] - pair_gamma(
                i, j, d, capacity, B)
            if exact < best[0]:
                best = (exact, (i, j), "crossing-edge")

    return best
