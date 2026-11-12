# Experiments and reproducibility

**Recorded run:** 2026-11-11. **Program:** [edge_transfer_topk.py](../edge_transfer_topk.py). **Random seed:** 20261111. Independent LP solver: SciPy/HiGHS.

## Reproduce

    python -m pip install -r requirements-test.txt
    python edge_transfer_topk.py

The script returns a nonzero process exit on an assertion failure.

## Observed local console output

    DETERMINISTIC PAIR CASES (formula, LP, constructive witness):
      empty graph                :  0.00,  0.00,  0.00
      direct edge, small budget  :  2.00,  2.00,  2.00
      direct edge, saturated     :  6.00,  6.00,  6.00
      two-edge path              :  2.50,  2.50,  2.50
      triangle                   :  5.00,  5.00,  5.00
      disconnected               :  4.00,  4.00,  4.00
      zero capacities            :  0.00, -0.00,  0.00
      reverse orientation        :  5.00,  5.00,  5.00

    RANDOMIZED: seed=20261111, graphs=350, pair-LPs=1987
      exact algorithm vs independently solved LPs: 350/350 agreements
      certified strict robust: 122; not robust: 228
      maximum pair |formula - LP|: 0
      failures: 0

    EXPLICIT RANK CASES:
      rank boundary tie at B=0                    : robust=False, reason=baseline, witness_pair=(0, 1)
      direct-edge correction detects failure      : robust=False, reason=crossing-edge, witness_pair=(0, 1)
      robust despite possible redistribution      : robust=True, reason=certified, witness_pair=None
      nonedge baseline detects failure            : robust=False, reason=baseline, witness_pair=(0, 1)

## Independent checks

- Eight deterministic pairwise cases include an empty graph, direct-edge saturation and partial allocation, a two-edge path, a triangle, disconnected components, zero capacities and orientation reversal.
- 350 random simple graphs were generated with 2–8 vertices, edge inclusion probability 0.43, capacities drawn from {0,...,5}, scores from {-4,...,15}, budgets in increments of 0.5 from 0 to 12, and random k from 1 to n-1.
- The algorithm's decision was compared against exhaustively optimizing all top-k-versus-outsider pairs with a separate linear program, for 1,987 solved LPs.
- The closed-form pairwise bound was compared to each optimized LP value.
- Explicit signed-flow witnesses were constructed and checked against capacities and budget.

Maximum observed discrepancy 0 means **in this finite test run**, not a general numerical-error bound. The implementation uses Python floating-point arithmetic; the theorem concerns exact real arithmetic. No large-scale wall-clock benchmark, uncertainty quantification, or independent peer review has been conducted.

## New independent exact enumeration (2026-11-12)

Command: `python -m unittest discover -s tests -v`. Observed output:

```
test_exhaustive_half_unit_flows ... ok
test_exhaustive_integer_flows ... ok
test_very_large_integer_scores ... ok
----------------------------------------------------------------------
Ran 3 tests in 0.037s
OK
```

- 260 deterministic-seed random integer instances and 90 half-integer Fraction instances. Each comparison enumerates all legal signed flows on the corresponding integer or half-integer grid. This is an independent **decision oracle**; it does not invoke the pairwise formula or the LP solver.
- Large-integer precision regression: scores `[10**100 + 1, 10**100]`, no edges, B=0 must be robust. The original implementation (weighted degrees initialized to floats) incorrectly returned nonrobust; initialization was changed to integer zero and the issue is now covered by a passing regression test.
- The integral/half-integer grid is exhaustive on the selected discretized examples and includes feasible extremal flows under these capacities and budgets. This does not exhaust the full space of real-valued graph inputs.

## Synthetic scaling illustration (2026-11-12)

Command: `python experiments/benchmark.py`, local CPython 3.13.5 container, one timed run per case, B=1000, n/2 high-scoring insiders. Observed:

| Vertices n | Edges m | Decision time (s) | Certified robust |
|---:|---:|---:|---|
| 1,000 | 4,000 | 0.003323 | yes |
| 10,000 | 40,000 | 0.037642 | yes |
| 50,000 | 200,000 | 0.215424 | yes |

These are environment-dependent, single-run demonstration timings, **not** statistically sound performance benchmarks or a new complexity proof.
