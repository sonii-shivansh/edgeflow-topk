---
title: "Exact Top-k Stability Certificates under Budgeted Edge Transfers"
subtitle: "An Unreviewed Technical Research Note"
author: "Shivansh Soni"
date: "12 November 2026"
lang: en
---

# Abstract

We consider strict membership stability of an initial top-k subset of vertices in a simple undirected graph. Independent signed transfers on edges obey individual nonnegative capacities and a shared absolute-flow budget. The worst-case pairwise score-gap perturbation is attained and admits a closed form. A baseline-and-boundary-edge reduction yields a deterministic O(m + n log n)-time and O(m + n)-space exact-arithmetic certificate. The source contains a complete mathematical proof. Independent numerical verification consists of 1,987 pairwise LP optimizations across 350 random graphs and a second exact-grid brute-force test suite with 350 random cases. A very-large-integer precision regression was discovered and corrected. The result is for this sharply defined model only. This AI-assisted note has not undergone external peer review; its originality and academic priority remain unconfirmed.

# Motivation and scope

A top-k ranking may be required to retain the same members when scores are redistributed among adjacent vertices. A global budget couples the possible score changes, so simply bounding each vertex independently does not provide a sharp pairwise certificate. We study an explicitly defined uncertainty set in which each undirected edge carries an independently signed amount, score is conserved globally, and a shared absolute-flow budget limits total transfer. The specific model matters: this is *not* a certification theorem for recomputed PageRank, edge-rewiring perturbations, or ordinary flow-routing problems.

This manuscript collects the exact theorem, proof, reproducible computational checks, prior-art notes, and limitations. The companion implementation and continuous-integration tests are at https://github.com/sonii-shivansh/edgeflow-topk .


# Mathematical statement and complete proof


**Status:** A self-contained mathematical proof, prepared with AI assistance. No priority or novelty claim is established; external peer review is pending.

## 1. Model and definitions

Let `G=(V,E)` be a finite **simple undirected** graph, n vertices and m edges. Each edge has a **finite nonnegative** capacity c_e, each vertex a finite initial score s_v, and B is a finite nonnegative total budget. Fix an arbitrary orientation of every edge. A signed flow f_e is feasible when

$$
|f_e|\leq c_e\quad(e\in E),\qquad
\sum_{e\in E}|f_e|\leq B.
$$

The updated vertex score is its initial score plus flows entering the vertex minus flows leaving it. Write this as

$$
s'_v=s_v+\sum_{e\ \mathrm{entering}\ v}f_e
-\sum_{e\ \mathrm{leaving}\ v}f_e.
$$

Fix 1 <= k < n. Let T be the k largest-score vertices initially, with deterministic tie-breaking if needed. The original top-k set T is **strictly robust** if every feasible flow satisfies s'_i > s'_j for every i in T, j outside T. A feasible boundary tie therefore violates strict robustness.

Set

$$
d_v=\sum_{e\ni v}c_e,\qquad
c_{ij}=\begin{cases}
c_e,&e=\{i,j\}\in E\\
0,&\{i,j\}\notin E.
\end{cases}
$$

The independent signed flows do **not** impose nonnegativity on updated scores or flow conservation at intermediate vertices; those extra constraints would define a different problem.

## 2. Exact pairwise adversarial bound

**Lemma 1.** For two different vertices i,j, the maximum increase in the outsider-minus-insider score difference is

$$
\Gamma_{ij}=2\min(c_{ij},B)+
\min(d_i+d_j-2c_{ij},(B-c_{ij})_+),
\qquad (x)_+=\max(0,x).
$$

**Proof.** For an oriented edge e=(u,v), its contribution to (s'_j-s'_i)-(s_j-s_i) equals a_e f_e, with

$$
a_e=\mathbf1_{\{v=j\}}-\mathbf1_{\{u=j\}}
-\mathbf1_{\{v=i\}}+\mathbf1_{\{u=i\}}.
$$

By direct substitution, the absolute value |a_e| is 2 if the edge directly joins i and j; it is 1 if the edge meets exactly one of i or j; otherwise it is zero. For a chosen nonnegative magnitude t_e, the sign of f_e can be chosen to make a_e f_e=|a_e|t_e. Consequently the exact maximization is

$$
\max\sum_{e}|a_e|t_e
\quad\mathrm{subject\ to}\quad
0\le t_e\le c_e,\quad \sum_e t_e\le B.
$$

Edges with coefficient 0 can be assigned zero flow. Since the graph is simple, at most one coefficient-2 edge exists; let its capacity be c=c_ij (take c=0 for a nonedge). All coefficient-1 edges together have capacity S=d_i+d_j-2c. This identity holds because each incident capacity is counted once in its respective weighted degree and the direct-edge capacity was counted twice.

Write x for flow magnitude on the coefficient-2 edge, and y for the sum of magnitudes on coefficient-1 edges. The remaining optimization is

$$
\max 2x+y,\quad
0\le x\le c,\quad
0\le y\le S,\quad x+y\le B.
$$

If y>0 while x<min(c,B), transferring a positive amount from y to x while remaining feasible increases the objective by that amount. If the remaining budget is unused and x<min(c,B), increasing x also improves the objective. Thus one optimum takes x*=min(c,B). After this choice, the largest feasible y is y*=min(S,max(0,B-c)). A total y* no larger than S can be distributed among coefficient-1 edges within their separate capacities, and all chosen magnitudes can be signed in the favorable direction. This constructs a feasible flow attaining 2x*+y*. Every feasible flow has objective no larger because a unit of budget yields at most 2, and allocating it to coefficient-2 edges first is optimal by the exchange argument. Therefore the displayed Gamma formula is exact. QED.

**Corollary 1.** T is strictly robust exactly when

$$
s_i-s_j>\Gamma_{ij}
\qquad \text{for every }i\in T,\ j\notin T.
$$

**Proof.** For each fixed pair, Lemma 1 gives the attained maximum increase in s'_j-s'_i. The strict inequality holds for *every* feasible flow exactly if the initial margin exceeds that maximum. Applying this to all crossing pairs proves the claim. Since the flow set is bounded and closed, equality corresponds to an attainable tie, not an unattainable supremum. QED.

## 3. Cheap baselines and the edge-only correction

Define L_ij=min(B,d_i+d_j).

**Lemma 2.** Gamma_ij >= L_ij for every distinct i,j, and equality holds when i,j are nonadjacent.

**Proof.** If c_ij=0, direct substitution gives Gamma_ij=min(d_i+d_j,B)=L_ij. Suppose c=c_ij>0 and S=d_i+d_j-2c>=0. When B<=c, Gamma=2B>=min(B,2c+S). When c<B<=c+S, Gamma=B+c>=min(B,2c+S). When B>c+S, Gamma=2c+S=d_i+d_j>=min(B,d_i+d_j). The three cases exhaust B>=0. QED.

**Lemma 3.** Strict robustness is equivalent to both:

1. s_i-s_j > L_ij for **all** i in T, j outside T; and
2. s_i-s_j > Gamma_ij for **every graph edge** joining T to its complement.

**Proof.** If T is robust, Corollary 1 supplies exact inequalities for every pair, which imply baseline inequalities by Lemma 2. Conversely consider any crossing pair. If nonadjacent, Lemma 2 says Gamma=L and condition 1 is exact. If adjacent, condition 2 checks the exact Gamma. Every pair falls into one of these cases. Corollary 1 finishes the proof. QED.

## 4. Exact algorithm

For each insider i, put

$$
M_i=\max_{j\notin T}
\left(s_j+\min(B,d_i+d_j)\right).
$$

The complete baseline test for i is exactly s_i>M_i.

Sort outsiders j_0,...,j_(q-1) by nondecreasing capacity degree d_j, q=n-k. Define prefix maxima P_r=max_{0<=t<=r}(s_(j_t)+d_(j_t)) and suffix maxima Q_r=max_{r<=t<q}s_(j_t). Find by binary search the first index r whose degree is strictly greater than B-d_i. (r=0 and r=q are allowed.)

For t<r, d_(j_t)<=B-d_i, so min(B,d_i+d_(j_t))=d_i+d_(j_t). For t>=r, the minimum is B. Thus

$$
M_i=\max(d_i+P_{r-1},\ B+Q_r),
$$

omitting a term if its corresponding range is empty. The partition contains every outsider and each maximum is computed correctly; hence the formula is exact.

Compute each M_i and reject if s_i<=M_i. Otherwise scan each graph edge once; if it crosses the top-k boundary, evaluate the Gamma formula and reject if s_i-s_j<=Gamma_ij. If no test rejects, accept.

**Correctness:** The binary-search/prefix/suffix procedure exactly evaluates the baseline condition. The crossing-edge scan exactly checks the second condition of Lemma 3. Lemma 3 therefore proves that the algorithm returns strict robustness if and only if T is strictly robust.

**Complexity:** Weighted degrees take O(m+n); finding T and sorting outsiders take O(n log n); building prefix/suffix maxima O(n); at most n binary searches O(n log n); and one edge scan O(m). Total **O(m+n log n)** time and **O(m+n)** storage, counting arithmetic/comparison operations on real numbers as constant time.

## 5. Scope

The result concerns the exact real-valued model. The companion Python implementation uses floating-point arithmetic and is not an exact-arithmetic proof assistant. It excludes multigraphs, directed-only flows, node-balance constraints, and scores recomputed from the modified graph. See [limitations](../LIMITATIONS.md).

Read [experimental evidence](../experiments/RESULTS.md) and [prior work](PRIOR_WORK.md). Passing tests and a complete proof cannot establish novelty.


# Appendix A: Computational verification and reproducibility


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


# Appendix B: Related literature and novelty caveat


**Assessment date: 2026-11-11.** These references were located and bibliographic information checked. They do not constitute a complete academic literature search.

1. **Dimitris Bertsimas and Melvyn Sim (2004)**, "The Price of Robustness," *Operations Research* 52(1):35–53. DOI: https://doi.org/10.1287/opre.1030.0065 . This is foundational work on robustness with a budget of uncertainty. The edge-pair optimization here has the flavor of a known budgeted linear allocation; we do not claim that greedy budget allocation itself is new.
2. **Kyriakos Mouratidis and Bo Tang (2018)**, "Exact Processing of Uncertain Top-k Queries in Multi-criteria Settings," *Proceedings of the VLDB Endowment* 11(8):866–879. DOI: https://doi.org/10.14778/3204028.3204031 . This studies exact top-k query processing under uncertain preference weights, different from independent signed graph-edge transfers.
3. **Ruiting Liang, Jake A. Soloff, Rina Foygel Barber, and Rebecca Willett (2025)**, "Assumption-free stability for ranking problems," arXiv:2506.02257. https://arxiv.org/abs/2506.02257 . This develops stability via ranking operators, with a different model and guarantee.

## Research status

A self-contained mathematical proof and reproducible small-case LP checks are supplied in this repository, but **we have not established priority** for either the pairwise formula or the near-linear reduction. Search-engine access, mathematical terminology, and journal coverage limit any novelty conclusion. Before a paper claims novelty, independently search MathSciNet/zbMATH, graph ranking and robust optimization literature, cited/citing papers, and the exact or equivalent algorithmic reduction.

Please open an issue if you find equivalent prior work, a stronger predecessor, or a counterexample.



# Quantitative extension: exact worst-case separation margin

The original theorem provides a strict yes/no stability test. A stronger quantity is the sharp guaranteed separation of the original top-k set T from all outsiders under any admissible signed transfer:

$
\rho(B)=\min_{f\ {\rm feasible}}\ \min_{i\in T,\ j\notin T}\ (s'_i(f)-s'_j(f)).
$

**Theorem (quantitative certificate).** With the pairwise bound Gamma_ij and capacity degrees as above, define the cheap baseline L_ij=min(B,d_i+d_j), and let delta(T) be all graph edges joining one original insider with one outsider. Then

$
\begin{aligned}
\rho(B)
&=\min_{i\in T,\ j\notin T}(s_i-s_j-\Gamma_{ij})\\
&=\min\left\{
\min_{i\in T,\ j\notin T}(s_i-s_j-L_{ij}),\
\min_{\{i,j\}\in\delta(T),\ i\in T}(s_i-s_j-\Gamma_{ij})
\right\}.
\end{aligned}
$

The second inner minimum is defined as positive infinity if there are no crossing edges. The exact value and an attaining pair can be computed using the same degree sorting, prefix/suffix maxima and crossing-edge scan in O(m+n log n) time and O(m+n) space.

**Proof.** For a fixed insider-outsider pair, the first lemma above gives an *attained* smallest possible separation equal to s_i-s_j-Gamma_ij. Taking the minimum over the finite set of crossing pairs and the feasible flows commutes: both sides equal the infimum over their Cartesian product, and here compactness guarantees attainment. This gives the first equality. On a nonadjacent pair, Gamma_ij=L_ij, so the baseline is exact. For an adjacent crossing pair, Gamma_ij>=L_ij, so the exact edge expression is no greater than its baseline expression. Consequently the minimum of *all* baseline expressions together with *all* exact crossing-edge expressions equals the minimum of exact expressions over all crossing pairs; every nonedge is represented exactly by its baseline, and every adjacent pair exactly by the crossing-edge correction. This is the second equality. Computing the baseline minimum uses the same outside-degree sorting and prefix/suffix maxima described in the preceding theorem; scanning the crossing edges completes the procedure in the stated complexity. The pair attaining the computed minimum is exact: if a baseline-selected adjacent pair had a strictly smaller exact value, the crossing-edge scan would have lowered the minimum. Choosing signed edge flows to attain its pairwise support function produces the advertised witness. QED.

Thus rho(B)>0 is equivalent to strict robustness; rho(B)=0 means a boundary tie is feasible but no crossing reversal; and rho(B)<0 means a strict reversal is feasible. This certificate is **not** a uniqueness or priority claim.

## Extension verification

A second test suite checked the quantitative margin against (i) direct enumeration of every insider-outsider pair on 2,600 randomly generated integer-score graphs, and (ii) direct enumeration of all feasible signed edge-transfer vectors on a half-unit grid for 420 independently generated small rational cases. All 3,020 checks passed in the local execution and are included in the committed GitHub Actions test suite. A regression exposed precision loss caused by initializing witness-flow entries as floating-point zero; that has been corrected to integer zero. The general theorem is for exact real arithmetic and does not give a floating-point safety guarantee.

# Novelty and publication status update — 12 November 2026

The related-work audit found strong pre-existing literature on **budgeted robust optimization**, including Bertsimas and Sim (2004) and later fractional-knapsack formulations. Greedy allocation of uncertainty budget is **not an original general method**. Robust top-k processing, stable ranking operators and graph-ranking perturbations also predate this note. The exact baseline-plus-boundary-edge reduction for the stated signed-transfer model was not located in the inspected sources, but **its novelty remains unconfirmed**; a more general published optimization or dominance-query theorem may imply it. See https://github.com/sonii-shivansh/edgeflow-topk/blob/main/research/NOVELTY_AUDIT_2026-11-12.md and https://github.com/sonii-shivansh/edgeflow-topk/blob/main/research/MARGIN_THEOREM.md .

This paper is a **publicly archived unreviewed technical note**, not a journal article, arXiv submission, external referee report, DOI assignment, or invention registration. It was prepared using AI assistance and requires independent human assessment before any assertion of substantial academic novelty.

# Acknowledgment of assistance

The derivation, implementation, testing, and manuscript preparation received AI assistance. The human repository owner is responsible for verifying all scientific claims. GitHub publication and automated tests do not constitute peer review, evidence of novelty, or acceptance by a scholarly venue.
