# Exact near-linear critical transfer budget (fixed error budget)

**Research status: self-contained model-conditional proof and finite numerical verification; priority unconfirmed; not independently peer-reviewed.**

## 1. Definition and assumptions

Use the directed dual-budget uncertainty model in [DIRECTIONAL_DUAL_BUDGET.md](DIRECTIONAL_DUAL_BUDGET.md): a finite simple directed graph with initial scores s_v, directed arc capacities c_uv >= 0, **nonnegative one-way** arc flows f_uv, each bounded by c_uv and jointly by sum(f_uv) <= F, and independent signed measurement errors e_v with |e_v| <= a_v and sum |e_v| <= H. All scores, arc capacities, error bounds and H are **integers** in this theorem, with scores allowed to be negative. F is allowed to be any nonnegative real number. Original top-k set T uses fixed deterministic tie-breaking.

Let

$$
D_i^{out} = \sum_{(i,v)\in A}c_{iv}, \qquad
D_j^{in} = \sum_{(v,j)\in A}c_{vj}.
$$

Define rho(F,H) as the exact minimum (under every feasible joint flow/error choice) of the top-k-vs-outsider separation s'_i-s'_j, as in the linked proof. We fix H and seek the **first failure budget**

$$
F_* = \inf\{F\ge 0: \rho(F,H)\le 0\}.
$$

If this set is empty, put F_*=+infinity. A possible boundary tie is already a failure of *strict* robustness.

## 2. Pairwise inversion

For each insider i and outsider j, write

$$
\Delta_{ij}
=s_i-s_j-\min(H,a_i+a_j).
$$

This is the original gap after the *worst* allowable measurement error, but before any directed flow.

The exact maximal remaining flow damage is

$$
g_{ij}(F)
=2\min(c_{ij},F)
+\min(D_i^{out}+D_j^{in}-2c_{ij},(F-c_{ij})_+)
$$

from the directed dual-budget pairwise lemma. Here c_ij=0 if no forward arc i->j; a reverse arc j->i alone does not count as a forward arc.

**Lemma 1 (pairwise critical budget).** If Delta_ij<=0, the pair fails strict separation already at F=0. If Delta_ij > D_i^{out}+D_j^{in}, no amount of feasible flow can bring that pair to a tie. In every remaining case (0<Delta_ij<=D_i^{out}+D_j^{in}), the **minimum** flow budget causing a tie or reversal is

$$
F^*_{ij}=\begin{cases}
\Delta_{ij}/2, & \Delta_{ij}\le 2c_{ij},\\
\Delta_{ij}-c_{ij}, & \Delta_{ij}>2c_{ij}.
\end{cases}
$$

*Proof.* Put c=c_ij, S=Dout_i+Din_j-2c >=0. For 0<=F<=c the first part of g(F) equals 2F and the second part zero, giving g(F)=2F. For c<=F<=c+S, the direct arc is saturated and other favorable arcs consume the remaining budget, giving g(F)=2c+(F-c)=F+c. Beyond c+S every favorable arc is saturated, so g(F)=2c+S=Dout_i+Din_j. These expressions agree at both breakpoints and are nondecreasing with F.

A pair loses strict separation precisely when its original gap is no greater than measurement damage plus g(F), equivalently g(F)>=Delta. For Delta<=0 this occurs at F=0. For Delta>2c+S the maximum g(infinity)=2c+S is insufficient; failure never occurs. For 0<Delta<=2c, solving 2F=Delta on the first linear segment gives the first feasible F=Delta/2. Otherwise 2c<Delta<=2c+S and solving F+c=Delta on the second segment gives the first feasible F=Delta-c. Because g is nondecreasing and the expressions were obtained on the relevant segments, no smaller F causes failure. QED.

**Corollary 1 (half-integrality).** Under the integer input assumptions, F_* is either zero, a nonnegative integer, a half-integer, or +infinity.

*Proof.* The global failure event is the union over finitely many insider-outsider pairwise failure events. Its minimum critical budget, when finite, equals min_{i in T,j outside} F^*_{ij}. Each Delta and c are integers, so each finite pair threshold in Lemma 1 is Delta/2 or Delta-c or zero: an integer or half-integer. The minimum of finitely many such values has the same property. QED.

## 3. Separate the cheap non-forward pairs and exceptional arcs

Assume the initial joint error budget H alone cannot cause a tie: rho(0,H)>0. Then Delta_ij>0 for *every* crossing pair, since rho(0,H)=min_{i,j}Delta_ij.

For a pair with no forward arc, c_ij=0, so Lemma 1 says its first failure budget is precisely Delta_ij if

$$
\Delta_{ij}\le D_i^{out}+D_j^{in},
$$

and +infinity otherwise.

Define the **baseline threshold** for every pair by pretending its direct forward arc is absent, but retaining the actual capacity degrees:

$$
B_{ij} =
\begin{cases}
\Delta_{ij}, & \Delta_{ij}\le D_i^{out}+D_j^{in},\\
+\infty,&\text{otherwise}.
\end{cases}
$$

For non-forward pairs, B_ij is exact. For forward pairs, B_ij is no smaller than the exact threshold F^*_{ij} when that threshold is finite: the sharp flow damage with a forward arc is at least min(F,Dout_i+Din_j), and both maximal damages equal Dout_i+Din_j. Thus, B_ij is either infinite for the same genuinely unreachable pair, or a conservative larger budget.

Let A_T be the set of forward arcs from original top-k insiders to outsiders.

**Lemma 2 (exact sparse threshold reduction).**

$$
\boxed{
F_*=\min\left(
\min_{\substack{i\in T\\j\notin T}}B_{ij},\
\min_{(i,j)\in A_T}F^*_{ij}
\right).
}
$$

*Proof.* Every non-forward pair has the exact threshold B_ij; every forward pair has its exact threshold represented in the second minimum. For each forward pair its baseline B_ij is no smaller than the exact threshold, so adding that baseline value to the pool cannot lower the minimum. Therefore the right-hand expression equals the minimum of exact F^*_{ij} over all crossing pairs, which by definition is F_*. QED.

Use +infinity for empty finite minimum sets. Thus computing all baseline thresholds quickly, plus scanning only forward crossing arcs, solves the full problem.

## 4. Two offline 2D dominance queries

For a fixed original insider i, we need to find the **smallest** positive Delta_ij among outsiders j satisfying

$$
\Delta_{ij}\le D_i^{out}+D_j^{in}.
$$

Split outsider j by whether its error capacity participates in the unsaturated or saturated part of min(H,a_i+a_j).

**Case U: a_j<=H-a_i.** Here min(H,a_i+a_j)=a_i+a_j. Put

$$
x_j=s_j+a_j,\quad y_j=s_j+a_j+D_j^{in},\quad
t_i=s_i-a_i-D_i^{out}.
$$

Then Delta_ij=(s_i-a_i)-x_j, and the feasibility condition Delta_ij<=Dout_i+Din_j is equivalent to y_j>=t_i. The exact baseline minimum for insider i in this case is obtained by **maximizing x_j** under both inequalities

$$
a_j\le H-a_i,\qquad y_j\ge t_i.
$$

**Case S: a_j>H-a_i.** The error budget is saturated and min(H,a_i+a_j)=H. Put

$$
x_j=s_j,\quad y_j=s_j+D_j^{in},\quad
t_i=s_i-H-D_i^{out}.
$$

Again Delta_ij=(s_i-H)-x_j. The exact minimum is obtained by **maximizing x_j** subject to

$$
a_j>H-a_i,\qquad y_j\ge t_i.
$$

Because all Delta_ij>0 by the initial robustness assumption, no further positive-gap constraint is required in either case.

**Lemma 3 (offline dominance maxima).** Both families of outsider maxima for all insiders can be evaluated in O(n log n) arithmetic/comparison time and O(n) auxiliary memory.

*Proof.* Fix one case U or S. Sort all outsider points in nonincreasing order of their y_j coordinates. Sort insider queries in nonincreasing order of their y-threshold t_i. Sweep queries from highest to lowest threshold; before evaluating a query insert every outsider with y_j>=t_i not already inserted. Since thresholds move downward, each outsider is inserted at most once and every inserted outsider satisfies the current y requirement. An outsider not yet inserted fails that requirement.

Compress outsider error capacities a_j to sorted distinct ranks 1,...,q. Maintain a Fenwick tree that stores the maximum pair (x_j,j) of inserted points for a prefix of ranks, with x as the primary comparison key. In case U, a_j<=H-a_i corresponds to a prefix ending at bisect_right(error_coords,H-a_i). In case S, a_j>H-a_i corresponds to a suffix of original ranks. Reverse the compressed error-rank order; this strict suffix becomes a prefix of length q-bisect_right(error_coords,H-a_i). Thus each query consists of exactly one Fenwick prefix maximum, and the returned point satisfies both inequalities and maximizes the objective among all eligible outsiders.

Each insertion/query uses O(log n) Fenwick operations. Both sorts and coordinate compression cost O(n log n). At most n insertions and n queries occur per case. The two cases are a constant number, so O(n log n) total time and O(n) extra space suffice. QED.

## 5. Main theorem

**Theorem (exact near-linear failure radius).** Under the integer input assumptions, the minimum transfer budget F_* at which strict original top-k separation can fail under fixed measurement-error budget H is computable exactly in

$$
\boxed{O(m+n\log n)\ \text{time},\qquad O(m+n)\ \text{space}}
$$

in the arithmetic/comparison model. If finite, F_* is an integer or half-integer and the algorithm returns an insider-outsider pair for which a feasible error/flow witness attains boundary failure. If no flow budget can cause failure, the algorithm returns +infinity (represented by None in code).

*Proof.* Compute capacity degrees Dout and Din and identify the original insiders, in O(m+n log n). Evaluate rho(0,H) using the previous exact fixed-budget algorithm in O(m+n log n). If it is nonpositive, F_*=0 and its returned crossing pair has a feasible witness. Otherwise all Delta_ij>0.

For positive Delta, Lemma 2 reduces the critical budget to the minimum baseline threshold and the minimum exact forward-arc threshold. Lemma 3 computes the baseline threshold minima for all insiders with two offline sweeps in O(n log n). Scan the at most m forward crossing arcs and compute their exact threshold using the constant-time formula of Lemma 1. Take the smallest of the baseline and arc values, or +infinity if neither produces finite failure. This matches F_* by Lemma 2.

For a selected minimum pair, choose the favorable directed transfers and signed measurement errors as in the constructive witness in DIRECTIONAL_DUAL_BUDGET.md, at budgets (F_*,H). If the selected pair came from a forward arc, its value is exact. If it came from the baseline but had a lower true forward-arc critical budget, the arc scan would have produced a smaller global answer; contradiction. Thus a baseline-selected pair is also an attaining pair. For its actual uncertainty model, a boundary tie or reversal is feasible at F_*; for any smaller F, no crossing pair can reach a tie by definition of the global minimum. The total running time and space bounds follow from the above steps. Half-integrality is Corollary 1. QED.

### Why integer inputs matter

The pairwise inversion formula applies with general real data, but the efficient implementation deliberately restricts scores, capacities, error caps and H to Python integers so exact comparisons can be made and the returned finite budget has a denominator at most 2. This is an **arithmetic-operation** complexity bound, not an unbounded-integer bit-complexity guarantee.

## 6. Safety-region geometry: a nonconvex example

For s=[3,0], one directed arc 0->1 of capacity 1, and node error caps a=[1,1] with k=1, the exact worst-case gap at budgets (F,H) is

$$
\rho(F,H)=3-2\min(1,F)-\min(2,H).
$$

The points (F,H)=(2,0) and (0,2) have rho=1 and hence are **both strictly robust**. Their midpoint (1,1) has rho=0 and hence is **not strictly robust**. Therefore the set of safe budget pairs {(F,H):rho(F,H)>0} is **not convex in general**, even for a two-vertex graph.

The safe region is nevertheless downward closed in both coordinates: increasing either budget enlarges the adversary's feasible set and can only decrease (or preserve) the worst-case margin. This observation does not imply convexity and demonstrates why taking convex hulls of certified safe budget pairs can be unsound.

## 7. Verification results and failed expectation

Deterministic-seed local execution (12 Nov 2026):

- 2,000 random simple directed integer graphs checked against an independently evaluated **all-pairs inverted threshold formula**: **2,000 agreements**.
- 120 tiny graphs independently checked by exhaustive enumeration of actual half-unit directed transfers and integer signed errors, not by the pairwise formula or the Fenwick sweep: **120 agreements**.
- Nine deterministic edge/tie/very-large-integer scenarios, and an explicit nonconvex-safe-region example.
- All four test methods passed after one *test expectation* correction. Initially a hand-written test wrongly asserted that a score gap of 3 could be overcome by an arc of capacity 1 without measurement error; maximal damage is only 2, so the correct critical budget is +infinity. The theorem and implementation were unchanged.

Synthetic one-run scaling illustration on a local Python environment with approximately 4n directed arcs: n=1000,m=4000 time 0.07665s; n=10000,m=40000 time 0.13405s; n=50000,m=200000 time 0.62139s. These are **single-run illustrative** numbers, not a controlled comparison or evidence of novelty.

## 8. Novelty investigation and limitations

After proving and testing this result, a targeted public-literature search located:

- **Gogoi (2026)**, *Exact Robustness Radius of Positional Scoring Rules via Greedy Allocation*, SSRN posted 8 July 2026, https://papers.ssrn.com/sol3/Delivery.cfm/6926060.pdf?abstractid=6926060&mirid=1 . An exact voting/ranking robustness radius is an existing concept; the model involves voter-ranking changes rather than directed graph score transfers.
- **Oyarhoseini, Lin and Karimi (2026)**, *A Unified Perturbation Framework for Analyzing Leaderboard Stability and Manipulation*, arXiv:2605.15761, https://arxiv.org/abs/2605.15761 . This studies minimal leaderboard action budgets using approximate influence guidance for match-edit perturbations, different from exact signed measurement/one-way directed flow budgets.
- **Certified top-k robustness** of neural rankings predates this work, e.g. Wu et al. (2022), https://doi.org/10.1145/3511808.3557256 . Its perturbation model and verification differ from this graph transfer model.
- More general minimum adversarial perturbation (robustness radius) methods using an exact or sound robustness verifier plus bisection are already common. This result's potential contribution, if any, is the **single near-linear nonparametric exact threshold computation** specialized to this model, not the general idea of a stability radius or range-max queries.

Search families: "robust top-k ranking minimum adversarial budget", "minimum budget to change top k ranking robust optimization", "graph edge transfer top-k stability radius", "exact top-k rank robustness radius", and target searches of arXiv, SSRN and robustness literature.

**Novelty status: UNCONFIRMED.** We did not establish that the two-dominance-query reduction has not appeared before. Generic half-integrality, budget inversion, and offline 2D range maximum are simple known ingredients. This research note does not claim a world-first invention, peer-reviewed scientific discovery, DOI, or external referee approval.

Falsification: any input obeying all listed assumptions whose first attainable boundary tie occurs at a different F than the algorithm returns, or a family invalidating the stated asymptotic arithmetic complexity. A published equivalent predecessor would defeat any originality claim but need not invalidate the theorem.
