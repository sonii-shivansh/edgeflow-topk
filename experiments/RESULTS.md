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
