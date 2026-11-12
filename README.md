# EdgeFlow Top-k

**Exact near-linear certification of strict top-k stability under budgeted graph-edge transfers**

> **Research status (11 November 2026):** Self-contained mathematical proof and reproducible tests available. **Novelty has not been established.** This is an AI-assisted, unreviewed research note, not a peer-reviewed paper and not a claim of a first discovery.

## The problem

Given a **simple undirected** graph with real initial vertex scores, nonnegative edge capacities, and one global transfer budget, the adversary can choose signed flows along edges. Every edge flow has magnitude at most its capacity, while the sum of all absolute flows is at most the global budget. A flow increases the score at one endpoint and decreases it at the other.

**Question:** Are the original highest-scoring k vertices strictly above all outsiders under **every** feasible flow? A possible tie at the top-k boundary counts as failure.

## Result

Let `d_v` be the sum of capacities on edges incident to vertex v, and `c_ij` the capacity of the edge joining i and j (or zero if missing). The exact maximum increase in the score difference between outsider j and insider i is

$$
\Gamma_{ij} = 2\min(c_{ij},B) +
\min(d_i+d_j-2c_{ij},\max(0,B-c_{ij})).
$$

The original top-k set T is strictly robust if and only if

$$
s_i-s_j>\Gamma_{ij}
\quad \text{for all }i\in T,\ j\notin T.
$$

A baseline inequality checked with prefix/suffix maxima, plus exact checks of all boundary-crossing edges, decides this in **O(m + n log n) time** and **O(m+n) space** under the stated model.

Read [the complete proof](research/PROOF.md) and [all limitations](LIMITATIONS.md).

## Quick start

Core algorithm: [edge_transfer_topk.py](edge_transfer_topk.py). It has no third-party runtime dependencies.

    from edge_transfer_topk import certifies_strict_topk

    scores = [10, 7, 0]
    edges = [(0, 1, 2)]  # (u, v, capacity)
    print(certifies_strict_topk(scores, edges, B=2, k=1))
    # (False, (0, 1), 'crossing-edge')

The edge orientation is arbitrary; negative signed flows are allowed. The routine returns (strictly_robust, violating_pair_or_None, reason). A reported pair can be used with `constructive_witness` to build a feasible flow demonstrating loss of strict separation.

## Reproduce the experiments

    python -m pip install -r requirements-test.txt
    python edge_transfer_topk.py

SciPy is used for independent pairwise linear-programming verification; not for the fast decision algorithm.

**Observed local results:** 350/350 agreement on random graph decisions, 1,987 independently solved pairwise LPs, maximum observed pairwise formula/LP discrepancy 0, and zero test failures. See [recorded experiments](experiments/RESULTS.md).

## Repository materials

- [Implementation and test program](edge_transfer_topk.py)
- [Formal theorem and proof](research/PROOF.md)
- [Recorded experiments and reproducibility](experiments/RESULTS.md)
- [Prior work and unresolved originality](research/PRIOR_WORK.md)
- [Limitations](LIMITATIONS.md)
- [How to contribute and report counterexamples](CONTRIBUTING.md)
- [MIT license](LICENSE), already selected by the repository owner

## Scientific integrity and citation

This note was prepared with AI assistance; **independent human review is required**. Mathematical correctness under the assumptions is not the same as academic novelty. No journal peer review, arXiv identifier, or DOI is claimed.

For now, cite the URL and exact commit hash: https://github.com/sonii-shivansh/edgeflow-topk . A Zenodo DOI may be obtained separately after publishing an intentional release. Do not claim this as a world-first result without a thorough prior-art review.

## Independent exact-enumeration audit (12 November 2026)

A second test suite checks the fast decision directly against exhaustive feasible signed-flow enumeration on **260 integer cases** and **90 exact half-integer cases**, independently of the pairwise formula and LP solver. A large-integer regression test exposed and prompted a correction to floating-point degree initialization. With integer scores, capacities, and budget, the core algorithm now performs **integer arithmetic without avoidable conversion to floats**. Read [tests/test_exact_enumeration.py](tests/test_exact_enumeration.py) and [experiments/RESULTS.md](experiments/RESULTS.md). Floating-point inputs still need special care at exact ties.

An illustrative, single-run synthetic scalability check (not a peer-reviewed benchmark) is in [experiments/benchmark.py](experiments/benchmark.py).
