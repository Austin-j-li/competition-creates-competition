"""Independent rational certificates and a read-only comparison with P1_core.csv.

Use from the repository root. All writes stay beside this script. No checked
module is imported. The output gives calculations, discrepancies, and bounds.
"""
import csv
import hashlib
import math
import pathlib
import re
from fractions import Fraction as Q

HERE = pathlib.Path(__file__).resolve().parent
TEAM = HERE.parents[1]
SCALE = 10**90


class I:
    """Closed intervals with exact rational endpoints."""

    def __init__(self, low, high=None):
        if isinstance(low, I):
            self.lo, self.hi = low.lo, low.hi
        else:
            self.lo = Q(low)
            self.hi = self.lo if high is None else Q(high)

    def __add__(self, other):
        other = I(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -I(other)

    def __rsub__(self, other):
        return I(other) + -self

    def __mul__(self, other):
        other = I(other)
        products = [a*b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return I(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = I(other)
        if other.lo <= 0 <= other.hi:
            raise ValueError("A divisor contains zero")
        return self * I(1/other.hi, 1/other.lo)

    def __rtruediv__(self, other):
        return I(other) / self

    def __pow__(self, n):
        result = I(1)
        for _ in range(n):
            result = result * self
        return result


def sqrt_interval(x):
    x = I(x)
    low = math.isqrt(x.lo.numerator * SCALE*SCALE // x.lo.denominator)
    high = math.isqrt(x.hi.numerator * SCALE*SCALE // x.hi.denominator) + 1
    return I(Q(low, SCALE), Q(high, SCALE))


def exp_one():
    # S_110 < e < S_110 + (112/111)/111! by a geometric bound on the tail.
    total = sum((Q(1, math.factorial(n)) for n in range(111)), Q(0))
    return I(total, total + Q(112, 111*math.factorial(111)))


def directed(q, digits=24, upper=False):
    unit = 10**digits
    n = -((-q.numerator*unit)//q.denominator) if upper else q.numerator*unit//q.denominator
    sign = "-" if n < 0 else ""
    n = abs(n)
    return f"{sign}{n//unit}.{n%unit:0{digits}d}"


def bounds(x, digits=24):
    x = I(x)
    return f"[{directed(x.lo, digits)}, {directed(x.hi, digits, True)}]"


def rounded(q, digits):
    unit = 10**digits
    n = (2*q.numerator*unit + q.denominator)//(2*q.denominator)
    sign = "-" if n < 0 else ""
    n = abs(n)
    return f"{sign}{n//unit}.{n%unit:0{digits}d}"


rho, cost, fee = Q(1,4), Q(6), Q(1,50)
r0, r1, r2 = Q(6,5), Q(3), Q(18,5)


def auction(r):
    # Direct integrals over the incumbent value, split at reserve and low value.
    r = Q(r)
    p, low, high = Q(1,2), Q(1), Q(10)
    t0 = p*(r-p)/r
    tH = (p*p + (r*r-p*p)/2)/r
    tL = (p*p + (low*low-p*p)/2 + low*(r-low))/r
    gL = ((low-p)*p + (low-p)**2/2)/r
    gH = ((high-p)*p + high*(r-p) - (r*r-p*p)/2)/r
    return t0,tH,tL,gH,gL,tH-tL


def D(r):
    return auction(r)[5]


def tau(r):
    _,_,_,gH,gL,_ = auction(r)
    return (cost-gL)/(gH-gL)


def gross(r, mu):
    _,_,_,gH,gL,_ = auction(r)
    return gL + mu*(gH-gL)


def J(r):
    return D(r)*(1-tau(r))


def root(fn, width=Q(1,10**95)):
    low, high = r0, r2
    while high-low > width:
        mid = (low+high)/2
        if fn(mid) < 0:
            low = mid
        else:
            high = mid
    return I(low,high)


def monotone(fn,x):
    return I(fn(x.lo),fn(x.hi))


def inv_D(d):
    return 1+d+sqrt_interval(d*d+2*d)


def produce():
    e = exp_one()
    u, beta = e-1, Q(294655,1000000)
    lam = u*beta/(1+u*beta)
    b = beta/(1+u*beta)
    M, m = e/(1+e), 1/(1+e)
    values = dict(u_B=u,beta_B=I(beta),lambda_B=lam,b_B=b,
                  b0_B=(1-lam)*(1-2*beta),M_half_B=M,m_half_B=m)
    for tag,r in (("r0",r0),("r1",r1),("r2",r2)):
        values[f"tau_{tag}"] = I(tau(r))
        values[f"tau_{tag}_frac"] = I(tau(r))
        values[f"Delta_{tag}"] = I(D(r))
    entry = rho+(1-rho)*(b+lam/2)
    eH,eL = rho+(1-rho)*(b+lam),rho+(1-rho)*b
    values.update(entry_r0=I(rho),entry_r1_B=entry,entry_r2=I(rho),
                  eH_r1_B=eH,eL_r1_B=eL,own_r0=I(rho/2),
                  own_r1_B=eH/2,own_r2_B=I(rho/2))
    for tag,r in (("r0",r0),("r1",r1),("r2",r2)):
        t0,tH,tL,gH,gL,d = auction(r)
        if tag == "r0":
            values["price_r0"] = I(t0+rho*(tL-t0+d/2))
        else:
            values[f"price_{tag}_m1_B"] = t0+rho*(tL-t0+d*m)
            values[f"price_{tag}_0_B"] = I(t0+rho*(tL-t0+d/2))
            values[f"price_{tag}_p1_B"] = t0+(1 if tag=="r1" else rho)*(tL-t0+d*M)
    values.update(margin_weakcost_B=I(cost-gross(r0,Q(1,2))),
        margin_recruit_B=gross(r1,M)-cost,
        margin_kweak_B=I(fee-D(r0)),margin_kstrong_B=rho*m*D(r1)-fee,
        margin_return_B=cost-gross(r2,M),margin_return_post_B=tau(r2)-M,
        margin_recruit_post_B=M-tau(r1),
        margin_implied_prior_r1=I(cost-gross(r1,Q(1,2))),
        margin_kstrong2_B=rho*m*D(r2)-fee,
        margin_implied_prior_r2=I(cost-gross(r2,Q(1,2))),
        margin_tau_r0_half=I(tau(r0)-Q(1,2)))
    ulo,uhi = Q(82,59),Q(2686,1559)
    for key,q in (("u_lo",ulo),("u_hi",uhi),("M_lo",tau(r1)),("M_hi",tau(r2))):
        values[key] = values[key+"_frac"] = I(q)
    llo,lhi = ulo*beta/(1+ulo*beta),uhi*beta/(1+uhi*beta)
    values.update(u_kstrong=I(Q(19,3)),margin_u_lo_B=u-ulo,margin_u_hi_B=uhi-u,
        lambda_lo_B=I(llo),lambda_hi_B=I(lhi),margin_lambda_lo_B=lam-llo,
        margin_lambda_hi_B=lhi-lam,lambda_lo_third=I(Q(82,259)),
        lambda_hi_third=I(Q(2686,7363)),margin_beta_B=I(Q(1,3)-beta))
    plo,phi = 141/(141+59*e),4245/(4245+1559*e)
    values.update(prior_lo_B=plo,prior_hi_B=phi,prior_ii_hi=I(tau(r0)),
        prior_kappa_lo_B=3*e/(22+3*e),prior_kappa_hi_B=22/(22+3*e),
        margin_prior_lo_B=Q(1,2)-plo,margin_prior_hi_B=phi-Q(1,2))
    rA,rJ,rstar = root(lambda r:J(r)-fee),root(lambda r:rho*J(r)-fee),root(lambda r:rho*D(r)*tau(r)-fee)
    tA,tJ,tstar = monotone(tau,rA),monotone(tau,rJ),monotone(tau,rstar)
    rN,rF,rS = inv_D(I(2*fee/rho)),inv_D(fee*(1+e)),inv_D(fee*(1+e)/rho)
    a = 10*M-cost
    rC = (a+sqrt_interval(a*a+M*(1-M-Q(1,4))))/M
    pal = tA/(tA+(1-tA)*e)
    values.update(rA=rA,rJ=rJ,rstar=rstar,tau_rA=tA,piA_hi=tA,tau_rJ=tJ,
        pimax=tstar,Delta_rA=monotone(D,rA),rN=rN,rF_B=rF,rS_B=rS,rC_B=rC,
        piA_lo_B=pal,margin_piA_lo_B=Q(1,2)-pal,margin_piA_hi=tA-Q(1,2))
    points = [("rA_r0",rA-I(r0)),("rF_rA",rF-rA),("rN_rF",rN-rF),
        ("rJ_rN",rJ-rN),("rS_rJ",rS-rJ),("r1_rS",r1-rS),
        ("rC_r1",rC-r1),("r2_rC",r2-rC)]
    for key,x in points:
        values["gap_"+key+"_B"] = x
    values["entry_rA_B"] = rho+(1-rho)*b/(2*(1-tA))
    for tag,r in (("r140",Q(7,5)),("r145",Q(29,20))):
        values[f"entry_mb_{tag}_B"] = rho+(1-rho)*b*D(r)/(2*fee)
    bA = Q(11,51)
    for tag,r in (("r155",Q(31,20)),("r160",Q(8,5)),("r165",Q(33,20))):
        mult = (fee-rho*J(r))/(2*D(r)*(1-tau(r))**2)
        values[f"entry_th_{tag}_B"] = rho+b*mult
        values[f"estar_{tag}"] = I(fee/J(r))
        values[f"entry_th_{tag}_A"] = I(rho+bA*mult)
    values.update(b_plus_lambda_B=b+lam,nec_cH=I(Q(47,10)),nec_r2=I(8),
        nec_margin_kweak=I(fee-D(r0)),nec_margin_prior_r1=I(Q(47,10)-gross(r1,Q(1,2))),
        nec_margin_recruit_B=gross(r1,M)-Q(47,10),nec_margin_kstrong_B=rho*m*D(r1)-fee,
        nec_margin_return_B=Q(47,10)-gross(Q(8),M),
        nec_margin_weakcost=I(Q(47,10)-gross(r0,Q(1,2))),nec_entry_r0=I(1),
        Delta_r155=I(D(Q(31,20))),margin_kstrong_r2pt0_B=rho*m*D(Q(2))-fee,
        J_r0=I(J(r0)),rhoJ_r1=I(rho*J(r1)),rhoJ_r2=I(rho*J(r2)),
        QJ_r0=I(sum(Q(c)*r0**i for i,c in enumerate([-1,40,-614,-12,743,-160,4]))),
        B_r0_half=I(gross(r0,Q(1,2))),Delta_r155_frac=I(D(Q(31,20))),
        ex_beta_mu0=I(Q(41,52)),ex_beta_M=I(Q(26,37)),entry_r1_B_7=entry,
        rF_A=inv_D(I(Q(4,55))))
    oldbeta = Q("0.294655575684807914696610854717407893")
    oldb = oldbeta/(1+u*oldbeta)
    values["entry_r1_unroundedbeta_7"] = rho+(1-rho)*oldb*(1+u/2)
    return values


def main():
    values = produce()
    rows = list(csv.DictReader((TEAM/"registry/P1_core.csv").open()))
    log = []
    def say(s):
        print(s)
        log.append(s)
    say("Exact rational interval certificate. e uses terms 0 through 110 and a geometric tail bound.")
    say("Square roots use integer square roots at scale 10^90. Roots use exact rational bisection at width 10^-95.")
    say("No P1 module is imported or executed. The registry is read only.")
    differences, bad, allrows = [],[],[]
    source_roots = [root(fn,Q(1,10**13)) for fn in
        (lambda r:J(r)-fee,lambda r:rho*J(r)-fee,lambda r:rho*D(r)*tau(r)-fee)]
    a,j,z = source_roots
    ta,tj,tz = (monotone(tau,x) for x in source_roots)
    e = exp_one()
    pal_lo = I(ta.lo)/(ta.lo+(1-ta.lo)*e)
    pal_hi = I(ta.hi)/(ta.hi+(1-ta.hi)*e)
    pal = I(pal_lo.lo,pal_hi.hi)
    ea_lo = rho+(1-rho)*values["b_B"]/(2*(1-ta.lo))
    ea_hi = rho+(1-rho)*values["b_B"]/(2*(1-ta.hi))
    source_bounds = dict(rA=a,rJ=j,rstar=z,tau_rA=ta,piA_hi=ta,tau_rJ=tj,
        pimax=tz,Delta_rA=monotone(D,a),margin_piA_hi=ta-Q(1,2),
        piA_lo_B=pal,margin_piA_lo_B=Q(1,2)-pal,entry_rA_B=I(ea_lo.lo,ea_hi.hi))
    inward = []
    for row in rows:
        key,disp = row["key"],row["display"]
        x = values.get(key)
        if x is None:
            say("UNRESOLVED KEY "+key)
            continue
        if re.fullmatch(r"-?\d+\.\d+",disp):
            digits = len(disp.split(".")[1])
            correct = rounded(x.lo,digits)==rounded(x.hi,digits)==disp
        else:
            correct = x.lo==x.hi==Q(disp)
        if not correct:
            differences.append(key)
        match = re.search(r"(?:enclosure|rational bracket) \[([^,]+), ([^\]]+)\]",row["note"])
        interval_result = "absent"
        if match:
            lo,hi = map(Q,match.groups())
            if lo <= x.lo and x.hi <= hi:
                interval_result = "contains true value"
            elif hi < x.lo or lo > x.hi:
                interval_result = "EXCLUDES true value"
                bad.append(key)
            else:
                interval_result = "undetermined"
            if key in source_bounds:
                raw=source_bounds[key]
                sides=[]
                if lo>raw.lo:
                    sides.append("lower endpoint moves inward")
                if hi<raw.hi:
                    sides.append("upper endpoint moves inward")
                if sides:
                    inward.append((key,", ".join(sides)))
        say(f"{key}: {bounds(x)}; display={disp}; display agrees={correct}; published interval={interval_result}")
        allrows.append(dict(key=key,low=str(x.lo),high=str(x.hi),outward_decimal=bounds(x),
            display=disp,display_agrees=correct,published_interval=interval_result,
            reported_value=row["value"],value_error=bounds(I(row["value"])-x)))
    say(f"ROWS {len(rows)}; RECOMPUTED {len(allrows)}; DISPLAY DIFFERENCES {len(differences)}: {differences}")
    say(f"PUBLISHED INTERVALS THAT EXCLUDE THE VALUE {len(bad)}: {bad}")
    say("NEAREST SERIALIZATION OF THE TWELVE WIDE BRACKETS: "+str(inward))
    (HERE/"xp1_numbers.log").write_text("\n".join(log)+"\n")
    with (HERE/"xp1_registry_recompute.csv").open("w",newline="") as out:
        writer = csv.DictWriter(out,fieldnames=list(allrows[0]))
        writer.writeheader()
        writer.writerows(allrows)
    paths = [TEAM/"proofs/P1_core.tex",TEAM/"proofs/build/P1_core.pdf",TEAM/"memos/P1_core.md",TEAM/"registry/P1_core.csv"]
    paths += sorted((TEAM/"scripts/P1_core").glob("*"))
    (HERE/"checked_sources.sha256").write_text("".join(hashlib.sha256(path.read_bytes()).hexdigest()+"  "+str(path)+"\n" for path in paths if path.is_file()))


if __name__ == "__main__":
    main()
