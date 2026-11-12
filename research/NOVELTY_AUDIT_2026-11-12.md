# Prior-art and originality audit — 12 November 2026

**Status:** An AI-assisted research-literature audit, **not** an independent referee report, systematic-review guarantee, priority determination, or peer-reviewed acceptance. Publication priority remains **UNCONFIRMED**.

## 1. Claim under investigation

The repository's precise model is a finite **simple undirected graph** with a fixed vector of real vertex scores. Signed edge transfers have separate nonnegative capacity limits and one global absolute-flow budget. Vertex scores gain or lose the incident signed transfers. The central claims are:

1. Sharp pairwise support value
   \[
   \Gamma_{ij}=2\min(c_{ij},B)+\min(d_i+d_j-2c_{ij},(B-c_{ij})_+).
   \]
2. Exact top-k strict membership certification in O(m+n log n) time through a degree-sorted outsider baseline and checking every crossing edge.
3. The additional sharp *global separation margin* in O(m+n log n), with a constructive adverse-flow witness; see [MARGIN_THEOREM.md](MARGIN_THEOREM.md).

These should be compared against more general results, not merely against exact title matches. A generic robust inequality support function and a known offline dominance-query algorithm could subsume the specialized result without using the words 'graph edge transfers'.

## 2. Primary source examination

### A. Budgeted robust optimization: strong conceptual overlap

**D. Bertsimas and M. Sim**, *The Price of Robustness*, Operations Research 52(1):35–53 (2004). DOI: https://doi.org/10.1287/opre.1030.0065 . The inspected paper studies protection against uncertain linear coefficients with a budget controlling how many coefficients can deviate. It derives a tractable robust counterpart using an inner linear optimization. This is foundational *prior art* for the budgeted adversarial/greedy mechanism; **do not claim the general greedy budget optimization as new**. Our budget is an absolute flow-volume budget on a graph rather than exactly their cardinality-normalized coefficient budget. Therefore the models are related but not identical.

**C. Büsing, T. Gersing, and A. M. C. A. Koster**, *Recycling valid inequalities for robust combinatorial optimization with budgeted uncertainty*, Mathematical Programming (published online 29 August 2024; volume 210, 2025). https://doi.org/10.1007/s10107-024-02135-7 . The checked article explicitly describes greedy optimization of a fractional-knapsack subproblem within budgeted uncertainty. This is particularly relevant to the derivation of the pairwise support function: the greediness itself is not novel.

### B. Top-k processing under uncertainty: nearby problem, different perturbations

**K. Mouratidis and B. Tang**, *Exact Processing of Uncertain Top-k Queries in Multi-criteria Settings*, PVLDB 11(8):866–879 (2018). DOI: https://doi.org/10.14778/3204028.3204031 . The paper addresses top-k membership under uncertain scoring-preference weights and scalable processing. It establishes that exact uncertain top-k processing existed long before this repository; its stated uncertainty does not match the fixed-score signed edge transfer model.

**R. Liang, J. A. Soloff, R. F. Barber, and R. Willett**, *Assumption-free stability for ranking problems*, arXiv:2506.02257 (2 June 2025). https://arxiv.org/abs/2506.02257 . They construct inflated ranking operators to improve stability under score estimation fluctuations. That differs from the present exact fixed-top-k robust feasibility problem.

**Y. Yang, A. Chen, L. Orecchia, and C. Ma**, *Top-K ranking with a monotone adversary*, COLT 2024, PMLR 247:5123–5162. https://proceedings.mlr.press/v247/yang24b.html . Here the adversary adds comparison-graph edges; the studied estimator, stochastic assumptions, and guarantees differ from independent score transfers.

### C. Robust graph ranking: same general application, different mechanism

**A. Timonina-Farkas and R. W. Seifert**, *Information Retrieval Under Network Uncertainty: Robust Internet Ranking*, Operations Research (2022). DOI: https://doi.org/10.1287/opre.2022.2298 . Their robust PageRank model accounts for uncertain graph structure and growing networks, with matrix-norm uncertainty and an optimization formulation. This is meaningful graph-ranking prior work, but not an identified instance of the present score-transfer model.

**I. Qin, P. Wong, and L. Oettershagen**, *Fair Top-k Katz Centrality via Graph Design*, arXiv:2609.03899 (3 September 2026). https://arxiv.org/abs/2609.03899 . They analyze edge *additions* and the resulting changes in Katz centrality, including boundary-driven top-k changes; they do not use fixed external scores with signed edge-flow perturbations.

**G. Ghoshal and A.-L. Barabási**, *Ranking stability and super-stable nodes in complex networks*, Nature Communications 2:394 (2011). https://www.nature.com/articles/ncomms1396 . This studies PageRank sensitivity to graph-topology perturbations, not our signed transfer budget.

## 3. Reproducible search queries / coverage

On 12 November 2026, the following query families were searched using general scholarly web indexing and direct arXiv/publisher pages:

- "graph node ranking robust top-k stability budgeted edge flow perturbations algorithm"
- "top k stability certificate graph edge transfer capacity l1 budget exact"
- "ranking under flow perturbations edge budget robust top k certificate"
- "robust top-k selection support function budgeted uncertainty graph incidence matrix"
- "robust top-k budgeted uncertainty ranking"
- "graph incidence ranking robust L1"
- "rank stability edge flow graph top k"
- "ranking stability budgeted perturbations exact graph"
- "robust ranking linear uncertainty edge graph"
- "top-k ranking with a monotone adversary"
- Targeted arXiv searches for graph top-k perturbation, robustness, ranking, and budget.
- Attempts to locate equivalent results via MathSciNet, Google Scholar, and OEIS indexing.

**Coverage limitations:** A complete full-text MathSciNet review was not available; direct Google Scholar coverage was incomplete. OEIS is a sequence resource and not an appropriate exhaustive algorithm-priority database. Search engines do not index every proof, thesis, preprint, or unpublished algorithm. No statement of 'first known result' is warranted.

## 4. Claim-by-claim novelty assessment

| Claim | Assessment | Evidence or concern |
| --- | --- | --- |
| Greedy allocation of budget to largest coefficients | **KNOWN general technique** | Bertsimas–Sim; fractional knapsack |
| Pairwise magnitude 2 on direct edge, 1 on other incident edges | **Easy specialization; priority unconfirmed** | Direct incidence-matrix coefficient count |
| Closed-form pairwise bound | **Mathematically derived; novelty unconfirmed** | Follows from established fractional-knapsack structure with a two-level coefficient set |
| Baseline plus crossing-edge correction | **Specific algorithmic candidate; novelty unconfirmed** | Exact sparse-graph structural reduction, but could follow from known support-function/dominance routines |
| O(m+n log n) robust membership and margin | **Specific complexity candidate; novelty unconfirmed** | Direct proof in this repository; no exact published predecessor located in this targeted search |
| Applications to PageRank under edge edits | **NOT CLAIMED** | Scores are fixed externally and are not recomputed |

## 5. Verdict and publication language

**Verdict: ORIGINALITY UNCONFIRMED; mathematical contribution plausible only as a narrow specialized algorithmic result.**

The most responsible contribution statement is:

> We give a self-contained exact algorithm for strict top-k membership certification and a quantitative worst-case separation margin in a particular signed edge-transfer model, based on a sharp pairwise support function and a sparse baseline-plus-edge correction. We do not claim that the general budgeted optimization method or the specific algorithm was historically first.

The paper should not advertise a "new invention", "world-first", "novel discovery", "peer-reviewed theorem", or accepted publication. A journal referee could regard the main bound as a straightforward specialization of a classical robust-optimization primitive. That would not falsify the proof, but could undermine publication-level novelty.

## 6. Remaining independent-review tasks

- Obtain an external algorithmist's critique of the reduction and an exact/stronger predecessor search.
- Search full-text ACM/DBLP/SIAM/MathSciNet/zbMATH and forward/backward citations.
- Compare worst-case complexity with generic robust ranking and offline orthogonal dominance reporting.
- Request empirical problem instances that genuinely satisfy the signed-transfer model.
- Keep [Issue #1](https://github.com/sonii-shivansh/edgeflow-topk/issues/1) open; do not represent this internally authored audit as an independent review.

**No exact predecessor was identified in the inspected sources, but this cannot establish novelty.** The linked sources above were directly located and their model descriptions checked.
