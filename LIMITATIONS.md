# Assumptions, limitations, and risks

1. **Simple undirected graph only:** At most one edge per vertex pair; parallel edges, hyperedges, and direction-constrained transfers are outside the theorem.
2. **Independent signed-edge flows:** Each edge may transfer positively or negatively under its own capacity and the shared L1 budget. Additional routing or intermediate-node conservation constraints change the feasible set.
3. **Exogenous initial scores:** This certifies a fixed initial score vector. It does not automatically certify PageRank, Katz centrality, or other scores recomputed when a graph changes.
4. **Updated scores may be negative:** Nonnegative post-transfer scores, per-vertex resource constraints, or other added inequalities can change the worst-case bound.
5. **Top-k membership, not full order:** Only strict separation of each original insider from every outsider is certified. The internal order inside the top-k is not protected.
6. **Ties are failures:** A potentially equal insider/outsider pair is not strictly robust even if a deterministic tie-breaker would preserve selected membership.
7. **Budget definition is essential:** The global constraint is `sum_e |f_e| <= B`. Weighted edge prices, quadratic costs, and path-length costs require a different proof.
8. **Floating-point implementation:** The mathematical theorem assumes real arithmetic. The Python code uses floats and comparisons, which can be unreliable near the equality threshold or with huge magnitudes. Validate independently or use exact rational/interval arithmetic for critical decisions.
9. **Input trust:** The code uses assertions, not complete production input validation. It assumes finite numeric capacities/scores/budget and a simple graph. Do not feed untrusted input directly.
10. **No production benchmarks:** The algorithm has an asymptotic proof, not reported real-world performance benchmarks.
11. **Research originality unconfirmed:** Similar budgeted optimization and robust ranking themes predate this note; priority cannot be asserted without deeper literature review.
12. **Human review required:** The research note and software were produced with AI assistance, have not been peer reviewed, and should be examined independently before formal scholarly publication.
