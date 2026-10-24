"""Print auction and order-slot outcomes from declared economic inputs."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
from typing import Any

import mpmath
from mpmath import mp, iv

mp.dps = 40
iv.dps = 40
TOL = mp.mpf("1e-30")


def number(value: Any, context: Any = mp) -> Any:
    if isinstance(value, F):
        return context.mpf(value.numerator) / value.denominator
    return context.mpf(value)


def display(value: Any) -> str:
    if isinstance(value, F):
        return str(value)
    return mp.nstr(value, 36)


def decimal(value: Any) -> str:
    return mp.nstr(number(value), 15)


@dataclass(frozen=True)
class ClassLaw:
    lower: F
    upper: F


@dataclass(frozen=True)
class Economy:
    name: str
    high: ClassLaw
    low: ClassLaw
    prior: F
    reserve: F
    rho: F
    cost: F
    fee: F
    strengths: tuple[F, ...]


def polynomial_integral(coef: tuple[F, ...], a: F, b: F) -> F:
    return sum((c * (b ** (i + 1) - a ** (i + 1)) / (i + 1)
                for i, c in enumerate(coef)), F(0))


def point_objects(p: F, r: F, value: F) -> tuple[F, F, F, F]:
    t0 = p * max(F(0), 1 - p / r)
    if value < p:
        return t0, F(0), F(0), F(0)
    if p >= r:
        return p, value - p, F(1), F(1)
    if value <= r:
        return (value - value * value / (2 * r) + p * p / (2 * r),
                (value * value - p * p) / (2 * r), value / r, F(1))
    payment = r / 2 + p * p / (2 * r)
    return payment, value - payment, F(1), F(1)


def class_objects(p: F, r: F, law: ClassLaw) -> tuple[F, F, F, F]:
    if law.lower == law.upper:
        return point_objects(p, r, law.lower)
    a, z = law.lower, law.upper
    cuts = sorted({a, z} | {v for v in (p, r) if a < v < z})
    totals = [F(0)] * 4
    t0 = p * max(F(0), 1 - p / r)
    for left, right in zip(cuts[:-1], cuts[1:]):
        middle = (left + right) / 2
        if middle < p:
            polynomials = ((t0,), (F(0),), (F(0),), (F(0),))
        elif p >= r:
            polynomials = ((p,), (-p, F(1)), (F(1),), (F(1),))
        elif middle < r:
            polynomials = ((p*p/(2*r), F(1), -1/(2*r)),
                           (-p*p/(2*r), F(0), 1/(2*r)),
                           (F(0), 1/r), (F(1),))
        else:
            t = r/2 + p*p/(2*r)
            polynomials = ((t,), (-t, F(1)), (F(1),), (F(1),))
        for i, coef in enumerate(polynomials):
            totals[i] += polynomial_integral(coef, left, right)
    return tuple(v / (z-a) for v in totals)


def auction(economy: Economy, r: F) -> dict[str, F]:
    p = economy.reserve
    th, gh, wh, ah = class_objects(p, r, economy.high)
    tl, gl, wl, al = class_objects(p, r, economy.low)
    return dict(t0=p*max(F(0), 1-p/r), th=th, tl=tl, gh=gh, gl=gl,
                wh=wh, wl=wl, ah=ah, al=al, delta=th-tl,
                s0=max(F(0), (r*r-p*p)/(2*r)), fp=min(F(1), p/r))


def calibration(context: Any = mp) -> dict[str, tuple[Any, Any]]:
    pi, rho = context.mpf(1)/2, context.mpf(1)/4
    tau = context.mpf(141)/200
    x = context.log(tau/(1-tau))
    alpha_h = 1-context.exp((x-1)/2)/2
    alpha_l = context.exp(-(x+1)/2)/2
    target = rho+(1-rho)*(alpha_h+alpha_l)/2
    u = context.exp(1)-1
    d = (target-rho)/(1-rho)
    b = d/(1+pi*u)
    lam = u*b
    beta = b/(1-lam)
    return {"A": (F(6,17), F(1,3)), "B": (lam, beta)}


def bounds(pi: Any, lam: Any, beta: Any) -> tuple[Any, Any]:
    b = (1-lam)*beta
    u = lam/b
    return pi/(pi+(1-pi)*(1+u)), pi*(1+u)/(pi*(1+u)+1-pi)


def entry(economy: Economy, objects: dict[str, Any], mu: Any) -> Any:
    difference = mu*objects["gh"]+(1-mu)*objects["gl"]-economy.cost
    if isinstance(difference, F):
        return F(1) if difference >= 0 else economy.rho
    if abs(difference) < TOL:
        print("entry tie or unresolved sign:", display(difference))
    return mp.mpf(1) if difference >= -TOL else number(economy.rho)


def outcome(economy: Economy, r: F, lam: Any, beta: Any,
            full: bool, hidden: bool = False, context: Any = None,
            reserve_override: Any = None, top_tie: bool = False,
            entry_pattern: tuple[int, int, int] | None = None) -> dict[str, Any]:
    raw = auction(economy, r)
    exact = isinstance(lam, F)
    cast = (lambda x: x) if exact else (lambda x: number(x, context or mp))
    obj = {key: cast(val) for key, val in raw.items()}
    pi, rho, cost, fee = map(cast, (economy.prior,economy.rho,economy.cost,economy.fee))
    p = cast(economy.reserve)
    rr = cast(r)
    if reserve_override is not None:
        p = reserve_override
        obj.update(t0=p*(1-p/rr), th=rr/2+p*p/(2*rr),
                   gh=cast(F(10))-rr/2-p*p/(2*rr), gl=cast(F(0)),
                   tl=p*(1-p/rr), ah=cast(F(1)), al=cast(F(0)),
                   fp=p/rr, s0=(rr*rr-p*p)/(2*rr), wh=cast(F(1)))
        obj["delta"] = obj["th"]-obj["tl"]
    b = (1-lam)*beta
    c = (1-lam)*(1-2*beta)
    ah = [b, c+lam, b]
    al = [b, c+lam, b]
    if full:
        ah = [b, c, b+lam]
        al = [b+lam, c, b]
    masses = [pi*h+(1-pi)*l for h,l in zip(ah,al)]
    mus = [pi*h/d for h,d in zip(ah,masses)]
    if context is iv:
        em = [rho if v==0 else cast(F(1)) for v in (entry_pattern or (0,0,1))]
        if hidden and entry_pattern is None:
            em = [rho]*3
        if top_tie:
            em = [rho,rho,cast(F(1))]
    elif top_tie:
        em = [rho,rho,cast(F(1))]
    else:
        em = [entry(economy,obj,pi if hidden else mu) for mu in mus]
    ejh = sum(h*e for h,e in zip(ah,em))
    ejl = sum(l*e for l,e in zip(al,em))
    total = pi*ejh+(1-pi)*ejl
    prices = [obj["t0"]+e*(obj["tl"]-obj["t0"]+obj["delta"]*mu)
              for mu,e in zip(mus,em)]
    revenue = obj["t0"]+pi*ejh*(obj["th"]-obj["t0"])+(1-pi)*ejl*(obj["tl"]-obj["t0"])
    adm = pi*ejh*obj["ah"]+(1-pi)*ejl*obj["al"]
    two = (1-obj["fp"])*adm
    sale = 1-obj["fp"]+adm-two
    surplus = obj["s0"]+pi*ejh*(obj["gh"]+p*obj["fp"]*obj["ah"])
    surplus += (1-pi)*ejl*(obj["gl"]+p*obj["fp"]*obj["al"])-cost*(total-rho)
    high_net = em[2]*obj["delta"]*(1-mus[2])-fee
    low_net = em[0]*obj["delta"]*mus[0]-fee
    return dict(entry=total, ownership=pi*ejh*obj["wh"], revenue=revenue,
                surplus=surplus, sale=sale, two=two, admissible=adm,
                eh=ejh, el=ejl, mu_minus=mus[0], mu_zero=mus[1], mu_plus=mus[2],
                high_net=high_net, low_net=low_net,
                trade_cost=lam*fee if full else cast(F(0)),
                price_minus=prices[0], price_zero=prices[1], price_plus=prices[2])


def margins(economy: Economy, lam: Any, beta: Any, context: Any = None) -> dict[str, Any]:
    exact = isinstance(lam,F)
    cast = (lambda x:x) if exact else (lambda x:number(x,context or mp))
    pi,rho,cost,fee = map(cast,(economy.prior,economy.rho,economy.cost,economy.fee))
    obs = [{key:cast(val) for key,val in auction(economy,r).items()} for r in economy.strengths]
    low,high = bounds(pi,lam,beta)
    b=(1-lam)*beta
    def gross(o: dict[str,Any], mu:Any)->Any:
        return mu*o["gh"]+(1-mu)*o["gl"]
    result = dict(weak_cost=cost-gross(obs[0],pi),
                  weak_trade=fee-obs[0]["delta"],
                  strong_prior=cost-gross(obs[1],pi),
                  strong_top=gross(obs[1],high)-cost,
                  strong_high_floor=rho*obs[1]["delta"]*(1-high)-fee,
                  strong_low_floor=rho*obs[1]["delta"]*low-fee,
                  ownership_if_recruited=(rho+(1-rho)*(lam+b))*obs[1]["wh"]-rho*obs[0]["wh"],
                  ownership_paper=(1+rho)*obs[1]["wh"]-2*rho*obs[0]["wh"])
    if len(obs)>2:
        result.update(collapse=cost-gross(obs[2],high),
                      collapse_high_floor=rho*obs[2]["delta"]*(1-high)-fee,
                      collapse_low_floor=rho*obs[2]["delta"]*low-fee)
    return result


def declarations() -> tuple[Economy,...]:
    pt=lambda v:ClassLaw(F(v),F(v))
    base=(F(1,2),F(1,4))
    return (
        Economy("benchmark",pt(10),pt(1),F(1,2),*base,F(6),F(1,50),(F(6,5),F(3),F(18,5))),
        Economy("moderate",pt(2),pt(1),F(1,2),*base,F(89,100),F(1,500),(F(21,20),F(3,2))),
        Economy("narrow",ClassLaw(F(199,20),F(201,20)),ClassLaw(F(19,20),F(21,20)),F(1,2),*base,F(6),F(1,50),(F(6,5),F(3),F(18,5))),
        Economy("class_A",pt(10),pt(1),F(3,10),*base,F(9,2),F(1,100),(F(11,10),F(3),F(18,5))),
        Economy("class_B",pt(10),pt(1),F(7,10),*base,F(36,5),F(1,100),(F(11,10),F(3),F(18,5))),
        Economy("class_C",ClassLaw(F(1),F(19)),ClassLaw(F(3,5),F(7,5)),F(7,10),*base,F(67,10),F(1,50),(F(1),F(9,2),F(11,2))),
        Economy("class_D",pt(10),pt(1),F(7,10),*base,F(67,10),F(1,50),(F(1),F(9,2),F(11,2))),
        Economy("ledger_counterexample",pt(10),pt(1),F(1,2),*base,F(47,10),F(1,50),(F(6,5),F(3),F(8))),
    )


def many_class() -> None:
    lam,beta=F(6,17),F(1,3)
    b=(1-lam)*beta
    prior=(F(1,4),F(1,2),F(1,4))
    weight=F(91,102)
    proceeds=(F(1),F(1)+(F(65,16)-1)*weight,F(65,16))
    rho,k,t0=F(1,4),F(1,8),F(7,8)
    flow=[]
    for q in range(3):
        mass=[prior[j]*(b+(lam if j==q else 0)) for j in range(3)]
        post=tuple(v/sum(mass) for v in mass)
        mean=sum(p*t for p,t in zip(post,proceeds))
        flow.append((post,mean,t0+rho*(mean-t0)))
    print("MANY CLASS: R uniform [0,8], p=1, rho=1/4, c_H=10, k=1/8")
    print("prior",prior,"middle probability of value 10",weight,"proceeds",proceeds)
    for q,(post,mean,price) in zip((-1,0,1),flow):
        print("flow",q,"posterior",post,"mean",mean,"price",price)
    for j,t in enumerate(proceeds):
        payoffs=tuple(q*rho*(t-flow[i][1])-k*abs(q) for i,q in enumerate((-1,0,1)))
        print("class",j+1,"payoffs sell/wait/buy",payoffs)


def many_class_b(lam: Any, beta: Any, context: Any) -> None:
    cast=lambda x:number(x,context)
    b=(1-lam)*beta
    c=(1-lam)*(1-2*beta)
    constant_plus=(b+lam)/(4*b+lam)
    constant_zero=c/(4*c+2*lam)
    slope_zero=(c+lam)/(2*c+lam)
    slope_plus=2*b/(4*b+lam)
    weight=(constant_plus-constant_zero)/(slope_zero-slope_plus)
    pri=tuple(cast(v) for v in (F(1,4),F(1,2),F(1,4)))
    proceeds=(cast(F(1)),1+cast(F(49,16))*weight,cast(F(65,16)))
    flow=[]
    for i in range(3):
        base=c if i==1 else b
        mass=[pri[j]*(base+(lam if j==i else 0)) for j in range(3)]
        post=tuple(v/sum(mass) for v in mass)
        mean=sum(p*t for p,t in zip(post,proceeds))
        flow.append((post,mean))
    print("MANY CLASS B", "interval" if context is iv else "decimal", "middle weight",str(weight))
    for i,(post,mean) in enumerate(flow):
        print("flow",i-1,"posterior",[str(v) for v in post],"mean",str(mean))
    for j,t in enumerate(proceeds):
        net=tuple(q*cast(F(1,4))*(t-flow[i][1])-cast(F(1,8))*abs(q) for i,q in enumerate((-1,0,1)))
        print("class",j+1,"net payoffs",[str(v) for v in net])


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,required=True)
    args=parser.parse_args()
    root=args.output_dir
    root.mkdir(parents=True,exist_ok=True)
    calibrations=calibration()
    intervals=calibration(iv)
    print("source=overleaf/paper commit 01bd5d6; mp.dps=40; iv.dps=40; numerical tie tolerance=1e-30")
    print("B uses the unrounded Laplace benchmark entry, not the displayed decimal 0.522757")
    for name,(lam,beta) in calibrations.items():
        print("CALIBRATION",name,"lambda",display(lam),"beta",display(beta),"b",display((1-lam)*beta))
    rows=[]
    cert=[]
    interval_rows=[]
    for ec in declarations():
        print("\nECONOMY",ec.name)
        for r in ec.strengths:
            print("auction r",r,{key:str(val) for key,val in auction(ec,r).items()})
        for cal,(lam,beta) in calibrations.items():
            mar=margins(ec,lam,beta)
            print("MARGINS",cal,{key:display(val) for key,val in mar.items()})
            if cal=="B":
                im=margins(ec,*intervals[cal],context=iv)
            else:
                im=mar
            for key,val in mar.items():
                cert.append(dict(economy=ec.name,calibration=cal,quantity=key,value=display(val),enclosure=str(im[key])))
            for i,r in enumerate(ec.strengths):
                full=i>0
                out=outcome(ec,r,lam,beta,full)
                row=dict(economy=ec.name,calibration=cal,r=str(r),profile="full" if full else "zero")
                row.update({key:display(val) for key,val in out.items()})
                rows.append(row)
                print("OUTCOME",cal,r,row)
                if cal=="B":
                    pattern=(1,1,1) if ec.name=="ledger_counterexample" and i==0 else ((0,0,0) if i==0 or i==2 or ec.name=="class_D" else (0,0,1))
                    enclosed=outcome(ec,r,*intervals[cal],full,context=iv,entry_pattern=pattern)
                    interval_rows.append(dict(economy=ec.name,r=str(r),reserve=str(ec.reserve),
                                              **{key:str(val) for key,val in enclosed.items()}))
                if ec.name=="benchmark" and i==1:
                    hidden=outcome(ec,r,lam,beta,True,hidden=True)
                    print("ACCESS",cal,"observed",{k:display(out[k]) for k in ("revenue","surplus","trade_cost")},
                          "hidden",{k:display(hidden[k]) for k in ("revenue","surplus","trade_cost")},
                          "difference",{k:display(out[k]-hidden[k]) for k in ("revenue","surplus")})
                    if cal=="B":
                        ob=outcome(ec,r,*intervals[cal],True,context=iv)
                        hb=outcome(ec,r,*intervals[cal],True,hidden=True,context=iv)
                        print("ACCESS INTERVAL",{k:str(ob[k]-hb[k]) for k in ("revenue","surplus")})
    benchmark=declarations()[0]
    for band,p_high in ((False,F(101,100)),(True,F(11,10))):
        for p in (F(1,2),p_high):
            ec=Economy("reserve_band" if band else "reserve_point",
                       ClassLaw(F(199,20),F(201,20)) if band else benchmark.high,
                       ClassLaw(F(19,20),F(21,20)) if band else benchmark.low,
                       F(1,2),p,F(1,4),F(6),F(1,50),(F(6,5),F(3)))
            for cal,(lam,beta) in calibrations.items():
                for r in ec.strengths:
                    obj=auction(ec,r)
                    full=not(p==F(1,2) and r==F(6,5))
                    out=outcome(ec,r,lam,beta,full)
                    row=dict(economy=ec.name,calibration=cal,r=str(r),reserve=str(p),profile="full" if full else "zero")
                    row.update({key:display(val) for key,val in out.items()})
                    rows.append(row)
                    print("RESERVE",row)
                    cast=(lambda x:x) if cal=="A" else number
                    lo,hi=bounds(cast(ec.prior),lam,beta)
                    floor_h=cast(ec.rho*obj["delta"])*(1-hi)-cast(ec.fee)
                    floor_l=cast(ec.rho*obj["delta"])*lo-cast(ec.fee)
                    print("RESERVE MARGINS",cal,p,r,"k-Delta",display(ec.fee-obj["delta"]),
                          "Hfloor-k",display(floor_h),"Lfloor-k",display(floor_l),
                          "Bprior-cost",display(ec.prior*obj["gh"]+(1-ec.prior)*obj["gl"]-ec.cost),
                          "Btop-cost",display(hi*obj["gh"]+(1-hi)*obj["gl"]-ec.cost))
                    if cal=="B":
                        il,ib=intervals[cal]
                        ilo,ihi=bounds(number(ec.prior,iv),il,ib)
                        vals={"Hfloor-k":number(ec.rho*obj["delta"],iv)*(1-ihi)-number(ec.fee,iv),
                              "Lfloor-k":number(ec.rho*obj["delta"],iv)*ilo-number(ec.fee,iv),
                              "Btop-cost":ihi*number(obj["gh"],iv)+(1-ihi)*number(obj["gl"],iv)-number(ec.cost,iv)}
                        print("RESERVE INTERVAL",{key:str(val) for key,val in vals.items()})
                        enclosed=outcome(ec,r,il,ib,full,context=iv,entry_pattern=(0,0,1) if full else (0,0,0))
                        interval_rows.append(dict(economy=ec.name,r=str(r),reserve=str(p),
                                                  **{key:str(val) for key,val in enclosed.items()}))
    print("\nRESERVE EVENTS")
    for cal,(lam,beta) in calibrations.items():
        ll,bb=number(lam),number(beta)
        _,hi=bounds(mp.mpf(1)/2,ll,bb)
        p=mp.sqrt(6*(10-6/hi)-9)
        out=outcome(benchmark,F(3),ll,bb,True,reserve_override=p,top_tie=True)
        print("p_H",cal,display(p),{k:display(out[k]) for k in ("entry","sale","two","revenue","high_net","low_net")})
        il,ib=intervals[cal]
        il,ib=number(il,iv) if isinstance(il,F) else il,number(ib,iv) if isinstance(ib,F) else ib
        _,ihi=bounds(iv.mpf(1)/2,il,ib)
        ip=iv.sqrt(6*(10-6/ihi)-9)
        enclosed=outcome(benchmark,F(3),il,ib,True,context=iv,reserve_override=ip,top_tie=True)
        print("p_H INTERVAL",cal,str(ip),"floor net",str(enclosed["low_net"]))
    ep=Economy("endpoint",benchmark.high,benchmark.low,F(1,2),F(10),F(1,4),F(6),F(1,50),(F(6,5),F(3)))
    print("p_L",outcome(ep,F(6,5),F(6,17),F(1,3),True))
    print("\nACCESS OUTSIDE THE RECRUITMENT REGION")
    for cal,cost in (("A",F(49,20)),("B",F(12,5))):
        lam,beta=calibrations[cal]
        ec=Economy("access_outside",benchmark.high,benchmark.low,F(1,2),F(1,2),F(1,4),cost,F(1,50),(F(3),))
        seen=outcome(ec,F(3),lam,beta,True)
        unseen=outcome(ec,F(3),lam,beta,True,hidden=True)
        print(cal,"c_H",cost,"differences",{key:display(seen[key]-unseen[key]) for key in ("revenue","surplus")})
        if cal=="B":
            il,ib=intervals[cal]
            seeni=outcome(ec,F(3),il,ib,True,context=iv,entry_pattern=(0,1,1))
            unseeni=outcome(ec,F(3),il,ib,True,hidden=True,context=iv,entry_pattern=(1,1,1))
            print("OUTSIDE ACCESS INTERVAL",{key:str(seeni[key]-unseeni[key]) for key in ("revenue","surplus")})
    for cal,(lam,beta) in calibrations.items():
        ec=Economy("reserve_alternative",benchmark.high,benchmark.low,F(1,2),F(31,20),F(1,4),F(6),F(1,50),(F(6,5),F(3)))
        for r in ec.strengths:
            print("ALTERNATIVE RESERVE",cal,r,{key:display(val) for key,val in outcome(ec,r,lam,beta,True).items()})
            if cal=="B":
                il,ib=intervals[cal]
                pat=(0,0,1) if r==F(6,5) else (0,0,0)
                enclosed=outcome(ec,r,il,ib,True,context=iv,entry_pattern=pat)
                obj=auction(ec,r)
                lo,hi=bounds(iv.mpf(1)/2,il,ib)
                top=hi*number(obj["gh"],iv)-6
                floor=number(F(1,4)*obj["delta"],iv)*lo-number(F(1,50),iv)
                print("ALTERNATIVE INTERVAL",r,"Btop-cost",str(top),"floor-k",str(floor),
                      "revenue",str(enclosed["revenue"]))
    print("\nACTIVITY CHOICES TO MATCH EACH LAPLACE ENTRY")
    for ec in declarations()[:7]:
        r=ec.strengths[1]
        obj=auction(ec,r)
        pi=number(ec.prior)
        tau=(number(ec.cost)-number(obj["gl"]))/number(obj["gh"]-obj["gl"])
        _,hi=bounds(pi,*calibrations["B"])
        if pi<tau<hi:
            x=mp.log(tau/(1-tau))-mp.log(pi/(1-pi))
            alpha_h=1-mp.exp((x-1)/2)/2
            alpha_l=mp.exp(-(x+1)/2)/2
            rho=number(ec.rho)
            target=rho+(1-rho)*(pi*alpha_h+(1-pi)*alpha_l)
            u=mp.exp(1)-1
            bb=((target-rho)/(1-rho))/(1+pi*u)
            ll=u*bb
            be=bb/(1-ll)
            print(ec.name,"target entry",display(target),"lambda",display(ll),"beta",display(be))
    print("\nCONSTRUCTIVE SEQUENCE: original cost recipe with Laplace scale 2")
    for ratio in (F(21,20),F(11,10),F(5,4),F(3,2),F(2)):
        for n in range(1,21):
            gap=ratio-1
            delta=gap/F(2)**n
            r0,r1=1+delta*delta/gap,1+delta
            ec0=Economy("construction",ClassLaw(ratio,ratio),ClassLaw(F(1),F(1)),F(1,2),F(1,2),F(1,4),F(1),F(1),(r0,r1))
            o0,o1=auction(ec0,r0),auction(ec0,r1)
            def choice(context:Any)->tuple[Any,Any]:
                m=1/(1+context.exp(1))
                top=1-m
                prior0=number((o0["gh"]+o0["gl"])/2,context)
                upper1=top*number(o1["gh"],context)+m*number(o1["gl"],context)
                k=(number(o0["delta"],context)+number(F(1,8)*o1["delta"],context)*m)/2
                return (prior0+upper1)/2,k
            cost,fee=choice(mp)
            icost,ifee=choice(iv)
            all_values=[]
            for cal,(lam,beta) in calibrations.items():
                lo,hi=bounds(mp.mpf(1)/2,number(lam),number(beta))
                vals=(cost-number((o0["gh"]+o0["gl"])/2),
                      hi*number(o1["gh"])+(1-hi)*number(o1["gl"])-cost,
                      fee-number(o0["delta"]),number(F(1,4)*o1["delta"])*lo-fee)
                all_values.extend(vals)
                il,ib=intervals[cal]
                il,ib=number(il,iv) if isinstance(il,F) else il,number(ib,iv) if isinstance(ib,F) else ib
                ilo,ihi=bounds(iv.mpf(1)/2,il,ib)
                ivals=(icost-number((o0["gh"]+o0["gl"])/2,iv),
                       ihi*number(o1["gh"],iv)+(1-ihi)*number(o1["gl"],iv)-icost,
                       ifee-number(o0["delta"],iv),number(F(1,4)*o1["delta"],iv)*ilo-ifee)
                print("SEQUENCE",ratio,"n",n,cal,"r0",r0,"r1",r1,"k",display(fee),"c_H",display(cost),
                      "margins",[display(v) for v in vals],"intervals",[str(v) for v in ivals])
            if min(all_values)>TOL:
                print("FIRST FEASIBLE",ratio,"n",n,"k",display(fee),"c_H",display(cost))
                break
    print("\nPRIOR WINDOWS")
    for cal,(lam,beta) in calibrations.items():
        u=lam/((1-lam)*beta)
        tau1,tau2=F(141,200),F(4245,5804)
        low=tau1/(1+u*(1-tau1))
        high=tau2/(1+u*(1-tau2))
        print(cal,"lower",display(low),"upper",display(high))
    lam,beta=F(6,17),F(2,5)
    c=(1-lam)*(1-2*beta)
    print("ZERO FLOW BOUND", "beta",beta,"lambda",lam,"zero posterior",(c+lam)/(2*c+lam),"tail M",bounds(F(1,2),lam,beta)[1])
    bargaining=[]
    for index in range(101):
        eta=F(index,100)
        for r in (F(6,5),F(3)):
            excess=(r-1)**2/(2*r)
            delta=eta*9+(1-2*eta)*excess
            gh=(1-eta)*(10-r/2)
            gl=(1-eta)/(2*r)
            th=(1-eta)*r/2+eta*10
            tl=th-delta
            bargaining.append(dict(eta=str(eta),r=str(r),t0=str(eta*r/2),th=str(th),tl=str(tl),delta=str(delta),gh=str(gh),gl=str(gl),
                                   spread_change=str((1-2*eta)*F(13,20)),profit_high_change=str(-(1-eta)*F(9,10)),profit_low_change=str(-(1-eta)*F(1,4))))
    print("BARGAINING selected rows")
    for row in bargaining:
        if row["eta"] in ("0","1/4","1/2","3/4","1"):
            print(row)
    many_class()
    many_class_b(*calibrations["B"],mp)
    many_class_b(*intervals["B"],iv)
    for name,data in (("examples.csv",rows),("margins.csv",cert),("bargaining.csv",bargaining),("outcome_intervals.csv",interval_rows)):
        keys=list(dict.fromkeys(key for row in data for key in row))
        with (root/name).open("w",newline="") as stream:
            writer=csv.DictWriter(stream,fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
    manifest=dict(source_commit="01bd5d6",python=platform.python_version(),mpmath=mpmath.__version__,precision_digits=40,
                  numerical_tie_tolerance="1e-30",interval_policy="outward arithmetic; strict signs only when zero is excluded",
                  inputs="declarations() and reserve cases in calculate.py",run_role="print economic outputs and payoff certificates")
    manifest["files"]={path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in (Path(__file__),root/"examples.csv",root/"margins.csv",root/"bargaining.csv",root/"outcome_intervals.csv")}
    (root/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")


if __name__=="__main__":
    main()
