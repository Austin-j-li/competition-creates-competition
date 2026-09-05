#!/usr/bin/env python3
"""Computer-assisted existence proofs for selected pure asymmetric CCC equilibria.

Uses exact elementary antiderivatives with mpmath interval arithmetic (50 digits).
No truncated integrals or floating-point quadrature are used for certification.
Analytical ingredients documented in the feedback note:
  (i) low-signal trader's correctly-signed payoff is strictly concave;
 (ii) high-signal payoff derivative has Lipschitz constant
      2*Delta/b + Delta/b**2;
(iii) all wrong-signed trades are strictly dominated by zero.

An interval sign change establishes an exact root of the low-signal FOC. The
high-signal derivative is enclosed on a mesh for the whole root bracket, and the
Lipschitz constant covers every between-mesh deviation.
"""
from __future__ import annotations
import json
from pathlib import Path
import mpmath as mp

iv=mp.iv
iv.dps=50
I=iv.mpf

def mid(x): return (float(x.a)+float(x.b))/2

def lo(x): return float(x.a)

def hi(x): return float(x.b)

def atan(x): return iv.atan2(x,I(1))

def expit(x):return 1/(1+iv.exp(-x))

def primitives(r):
    p=I('.5');ell=I(1);h=I(10)
    return dict(t0=p*(1-p/r),tH=r/2+p*p/(2*r),tL=ell-(ell*ell-p*p)/(2*r),
                gH=h-r/2-p*p/(2*r),gL=(ell*ell-p*p)/(2*r),Delta=(r-ell)**2/(2*r))

def objects(r,v,s,sgn,at_low_candidate=False):
    """Enclose U(s), U'(s), F(s), entry; q_H=1 and q_L=-v."""
    u=I(1);b=I(2);rho=I('.25');k=I('.02');p=primitives(r);D=p['Delta']
    tau=(I(6)-p['gL'])/(p['gH']-p['gL'])
    xs=(b*iv.ln(tau/(1-tau))+u-v)/2
    mu_hi=expit((u+v)/b);mu_lo=1-mu_hi
    assert lo(tau)>0.5 and hi(tau)<lo(mu_hi)
    center=sgn*s;c=(u-v)/2
    cuts=[('left',-v),('entry',xs),('right',u)]
    if not at_low_candidate and not(sgn==1 and lo(s)==1. and hi(s)==1.):
        cuts.append(('center',center))
    cuts.sort(key=lambda item:mid(item[1]))
    for (_,x),(_,y) in zip(cuts[:-1],cuts[1:]):
        assert hi(x)<lo(y),f'Unresolved interval ordering: {x}, {y}'
    points=[(None,None)]+cuts+[(None,None)]
    F=I(0);Fp=I(0)
    for j in range(len(points)-1):
        left=points[j][1];right=points[j+1][1]
        if left is None: test=mid(right)-10
        elif right is None:test=mid(left)+10
        else:test=(mid(left)+mid(right))/2
        left_of_center=test<mid(center)
        e=rho if test<mid(xs) else I(1)
        if test<mid(-v):
            coeff=(1-mu_lo) if sgn==1 else mu_lo
            interior=False
        elif test>1.:
            coeff=(1-mu_hi) if sgn==1 else mu_hi
            interior=False
        else:interior=True
        if not interior:
            if left_of_center:
                val=I('.5')*((iv.exp((right-center)/b) if right is not None else I(0))-
                              (iv.exp((left-center)/b) if left is not None else I(0)))
            else:
                val=I('.5')*((iv.exp(-(left-center)/b) if left is not None else I(0))-
                              (iv.exp(-(right-center)/b) if right is not None else I(0)))
            part=e*D*coeff*val
        else:
            assert left is not None and right is not None
            tL=iv.exp((left-c)/b);tR=iv.exp((right-c)/b)
            if sgn==1 and left_of_center:
                primitive=lambda t:atan(t)
                fac=iv.exp((c-center)/b)/2
            elif sgn==1 and not left_of_center:
                primitive=lambda t:-1/t-atan(t)
                fac=iv.exp((center-c)/b)/2
            elif sgn==-1 and left_of_center:
                primitive=lambda t:t-atan(t)
                fac=iv.exp((c-center)/b)/2
            else:
                primitive=lambda t:atan(t)
                fac=iv.exp((center-c)/b)/2
            part=e*D*fac*(primitive(tR)-primitive(tL))
        F+=part
        Fp+=sgn*(-1 if left_of_center else 1)*part/b
    U=s*(F-k);Up=F+s*Fp-k
    # xs lies strictly between -v and u.
    alphaH=1-iv.exp((xs-u)/b)/2
    alphaL=iv.exp(-(xs+v)/b)/2
    E=rho+(1-rho)*(alphaH+alphaL)/2
    return U,Up,F,E

def bounds(x):return {'interval':str(x),'lower_display':lo(x),'upper_display':hi(x)}

def certify(r_string,vleft_string,vright_string,n=200):
    r=I(r_string);vl=I(vleft_string);vr=I(vright_string);v=I([vleft_string,vright_string])
    low_left=objects(r,vl,vl,-1,True)[1]
    low_right=objects(r,vr,vr,-1,True)[1]
    assert lo(low_left)>0 and hi(low_right)<0
    p=primitives(r)
    global_m=1/(1+iv.exp(I(1)))
    low_cost_margin=p['gL']+global_m*(p['gH']-p['gL'])-I(1)
    high_cost_prior_margin=I(6)-(p['gH']+p['gL'])/2
    assert lo(low_cost_margin)>0 and lo(high_cost_prior_margin)>0
    lip=2*p['Delta']/I(2)+p['Delta']/I(4)
    # Every s in [0,1] is at distance <= 1/(2*n) of this derivative mesh.
    vals=[]
    for j in range(n+1):
        s=I(j)/I(n)
        d=objects(r,v,s,1)[1]
        vals.append(d)
    minimum_lower=min(x.a for x in vals)
    global_lower=minimum_lower-lip/(2*n)
    assert lo(global_lower)>0
    # Independent analytical pooling condition at the same r.
    pooling_margin=I('.02')-I('.25')*p['Delta']/2
    assert lo(pooling_margin)>0
    rootpayoff,_,_,entry=objects(r,v,v,-1,True)
    hpayoff=objects(r,v,I(1),1)[0]
    return dict(r=r_string,low_order_magnitude_bracket=[vleft_string,vright_string],
       FOC_at_left=bounds(low_left),FOC_at_right=bounds(low_right),
       high_derivative_mesh_min_lower=str(minimum_lower),
       high_global_derivative_lower=bounds(global_lower),
       high_derivative_mesh_intervals=n,
       derivative_Lipschitz_bound=bounds(lip),
       pooling_margin=bounds(pooling_margin),low_cost_margin=bounds(low_cost_margin),
       high_cost_prior_margin=bounds(high_cost_prior_margin),entry=bounds(entry),
       low_trader_payoff=bounds(rootpayoff),high_trader_payoff=bounds(hpayoff))

def main():
    # Proposed root brackets from exploratory floating-point calculations;
    # every proof test below uses interval arithmetic, not those root estimates.
    results=[certify('1.55','0.46031618','0.46031620'),
             certify('1.6','0.70747537','0.70747539'),
             certify('1.65','0.90333198','0.90333201')]
    assert results[0]['entry']['upper_display']<results[1]['entry']['lower_display']
    assert results[1]['entry']['upper_display']<results[2]['entry']['lower_display']
    out=Path(__file__).resolve().parent/'results';out.mkdir(exist_ok=True)
    (out/'asymmetric_interval_certificates.json').write_text(json.dumps(dict(mpmath=mp.__version__,
       interval_decimal_precision=iv.dps,results=results),indent=2))
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()
