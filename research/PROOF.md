# Exact top-k stability under budgeted graph-edge transfers

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
