# Invitation for independent research review — EdgeFlow Top-k

**Review target:** self-contained mathematical proof and quantitative extension under a signed edge-transfer budget. **This is not an externally reviewed result.**

- Repository: https://github.com/sonii-shivansh/edgeflow-topk
- Public review issue: https://github.com/sonii-shivansh/edgeflow-topk/issues/1
- Original theorem: [PROOF.md](PROOF.md)
- Quantitative extension: [MARGIN_THEOREM.md](MARGIN_THEOREM.md)
- Source: [edge_transfer_topk.py](../edge_transfer_topk.py)
- Exact-enumeration tests: [test_exact_enumeration.py](../tests/test_exact_enumeration.py), [test_exact_margin.py](../tests/test_exact_margin.py)
- Prior-art audit: [NOVELTY_AUDIT_2026-11-12.md](NOVELTY_AUDIT_2026-11-12.md)
- Caveats: [LIMITATIONS.md](../LIMITATIONS.md)

## Concise reviewer question

For a finite simple undirected graph with fixed real vertex scores, allow independent signed transfers on its edges with edge capacities c_e and global L1 budget B. Given the original top-k vertices, can one certify their strict separation from outsiders, and compute the exact minimum separation margin, in O(m+n log n) time? We give a self-contained proof based on a sharp pairwise adversarial bound, nonedge baseline, and exact crossing-edge correction.

We are not asking a reviewer to endorse a novelty claim. We specifically request them to determine if the argument is valid **and** whether a more general published result already contains it.

## Audit prompts for an external researcher

1. Can a feasible signed flow violate the pairwise expression (Lemma 1), including cases B=0, c_ij=0, isolated vertices, or extremely skewed capacities?
2. Is the baseline-plus-crossing-edge reduction actually necessary and sufficient for all crossing pairs, including ties?
3. Does the quantitative margin reduction compute the **minimum over all feasible flows and boundary pairs**, not just a sufficient lower bound?
4. Is the claimed O(m+n log n) worst-case comparison-model running time valid for arbitrary finite simple graphs?
5. Could a prior robust optimization theorem or an offline dominance-minimum data structure imply the identical reduction or stronger result? Please provide theorem number/page and a concise mapping of variables.
6. Are the independently enumerated exact-grid cases sufficiently independent of the claimed pairwise formula?
7. Do known application areas genuinely have independently signed edge transfers, as opposed to directed routing or re-evaluated centrality?

## Review response format

- Verdict: correct / counterexample / conditionally correct / insufficiently novel / needs clarification.
- Exact mathematical claim or source line under review.
- A reproducible counterexample (scores, edges, capacities, budget, k, and legal flow), or a full proof argument.
- Full bibliographic information, URL/DOI, theorem number/page for proposed prior art.
- Whether the review was independent of the author team's AI-assisted notes.

A public GitHub issue does **not** imply an invitation has reached or been accepted by external researchers. An external expert must actually examine and comment before the research can be called independently reviewed.
