"""Print rational derivative bounds and exact polynomial root counts for W3."""
from fractions import Fraction as Q
from math import comb
import json


def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:
        p.pop()
    return p


def add(p,q):
    return trim([(p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q)))])


def mul(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):
            out[i+j]+=x*y
    return trim(out)


def scale(p,s):
    return trim([s*x for x in p])


def deriv(p):
    return trim([i*p[i] for i in range(1,len(p))])


def evaluate(p,x):
    out=Q(0)
    for c in reversed(p):
        out=out*x+c
    return out


def remainder(p,q):
    p=trim(p)
    while len(p)>=len(q) and p!=[0]:
        degree=len(p)-len(q)
        factor=p[-1]/q[-1]
        p=add(p,[Q(0)]*degree+scale(q,-factor))
    return p


def sturm_count(p,lo,hi):
    seq=[trim(p),deriv(p)]
    while seq[-1] != [0]:
        rr=scale(remainder(seq[-2],seq[-1]),-1)
        if rr==[0]:
            break
        seq.append(rr)
    def changes(x):
        vals=[evaluate(s,x) for s in seq]
        signs=[1 if v>0 else -1 for v in vals if v]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    return changes(lo)-changes(hi)


def bernstein(p,lo,hi):
    n=len(p)-1
    # Power coefficients in t after x=lo+(hi-lo)t.
    power=[sum(p[j]*comb(j,k)*lo**(j-k)*(hi-lo)**k for j in range(k,n+1)) for k in range(n+1)]
    return [sum(power[k]*Q(comb(i,k),comb(n,k)) for k in range(i+1)) for i in range(n+1)]


def rational_monotonicity(c,beta,a,lo,hi,n):
    def D(r):
        return (r-1)**2/(2*r)
    def tau(r):
        return (2*c*r-Q(3,4))/(20*r-r*r-1)
    out=[]
    for i in range(n):
        l=lo+(hi-lo)*i/n; u=lo+(hi-lo)*(i+1)/n
        dp=(1-1/l**2)/2
        tp=(2*c*u*u-Q(3,2)*u+15-2*c)/(20*l-l*l-1)**2
        lp=beta/(beta+(1-2*beta)*(1-tau(u)))**2
        bound=dp*(1-tau(u))-(D(u)+2*a*lp)*tp
        out.append((bound,l,u))
    v,l,u=min(out)
    return dict(min_bound=float(v),interval=[float(l),float(u)],partitions=n,
                exact_lower_bound=str(v))


if __name__=='__main__':
    print('benchmark_phi_monotonicity_a_041',json.dumps(rational_monotonicity(Q(6),Q('0.294655'),Q('.41'),Q('1.2'),Q('3.6'),240)))
    print('solver_D_full_phi_monotonicity',json.dumps(rational_monotonicity(Q(5),Q('0.294655'),Q('.1'),Q('1.4'),Q('2.05'),65)))
    # Solver B example: J=(r-1)^2(-4r^2+42r-1)/(8r(20r-r^2-1)).
    jn=mul([Q(1),Q(-2),Q(1)],[Q(-1),Q(42),Q(-4)])
    jd=[Q(0),Q(-8),Q(160),Q(-8)]
    jder=add(mul(deriv(jn),jd),scale(mul(jn,deriv(jd)),-1))
    print('solver_B_J_derivative_polynomial',json.dumps([str(x) for x in jder]))
    print('solver_B_J_derivative_Bernstein_min',float(min(bernstein(jder,Q('1.2'),Q(5)))))
    # lambda_E=3(r^2-r-1/2)/(102r-7r^2-4).
    ln=[Q(-3,2),Q(-3),Q(3)]
    ld=[Q(-4),Q(102),Q(-7)]
    # phi=J-.02-4 lambda_E; phi*=1.25J-.04-4lambda_E on J>.08.
    pold=add(add(mul(jn,ld),scale(mul(jd,ld),Q(-1,50))),scale(mul(ln,jd),-4))
    pfull=add(add(scale(mul(jn,ld),Q(5,4)),scale(mul(jd,ld),Q(-1,25))),scale(mul(ln,jd),-4))
    for label,p in [('phi',pold),('phi_star_full',pfull)]:
        print('solver_B_'+label+'_polynomial',json.dumps([str(x) for x in p]))
        print('solver_B_'+label+'_roots_1_2_to_5',sturm_count(p,Q('1.2'),Q(5)))
    psol=[Q(-441),Q(595),Q(-214),Q(20)]
    print('solver_A_phi_polynomial_roots',sturm_count(psol,Q('1.1'),Q('2.99')))
