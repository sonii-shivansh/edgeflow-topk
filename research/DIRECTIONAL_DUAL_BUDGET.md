# Directional dual-budget top-k certification: derivation and validation

> **Research status (12 Nov 2026):** Candidate algorithmic result derived in this project, with a complete model-conditional proof and numerical checks. **Novelty and priority NOT established. Not peer reviewed.** The proof uses established budgeted robust-optimization and offline orthogonal-range-query ideas. This is a separate, experimental generalization of EdgeFlow.

## 1. Problem definition

Let G=(V,A) be a **finite directed graph** with n vertices, m directed arcs, and at most one arc for each ordered vertex pair (reciprocal arcs are allowed). Every arc (u,v) has a finite nonnegative capacity c_uv. Every vertex v has a finite initial real score s_v and a finite nonnegative measurement-error capacity a_v.

Adversarial **one-way transfers** f_uv are independent nonnegative values satisfying

$$
0\le f_{uv}\le c_{uv},
\qquad \sum_{(u,v)\in A}f_{uv}\le F.
$$

Measurement errors epsilon_v are signed and independent of transfers, subject to

$$
|\epsilon_v|\le a_v,
\qquad \sum_{v\in V}|\epsilon_v|\le H.
$$

Both budgets F,H are nonnegative and finite. Updated scores are

$$
s'_v=s_v+\sum_{u:(u,v)\in A}f_{uv}
-\sum_{w:(v,w)\in A}f_{vw}+\epsilon_v.
$$

The transfer component conserves the sum of scores. Measurement errors need not conserve the sum. **There are no additional path-flow or intermediate-vertex conservation constraints and updated scores need not remain nonnegative.**

Fix 1<=k<n, and take T as the original highest-scoring k vertices, with deterministic initial tie-breaking. Define the global **worst-case top-k separation margin**

$$
\rho(F,H)=
\min_{\substack{f,\epsilon\ {\rm feasible}}}
\min_{\substack{i\in T\\j\notin T}}
(s'_i-s'_j).
$$

Strict robustness means rho(F,H)>0. Equality means an attainable boundary tie; a negative margin means an attainable outsider-over-insider reversal.

For a vertex v, let

$$
D_v^{\rm out}=\sum_{w:(v,w)\in A}c_{vw},
\qquad
D_v^{\rm in}=\sum_{u:(u,v)\in A}c_{uv}.
$$

Let c_ij be the forward-arc capacity (i,j), or zero if it does not exist.

## 2. Exact pairwise bound

**Lemma 1 (attained pairwise loss).** For distinct vertices i,j, the maximum feasible increase in (s'_j-s'_i) relative to (s_j-s_i) equals

$$
\boxed{
\Gamma_{ij}(F,H)=
2\min(c_{ij},F)
+\min\left(D_i^{\rm out}+D_j^{\rm in}-2c_{ij},
(F-c_{ij})_+\right)
+\min(H,a_i+a_j).
}
$$

*Proof.* For an arc e=(u,v), the coefficient of its nonnegative flow f_e in the outsider-minus-insider score change is

$$
\alpha_e=
\mathbf1_{\{v=j\}}-\mathbf1_{\{u=j\}}
-\mathbf1_{\{v=i\}}+\mathbf1_{\{u=i\}}.
$$

An arc i->j has coefficient +2; an arc j->i has coefficient -2. Other outgoing arcs from i and incoming arcs to j have coefficient +1. Other incoming arcs to i and outgoing arcs from j have coefficient -1, and all unrelated arcs have coefficient 0. Because flows are **nonnegative**, an optimum sets all arcs with nonpositive coefficient to zero. The forward arc i->j, when present, is the only coefficient-2 arc and has capacity c=c_ij. The coefficient-1 arcs have total capacity

$$
S=D_i^{\rm out}+D_j^{\rm in}-2c\ge0.
$$

This follows because the direct arc is counted once by each of the two capacity sums. Let x be the flow on the direct arc, and y the sum on the coefficient-1 arcs. Maximizing their total contribution is precisely

$$
\max 2x+y
\quad\text{such that}\quad
0\le x\le c,\ 0\le y\le S,\ x+y\le F.
$$

Any feasible x,y can be realized by distributing y among the coefficient-1 arcs up to their individual capacities. The coefficient-2 arc always gives at least as much improvement per unit as any coefficient-1 arc, so an exchange argument fills x first. Specifically, if x<min(c,F) while y>0, shift a positive feasible amount from y to x and strictly improve the objective; if there is unused budget, increasing x improves it. Thus an optimum has x*=min(c,F), followed by y*=min(S,(F-c)_+). The exact transfer contribution equals 2x*+y*.

For measurement errors, the outsider-minus-insider change is epsilon_j-epsilon_i. Assigning epsilon_i<=0 and epsilon_j>=0 cannot worsen the objective, and setting all other errors to zero is feasible. Their combined favorable magnitude can be any t between zero and min(H,a_i+a_j). The maximum is therefore exactly min(H,a_i+a_j); allocate first to i then to j up to the individual caps. Because the flow and error feasibility constraints are separate, these two maxima can be achieved simultaneously. Adding them yields Gamma_ij and the explicit feasible witness. QED.

**Corollary.** The exact global margin is

$$
\rho(F,H)=
\min_{\substack{i\in T\\j\notin T}}
(s_i-s_j-\Gamma_{ij}(F,H)).
$$

*Proof.* For a fixed pair, Lemma 1 gives the attained minimum of s'_i-s'_j. The joint feasible set is nonempty and compact, and there are finitely many crossing pairs. Taking the minimum over all pairs and over all feasible perturbations commutes because both are minimizations over their finite-product index/feasible set. Therefore the global minimum equals the minimum of the attained pairwise minima. QED.

## 3. Baseline and exceptional forward-arc correction

Put

$$
L_{ij}=\min(F,D_i^{\rm out}+D_j^{\rm in})+\min(H,a_i+a_j).
$$

**Lemma 2.** Gamma_ij >= L_ij for every crossing pair, with **equality whenever there is no forward arc i->j** (including when the opposite arc j->i exists).

*Proof.* The measurement-error term is identical in Gamma and L, so it cancels from the comparison. When c_ij=0, the flow expression reduces to min(F,Dout_i+Din_j), proving equality. For c=c_ij>0 and S=Dout_i+Din_j-2c, distinguish three exhaustive cases. If F<=c then the flow Gamma term is 2F >= min(F,2c+S). If c<F<=c+S then it is F+c >= min(F,2c+S). If F>c+S then it is 2c+S = Dout_i+Din_j >= min(F,Dout_i+Din_j). QED.

Define the set of **forward crossing arcs** A_T={(i,j) in A: i in T, j not in T}. Let

$$
\rho_0=\min_{i\in T,j\notin T}(s_i-s_j-L_{ij})
$$

and

$$
\rho_A=\min_{(i,j)\in A_T}(s_i-s_j-\Gamma_{ij}),
$$

where rho_A=+infinity if A_T is empty.

**Lemma 3 (exact sparse correction).**

$$
\boxed{\rho(F,H)=\min(\rho_0,\rho_A).}
$$

*Proof.* For every pair without a forward arc, the baseline is exact by Lemma 2. For a pair with a forward arc, its exact expression appears in rho_A, and by Lemma 2 that exact expression is no larger than its baseline expression. Hence adding the exact expressions of forward arcs to all baseline expressions and taking their minimum discards no smaller quantity and leaves precisely the minimum over all exact pairwise expressions. This is rho(F,H) by the corollary. QED.

## 4. Four orthogonal-range maximum queries

For a given insider i, the largest baseline-perturbed outsider score is

$$
M_i=\max_{j\notin T}
\left[
s_j+\min(F,D_i^{\rm out}+D_j^{\rm in})
+\min(H,a_i+a_j)
\right].
$$

Then rho_0 = min_{i in T}(s_i-M_i).

Let the outsider coordinates be y_j=D_j^in and z_j=a_j, and the insider query thresholds be

$$
t_i=F-D_i^{\rm out},\qquad h_i=H-a_i.
$$

For each insider, every outsider belongs to exactly one of four disjoint quadrants:

| Quadrant | Constraints on outsider (y_j,z_j) | Offset depending on i | Weight to maximize |
|---|---|---|---|
| LL | y_j<=t_i, z_j<=h_i | Dout_i+a_i | s_j+y_j+z_j |
| LH | y_j<=t_i, z_j>h_i | Dout_i+H | s_j+y_j |
| HL | y_j>t_i, z_j<=h_i | F+a_i | s_j+z_j |
| HH | y_j>t_i, z_j>h_i | F+H | s_j |

These expressions follow by explicitly replacing each minimum by its unsaturated or saturated branch. Consequently, for a fixed i, M_i is the maximum of four independent orthogonal-range-max answers plus their associated offsets.

**Lemma 4.** All four families of M_i quadrant queries can be evaluated in O(n log n) time and O(n) auxiliary space.

*Proof.* Consider any fixed quadrant. Sort outsiders by y_j (ascending for y_j<=t, descending for y_j>t) and sort insider queries by t in the same order. As queries are processed, insert each newly qualifying outsider point exactly once into a Fenwick tree. Compress the z_j values to ranks 1,...,q (q<=n). Store the maximum of the quadrant-specific weight together with its outsider index at every updated Fenwick entry. When the second inequality is z_j<=h, standard rank order makes the desired z-constraint a Fenwick prefix query with end rank bisect_right(z_coords,h). When it is z_j>h, reverse the rank order, making the strict upper condition a Fenwick prefix query of length q-bisect_right(z_coords,h). Therefore each outsider inserts once and each insider queries once. Insertion, prefix maximum, rank binary searches and sorting take O(log n) operations per point/query; the Fenwick array takes O(n) space. Repeat this sweep for the four constant-sized quadrants, reusing memory. This proves the claimed total. QED.

## 5. Main theorem and algorithm

**Theorem (exact directional dual-budget margin).** For the model above, one can compute the exact worst-case top-k separation margin rho(F,H), an attaining insider-outsider pair, and whether the original top-k set is strictly robust, in

$$
\boxed{O(m+n\log n)\ {\rm time},\qquad O(m+n)\ {\rm space}}
$$

in the exact-arithmetic comparison model. Given the returned pair, one can construct an attaining feasible directed-flow and signed-error perturbation in an additional O(m+n) time.

*Proof.* Compute Dout and Din in one arc pass, O(m+n). Identify the original k highest scoring vertices, O(n log n), and build outsider coordinates. Evaluate all four quadrant maxima by Lemma 4, obtaining all M_i in O(n log n). Let rho_0=min_i(s_i-M_i) and preserve the minimizing pair and its originating quadrant. Then scan every arc once, evaluate the exact Gamma_ij of Lemma 1 for every **forward crossing** arc (i,j), and minimize to find rho_A in O(m). By Lemma 3, min(rho_0,rho_A) is exactly rho(F,H), hence strict robustness iff the returned margin is positive.

For the witness, take a pair that attains this minimum. If the pair arose from rho_A, its chosen expression is the exact pairwise margin. If it arose from rho_0 and had a forward arc with strictly larger Gamma_ij than L_ij, that arc's exact expression would be strictly smaller than rho_0 and have been found in rho_A, contradiction. Therefore the chosen baseline pair's expression is also exact. Lemma 1 constructs independently feasible directed flows and measurement errors attaining Gamma_ij, hence the returned global margin. The witness scans up to m arcs and initializes n errors, in O(m+n). The sorting, offline sweeps and arc pass establish O(m+n log n) time and O(m+n) space. QED.

## 6. Reproducible numerical checks

Code: [../experimental/directional_dual_budget.py](../experimental/directional_dual_budget.py). Tests: [../tests/test_directional_dual_budget.py](../tests/test_directional_dual_budget.py).

The following **actual local executions** passed on 12 November 2026:

- 8 explicit deterministic cases (forward and reverse arc direction, independent error-only, combined budgets, exact boundary tie and a large-integer gap).
- 1,000 pseudo-random integer graph cases checked against the explicit all-crossing-pairs formula with independent constructive witnesses.
- 115 additional small **exact rational (Fraction)** cases, directly enumerating every feasible directed-flow and signed-error vector on a half-integer grid, **without calling Gamma or the fast algorithm to compute the oracle**.
- 390 pairwise maximizations independently optimized by SciPy/HiGHS on 85 further random graphs, using positive/negative error split variables and explicit flow/measurement budgets. Every LP objective matched the bound to test tolerance, and every graph's minimum matched the fast algorithm.

Local test summary: four unittest methods, all passed; no failures. The tests cannot prove originality or cover all inputs.

A synthetic single-run CPython performance illustration (n,m,time): (1,000,4,000,0.004725 s), (5,000,20,000,0.019664 s), (20,000,80,000,0.104929 s). These measurements depend on the machine, workload and interpreter and are not an empirical lower-bound or speedup claim.

## 7. Scientific novelty check (performed after deriving and testing the claim)

The following primary sources were found when searching directed edge-flow robust top-k, joint measurement/transfer budgets, and offline 2D dominance:

1. **Bertsimas and Sim (2004), The Price of Robustness**, *Operations Research* 52(1), 35-53, https://doi.org/10.1287/opre.1030.0065 . Budgeted adversarial allocation is longstanding mathematics. The greedy pairwise budget allocation is **not** a new general optimization principle.
2. **Chan, Larsen and Patrascu (2011), Orthogonal Range Searching on the RAM, Revisited**, https://arxiv.org/abs/1103.5510 . Orthogonal range-search techniques, including strong offline dominance results, are well-established. The Fenwick sweep itself is **not** a novel general data structure.
3. **Aolaritei, Huang, Jordan and Grigas (2026), Diffusion-Robust Optimization over Graphs**, https://arxiv.org/abs/2605.30853 . Their topology-aware directed graph uncertainty has propagation and conservation constraints, which differ materially from our **independent** directed arc transfers and exogenous measurement errors.
4. **Robust Combinatorial Optimization with Locally Budgeted Uncertainty**, https://ojmo.centre-mersenne.org/articles/10.5802/ojmo.5/ . The use of multiple/region-specific uncertainty budgets is pre-existing.
5. **Mouratidis and Tang (2018), Exact Processing of Uncertain Top-k Queries in Multi-criteria Settings**, https://doi.org/10.14778/3204028.3204031 . Exact top-k processing under scoring-weight uncertainty is longstanding, but the uncertainty model differs.

Queries performed include "robust top-k directed graph edge flow perturbations node measurement errors two budgets 2D dominance", "budgeted uncertainty robust top k ranking independent simultaneous additive score uncertainty network flow capacity", "orthogonal range maxima robust ranking two budgets edge flows top k algorithm", and "top k ranking robustness multiple independent uncertainty budgets node edge directed flow".

**Novelty verdict: UNCONFIRMED.** No exact predecessor was identified in this targeted search, but standard techniques may subsume this model and algorithm. The formula is an accessible specialization of support-function / fractional-knapsack calculations, and the range query reduction uses textbook offline geometry techniques. It would be incorrect to claim 'new scientific discovery', 'first' or 'peer reviewed' without independent literature and mathematical evaluation.

## 8. Limitations and falsifiability

- **Independent one-way arc transfers only:** no intermediate-vertex flow conservation, no mandatory path routing, no directed edge failure/reweighting, and no recomputed PageRank or Katz centrality.
- **Independent measurement errors:** signed, bounded per node and by an independent global L1 budget. If errors are correlated with transfers or required to conserve their sum, the formula changes.
- **Finite simple directed graphs:** no multiple arcs per ordered pair; reciprocal arcs are permitted.
- **Real arithmetic in theorem:** the code does not offer formal floating-point certification near ties; Python integers or Fractions support exact comparisons for rational inputs.
- **No evidence of application relevance:** performance data are synthetic, not calibrated to a real dataset with this physical model.
- **No general lower bound, independent peer review, publication DOI, or priority certificate** has been established.

A falsifier is any legal instance in which the returned margin differs from the actual minimum over feasible flows/errors, a legal witness fails to attain it, or the complexity bound fails for a comparison-model family. A bibliographically proven prior equivalent algorithm would falsify an originality claim, but not necessarily mathematical correctness.

**Confidence:** High in the conditional theorem after the full proof and independent LP/grid checks; insufficient evidence to assert historical novelty. External review is requested.
