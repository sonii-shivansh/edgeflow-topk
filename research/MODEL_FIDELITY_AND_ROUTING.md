# Model-fidelity audit: independent arc transfers versus routed flows

**Date:** 12 November 2026. **Status:** Model-boundary analysis, not a claim of novelty or external peer review.

## 1. Why this matters

The exact EdgeFlow directed dual-budget algorithm assumes independently selectable **nonnegative arc transfers**, subject to arc capacities and a single sum-of-arc-flows budget. Each transfer updates only the scores of its two endpoints. There is **no requirement** that flow entering an intermediate vertex must also leave it. This assumption is mathematically essential. It makes the uncertainty set a box intersected with one L1 budget, and gives the pairwise support function its simple fractional-knapsack structure.

Real-world physical routing systems may impose additional conservation constraints at transit nodes. Adding them can change the worst-case separation, invalidating the use of the independent-arc formula as an *exact* certificate for the more constrained model.

## 2. Explicit counterexample to transferring the theorem to routed flows

Take three vertices with initial scores s=(3,0,0), two directed arcs 0->1 and 1->2, each of capacity 1, and a global transfer budget F=1. There are no measurement errors (all error capacities zero, H=0). Let k=1, so the original top vertex is 0.

**Independent-arc model (the actual EdgeFlow theorem).** For pair i=0, j=2, both arcs have coefficient +1 in the change of outsider-minus-insider separation: the first reduces score 0, and the second increases score 2. The optimal transfer loss is min(F,2)=1. A feasible witness is f_01=1,f_12=0, giving updated scores (2,1,0), hence separation 2. Alternatively f_01=0,f_12=1 gives (3,-1,1), also separation 2. The exact pairwise margin is 3-1=2.

**Conserved routed-flow model (NOT the EdgeFlow theorem).** Impose flow conservation at the intermediate vertex 1: f_01=f_12=t. The global budget is the same sum of arc transfers, so 2t<=1, i.e. t<=1/2. Both endpoints change by t, so the separation between 0 and 2 becomes 3-2t. The exact minimum is 2 at t=1/2. Thus the numerical optimum happens to coincide in this example, despite different feasible sets. This example by itself does **not** establish a failure of the independent-arc margin as an exact routed-flow margin.

A sharper counterexample uses a **three-edge path** 0->1->2->3, each capacity 1, initial scores (4,0,0,0), k=1, F=1, H=0. Consider pair i=0, j=3. In the independent-arc model the favorable arcs are 0->1 and 2->3, each coefficient +1, so the worst pairwise loss is 1 and its exact margin is 3. Under conservation at both internal vertices, f_01=f_12=f_23=t and 3t<=1. The score gap between 0 and 3 is 4-2t, whose minimum is 4-2/3=10/3, strictly **larger** than the independent-arc pairwise margin 3. In fact this same four-vertex example also proves a **global top-1 margin mismatch**. In the independent-arc model, the pair (0,1) has harmful coefficient 2 on arc 0->1 and capacity 1, so its exact margin is 4-2=2; every other outsider has margin at least 3, hence the independent-arc global top-1 margin is 2. In the conserved routed model, all three flows equal t<=1/3, yielding updated scores (4-t,0,0,t). The worst outsider is vertex 3 and the exact global margin is 4-2t>=10/3, attained at t=1/3. Therefore **2 is strictly smaller than 10/3**: the independent-arc certificate is conservative but not exact for the routed-flow model.

The distinction is not a defect in the original theorem; it demonstrates that **changing the uncertainty model changes the exact result**.

## 3. Important logical qualification

Because routed/conserved flows form a **subset** of independently admissible arc transfers (when the same arc capacities and sum-of-arc-flow budget are used), the independent-arc worst-case margin is a **valid lower bound** for the routed-flow worst-case margin. Thus:

- If the independent-arc margin is positive, then the more constrained routed-flow system is also strictly robust.
- If the independent-arc margin is zero or negative, one cannot conclude that the routed-flow system is actually nonrobust: the adverse witness may violate transit conservation.
- The independent-arc pairwise loss is an upper bound on routed-flow pairwise loss, but not necessarily exact.

This is a precise and potentially useful **conservative screening guarantee**, distinct from claiming exact routing robustness.

## 4. Why this is a meaningful scientific boundary

Related work:

- Bojchevski and Günnemann, *Certifiable Robustness to Graph Perturbations*, NeurIPS 2019, https://papers.neurips.cc/paper/9041-certifiable-robustness-to-graph-perturbations.pdf . Their global/local perturbation budgets and PageRank-like propagation model differ from our fixed-score independent transfers; they report hardness for a globally constrained structural perturbation setting.
- Zügner and Günnemann, *Certifiable Robustness of Graph Convolutional Networks under Structure Perturbations*, KDD 2020, DOI https://doi.org/10.1145/3394486.3403217 . They consider GCN structure perturbations and bilinear verification, not our independent linear arc transfers.
- Aolaritei, Huang, Jordan, and Grigas, *Diffusion-Robust Optimization over Graphs*, arXiv:2605.30853 (2026), https://arxiv.org/abs/2605.30853 . Their uncertainty includes propagation and conservation constraints, highlighting why the uncertainty model controls complexity.
- Mouratidis and Tang, *Exact Processing of Uncertain Top-k Queries in Multi-criteria Settings*, PVLDB 2018, DOI https://doi.org/10.14778/3204028.3204031 . The uncertain top-k model varies scoring weights, not independent graph transfers.

The existence of other graph-robustness papers does not invalidate the EdgeFlow proof, but it prevents broad claims such as "first certified graph ranking method". A novelty assessment must compare precise uncertainty sets, objectives, guarantees, and algorithmic complexity.

## 5. Testable future research direction

A more scientifically useful next question is whether an **exact, scalable certificate** exists for original top-k stability when flow conservation is imposed at specified transit vertices. The independent-arc margin provides a computable conservative lower bound, and its feasible witness may not respect transit constraints. Any exact algorithm for the conserved model needs a new derivation, likely involving flow optimization rather than simply reusing the fractional-knapsack formula.

**Status:** This is a concrete research problem, not a theorem of novelty, a claimed complexity lower bound, or an accepted publication. Independent algorithmic review is still required.
