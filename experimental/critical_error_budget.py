"""Exact minimal measurement-error budget at a fixed directed flow budget.

For the independently budgeted one-way arc-transfer / signed-node-error model.
Proof: research/CRITICAL_ERROR_BUDGET.md.
Time O(m+n log n), space O(m+n), in the exact comparison model.
Inputs must be Python int or fractions.Fraction. Novelty unconfirmed.
"""
from bisect import bisect_left, bisect_right
from fractions import Fraction
from numbers import Integral

from experimental.directional_dual_budget import topk_dual_budget_margin


def _exact_number(v):
    return isinstance(v, (Integral, Fraction)) and not isinstance(v, bool)


def critical_error_budget(scores, arcs, error_caps, flow_budget, k):
    """Return (minimum_H, pair, origin); H=None if failure is impossible.

    Every allowed directed transfer has 0<=f_uv<=c_uv, sum(f)<=flow_budget.
    Independent node errors obey |e_v|<=error_caps[v], sum|e|<=H.
    H is minimized over all nonnegative real values. A feasible tie is failure
    of strict top-k robustness. For rational inputs the result is exact.
    """
    n = len(scores)
    if not (1 <= k < n and len(error_caps) == n):
        raise ValueError("Require 1 <= k < n and one error cap per vertex")
    if not (all(_exact_number(v) for v in scores)
            and all(_exact_number(v) and v >= 0 for v in error_caps)
            and _exact_number(flow_budget) and flow_budget >= 0):
        raise ValueError("Scores, nonnegative error caps and F must be ints/Fractions")

    Dout, Din = [0]*n, [0]*n
    capacity = {}
    for arc in arcs:
        if len(arc) != 3:
            raise ValueError("Each arc must be (u, v, capacity)")
        u, v, c = arc
        if (not isinstance(u, Integral) or isinstance(u, bool)
                or not isinstance(v, Integral) or isinstance(v, bool)
                or not _exact_number(c) or c < 0
                or not (0 <= u < n and 0 <= v < n and u != v)
                or (u, v) in capacity):
            raise ValueError("Require simple directed arcs with valid exact capacity")
        capacity[u, v] = c
        Dout[u] += c
        Din[v] += c

    top = sorted(range(n), key=lambda v: (-scores[v], v))[:k]
    inside = set(top)
    outsiders = [j for j in range(n) if j not in inside]
    F = flow_budget
    at_zero = topk_dual_budget_margin(scores, arcs, error_caps, F, 0, k)
    if at_zero[0] <= 0:
        return 0, at_zero[1], "already"

    coordinates = sorted(set(Din[j] for j in outsiders))
    q = len(coordinates)
    best = None

    # Non-forward-pair baseline g0=min(F,Dout_i+Din_j).
    # Unsaturated: Din_j<=F-Dout_i; saturated: strict complement.
    for unsaturated in (True, False):
        def x(j):
            return scores[j] + (Din[j] if unsaturated else 0)

        def y(j):
            return x(j) + error_caps[j]

        def query_threshold(i):
            return scores[i] - (Dout[i] if unsaturated else F) - error_caps[i]

        points = sorted(outsiders, key=y, reverse=True)
        queries = sorted(top, key=query_threshold, reverse=True)
        fenwick = [None]*(q+1)

        def insert(pos, entry):
            while pos <= q:
                if fenwick[pos] is None or entry > fenwick[pos]:
                    fenwick[pos] = entry
                pos += pos & -pos

        def query(pos):
            result = None
            while pos > 0:
                entry = fenwick[pos]
                if entry is not None and (result is None or entry > result):
                    result = entry
                pos -= pos & -pos
            return result

        cursor = 0
        for i in queries:
            cut = query_threshold(i)
            while cursor < len(points) and y(points[cursor]) >= cut:
                j = points[cursor]
                rank = bisect_left(coordinates, Din[j])
                insert(rank+1 if unsaturated else q-rank, (x(j), j))
                cursor += 1

            split = bisect_right(coordinates, F-Dout[i])
            eligible = query(split if unsaturated else q-split)
            if eligible is None:
                continue
            max_x, j = eligible
            delta = scores[i] - (Dout[i] if unsaturated else F) - max_x
            assert delta > 0
            if best is None or delta < best[0]:
                best = (delta, (i, j), "baseline")

    # Exact correction only for forward insider -> outsider arcs.
    for (i, j), c in capacity.items():
        if i not in inside or j in inside:
            continue
        other = Dout[i] + Din[j] - 2*c
        damage = 2*min(c, F) + min(other, max(0, F-c))
        delta = scores[i] - scores[j] - damage
        assert delta > 0
        if delta <= error_caps[i] + error_caps[j]:
            if best is None or delta < best[0]:
                best = (delta, (i, j), "arc")

    return best if best is not None else (None, None, "never")
