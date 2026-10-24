"""Independent finite-support equilibrium calculation through the flow interface.

Every candidate fixes its prices and entry probabilities before all six order
payoffs are evaluated. Exact slots use rational arithmetic. Calibration B uses
rational intervals from xp1_numbers. Scripts print calculations, not assertions.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

from xp1_numbers import I, D, tau, J, auction, exp_one, bounds, rho, fee

HERE=Path(__file__).resolve().parent


def sign(x):
    if isinstance(x,I):
        if x.lo>0:
            return 1
        if x.hi<0:
            return -1
        if x.lo==x.hi==0:
            return 0
        return None
    return (x>0)-(x<0)


def le(a,b):
    return sign(a-b) in (-1,0)


def lt(a,b):
    return sign(a-b)==-1


def post(cls,rate,pi,b):
    if isinstance(rate,(int,Q)) and rate==0:
        return pi
    return pi*(b+rate)/(b+pi*rate) if cls=="H" else pi*b/(b+(1-pi)*rate)


def correct_return(cls,mu,d,e):
    return e*d*((1-mu) if cls=="H" else mu)


def candidates(cls,r,pi,lam,b,investor,challenger):
    d,threshold=D(r),tau(r)
    out=[]
    for label,rate in (("zero",0),("full",lam)):
        mu=post(cls,rate,pi,b)
        side=sign(mu-threshold)
        if side is None:
            continue
        if side!=0 or challenger=="C1":
            e=Q(1) if side>=0 else rho
            v=correct_return(cls,mu,d,e)
            good=le(v,fee) if label=="zero" else (lt(fee,v) if investor=="I0" else le(fee,v))
            if good:
                out.append((label,rate,mu,e,e,False))
        else:
            cutoff=fee/correct_return(cls,mu,d,1)
            if label=="zero":
                lo,hi=rho,min(Q(1),cutoff)
                op=False
            else:
                lo,hi=max(rho,cutoff),Q(1)
                op=investor=="I0" and cutoff>=rho
            if lo<hi or (lo==hi and not op):
                out.append((label+"-tie",rate,mu,lo,hi,op))
    if investor=="IM":
        for e in (rho,Q(1)):
            mu=1-fee/(e*d) if cls=="H" else fee/(e*d)
            if not 0<mu<1:
                continue
            if (e==rho and not mu<threshold) or (e==1 and not mu>threshold):
                continue
            rate=b*(mu-pi)/(pi*(1-mu)) if cls=="H" else b*(pi-mu)/((1-pi)*mu)
            if lt(0,rate) and lt(rate,lam):
                out.append(("mix-floor" if e==rho else "mix-entry",rate,mu,e,e,False))
        mu=threshold
        rate=b*(mu-pi)/(pi*(1-mu)) if cls=="H" else b*(pi-mu)/((1-pi)*mu)
        e=fee/correct_return(cls,mu,d,1)
        if lt(0,rate) and lt(rate,lam) and rho<=e<=1 and (challenger=="CM" or e==1):
            out.append(("threshold",rate,mu,e,e,False))
    return out


def solve(r,pi,lam,b,beta,investor,challenger):
    hs=candidates("H",r,pi,lam,b,investor,challenger)
    ls=candidates("L",r,pi,lam,b,investor,challenger)
    b0=(1-lam)*(1-2*beta)
    t0,tH,tL,gH,gL,d=auction(r)
    results=[]
    for h,l in product(hs,ls):
        s,t=h[1],l[1]
        aH=(b,b0+lam-s,b+s)
        aL=(b+t,b0+lam-t,b)
        mus=tuple(pi*x/(pi*x+(1-pi)*y) for x,y in zip(aH,aL))
        if isinstance(s,(int,Q)) and isinstance(t,(int,Q)) and s==t:
            mus=(mus[0],pi,mus[2])
        s0=sign(mus[1]-tau(r))
        if s0 is None:
            continue
        e0=rho if s0<0 else Q(1)
        # At a zero-order tie, the upper entry endpoint supplies a valid tuple.
        es=(l[3] if not l[5] else (l[3]+l[4])/2,e0,h[3] if not h[5] else (h[3]+h[4])/2)
        prices=tuple(t0+e*(tL-t0+d*mu) for e,mu in zip(es,mus))
        ups={}
        unresolved=0
        for cls,tj in (("H",tH),("L",tL)):
            ups[cls]=tuple(q*(t0+e*(tj-t0)-price)-fee*abs(q)
                for q,e,price in zip((-1,0,1),es,prices))
            unresolved+=sum(sign(x) is None for x in ups[cls])
        mass=tuple(pi*x+(1-pi)*y for x,y in zip(aH,aL))
        entry=sum(x*y for x,y in zip(mass,es))
        results.append(dict(h=h,l=l,mu=mus,e=es,price=prices,payoff=ups,entry=entry,unresolved=unresolved))
    return results


def forms(eqs):
    out=set()
    for eq in eqs:
        h,l=eq["h"][0],eq["l"][0]
        out.add((h,l))
    return out


def prediction(r,u,inv,ch):
    M=(1+u)/(2+u)
    d,thr=D(r),tau(r)
    low="zero" if rho*d/2<=fee else ("full" if le(fee,rho*d*(1-M)) else "mix-floor")
    if inv=="I0" and (low=="mix-floor" or sign(rho*d*(1-M)-fee)==0):
        return set()
    out=set()
    if rho*d/2<=fee:
        out.add(("zero",low))
    if lt(fee,d*(1-M)) or (inv=="IM" and sign(d*(1-M)-fee)==0):
        out.add(("full",low))
    if inv=="IM":
        if J(r)>fee and lt(d*(1-M),fee):
            out.add(("mix-entry",low))
        if rho*d/2>fee and rho*J(r)<fee:
            out.add(("mix-floor",low))
        if fee<=J(r) and rho*J(r)<=fee and ch=="CM":
            out.add(("threshold",low))
    return out


def main():
    lines=[]
    def say(x):
        print(x)
        lines.append(str(x))
    say("Exact support enumeration: each class uses zero, full, interior floor, interior entry, or threshold.")
    say("Both classes may mix. Wrong-sign orders have negative profit because d>0, e>=rho, and k>0.")
    mismatch,counts=0,0
    for beta,u in product((Q(1,5),Q(1,3),Q(2,5),Q(49,100)),(Q(7,5),Q(8,5),Q(43,25))):
        lam=u*beta/(1+u*beta)
        b=(1-lam)*beta
        for inv,ch in product(("IM","I0"),("C1","CM")):
            for n in range(121):
                r=Q(6,5)+Q(n,50)
                found=forms(solve(r,Q(1,2),lam,b,beta,inv,ch))
                predicted=prediction(r,u,inv,ch)
                counts+=1
                if found!=predicted:
                    mismatch+=1
                    say(f"PATH DIFFERENCE beta={beta} u={u} r={r} {inv}/{ch}: {found} vs {predicted}")
    say(f"Rational path calculations={counts}; differences from the piecewise set={mismatch}.")
    # An exact challenger tie at a full-order posterior, inside the band.
    r=Q(31,10)
    M=tau(r)
    u=(2*M-1)/(1-M)
    beta=Q(2,5)
    lam=u*beta/(1+u*beta)
    b=(1-lam)*beta
    for inv,ch in product(("IM","I0"),("C1","CM")):
        eqs=solve(r,Q(1,2),lam,b,beta,inv,ch)
        say(f"Exact ceiling r={r}, beta={beta}, u={u}, {inv}/{ch}: "+str([(e['h'][0],e['h'][3:6],e['l'][0]) for e in eqs]))
    # Calibration B retains the exact declaration of e as an interval.
    beta=Q(294655,1000000)
    u=exp_one()-1
    lam=u*beta/(1+u*beta)
    b=beta/(1+u*beta)
    total=diffs=0
    for inv,ch in product(("IM","I0"),("C1","CM")):
        for n in range(121):
            r=Q(6,5)+Q(n,50)
            eqs=solve(r,Q(1,2),lam,b,beta,inv,ch)
            found=forms(eqs)
            pred=prediction(r,u,inv,ch)
            total+=1
            if found!=pred:
                diffs+=1
                say(f"B PATH DIFFERENCE r={r}, {inv}/{ch}: {found} vs {pred}")
    say(f"Calibration B interval path calculations={total}; branch differences={diffs}.")
    for r in (Q(7,5),Q(31,20),Q(9,5),Q(2),Q(3),Q(18,5)):
        for ch in ("C1","CM"):
            for eq in solve(r,Q(1,2),lam,b,beta,"IM",ch):
                say(f"B tuple r={r}, IM/{ch}, {eq['h'][0]}/{eq['l'][0]} entry={bounds(eq['entry'],18)}")
                say("  posteriors="+str([bounds(x,18) for x in eq['mu']]))
                say("  prices="+str([bounds(x,18) for x in eq['price']]))
                say("  fixed-tuple H payoffs="+str([bounds(x,18) for x in eq['payoff']['H']]))
                say("  fixed-tuple L payoffs="+str([bounds(x,18) for x in eq['payoff']['L']]))
    # General priors: the set condition is compared with both classes' supports.
    total=diffs=0
    for pi in (Q(1,10),Q(3,10),Q(39,100),Q(2,5),Q(1,2),Q(16,25),Q(129,200),Q(649,1000),Q(13,20),Q(651,1000),Q(7,10),Q(9,10)):
        coexist=[]
        for n in range(241):
            r=Q(6,5)+Q(n,100)
            eqs=solve(r,pi,lam,b,beta,"IM","C1")
            labs=forms(eqs)
            found=("zero","zero") in labs and len(labs)>1
            top=pi*(1+u)/(1+pi*u)
            pred=J(r)>=fee and pi<tau(r) and le(tau(r),top) and rho*D(r)*max(pi,1-pi)<=fee
            total+=1
            if found!=pred:
                diffs+=1
                say(f"PRIOR DIFFERENCE pi={pi}, r={r}: found={found}, predicted={pred}")
            if found:
                coexist.append(r)
        say(f"B prior={pi}: coexistence grid range="+str((coexist[0],coexist[-1],len(coexist)) if coexist else None))
    say(f"General-prior interval calculations={total}; set differences={diffs}.")
    # CM endpoint at the prior: positive informative rates need J>k.
    for r in (Q(7,5),Q(8,5),Q(33,20)):
        pi=tau(r)
        eqs=solve(r,pi,lam,b,beta,"IM","CM")
        say(f"CM prior tie r={r}, pi={pi}: "+str(sorted(forms(eqs))))
    (HERE/"xp1_equilibria.log").write_text("\n".join(lines)+"\n")


if __name__=="__main__":
    main()
