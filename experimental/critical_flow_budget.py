"""Exact critical directional-transfer budget with fixed measurement-error budget.

The first flow budget at which strict original top-k membership can fail is
obtained using two offline 2D dominance-max sweeps and an exceptional-arc scan.
Time: O(m+n log n) comparisons/arithmetic; space O(m+n).
Assumptions: integer scores, arc capacities, per-node error capacities, and H;
simple directed graph, independent nonnegative one-way arc flows.
Academic novelty is UNCONFIRMED; this is unreviewed research software.
"""
from bisect import bisect_left, bisect_right
from fractions import Fraction
from numbers import Integral

from experimental.directional_dual_budget import topk_dual_budget_margin


def critical_flow_budget(scores, arcs, error_caps, error_budget, k):
    """Return (smallest_F, (insider, outsider), reason).

    A finite threshold is a nonnegative integer or half-integer (Fraction).
    Return (None, None, 'never') if no feasible flow budget can break strict
    separation, even when all arcs are saturated.
    Return (0, pair, 'already') if measurement errors alone suffice.
    Values are mathematically exact for Python integer inputs.
    """
    n = len(scores)
    assert len(error_caps) == n and 1 <= k < n
    assert all(isinstance(x, Integral) and not isinstance(x, bool) for x in scores)
    assert all(isinstance(x, Integral) and x >= 0 for x in error_caps)
    assert isinstance(error_budget, Integral) and error_budget >= 0
    assert all(len(arc) == 3 and all(
        isinstance(y, Integral) and not isinstance(y, bool) for y in arc)
        for arc in arcs)

    H = error_budget
    Dout, Din = [0] * n, [0] * n
    capacity = {}
    for u, v, c in arcs:
        assert 0 <= u < n and 0 <= v < n and u != v and c >= 0
        assert (u, v) not in capacity, "No repeated ordered arcs"
        capacity[u, v] = c
        Dout[u] += c
        Din[v] += c

    insiders = sorted(range(n), key=lambda v: (-scores[v], v))[:k]
    inside = set(insiders)
    outsiders = [j for j in range(n) if j not in inside]
    margin_at_zero = topk_dual_budget_margin(
        scores, arcs, error_caps, 0, H, k)
    if margin_at_zero[0] <= 0:
        return 0, margin_at_zero[1], "already"

    error_coords = sorted(set(error_caps[j] for j in outsiders))
    q = len(error_coords)
    best = None

    # For a baseline pair, delta=s_i-s_j-min(H,a_i+a_j)>0.
    # It fails at F=delta iff delta <= Dout_i+Din_j.
    # Split at the exact saturation boundary a_j <= H-a_i.
    for unsaturated in (True, False):
        def y(j):
            return scores[j] + Din[j] + (
                error_caps[j] if unsaturated else 0)

        def x(j):
            return scores[j] + (error_caps[j] if unsaturated else 0)

        points = sorted(outsiders, key=y, reverse=True)
        queries = sorted(insiders, key=lambda i:
            scores[i] - (error_caps[i] if unsaturated else H) - Dout[i],
            reverse=True)
        fenwick = [None] * (q + 1)

        def insert(pos, entry):
            while pos <= q:
                if fenwick[pos] is None or entry > fenwick[pos]:
                    fenwick[pos] = entry
                pos += pos & -pos

        def prefix_max(pos):
            value = None
            while pos > 0:
                if fenwick[pos] is not None and (
                    value is None or fenwick[pos] > value
                ):
                    value = fenwick[pos]
                pos -= pos & -pos
            return value

        cursor = 0
        for i in queries:
            lower = scores[i] - (
                error_caps[i] if unsaturated else H) - Dout[i]
            while cursor < len(points) and y(points[cursor]) >= lower:
                j = points[cursor]
                rank = bisect_left(error_coords, error_caps[j])
                pos = rank + 1 if unsaturated else q - rank
                insert(pos, (x(j), j))
                cursor += 1

            split = bisect_right(error_coords, H - error_caps[i])
            selected = prefix_max(split if unsaturated else q - split)
            if selected is None:
                continue
            largest, j = selected
            delta = scores[i] - (
                error_caps[i] if unsaturated else H) - largest
            assert delta > 0
            if best is None or delta < best[0]:
                best = (delta, (i, j), "baseline")

    # Only a forward crossing arc i->j can improve on the cheap baseline.
    for (i, j), c in capacity.items():
        if i not in inside or j in inside:
            continue
        delta = scores[i] - scores[j] - min(
            H, error_caps[i] + error_caps[j])
        assert delta > 0
        if delta > Dout[i] + Din[j]:
            continue
        threshold = Fraction(delta, 2) if delta <= 2 * c else delta - c
        if best is None or threshold < best[0]:
            best = (threshold, (i, j), "arc")

    return best if best is not None else (None, None, "never")
