"""Independent validation for minimum node-error budget at fixed flow budget.

Oracles: direct all-pairs threshold, exhaustive exact signed errors/flows,
and independently formulated SciPy minimization LP. No reuse of fast sweep
inside the independent oracles. All seeds and instance sizes are fixed.
"""
import random
import unittest
from fractions import Fraction
from itertools import product

from experimental.critical_error_budget import critical_error_budget
from experimental.directional_dual_budget import (
    topk_dual_budget_margin, witness_for_pair, adjusted_scores
)


def all_pairs_oracle(scores, arcs, caps, F, k):
    n=len(scores)
    top=sorted(range(n),key=lambda v:(-scores[v],v))[:k]
    outsiders=[j for j in range(n) if j not in top]
    Dout=[0]*n; Din=[0]*n; c={}
    for u,v,capacity in arcs:
        Dout[u]+=capacity; Din[v]+=capacity; c[u,v]=capacity
    best=None
    for i in top:
        for j in outsiders:
            direct=c.get((i,j),0)
            damage=(2*min(direct,F)
                    +min(Dout[i]+Din[j]-2*direct,max(0,F-direct)))
            delta=scores[i]-scores[j]-damage
            if delta<=0:return 0
            if delta<=caps[i]+caps[j]:
                if best is None or delta<best:best=delta
    return best


def exact_perturbation_oracle(scores, arcs, caps, F, k, step=Fraction(1,2)):
    n=len(scores)
    top=sorted(range(n),key=lambda v:(-scores[v],v))[:k]
    outsiders=[j for j in range(n) if j not in top]
    flow_ranges=[range(int(capacity/step)+1) for u,v,capacity in arcs]
    error_ranges=[range(-int(c/step),int(c/step)+1) for c in caps]
    best=None
    for flow_digits in product(*flow_ranges):
        flow=[t*step for t in flow_digits]
        if sum(flow)>F:continue
        for error_digits in product(*error_ranges):
            error=[t*step for t in error_digits]
            h=sum(abs(x) for x in error)
            if best is not None and h>=best:continue
            updated=adjusted_scores(scores,arcs,flow,error)
            if any(updated[i]<=updated[j] for i in top for j in outsiders):
                best=h
    return best


def lp_oracle_for_pair(i,j,scores,arcs,caps,F):
    from scipy.optimize import linprog
    n=len(scores);m=len(arcs)
    # [flow_m, positive_error_n, negative_error_n], objective L1 error
    objective=[0]*m+[1]*(2*n)
    constraints=[];rhs=[]
    for v in range(n):
        row=[0]*(m+2*n);row[m+v]=row[m+n+v]=1
        constraints.append(row);rhs.append(caps[v])
    constraints.append([1]*m+[0]*(2*n));rhs.append(F)
    # Require updated s_i-s_j<=0.
    row=[]
    for u,v,capacity in arcs:
        alpha=int(u==i)+int(v==j)-int(v==i)-int(u==j)
        row.append(-alpha)
    row.extend(int(v==i)-int(v==j) for v in range(n))
    row.extend(-int(v==i)+int(v==j) for v in range(n))
    constraints.append(row);rhs.append(-(scores[i]-scores[j]))
    bounds=[(0,c) for u,v,c in arcs]+[(0,None)]*(2*n)
    result=linprog(objective,A_ub=constraints,b_ub=rhs,
                   bounds=bounds,method="highs")
    if result.status==2:return None
    assert result.success,result.message
    return result.fun


class CriticalErrorBudgetTests(unittest.TestCase):
    def test_nine_deterministic_and_fraction_cases(self):
        cases=[
            ([10,7],[(0,1,2)],[2,2],0,1,3),
            ([10,7],[(0,1,2)],[2,2],2,1,0),
            ([10,7],[(1,0,2)],[1,1],2,1,None),
            ([5,5],[],[0,0],0,1,0),
            ([2,0],[(0,1,1)],[1,1],0,1,2),
            ([2,0],[(0,1,1)],[0,0],1,1,0),
            ([10**100+1,10**100],[],[1,0],0,1,1),
            ([10,0],[],[2,3],0,1,None),
            ([1,0],[(0,1,Fraction(1,3))],[1,1],Fraction(1,3),1,Fraction(1,3)),
        ]
        for scores,arcs,a,F,k,expected in cases:
            self.assertEqual(
                critical_error_budget(scores,arcs,a,F,k)[0],expected)

    def test_2000_random_pairwise_checks(self):
        rng=random.Random(121126)
        for trial in range(2000):
            n=rng.randrange(2,11)
            arcs=[(i,j,rng.randrange(5))
                  for i in range(n) for j in range(n)
                  if i!=j and rng.random()<0.24]
            scores=[rng.randrange(-12,24) for _ in range(n)]
            caps=[rng.randrange(6) for _ in range(n)]
            F=rng.randrange(15);k=rng.randrange(1,n)
            expected=all_pairs_oracle(scores,arcs,caps,F,k)
            actual,pair,source=critical_error_budget(scores,arcs,caps,F,k)
            self.assertEqual(actual,expected,(trial,scores,arcs,caps,F,k,source))
            if actual is not None:
                if actual>0:
                    just_below=topk_dual_budget_margin(
                        scores,arcs,caps,F,actual-Fraction(1,2),k)[0]
                    self.assertGreater(just_below,0)
                at=topk_dual_budget_margin(scores,arcs,caps,F,actual,k)[0]
                self.assertLessEqual(at,0)
                f,e=witness_for_pair(n,*pair,arcs,caps,F,actual)
                updated=adjusted_scores(scores,arcs,f,e)
                self.assertLessEqual(updated[pair[0]],updated[pair[1]])
                self.assertLessEqual(sum(f),F)
                self.assertLessEqual(sum(abs(x) for x in e),actual)

    def test_150_independent_fraction_grid_cases(self):
        rng=random.Random(121226);half=Fraction(1,2)
        for trial in range(150):
            n=rng.randrange(2,5);arcs=[]
            for i in range(n):
                for j in range(n):
                    if i!=j and len(arcs)<3 and rng.random()<0.25:
                        arcs.append((i,j,rng.randrange(3)*half))
            scores=[rng.randrange(-2,10)*half for _ in range(n)]
            a=[rng.randrange(3)*half for _ in range(n)]
            F=rng.randrange(5)*half;k=rng.randrange(1,n)
            expected=exact_perturbation_oracle(
                scores,arcs,a,F,k,half)
            actual=critical_error_budget(scores,arcs,a,F,k)[0]
            self.assertEqual(actual,expected,(trial,scores,arcs,a,F,k))

    def test_110_independent_lp_pairs(self):
        rng=random.Random(240126);count=0
        for trial in range(35):
            n=rng.randrange(2,7)
            arcs=[(i,j,rng.randrange(4))
                  for i in range(n) for j in range(n)
                  if i!=j and rng.random()<0.2]
            scores=[rng.randrange(15) for _ in range(n)]
            caps=[rng.randrange(4) for _ in range(n)]
            F=rng.randrange(10);k=rng.randrange(1,n)
            top=sorted(range(n),key=lambda v:(-scores[v],v))[:k]
            outside=[j for j in range(n) if j not in top]
            expected=None
            for i in top:
                for j in outside:
                    count+=1
                    lp=lp_oracle_for_pair(i,j,scores,arcs,caps,F)
                    if lp is not None and (expected is None or lp<expected):
                        expected=lp
            actual=critical_error_budget(scores,arcs,caps,F,k)[0]
            if expected is None:self.assertIsNone(actual)
            else:self.assertAlmostEqual(float(actual),expected,places=7)
        self.assertEqual(count,110)


if __name__=="__main__":
    unittest.main(verbosity=2)
