# Related literature and originality assessment

**Assessment date: 2026-11-11.** These references were located and bibliographic information checked. They do not constitute a complete academic literature search.

1. **Dimitris Bertsimas and Melvyn Sim (2004)**, "The Price of Robustness," *Operations Research* 52(1):35–53. DOI: https://doi.org/10.1287/opre.1030.0065 . This is foundational work on robustness with a budget of uncertainty. The edge-pair optimization here has the flavor of a known budgeted linear allocation; we do not claim that greedy budget allocation itself is new.
2. **Kyriakos Mouratidis and Bo Tang (2018)**, "Exact Processing of Uncertain Top-k Queries in Multi-criteria Settings," *Proceedings of the VLDB Endowment* 11(8):866–879. DOI: https://doi.org/10.14778/3204028.3204031 . This studies exact top-k query processing under uncertain preference weights, different from independent signed graph-edge transfers.
3. **Ruiting Liang, Jake A. Soloff, Rina Foygel Barber, and Rebecca Willett (2025)**, "Assumption-free stability for ranking problems," arXiv:2506.02257. https://arxiv.org/abs/2506.02257 . This develops stability via ranking operators, with a different model and guarantee.

## Research status

A self-contained mathematical proof and reproducible small-case LP checks are supplied in this repository, but **we have not established priority** for either the pairwise formula or the near-linear reduction. Search-engine access, mathematical terminology, and journal coverage limit any novelty conclusion. Before a paper claims novelty, independently search MathSciNet/zbMATH, graph ranking and robust optimization literature, cited/citing papers, and the exact or equivalent algorithmic reduction.

Please open an issue if you find equivalent prior work, a stronger predecessor, or a counterexample.

## Additional related results located 12 November 2026

4. **Information Retrieval Under Network Uncertainty: Robust Internet Ranking**, *Operations Research*. DOI https://doi.org/10.1287/opre.2022.2298. A network-ranking robustness approach involving uncertainty budgets, but oriented around perturbations of the underlying ranking network; it is not direct evidence of the present edge-transfer bound's priority.

5. **Changing the ranking in eigenvector centrality of a weighted graph by small perturbations**, *Mathematics of Computation* (2026). DOI https://doi.org/10.1090/mcom/4149. Considers adjacency-weight perturbations and eigenvector ranking changes, a materially different uncertainty model.

An additional targeted search of robust top-k selection, graph incidence perturbations, network score transfer budgets, and L1 robust ranking did not expose an exact matching published theorem. **This remains an incomplete search, not a novelty finding.**
