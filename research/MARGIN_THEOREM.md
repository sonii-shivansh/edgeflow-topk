# An exact worst-case top-k separation margin

**Research status:** Self-contained deterministic proof (AI-assisted). This is a quantitative extension of the existing EdgeFlow model. **Not independently peer reviewed; mathematical priority/novelty unconfirmed.**

## 1. Definition

Use precisely the model in [PROOF.md](PROOF.md): a finite simple undirected graph G=(V,E), initial real vertex scores s, nonnegative finite capacities c_e, signed independent edge transfers satisfying |f_e|<=c_e and sum_e |f_e|<=B, and an original top-k set T with 1<=k<|V|.

Define the **global worst-case separation margin**

$$
\rho(B):=\min_{\text{feasible }f}
\min_{\substack{i\in T\\j\notin T}}
\left(s'_i(f)-s'_j(f)\right).
$$

This number is finite because the graph and feasible transfer set are bounded. It can be positive, zero or negative. Unlike the previous yes/no decision, rho measures the **sharp guaranteed separation** of T from outsiders.

Let d_v be the sum of capacities incident to vertex v, c_ij the capacity of the edge {i,j} or zero if no such edge, and

$$
\Gamma_{ij}=2\min(c_{ij},B)+
\min(d_i+d_j-2c_{ij},(B-c_{ij})_+).
$$

## 2. Quantitative theorem

**Theorem.** The exact worst-case separation is

$$
\rho(B)=\min_{\substack{i\in T\\j\notin T}}
(s_i-s_j-\Gamma_{ij}).
$$

Define baseline L_ij=min(B,d_i+d_j) and the top-vs-outsider crossing-edge set

$$
\delta(T)=\{\{i,j\}\in E:i\in T,\ j\notin T\}.
$$

Let

$$
\rho_0:=\min_{\substack{i\in T\\j\notin T}}
(s_i-s_j-L_{ij}),
\qquad
\rho_E:=\min_{\substack{\{i,j\}\in\delta(T)\\i\in T}}
(s_i-s_j-\Gamma_{ij}),
$$

with rho_E=+infinity if the crossing-edge set is empty.

Then

$$
\boxed{\rho(B)=\min(\rho_0,\rho_E).}
$$

The value rho(B) and a pair (i,j) at which this value is attained can both be computed in O(m+n log n) time and O(m+n) space. A signed transfer vector attaining the worst-case difference for this pair can be constructed in an additional O(m) time.

**Consequences.**
- rho(B)>0 precisely when the original T is strictly robust;
- rho(B)=0 precisely when there exists a feasible flow producing a boundary tie but none producing a strict reversal;
- rho(B)<0 precisely when at least one feasible flow places an outsider strictly above an original insider;
- every feasible flow maintains every pairwise separation at least rho(B), and at least one feasible flow attains equality for some pair.

## 3. Complete proof

**Step 1: swap finite pair minimum with flow minimum.**

Let P={(i,j):i in T,j not in T}. This finite set is nonempty since 1<=k<n. For arbitrary real-valued functions h_p(f), the infimum over a product set satisfies

$$
\inf_{f}\min_{p\in P}h_p(f)=\min_{p\in P}\inf_fh_p(f).
$$

To justify both directions without omission: For each f and each p, h_p(f)>=inf_g h_p(g), hence min_p h_p(f)>=min_p inf_g h_p(g), so the left side is at least the right side. Conversely, for each p and every epsilon>0 there exists f_p with h_p(f_p)<inf_f h_p(f)+epsilon; using this particular f_p in the left-hand infimum implies LHS <= inf_f h_p(f)+epsilon. This holds for all p and all positive epsilon, so LHS <= min_p inf_f h_p(f). Thus equality holds. In our model the feasible set is compact and all h_p are continuous, so all infima are attained minima.

Set h_(i,j)(f)=s'_i(f)-s'_j(f). The exact pairwise perturbation theorem in PROOF.md shows

$$
\min_{\text{feasible }f}(s'_i(f)-s'_j(f))
=s_i-s_j-\Gamma_{ij}.
$$

Therefore rho is the minimum of these exact pairwise expressions.

**Step 2: separate nonedges and crossing edges.**

Lemma 2 in PROOF.md establishes Gamma_ij>=L_ij for all pairs, with equality for nonadjacent pairs. Define a_ij=s_i-s_j-L_ij and e_ij=s_i-s_j-Gamma_ij. For all crossing pairs, a_ij>=e_ij. For nonadjacent crossing pairs, a_ij=e_ij.

Let E_T be the set of crossing pairs joined by an edge, and N_T the nonadjacent crossing pairs. We have

$$
\min(\min_{p\in P}a_p,\min_{p\in E_T}e_p)
=\min(\min_{p\in N_T}a_p,\min_{p\in E_T}a_p,\min_{p\in E_T}e_p).
$$

For each p in E_T, e_p<=a_p, so removing the terms a_p for p in E_T does not change the minimum. For p in N_T, a_p=e_p. Consequently the right-hand side is

$$
\min(\min_{p\in N_T}e_p,\min_{p\in E_T}e_p)
=\min_{p\in P}e_p=\rho(B).
$$

Empty inner sets are assigned the value +infinity, so this argument covers graphs with no crossing edges or all crossing pairs adjacent.

**Step 3: compute rho_0 in near-linear time.**

Sort the outsiders by increasing d_j. For each i in T, write

$$
M_i=\max_{j\notin T}[s_j+\min(B,d_i+d_j)].
$$

Then the minimum baseline separation for this fixed i is s_i-M_i. The prefix/suffix maxima construction in PROOF.md computes each M_i in O(log n) time after O(n log n) sorting and O(n) preprocessing. Taking the minimum of s_i-M_i over i in T gives rho_0. The crossing-edge correction rho_E is obtained by scanning edges and applying Gamma to each crossing edge in constant time per edge. Therefore O(m+n log n) time and O(m+n) space suffice.

**Step 4: construct a worst-case witness.**

Retain the pair (i,j) minimizing the combined baseline and crossing-edge expressions. If this pair is a crossing edge, its selected value is its exact e_ij. If its value instead originates from the baseline and is attained at an adjacent pair with e_ij<a_ij, the crossing-edge scan would have produced a strictly smaller value, contradicting minimality. Therefore a baseline-selected pair also has e_ij=a_ij, and in every case the returned pair attains rho(B) in the exact pairwise formula.

The constructive flow from Lemma 1 of PROOF.md allocates absolute transfer budget first to the direct edge (coefficient 2), then to other edges incident to either endpoint (coefficient 1), using favorable signs. It is feasible and achieves the pairwise maximum Gamma_ij. Hence the corresponding updated separation equals rho(B). This takes at most one scan of all edges and O(m) time.

All four steps together prove the theorem and the consequences.

## 4. Evidence and limitations

The quantitative algorithm is implemented in the function topk_robustness_margin in [../edge_transfer_topk.py](../edge_transfer_topk.py). The new test suite [../tests/test_exact_margin.py](../tests/test_exact_margin.py) checks 2,600 random integer graphs against a direct all-pairs calculation, 420 additional exact-rational signed-flow enumerations independent of the Gamma formula, and several very-large-integer/tie edge cases. It also verifies constructed witness flows.

These tests are corroboration, not proof; the proof above gives the universal mathematical argument. The result assumes exact real arithmetic, independently signed flows, nonnegative finite capacities, and a simple graph. Arbitrary floating-point inputs near equality can lead to incorrect decisions. Nothing in this note establishes novelty in the literature.
