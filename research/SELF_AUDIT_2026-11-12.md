# Internal proof and implementation audit — 12 November 2026

**Authorship of this audit:** AI-assisted self-review. This is **not** an independent referee report, not an acceptance decision, and not evidence of priority.

## Mathematical checks

1. Pairwise signed-edge coefficient calculation: an edge directly connecting the two compared vertices contributes magnitude 2; an edge incident to exactly one contributes 1; others contribute 0. An arbitrary orientation does not affect the maximum because the corresponding signed flow can be reversed.
2. Edge-capacity aggregation: in a **simple** undirected graph, there is at most one direct edge and the combined capacity on coefficient-1 edges is d_i+d_j-2c_ij. Extending to multigraphs requires revisiting the source's simple-graph validation and its direct-edge capacity representation.
3. Budgeted support: the resulting maximization max(2x+y) subject to 0<=x<=c_ij, 0<=y<=S and x+y<=B is an elementary fractional-knapsack problem and is exactly attained at x=min(B,c_ij), y=min(S,(B-c_ij)_+).
4. Baseline correctness: for nonedges, Gamma_ij=min(B,d_i+d_j). For adjacent pairs, Gamma_ij>=that baseline. Checking every baseline pair plus every crossing edge therefore checks precisely all exact pairs.
5. Global margin: the finite minimum over pairs commutes with minimization over feasible flows; the global minimum of baseline and crossing-edge exact margins equals the sharp worst-case separation. See [MARGIN_THEOREM.md](MARGIN_THEOREM.md) for step-by-step proof.
6. Complexity: degrees and crossing-edge scan O(m+n); sorting top set and outsider degrees O(n log n); prefix/suffix maxima O(n); a binary search per top vertex O(n log n). Total O(m+n log n) arithmetic/comparisons; memory O(m+n).

**No mathematical counterexample found in the tested cases. This does not imply external validation.**

## Independent numerical designs

**Original tests:** 350 random small graph-level cases, 1,987 independently solved signed-edge linear programs, explicit feasible witnesses, 8 deterministic edge cases.

**First exact-grid suite:** 260 integer cases, 90 half-integer rational cases, plus large-integer regressions.

**New exact-margin suite, using seed 20261112:** 2,600 randomized integer graphs compared against a direct all crossing-pairs computation and 420 exact-rational graphs independently checked by enumerating actual feasible signed edge transfers on a half-unit grid. This oracle computes post-transfer scores directly; it does **not** invoke the pairwise support formula. All 3,020 new checks passed in local execution. The GitHub Actions workflow also runs the committed suites.

**Very large integer stress:** With scores [10**100+1, 10**100], no edges, B=0, the correct margin is 1. Explicit floating-point conversion makes the scores equal and destroys this distinction. The core algorithm was previously changed to initialize degrees as integer zeros. On 12 November 2026 we additionally changed the constructive-witness flow vector initialization from floating-point 0.0 to integer 0, allowing exact all-integer or Fraction witness arithmetic for the prescribed inputs.

## Remaining software and proof gaps

- Input validation uses assertions and is not hardened for hostile inputs or non-finite floats.
- Floating-point comparisons near ties can still be incorrect; users needing exact certificates should use Python ints/Fractions and independently check their input model.
- Tests sample only a small fraction of possible graphs and budgets. The mathematical proof, not random testing, is the basis of the universal claim.
- The benchmark is a synthetic illustration, not a real workload or a statistically sound comparison.
- The qualitative connection to robust optimization is already prior art. The precise algorithm's originality is **unconfirmed**.
- No external reviewer has supplied a signed report or counterexample.
- The published release remains an unreviewed technical artifact and is not an arXiv or journal publication.

## Audit outcome

**Correctness assessment:** theorem-level argument is complete under its stated model, and the numerical implementation passes the documented independent checks.

**Implementation assessment:** suitable as a reproducible research prototype, not a production input-validation or floating-point certified library.

**Originality assessment:** unconfirmed; the greedy support computation is not an original general mathematical technique.

**Publication readiness:** not yet suitable for journal submission asserting a substantial original contribution without stronger prior-art comparison and independent human verification.
