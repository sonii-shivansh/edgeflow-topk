# Exact minimum measurement-error budget for fixed directed transfer budget

**Status (12 November 2026): AI-assisted, internally checked mathematical research candidate; not externally peer reviewed. Academic novelty and priority are UNCONFIRMED.**

This complements [the exact critical transfer-budget theorem](CRITICAL_FLOW_BUDGET.md), which fixes measurement-error budget H and finds the first destabilizing flow budget F. Here we fix F and minimize H.

## 1. Exact mathematical model

Let G=(V,A) be a finite **simple directed graph**: for each ordered pair there is at most one arc, and opposite-direction arcs may coexist. Every arc (u,v) has finite capacity c_uv>=0 and carries an independent **nonnegative** one-way transfer f_uv, with f_uv<=c_uv and sum_A f_uv<=F, for fixed F>=0. Each node v has finite initial real score s_v and error bound a_v>=0. Signed errors e_v satisfy |e_v|<=a_v and sum_v|e_v|<=H, where H>=0 is varied. The two uncertainties have **separate budgets** and impose no flow-routing, intermediate conservation, or updated-node nonnegativity constraints.

For each v, define s'_v=s_v+sum_{u->v}f_uv-sum_{v->w}f_vw+e_v. Let T be the highest-scoring k original vertices (1<=k<n), with deterministic tie-breaking. Define the exact adversarial separation margin

$$
\rho(F,H)=\min_{\substack{f,e\ \mathrm{feasible}}}
\min_{\substack{i\in T\\j\notin T}}
(s'_i-s'_j).
$$

Strict robustness holds exactly when rho(F,H)>0, and **even an attainable tie is failure**. The minimum error budget allowing a failure is

$$
H_*(F)=\inf\{H\ge0:\rho(F,H)\le0\},
$$

with H_*=+infinity if no such budget exists.

Write Dout_i=sum_{i->v}c_iv and Din_j=sum_{u->j}c_uj. Let c_ij be the capacity of the forward arc i->j if it exists, otherwise 0.

## 2. Pairwise inversion theorem

The [directional dual-budget pairwise theorem](DIRECTIONAL_DUAL_BUDGET.md) gives the attained worst harmful flow increase

$$
g_{ij}(F)=
2\min(c_{ij},F)+
\min\bigl(Dout_i+Din_j-2c_{ij},(F-c_{ij})_+\bigr),
$$

where (x)_+=max(0,x). The worst signed measurement error contributes exactly min(H,a_i+a_j), and can be realized simultaneously because flow and error budgets constrain different variables.

Define the residual pair gap after the worst possible flow, but before measurement error:

$$
\Delta_{ij}(F)=s_i-s_j-g_{ij}(F).
$$

**Lemma 1 (exact pairwise first-error budget).** The first H that permits a tie or reversal for this pair equals

$$
H^*_{ij}(F)=
\begin{cases}
0,&\Delta_{ij}(F)\le0,\\
\Delta_{ij}(F),&0<\Delta_{ij}(F)\le a_i+a_j,\\
+\infty,&\Delta_{ij}(F)>a_i+a_j.
\end{cases}
$$

**Proof.** A pair fails strict separation exactly when the maximum harmful change from flows and errors meets or exceeds the original gap, i.e.

$$
g_{ij}(F)+\min(H,a_i+a_j)\ge s_i-s_j.
$$

When the residual Delta is nonpositive this inequality holds at H=0. When it is greater than a_i+a_j, measurement errors cannot close the gap even if all available per-node error capacity is used. In the remaining case the inequality holds exactly when H>=Delta. The pairwise maximizers are attainable by allocating errors of the harmful signs to i and j and using a flow achieving g; thus the threshold is attained. QED.

**Corollary.** The global first error budget is min_{i in T,j outside} H^*_{ij}(F). This follows since the ranking fails if and only if **at least one** top-vs-outsider pair fails. All minima exist when finite, by compactness and the finite set of pairs.

## 3. Cheap baseline and exceptional forward arcs

At fixed F define the non-forward flow baseline

$$
g^0_{ij}(F)=\min(F,Dout_i+Din_j),\qquad
\Delta^0_{ij}(F)=s_i-s_j-g^0_{ij}(F).
$$

The directional flow proof shows g_ij>=g^0_ij, and equality **whenever there is no forward arc i->j**, even if a reverse arc j->i exists. Define B^*_{ij} using the three-branch formula of Lemma 1 with Delta^0 instead of Delta.

**Lemma 2 (sparse correction).** Let A_T be the set of directed arcs (i,j) with i in T and j outside. Then

$$
\boxed{
H_*(F)=\min\left(
\min_{\substack{i\in T\\j\notin T}}B^*_{ij},
\min_{(i,j)\in A_T}H^*_{ij}(F)
\right).
}
$$

The second minimum is +infinity when A_T is empty.

**Proof.** Every non-forward pair has exact threshold B^*=H^*. For a forward pair, g>=g0 gives Delta<=Delta0; the three-branch threshold rule is nondecreasing in Delta (taking +infinity above the per-node capacity sum). Therefore its exact threshold H^* is no greater than its baseline B^*. The combined minimum includes the exact value for every forward pair and the exact baseline for every non-forward pair; adding weaker baseline thresholds for forward pairs cannot lower that minimum. QED.

First compute rho(F,0) with the existing fixed-budget exact algorithm. If rho(F,0)<=0, return H_*=0 and its attaining pair. Otherwise all Delta_ij>0, and, since Delta0>=Delta, all baseline Delta0>0 as well. Under this **strictly safe-at-zero** case, a finite baseline threshold is simply Delta0 provided Delta0<=a_i+a_j. This is what the fast algorithm computes.

## 4. Two offline 2D dominance-max sweeps

For a given original insider i and outsider j, split the baseline into two mutually exclusive cases according to whether the flow budget is saturated:

**Case U (unsaturated): Din_j <= F-Dout_i.**

Here g0=Dout_i+Din_j and

$$
\Delta^0_{ij}=(s_i-Dout_i)-(s_j+Din_j).
$$

The feasibility condition for a finite baseline threshold, Delta0<=a_i+a_j, becomes

$$
(s_j+Din_j+a_j)\ge(s_i-Dout_i-a_i).
$$

For every insider i, it is therefore enough to **maximize** x_j=s_j+Din_j among outsiders simultaneously satisfying

$$
Din_j\le F-Dout_i,\qquad
y_j=s_j+Din_j+a_j\ge s_i-Dout_i-a_i.
$$

The best candidate for this insider is (s_i-Dout_i)-max x_j.

**Case S (saturated): Din_j > F-Dout_i.**

Now g0=F, Delta0=(s_i-F)-s_j, and the condition Delta0<=a_i+a_j becomes

$$
s_j+a_j\ge s_i-F-a_i.
$$

Thus for every insider maximize x_j=s_j subject to the two conditions

$$
Din_j>F-Dout_i,\qquad
y_j=s_j+a_j\ge s_i-F-a_i.
$$

The best candidate is (s_i-F)-max x_j.

**Lemma 3.** All the above queries can be answered offline in O(n log n) arithmetic/comparison time and O(n) space using two Fenwick prefix-maximum sweeps.

**Proof.** In each case sort outsiders in nonincreasing y_j order and insider queries by their required lower y threshold in nonincreasing order. For each query insert all not-yet-inserted outsiders with y_j above or equal to the threshold. Exactly the qualifying points have been inserted, and each point is inserted once. Compress the Din_j coordinates to ranks 1,...,q. Store the best (x_j,j) at Fenwick prefixes during insertion. In case U, the inequality Din_j<=F-Dout_i becomes a Fenwick prefix query through rank bisect_right(Din_coords,F-Dout_i). In case S, the strict complement Din_j>F-Dout_i becomes a prefix query of length q-bisect_right(...) after reversing the rank order. Each insert/query costs O(log n). Each sweep uses one O(n log n) sort and O(n) Fenwick storage; two sweeps preserve the O(n log n) bound. Since x_j is maximized over exactly the eligible points, each returned Delta0 is the least feasible baseline error threshold for the insider in the given case. QED.

## 5. Main theorem

**Theorem (exact critical measurement-error budget).** Under the model of Section 1, the global first error budget H_*(F) can be computed in

$$
\boxed{O(m+n\log n)\text{ arithmetic/comparison time and }O(m+n)\text{ space}.}
$$

If the input scores, capacities, error bounds and fixed F are integers, the finite H_* is an integer; for rational inputs, H_* is a rational value computed exactly using Python int and Fraction. For arbitrary exact real inputs the mathematical comparison-model theorem still applies. An attaining pair and an admissible flow/error witness can be constructed when H_* is finite.

**Proof.** Compute the weighted in/out degrees and original top set in O(m+n log n). Evaluate rho(F,0) in the same bound. If nonpositive, return zero. Otherwise apply Lemma 2. Lemma 3 computes the smallest finite baseline threshold for all crossing pairs in O(n log n). A single O(m) scan of forward insider-to-outsider arcs computes the remaining exact thresholds using Lemma 1. Taking the minimum recovers H_* exactly.

For a threshold pair returned by the arc scan, the value is exact by Lemma 1. If the minimizing pair comes from the baseline and its true forward-arc threshold were smaller, the arc scan would have found an even smaller global value, contradiction. Thus the baseline-selected pair is also an attaining true pair. Allocate the permitted flow F to its favorable edges (direct i->j first) and signed errors of total H_* to its two endpoints as in the pairwise witness construction. This realizes a tie at H_*, and no H<H_* can yield a tie by the global minimum definition. All preprocessing/sweeps/scans and memory bounds follow from the prior lemmas. QED.

**Two-budget interpretation:** Combining this H_*(F) with the companion critical-flow oracle F_*(H) gives **exact vertical and horizontal first-failure slices** of the monotone two-dimensional stability region. It does not automatically enumerate the complete Pareto frontier or make the safe region convex. The [critical-flow note](CRITICAL_FLOW_BUDGET.md) contains a verified nonconvex example.

## 6. Numerical falsification attempts and reproducibility

Implementation: [../experimental/critical_error_budget.py](../experimental/critical_error_budget.py). Independent tests: [../tests/test_critical_error_budget.py](../tests/test_critical_error_budget.py). Benchmark: [../experimental/benchmark_critical_error.py](../experimental/benchmark_critical_error.py).

Actual local checks on 12 November 2026:

- **9 deterministic cases**: forward/reverse arcs, impossible attacks, F=0, exact tie, huge integer gaps, and non-half rational critical budget 1/3.
- **2,000 random graphs**: fast threshold vs directly computed every-insider-outsider first-failure threshold, including exact witness and stability checks just below/at the budget.
- **150 independent exact-rational grid cases**: enumerate all feasible one-way arc flows and signed measurement errors directly; this oracle **does not call the fast algorithm or pairwise loss formula**.
- **110 separately optimized pairwise linear programs** across 35 random graphs: minimize the sum of positive/negative error variables under flow budget, per-node error bounds and ranking-failure inequality. LP results agreed to seven decimal places with the fast exact budget.
- Four Python unit tests succeeded locally with zero failures. CI repeats these tests. The mathematical theorem is not inferred from the finite tests.

Single-run synthetic scaling example on local CPython (not a statistical benchmark):

| n | m | elapsed seconds | exact minimum H |
|---:|---:|---:|---:|
| 1,000 | 4,000 | 0.010875 | 8 |
| 10,000 | 40,000 | 0.124147 | 8 |
| 50,000 | 200,000 | 0.690674 | 8 |

These data demonstrate one test environment and synthetic configuration only, not a performance guarantee on real workloads.

## 7. Literature comparison and limits

The notion of robustness radius and ranking robustness is established prior work, and orthogonal range maxima and budgeted adversarial allocation are known optimization/data-structure tools:

- D. Bertsimas and M. Sim, *The Price of Robustness*, Operations Research 52(1), 2004, https://doi.org/10.1287/opre.1030.0065 .
- M. Benzi and N. Guglielmi, *Changing the ranking in eigenvector centrality of a weighted graph by small perturbations*, Mathematics of Computation (electronically published 2025), https://doi.org/10.1090/mcom/4149 . Their robustness radius concerns perturbing adjacency weights and **recomputing eigenvector centrality**, not exogenous scores changed through independent edge transfers and node measurement errors.
- M. Goerigk and S. Lendl, *Robust Combinatorial Optimization with Locally Budgeted Uncertainty*, Open Journal of Mathematical Optimization (2021), https://doi.org/10.5802/ojmo.5 .
- H. Oyarhoseini, J. Lin and A.-H. Karimi, *A Unified Perturbation Framework for Analyzing Leaderboard Stability and Manipulation*, arXiv:2605.15761 (2026), https://arxiv.org/abs/2605.15761 . The work uses pairwise-comparison perturbations and influence approximations, unlike the exact signed-error/one-way-transfer model.

**Novelty verdict: UNCONFIRMED.** A targeted search did not establish an exact prior match for these two offline sweeps, but it also cannot demonstrate priority, especially because a general support-function or dominance-query theorem may subsume the result. The separate-budget mathematics is a specialization built from known components; no claim of first discovery, peer review, journal acceptance or DOI is warranted.

**Falsifiability and limitations:** The theorem excludes multiarcs, intermediate flow conservation, correlated errors, post-transfer score nonnegativity constraints, and graph-ranking scores recomputed after graph edits. Code accepts integer/Fraction data only and is not a floating-point verified decision procedure. The O(m+n log n) claim is in arithmetic/comparison operations, not bit complexity for arbitrarily large integers or rationals. Real-world datasets meeting the model remain unvalidated. We actively invite reproducible counterexamples and exact prior-art citations via [review issue #1](https://github.com/sonii-shivansh/edgeflow-topk/issues/1).
