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


## Exact minimum destabilizing transfer budget (integer inputs)

The new [critical-flow-budget implementation](critical_flow_budget.py) computes the **first transfer budget F at which any feasible directed flow and fixed-budget signed measurement error can destroy strict original top-k separation**. It returns a finite budget, an insider/outsider pair and a reason; finite F is an integer or half-integer, or None when no amount of transfer can cause failure.

**Theorem:** In the directed dual-budget uncertainty model with integer scores, arc capacities, error caps and fixed measurement-error budget H, this first-failure budget can be computed in **O(m+n log n) arithmetic/comparison time** and O(m+n) space. The proof uses two offline 2D dominance maxima and an exact forward-arc correction; it does **not** require repeated calls to a fixed-budget verifier.

- [Full mathematical proof, model assumptions and novelty limits](../research/CRITICAL_FLOW_BUDGET.md)
- [Code](critical_flow_budget.py)
- [Independent tests](../tests/test_critical_flow_budget.py)
- [Synthetic scaling reproducer](benchmark_critical_budget.py)

Reproduce tests from repository root:

    python -m pip install -r requirements-test.txt
    python -m unittest discover -s tests -v

One local audit checked 2,000 randomized instances against an all-pairs analytical threshold oracle, 120 tiny instances against exhaustive half-integer directed-flow and signed-error enumeration, and deterministic boundary and nonconvexity cases. A mistaken hand-written test expectation was corrected after the first test run; no mathematical algorithm correction was needed.

**Scientific status: conditional mathematical proof; numerical tests passed; historical novelty UNCONFIRMED; not independently peer reviewed.** Robustness-radius searches and orthogonal range queries are established techniques. This is a candidate specialized reduction, not an established original discovery.


## Exact critical measurement-error budget (complementary theorem)

For fixed *directed flow budget* F, the new function **critical_error_budget(scores, arcs, error_caps, F, k)** returns the minimum *independent measurement-error budget* H at which a top-k boundary tie or reversal first becomes feasible. Returns (None, None, "never") if it is impossible even with all per-node error caps fully used.

The proof uses two offline 2D dominance-max sweeps and checks only exceptional forward crossing arcs, giving **O(m+n log n)** arithmetic/comparison time and **O(m+n)** storage. Integer and Fraction inputs are treated exactly. For integer scores/caps/F, the finite critical H is an integer; for rational data it need not be integer or half-integer.

- [Full mathematical theorem, proof and related work](../research/CRITICAL_ERROR_BUDGET.md)
- [Core code](critical_error_budget.py)
- [Independent exact-grid, LP and randomized tests](../tests/test_critical_error_budget.py)
- [Synthetic scaling illustration](benchmark_critical_error.py)
- [Companion critical flow-budget theorem (fixed H, minimum F)](../research/CRITICAL_FLOW_BUDGET.md)

Example:

```python
from experimental.critical_error_budget import critical_error_budget

scores = [10, 7]
arcs = [(0, 1, 2)]
error_caps = [2, 2]

assert critical_error_budget(scores, arcs, error_caps, flow_budget=0, k=1)[0] == 3
assert critical_error_budget(scores, arcs, error_caps, flow_budget=2, k=1)[0] == 0
```

Reproduce with **python -m pip install -r requirements-test.txt** and **python -m unittest discover -s tests -v**. Local tests passed 2,000 direct all-pairs comparisons, 150 independent exact-rational perturbation enumerations, 110 independently solved SciPy LPs and nine deterministic edge cases.

This is **AI-assisted experimental research, NOT independently peer reviewed, and novelty is UNCONFIRMED**. A pair of exact horizontal/vertical budget threshold oracles does not automatically produce the complete Pareto frontier; the stability region is not necessarily convex. See the manuscript for explicit assumptions.
