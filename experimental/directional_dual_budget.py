"""Exact top-k margin with directed transfers and measurement-error budgets.

Research prototype for a mathematically specified uncertainty model.
Core algorithm: O(m+n log n) comparison/arithmetic operations, O(m+n) space.
Novelty unconfirmed; not peer reviewed.
"""
from bisect import bisect_left, bisect_right


def topk_dual_budget_margin(scores, arcs, error_caps, flow_budget, error_budget, k):
    """Return (worst_margin, (insider, outsider), source).

    Arc (u,v,c) carries a nonnegative transfer from u to v, up to capacity c.
    Sum of transfers <= flow_budget. Each node has signed measurement error
    bounded in magnitude by error_caps[v], with L1 sum <= error_budget.
    Input is a simple directed graph (no repeated ordered arc).
    Use Python int/Fraction inputs for exact numerical comparisons.
    """
    n = len(scores)
    assert len(error_caps) == n and 1 <= k < n
    assert flow_budget >= 0 and error_budget >= 0
    out_capacity = [0] * n
    in_capacity = [0] * n
    arc_capacity = {}
    for u, v, c in arcs:
        assert 0 <= u < n and 0 <= v < n and u != v and c >= 0
        assert (u, v) not in arc_capacity, "No duplicate directed arcs"
        arc_capacity[u, v] = c
        out_capacity[u] += c
        in_capacity[v] += c
    assert all(a >= 0 for a in error_caps)

    insiders = sorted(range(n), key=lambda v: (-scores[v], v))[:k]
    inside = set(insiders)
    outsiders = [v for v in range(n) if v not in inside]
    error_coords = sorted(set(error_caps[j] for j in outsiders))
    q = len(error_coords)
    minimum = None

    # Four offline 2D orthogonal dominance-max sweeps.
    for low_flow in (True, False):
        ordered_outsiders = sorted(
            outsiders, key=lambda j: in_capacity[j],
            reverse=not low_flow)
        ordered_insiders = sorted(
            insiders, key=lambda i: flow_budget - out_capacity[i],
            reverse=not low_flow)
        for low_error in (True, False):
            fenwick = [None] * (q + 1)

            def insert(position, item):
                while position <= q:
                    old = fenwick[position]
                    if old is None or item > old:
                        fenwick[position] = item
                    position += position & -position

            def query(position):
                ans = None
                while position > 0:
                    item = fenwick[position]
                    if item is not None and (ans is None or item > ans):
                        ans = item
                    position -= position & -position
                return ans

            cursor = 0
            for i in ordered_insiders:
                y_threshold = flow_budget - out_capacity[i]
                a_threshold = error_budget - error_caps[i]
                while cursor < len(ordered_outsiders):
                    j = ordered_outsiders[cursor]
                    condition = (
                        in_capacity[j] <= y_threshold if low_flow
                        else in_capacity[j] > y_threshold)
                    if not condition:
                        break
                    location = bisect_left(error_coords, error_caps[j])
                    position = location + 1 if low_error else q - location
                    weight = (
                        scores[j]
                        + (in_capacity[j] if low_flow else 0)
                        + (error_caps[j] if low_error else 0))
                    insert(position, (weight, j))
                    cursor += 1

                count = bisect_right(error_coords, a_threshold)
                max_index = count if low_error else q - count
                result = query(max_index)
                if result is None:
                    continue
                value, j = result
                offset = (
                    (out_capacity[i] if low_flow else flow_budget)
                    + (error_caps[i] if low_error else error_budget))
                margin = scores[i] - value - offset
                if minimum is None or margin < minimum[0]:
                    minimum = (margin, (i, j), "baseline")

    assert minimum is not None

    # Only forward arcs from insiders to outsiders get coefficient 2.
    for (i, j), c in arc_capacity.items():
        if i not in inside or j in inside:
            continue
        spare = out_capacity[i] + in_capacity[j] - 2 * c
        flow_loss = 2 * min(c, flow_budget) + min(
            spare, max(0, flow_budget - c))
        error_loss = min(error_budget, error_caps[i] + error_caps[j])
        exact = scores[i] - scores[j] - flow_loss - error_loss
        if exact < minimum[0]:
            minimum = (exact, (i, j), "arc")
    return minimum


def pairwise_dual_bound(i, j, arcs, error_caps, flow_budget, error_budget):
    """Exact worst-case increase in outsider-minus-insider score gap."""
    out_i = sum(c for u, v, c in arcs if u == i)
    in_j = sum(c for u, v, c in arcs if v == j)
    direct = sum(c for u, v, c in arcs if u == i and v == j)
    return (
        2 * min(direct, flow_budget)
        + min(out_i + in_j - 2 * direct,
              max(0, flow_budget - direct))
        + min(error_budget, error_caps[i] + error_caps[j]))


def witness_for_pair(n, i, j, arcs, error_caps, flow_budget, error_budget):
    """Construct directed flows and signed errors attaining the pair bound."""
    flow = [0] * len(arcs)
    candidates = []
    for index, (u, v, capacity) in enumerate(arcs):
        coeff = (int(u == i) + int(v == j)
                 - int(v == i) - int(u == j))
        if coeff > 0:
            candidates.append((coeff, index, capacity))
    remaining = flow_budget
    for coeff, index, capacity in sorted(candidates, reverse=True):
        t = min(capacity, remaining)
        flow[index] = t
        remaining -= t
    errors = [0] * n
    available = error_budget
    spend_i = min(available, error_caps[i])
    errors[i] = -spend_i
    available -= spend_i
    spend_j = min(available, error_caps[j])
    errors[j] = spend_j
    return flow, errors


def adjusted_scores(scores, arcs, flow, error):
    updated = [s + e for s, e in zip(scores, error)]
    for (u, v, _), f in zip(arcs, flow):
        updated[u] -= f
        updated[v] += f
    return updated
