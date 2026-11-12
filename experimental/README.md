# Experimental research: directional flow + measurement-error budgets

**Status: Proposed mathematical extension — self-contained proof and reproducible tests; not independently peer reviewed and not established as historically novel.**

The exact top-k separation margin under one-way directed arc transfers and independently budgeted signed node measurement errors is computed in O(m+n log n) arithmetic/comparison time with O(m+n) space.

Full theorem and proof: [research/DIRECTIONAL_DUAL_BUDGET.md](../research/DIRECTIONAL_DUAL_BUDGET.md).

## One example

```python
from experimental.directional_dual_budget import topk_dual_budget_margin, witness_for_pair

scores = [10, 7]
arcs = [(0, 1, 2)]  # fixed forward direction, only nonnegative flow
error_caps = [2, 2]
B, H, k = 2, 3, 1

margin, pair, source = topk_dual_budget_margin(
    scores, arcs, error_caps, B, H, k
)
assert margin == -4
flow, errors = witness_for_pair(
    len(scores), *pair, arcs, error_caps, B, H
)
print(margin, pair, source, flow, errors)
```

The negative margin means there exists a feasible joint flow/error assignment under which the outsider strictly overtakes the original insider. Reversing the arc direction can change the result.

## Verification

Run from repository root:

```bash
python -m pip install -r requirements-test.txt
python -m unittest tests.test_directional_dual_budget -v
python -m unittest discover -s tests -v
python experimental/benchmark_directional_dual_budget.py
```

The local validation on 12 November 2026 consisted of 8 deterministic cases, 1,000 all-pairs random graph checks, 115 small exact-rational direct-flow/error enumerations, and 390 independent SciPy/HiGHS pairwise LP optimizations. All passed. The verification script runs the same fixed-seed cases in CI. The synthetic benchmark has three sample sizes and no representative external dataset; do not infer production performance from its single-run timing.

## Limitation and priority

Transfers are **not** path-constrained network flows. Their only constraints are one-way arc capacities and a global transfer sum. Measurement errors have independent per-node bounds and their own global L1 budget. Updated scores may be negative. The proof does not cover recomputed PageRank or centrality scores.

The pairwise optimization draws on established budgeted optimization. The 2D orthogonal maximum sweep is a standard computational-geometric technique. The specialization to these simultaneous disturbances and an exact sparse top-k certificate has not been identified in the targeted literature search, but **absence of a match is not evidence of a first discovery**. This is a research candidate, not a claim of an invention or journal acceptance.
