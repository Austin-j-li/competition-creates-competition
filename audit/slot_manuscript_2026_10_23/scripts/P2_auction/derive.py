"""Print auction outcomes and finite interval certificates for R6 and R9.

Run: .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/P2_auction/derive.py
All economic inputs enter as exact fractions. Irrational calculations use
outward intervals at 60 decimal digits. Decimal midpoints serve display only.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from decimal import Decimal, localcontext, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
from typing import Any

import mpmath
from mpmath import iv, mp

mp.dps = 80
iv.dps = 60
HERE = Path(__file__).resolve().parent
TEAM = HERE.parent.parent
SOURCE = "audit/slot_manuscript_2026_10_23/scripts/P2_auction/derive.py"
RUN_LOG = "audit/slot_manuscript_2026_10_23/scripts/P2_auction/run.log"
REGISTRY = TEAM / "registry/P2_auction.csv"
Q = (-1, 0, 1)


def I(x: Any) -> Any:
    """Convert exact rationals without a binary floating point step."""
    return iv.mpf(x.numerator) / x.denominator if isinstance(x, F) else iv.mpf(x)


def midpoint(x: Any) -> Any:
    if isinstance(x, F):
        return mp.mpf(x.numerator) / x.denominator
    return mp.mpf(x.mid.a)


def exact_endpoints(x: Any) -> tuple[F, F]:
    """Read the binary endpoints as exact rational numbers."""
    if isinstance(x, F):
        return x, x
    ends = []
    for negative, mantissa, exponent, _ in x._mpi_:
        value = F(mantissa) * F(2) ** exponent
        ends.append(-value if negative else value)
    return ends[0], ends[1]


def enclosure(x: Any, digits: int = 60) -> str:
    """Round the exact lower end down and the exact upper end up."""
    lower, upper = exact_endpoints(x)
    with localcontext() as context:
        context.prec = digits
        context.rounding = ROUND_FLOOR
        low = Decimal(lower.numerator) / Decimal(lower.denominator)
        context.rounding = ROUND_CEILING
        high = Decimal(upper.numerator) / Decimal(upper.denominator)
    return f"[{low}, {high}]"


def text_number(x: Any, digits: int = 6) -> str:
    return f"{float(midpoint(x)):.{digits}f}"


def sign(x: Any) -> str:
    if isinstance(x, F):
        return "positive" if x > 0 else "negative" if x < 0 else "zero"
    return "positive" if x.a > 0 else "negative" if x.b < 0 else "zero" if x.a == 0 and x.b == 0 else "unresolved"


def minimum(xs: tuple[Any, ...]) -> Any:
    if all(isinstance(x, F) for x in xs):
        return min(xs)
    vals = tuple(I(x) for x in xs)
    return iv.mpf([min(x.a for x in vals), min(x.b for x in vals)])


@dataclass(frozen=True)
class Law:
    lo: F
    hi: F


@dataclass(frozen=True)
class Objects:
    t: F
    g: F
    win: F
    admissible: F
    allocation: F


@dataclass(frozen=True)
class Auction:
    t0: F
    s0: F
    fp: F
    high: Objects
    low: Objects

    @property
    def delta(self) -> F:
        return self.high.t - self.low.t


@dataclass(frozen=True)
class Economy:
    name: str
    high: Law
    low: Law
    pi: F
    p: F
    rho: F
    cost: Any
    k: Any
    strengths: tuple[F, ...]


def point(value: F, p: F, r: F) -> Objects:
    """Integrate the realized auction payoff on its linear pieces."""
    cuts = sorted({F(0), r} | {x for x in (p, value) if 0 < x < r})
    total = [F(0)] * 5
    for left, right in zip(cuts[:-1], cuts[1:]):
        incumbent = (left + right) / 2
        old = incumbent if incumbent >= p else F(0)
        if value >= p:
            vals = (max(p, min(incumbent, value)),
                    max(value - max(p, incumbent), F(0)),
                    F(incumbent < value), F(1), max(old, value))
        else:
            vals = (p if incumbent >= p else F(0), F(0), F(0), F(0), old)
        for j, val in enumerate(vals):
            total[j] += (right - left) * val / r
    return Objects(*total)


def averaged(law: Law, p: F, r: F) -> Objects:
    """Integrate each class by the open cubic quadrature formula."""
    if law.lo == law.hi:
        return point(law.lo, p, r)
    cuts = sorted({law.lo, law.hi} | {x for x in (p, r) if law.lo < x < law.hi})
    total = [F(0)] * 5
    for left, right in zip(cuts[:-1], cuts[1:]):
        width = right - left
        for position, weight in ((F(1, 4), F(2, 3)), (F(1, 2), F(-1, 3)), (F(3, 4), F(2, 3))):
            obj = point(left + width * position, p, r)
            for j, val in enumerate((obj.t, obj.g, obj.win, obj.admissible, obj.allocation)):
                total[j] += width * weight * val / (law.hi - law.lo)
    return Objects(*total)


def auction(ec: Economy, r: F) -> Auction:
    fp = min(ec.p / r, F(1))
    return Auction(ec.p * (1 - fp), max((r*r - ec.p*ec.p) / (2*r), F(0)), fp,
                   averaged(ec.high, ec.p, r), averaged(ec.low, ec.p, r))


def gross(ob: Auction, mu: Any) -> Any:
    return I(ob.low.g) + mu * I(ob.high.g - ob.low.g)


def bounds(pi: F, u: Any) -> tuple[Any, Any]:
    z = I(pi)
    return z / (z + (1-z)*(1+u)), z*(1+u)/(1+z*u)


class Report:
    def __init__(self) -> None:
        self.rows: list[dict[str, str]] = []
        self.margins: list[dict[str, str]] = []
        self.enclosures: dict[str, dict[str, str]] = {}

    def emit(self, key: str, value: Any, note: str = "", display: str | None = None,
             status: str | None = None) -> Any:
        state = status or ("analytical" if isinstance(value, F) else "computer-assisted")
        raw = str(value) if isinstance(value, F) else mp.nstr(midpoint(value), 50)
        shown = display if display is not None else text_number(value)
        if not isinstance(value, F):
            lower, upper = exact_endpoints(value)
            self.enclosures[key] = dict(lo=str(lower), hi=str(upper))
        self.rows.append(dict(key=key, value=raw, display=shown, status=state,
                              source_script=SOURCE, run_log=RUN_LOG,
                              note=note + ("; enclosure=" + enclosure(value) if not isinstance(value, F) else "")))
        print(key, raw, "display=" + shown, "status=" + state,
              "enclosure=" + enclosure(value) if not isinstance(value, F) else "exact")
        return value

    def margin(self, key: str, value: Any, condition: str, group: str) -> Any:
        self.emit(key, value, condition)
        self.margins.append(dict(group=group, key=key, condition=condition,
                                 display=text_number(value, 10), sign=sign(value), enclosure=enclosure(value)))
        print("condition", condition, "sign", sign(value))
        return value

    def save(self) -> None:
        fields = ("key", "value", "display", "status", "source_script", "run_log", "note")
        with REGISTRY.open("w", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self.rows)
        (HERE / "EX_exact_enclosures.json").write_text(json.dumps(self.enclosures, indent=2) + "\n")
        with (HERE / "margins.csv").open("w", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=tuple(self.margins[0]))
            writer.writeheader()
            writer.writerows(self.margins)
        macros = [r"\providecommand{\reg}[1]{\ifcsname p2number@#1\endcsname\csname p2number@#1\endcsname\else\textbf{??#1}\fi}"]
        macros.extend(r"\expandafter\def\csname p2number@" + row["key"] + r"\endcsname{" + row["display"] + "}" for row in self.rows)
        (HERE / "numbers.tex").write_text("\n".join(macros) + "\n")
        manifest = dict(date=datetime.now(timezone.utc).isoformat(), source_commit="01bd5d6",
                        python=platform.python_version(), mpmath=mpmath.__version__, interval_digits=iv.dps,
                        inputs="Economy declarations in derive.py; beta=58931/200000; u=exp(1)-1",
                        method="Exact piecewise integration; outward interval arithmetic; fixed-candidate payoff tables",
                        equilibrium_definition="P1_core.tex: zero-cost preparation fixed at every price; C1/CM apply to high-cost ties",
                        scope="R6 and R9; no global reserve optimization")
        manifest["P1_core_sha256_at_read"] = hashlib.sha256((TEAM / "proofs/P1_core.tex").read_bytes()).hexdigest()
        files = (Path(__file__), HERE / "margins.csv", HERE / "numbers.tex", REGISTRY)
        manifest["sha256"] = {str(p.relative_to(TEAM)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def cases() -> tuple[Economy, ...]:
    atom = lambda x: Law(F(x), F(x))
    common = (F(1, 2), F(1, 4))
    return (
        Economy("base", atom(10), atom(1), F(1, 2), *common, F(6), F(1, 50), (F(6, 5), F(3), F(18, 5))),
        Economy("moderate", atom(2), atom(1), F(1, 2), *common, F(89, 100), F(1, 500), (F(21, 20), F(3, 2))),
        Economy("bands", Law(F(199, 20), F(201, 20)), Law(F(19, 20), F(21, 20)), F(1, 2), *common, F(6), F(1, 50), (F(6, 5), F(3), F(18, 5))),
        Economy("ex_a", atom(10), atom(1), F(3, 10), *common, F(9, 2), F(1, 100), (F(11, 10), F(3), F(18, 5))),
        Economy("ex_b", atom(10), atom(1), F(7, 10), *common, F(36, 5), F(1, 100), (F(11, 10), F(3), F(18, 5))),
        Economy("ex_c", Law(F(1), F(19)), Law(F(3, 5), F(7, 5)), F(7, 10), *common, F(67, 10), F(1, 50), (F(1), F(9, 2), F(11, 2))),
        Economy("ex_d", atom(10), atom(1), F(7, 10), *common, F(67, 10), F(1, 50), (F(1), F(9, 2), F(11, 2))),
    )


def node(report: Report, ec: Economy, r: F, index: str, lam: Any, beta: F,
         orders: tuple[int, int], pattern: tuple[int, int, int], hidden: bool = False) -> dict[str, Any]:
    ob = auction(ec, r)
    prefix = "p2_" + ec.name + "_" + index
    pi, rho = I(ec.pi), I(ec.rho)
    bases = ((1-lam)*I(beta), (1-lam)*(1-2*I(beta)), (1-lam)*I(beta))
    ah = tuple(bases[i] + (lam if orders[0] == q else 0) for i, q in enumerate(Q))
    al = tuple(bases[i] + (lam if orders[1] == q else 0) for i, q in enumerate(Q))
    mass = tuple(pi*h + (1-pi)*l for h, l in zip(ah, al))
    mu = tuple(pi*h/d for h, d in zip(ah, mass))
    entry = tuple(rho + (1-rho)*x for x in pattern)
    price = tuple(I(ob.t0)+e*(I(ob.low.t-ob.t0)+I(ob.delta)*m) for e, m in zip(entry, mu))
    for name, val in (("t0", ob.t0), ("th", ob.high.t), ("tl", ob.low.t), ("gh", ob.high.g), ("gl", ob.low.g),
                      ("wh", ob.high.win), ("delta", ob.delta)):
        report.emit(prefix + "_" + name, val, "Exact auction integral")
    for i, suffix in enumerate(("minus", "zero", "plus")):
        for name, val in (("mass", mass[i]), ("mu", mu[i]), ("price", price[i]), ("entry", entry[i])):
            report.emit(prefix+"_"+name+"_"+suffix, val)
        belief = pi if hidden else mu[i]
        report.margin(prefix+"_cost_sign_"+suffix, gross(ob, belief)-I(ec.cost), "B(belief)-c_H; sign matches entry pattern", ec.name)
        report.margin(prefix+"_low_profit_"+suffix, gross(ob, belief),
                      "B(belief)>0 gives strict zero-cost entry" if ob.high.g > 0 else "B=0; fixed zero-cost preparation", ec.name)
    report.emit(prefix+"_prior_cost_margin",I(ec.cost)-gross(ob,pi),"c_H-B(pi)")
    for cls, tj, chosen in (("h", ob.high.t, orders[0]), ("l", ob.low.t, orders[1])):
        pays = tuple(q*(I(ob.t0)+entry[i]*I(tj-ob.t0)-price[i])-I(ec.k)*abs(q) for i, q in enumerate(Q))
        for q, val in zip(Q, pays):
            report.emit(prefix+"_pay_"+cls+"_"+str(q+1), val, "Fixed candidate prices and entry")
        advantage = minimum(tuple(pays[chosen+1]-pays[q+1] for q in Q if q != chosen))
        report.margin(prefix+"_choice_"+cls, advantage, "Prescribed order payoff minus each deviation payoff", ec.name)
    eh = sum(h*e for h, e in zip(ah, entry))
    el = sum(l*e for l, e in zip(al, entry))
    total = pi*eh+(1-pi)*el
    revenue = I(ob.t0)+pi*eh*I(ob.high.t-ob.t0)+(1-pi)*el*I(ob.low.t-ob.t0)
    allocation = I(ob.s0)+pi*eh*I(ob.high.allocation-ob.s0)+(1-pi)*el*I(ob.low.allocation-ob.s0)
    paid_cost = (1-rho)*I(ec.cost)*sum(d*x for d, x in zip(mass, pattern))
    surplus = allocation-paid_cost
    adm = pi*eh*I(ob.high.admissible)+(1-pi)*el*I(ob.low.admissible)
    two = (1-I(ob.fp))*adm
    sale = 1-I(ob.fp)+adm-two
    outcome = dict(entry=total, ownership=pi*eh*I(ob.high.win), proceeds=revenue, surplus=surplus,
                   admissible=adm, sale=sale, two=two, eh=eh, el=el, paid_cost=paid_cost)
    for name, val in outcome.items():
        report.emit(prefix+"_"+name, val)
    return dict(outcome, ob=ob, mu=mu, price=price, em=entry, mass=mass)


def main() -> None:
    report = Report()
    e = iv.exp(I(F(1)))
    u, beta = e-1, F(58931, 200000)
    lam = u*I(beta)/(1+u*I(beta))
    b, b0 = (1-lam)*I(beta), (1-lam)*(1-2*I(beta))
    m, M = bounds(F(1, 2), u)
    print("R6/R9 outward interval certificate; beta is the exact declared decimal; source commit 01bd5d6")
    for key, value, display in (("u_B", u, None), ("beta_B", beta, "0.294655"), ("lambda_B", lam, None),
                                ("b_B", b, None), ("M_half_B", M, None), ("m_half_B", m, None)):
        report.emit(key, value, note="Declared primitive 1+u=exp(1)" if key=="u_B" else "",
                    display=display, status="input" if key in ("u_B","beta_B") else None)
    report.margin("margin_p2_beta_lower_B", beta, "beta>0", "domain")
    report.margin("margin_p2_beta_upper_B", F(1, 3)-beta, "beta<1/3", "domain")
    report.margin("margin_p2_lambda_lower_B", lam, "lambda>0", "domain")
    report.margin("margin_p2_lambda_upper_B", 1-lam, "lambda<1", "domain")
    report.margin("margin_p2_bplus_B", b+lam-I(F(1, 2)), "b+lambda>1/2 for the older ownership sufficient condition", "domain")
    nodes: dict[tuple[str, int], dict[str, Any]] = {}
    for ec in cases():
        for label, value in (("pi",ec.pi),("p",ec.p),("rho",ec.rho),("cost",ec.cost),("k",ec.k),
                             ("high_lo",ec.high.lo),("high_hi",ec.high.hi),("low_lo",ec.low.lo),("low_hi",ec.low.hi)):
            report.emit("p2_input_"+ec.name+"_"+label,value,display=str(value),status="input")
        for i,r in enumerate(ec.strengths):
            report.emit("p2_input_"+ec.name+"_r"+str(i),r,display=str(r),status="input")
        lo, hi = bounds(ec.pi, u)
        obs = tuple(auction(ec, r) for r in ec.strengths)
        margins = dict(weak_cost=I(ec.cost)-gross(obs[0], I(ec.pi)), weak_trade=I(ec.k)-I(obs[0].delta),
                       strong_top=gross(obs[1], hi)-I(ec.cost), strong_prior=I(ec.cost)-gross(obs[1], I(ec.pi)),
                       high_floor=I(ec.rho*obs[1].delta)*(1-hi)-I(ec.k), low_floor=I(ec.rho*obs[1].delta)*lo-I(ec.k),
                       ownership=(I(ec.rho)+(1-I(ec.rho))*(b+lam))*I(obs[1].high.win)-I(ec.rho*obs[0].high.win))
        if len(obs) == 3:
            margins.update(collapse=I(ec.cost)-gross(obs[2], hi), collapse_high=I(ec.rho*obs[2].delta)*(1-hi)-I(ec.k),
                           collapse_low=I(ec.rho*obs[2].delta)*lo-I(ec.k))
        for label, value in margins.items():
            report.margin("margin_p2_"+ec.name+"_"+label+"_B", value, label, ec.name)
        for i, r in enumerate(ec.strengths):
            pattern = (0, 0, 1) if i == 1 and ec.name != "ex_d" else (0, 0, 0)
            nodes[(ec.name, i)] = node(report, ec, r, "r"+str(i), lam, beta, (0, 0) if i == 0 else (1, -1), pattern)
    base = cases()[0]
    for label,value in (("p",base.p),("low_above_p",base.low.lo-base.p),
                        ("r0_above_low",base.strengths[0]-base.low.hi),
                        ("r1_above_r0",base.strengths[1]-base.strengths[0]),
                        ("r2_above_r1",base.strengths[2]-base.strengths[1]),
                        ("high_above_r2",base.high.lo-base.strengths[2]),
                        ("pi",base.pi),("one_minus_pi",1-base.pi),
                        ("rho",base.rho),("one_minus_rho",1-base.rho),("k",base.k),("cost",base.cost),
                        ("class_gap",base.high.lo-base.low.lo)):
        report.margin("margin_p2_primitive_"+label+"_B",value,"Positive primitive or support distance: "+label,"primitives")
    for i, key in enumerate(("tau_r0", "tau_r1", "tau_r2")):
        ob = auction(base, base.strengths[i])
        report.emit(key, (base.cost-ob.low.g)/(ob.high.g-ob.low.g))
    tau1, tau2 = F(141, 200), F(4245, 5804)
    lo, hi = I(tau1)/(1+u*(1-I(tau1))), I(tau2)/(1+u*(1-I(tau2)))
    report.emit("prior_lo_B", lo)
    report.emit("prior_hi_B", hi)
    report.margin("margin_p2_posterior_collapse_B",I(tau2)-M,"tau(r2)>M","base")
    for name, z in (("lo", lo), ("hi", hi)):
        ml, mh = z/(z+(1-z)*(1+u)), z*(1+u)/(1+z*u)
        report.margin("margin_p2_prior_"+name+"_trade_B", I(base.rho*auction(base, F(3)).delta)*minimum((ml, 1-mh))-I(base.k), "Trade floor at the stated prior endpoint", "prior")
        report.margin("margin_p2_prior_"+name+"_weak_B", I(base.cost)-gross(auction(base, F(6,5)), z), "Weak cost margin at the stated prior endpoint", "prior")
    report.emit("p2_prior_trade_lo", e/(9+e))
    report.emit("p2_prior_trade_hi", 9/(9+e))
    report.emit("p2_prior_fixed_k_lo", 3*e/(22+3*e))
    report.emit("p2_prior_fixed_k_hi", 22/(22+3*e))
    ob0 = auction(base, F(6,5))
    report.emit("p2_prior_cost_hi", (base.cost-ob0.low.g)/(ob0.high.g-ob0.low.g))
    for prior,tag in ((F(3,10),"three_tenths"),(F(7,10),"seven_tenths")):
        pm,pM=bounds(prior,u)
        floor=I(F(1,4))*minimum((pm,1-pM))*I(F(2,3))
        report.emit("p2_other_prior_"+tag+"_trade_upper",floor)
        report.margin("p2_other_prior_"+tag+"_trade_window",floor-I(F(1,60)),"Nonempty trade-cost window at benchmark strengths","prior")
        report.margin("p2_other_prior_"+tag+"_weak_cost",6-gross(auction(base,F(6,5)),I(prior)),"Fixed high cost minus weak prior profit","prior")
        report.margin("p2_other_prior_"+tag+"_top_cost",gross(auction(base,F(3)),pM)-6,"Strong upper profit minus the fixed high cost","prior")
        fixed=replace(base,name="fixed_prior_"+tag,pi=prior)
        for j,r in enumerate(fixed.strengths):
            pattern=(0,0,0) if prior==F(3,10) else (1,1,1) if j==0 else (0,0,1)
            node(report,fixed,r,"r"+str(j),lam,beta,(0,0) if j==0 else (1,-1),pattern)
    cap=I((base.cost-ob0.low.g)/(ob0.high.g-ob0.low.g))
    for name,value in (("lower_order",lo-3*e/(22+3*e)),("upper_order",22/(22+3*e)-cap),
                       ("window_order",cap-lo)):
        report.margin("margin_p2_prior_"+name+"_B",value,"Endpoint order for the two-strength prior interval","prior")
    report.emit("u_lo", F(82,59))
    report.emit("u_hi", F(2686,1559))
    report.margin("margin_p2_u_lo_B", u-I(F(82,59)), "u>82/59", "domain")
    report.margin("margin_p2_u_hi_B", I(F(2686,1559))-u, "u<2686/1559", "domain")
    print("CONSTRUCTIVE SEQUENCE: original cost recipe, with every member retained")
    for ratio in (F(21,20), F(11,10), F(5,4), F(3,2), F(2)):
        name = str(ratio.numerator)+"_"+str(ratio.denominator)
        for n in range(1,21):
            gap = ratio-1
            d = gap/F(2)**n
            r0, r1 = 1+d*d/gap, 1+d
            ec = replace(base, name="seq_"+name, high=Law(ratio, ratio), strengths=(r0,r1))
            a0, a1 = auction(ec,r0), auction(ec,r1)
            cost = (gross(a0,I(F(1,2)))+gross(a1,M))/2
            k = (I(a0.delta)+I(F(1,8)*a1.delta)*m)/2
            mar = (cost-gross(a0,I(F(1,2))), gross(a1,M)-cost,
                   k-I(a0.delta), I(F(1,4)*a1.delta)*m-k)
            for j,v in enumerate(mar):
                report.margin("p2_seq_"+name+"_n"+str(n)+"_margin"+str(j),v,"Construction margin "+str(j),"sequence")
            if all(sign(v)=="positive" for v in mar):
                stem="p2_seq_"+name
                for label, val, shown in (("ratio",ratio,str(ratio)),("n",F(n),str(n)),("r0",r0,None),("r1",r1,None),("k",k,mp.nstr(midpoint(k),12)),("cost",cost,None)):
                    report.emit(stem+"_"+label,val,display=shown)
                node(report, replace(ec,cost=cost,k=k),r0,"weak",lam,beta,(0,0),(0,0,0))
                node(report, replace(ec,cost=cost,k=k),r1,"strong",lam,beta,(1,-1),(0,0,1))
                break
    seen = nodes[("base",1)]
    hidden = node(report, base,F(3),"hidden",lam,beta,(1,-1),(0,0,0),True)
    dR, dW = seen["proceeds"]-hidden["proceeds"], seen["surplus"]-hidden["surplus"]
    G = lam*I(F(2,3))*(I(F(1,2))*(1-M)+I(F(1,2))*I(base.rho)*m)
    for label,val in (("proceeds_gain",dR),("surplus_gain",dW),("gross_transfer",G),
                      ("gross_conditional",G/lam),("break_even",dR/G),("trade_resource_cost",lam*I(base.k))):
        report.emit("p2_access_"+label,val)
    outside = replace(base,name="outside",cost=F(12,5))
    outseen=node(report,outside,F(3),"seen",lam,beta,(1,-1),(0,1,1))
    outhid=node(report,outside,F(3),"hidden",lam,beta,(1,-1),(1,1,1),True)
    for label in ("proceeds","surplus"):
        report.emit("p2_outside_"+label+"_gain",outseen[label]-outhid[label])
    reserve_nodes: dict[tuple[str,str,int], dict[str,Any]] = {}
    for name, ec, highp in (("points",base,F(101,100)),("bands",cases()[2],F(11,10))):
        for ptag,p in (("base",F(1,2)),("exclude",highp),("deter",F(31,20))):
            pec=replace(ec,name="reserve_"+name+"_"+ptag,p=p)
            for i,r in enumerate((F(6,5),F(3))):
                full=not(ptag=="base" and i==0)
                pattern=(0,0,1) if full and not(ptag=="deter" and i==1) else (0,0,0)
                ob=auction(pec,r)
                report.margin("p2_reserve_"+name+"_"+ptag+"_r"+str(i)+"_global", I(pec.rho*ob.delta)*m-I(pec.k) if full else I(pec.k)-I(ob.delta),"Global order bound", "reserve")
                reserve_nodes[(name,ptag,i)] = node(report,pec,r,"r"+str(i),lam,beta,(1,-1) if full else (0,0),pattern)
        for i in range(2):
            report.margin("margin_p2_reserve_"+name+"_exclude_gain"+str(i)+"_B",
                          reserve_nodes[(name,"exclude",i)]["proceeds"]-reserve_nodes[(name,"base",i)]["proceeds"],
                          "Exclusion reserve raises proceeds","reserve")
    ph=iv.sqrt(6*(10-6/M)-9)
    report.emit("p2_reserve_ph",ph)
    report.emit("p2_reserve_weak_top",10-6/M)
    report.margin("margin_p2_ph_weak_B",ph-I(F(6,5)),"p_H>r_0", "reserve")
    report.margin("margin_p2_deter_lower_B",I(F(31,20))-ph,"31/20>p_H", "reserve")
    report.margin("margin_p2_deter_upper_B",10-6/M-I(F(31,20)),"31/20<h-c_H/M", "reserve")
    report.margin("margin_p2_reserve_admissible_top_B",M*I(F(413,50))-6,
                  "Strong upper profit exceeds c_H even at p=r0", "reserve")
    report.margin("margin_p2_reserve_uniform_weak_B",I(F(1,4))*m*I(F(17,20))-I(F(1,50)),
                  "Uniform weak trade bound when the incumbent remains admissible", "reserve")
    report.margin("margin_p2_reserve_uniform_strong_B",I(F(1,4))*m-I(F(1,50)),
                  "Uniform strong trade bound when the weak incumbent remains admissible", "reserve")
    delta_ph=I(F(3,2))+ph*ph/6-ph*(1-ph/3)
    report.margin("margin_p2_ph_trade_B",I(F(1,4))*m*delta_ph-I(F(1,50)),
                  "All-profile trade bound at the exact reserve equality","reserve")
    report.margin("margin_p2_ph_prior_B",6-3/M,"Prior profit below cost at p_H","reserve")
    ph_entry=(I(F(1,4)),I(F(1,4)),I(F(1)))
    ph_mu=(m,I(F(1,2)),M)
    t0_ph=ph*(1-ph/3)
    th_ph=I(F(3,2))+ph*ph/6
    ph_prices=tuple(t0_ph+ee*delta_ph*mm for ee,mm in zip(ph_entry,ph_mu))
    for i,price in enumerate(ph_prices):
        report.emit("p2_ph_price"+str(i),price)
    for cls,tj,chosen in (("h",th_ph,2),("l",t0_ph,0)):
        pays=tuple(q*(t0_ph+ph_entry[i]*(tj-t0_ph)-ph_prices[i])-I(F(1,50))*abs(q) for i,q in enumerate(Q))
        for i,pay in enumerate(pays):
            report.emit("p2_ph_"+cls+"_pay"+str(i),pay)
        report.margin("p2_ph_"+cls+"_choice",minimum(tuple(pays[chosen]-pays[i] for i in range(3) if i!=chosen)),
                      "Strict choice at p_H under C1","reserve")
    for label, laws in (("points",base),("bands",cases()[2])):
        for i,r in enumerate((F(6,5),F(3))):
            pec=replace(laws,p=F(31,20))
            ob=auction(pec,r)
            eh=I(F(1,4))+(1-I(F(1,4)))*(b+lam) if i==0 else I(F(1,4))
            el=I(F(1,4))+(1-I(F(1,4)))*b if i==0 else I(F(1,4))
            rev=I(ob.t0)+I(F(1,2))*(eh*I(ob.high.t-ob.t0)+el*I(ob.low.t-ob.t0))
            report.margin("margin_p2_reserve_"+label+"_rev"+str(i)+"_B",rev-nodes[(laws.name,i)]["proceeds"],"Proceeds at 31/20 exceed proceeds at 1/2", "reserve")
    endpoint=replace(base,name="endpoint",p=F(10))
    node(report,endpoint,F(3),"r1",lam,beta,(1,-1),(0,0,0))
    band_endpoint=replace(cases()[2],name="band_endpoint",p=F(201,20))
    node(report,band_endpoint,F(3),"r1",lam,beta,(0,0),(0,0,0))
    many(report,lam,beta,b,b0)
    for index in range(101):
        eta=F(index,100)
        etag=str(eta.numerator)+"_"+str(eta.denominator)
        for j,r in enumerate((F(6,5),F(3))):
            excess=(r-1)**2/(2*r)
            for label,value in (("spread",eta*9+(1-2*eta)*excess),("gh",(1-eta)*(10-r/2)),("gl",(1-eta)/(2*r))):
                report.emit("p2_payment_"+etag+"_r"+str(j)+"_"+label,value)
    for name,value in (("spread_a0",F(1,60)),("spread_b0",F(269,30)),("spread_a1",F(2,3)),
                       ("spread_b1",F(23,3)),("high0",F(47,5)),("high1",F(17,2)),
                       ("low0",F(5,12)),("low1",F(1,6)),("excess_change",F(13,20))):
        report.emit("p2_payment_coefficient_"+name,value,display=str(value))
    report.save()


def many(report: Report, lam: Any, beta: F, b: Any, b0: Any) -> None:
    prior=(I(F(1,4)),I(F(1,2)),I(F(1,4)))
    w=(1+2*b0+lam)/2
    report.emit("p2_many_weight",w)
    report.margin("margin_p2_many_w_lower_B",w,"w>0","many")
    report.margin("margin_p2_many_w_upper_B",1-w,"w<1","many")
    report.margin("margin_p2_many_beta_B",beta-F(1,4),"beta>1/4","many")
    for perturb in (F(0),F(-1,1000),F(1,1000)):
        ww=w+I(perturb)
        ts=(I(F(1)),1+I(F(49,16))*ww,I(F(65,16)))
        stem="p2_many" if perturb==0 else "p2_many_"+("down" if perturb<0 else "up")
        means=[]
        for qi,q in enumerate(Q):
            base=b0 if q==0 else b
            joint=tuple(prior[j]*(base+(lam if j==qi else 0)) for j in range(3))
            d=sum(joint)
            post=tuple(x/d for x in joint)
            mean=sum(x*t for x,t in zip(post,ts))
            means.append(mean)
            for j,x in enumerate(post):
                report.emit(stem+"_q"+str(qi)+"_mu"+str(j),x)
            report.emit(stem+"_q"+str(qi)+"_mean",mean)
            report.emit(stem+"_q"+str(qi)+"_price",I(F(7,8))+I(F(1,4))*(mean-I(F(7,8))))
        report.emit(stem+"_mean_zero_minus_plus",F(0) if perturb==0 else means[1]-means[2],
                    "Exact equality at the declared weight; perturbations use outward intervals")
        for j,t in enumerate(ts):
            pays=tuple(q*I(F(1,4))*(t-means[i])-I(F(1,8))*abs(q) for i,q in enumerate(Q))
            for i,val in enumerate(pays):
                report.emit(stem+"_class"+str(j)+"_pay"+str(i),val)
            report.margin(stem+"_choice"+str(j),minimum(tuple(pays[j]-pays[i] for i in range(3) if i!=j)),"Prescribed payoff minus each deviation payoff","many")
    report.margin("p2_many_high_cost",F(10)-F(95,16),"Every class gross profit is below c_H","many")
    report.margin("p2_many_low_cost",(I(F(1,4))*b/(b0+lam/2))*I(F(95,16)),"A common positive lower bound on gross profit at every price","many")
    # Four separated classes give a concrete strict group comparison.
    vals=(F(1),F(1001,1000),F(9999,1000),F(10))
    rho,k,cost=F(1,4),F(1,50),F(6)
    ts0=tuple(point(v,F(1,2),F(6,5)).t for v in vals)
    ob1=tuple(point(v,F(1,2),F(3)) for v in vals)
    means=[]
    for mask in range(16):
        weights=tuple(1+(lam/b if mask & (1<<j) else 0) for j in range(4))
        means.append(sum(x*I(ob.t) for x,ob in zip(weights,ob1))/sum(weights))
    lower=minimum(tuple(means))
    upper=-minimum(tuple(-x for x in means))
    gamma=minimum((I(min(ob.t for ob in ob1[2:]))-upper,lower-I(max(ob.t for ob in ob1[:2]))))
    report.emit("p2_groups_gamma",gamma)
    report.margin("p2_groups_weak_range",k-(max(ts0)-min(ts0)),"Weak proceeds range below k","groups")
    report.margin("p2_groups_trade",I(rho)*gamma-I(k),"rho*gamma>k","groups")
    g0=sum(point(v,F(1,2),F(6,5)).g for v in vals)/4
    report.margin("p2_groups_weak_cost",cost-g0,"Weak prior profit below c_H","groups")
    gl=sum(ob.g for ob in ob1[:2])/2
    gh=sum(ob.g for ob in ob1[2:])/2
    M=(b+lam)/(2*b+lam)
    report.margin("p2_groups_profit_gap",gh-gl,"High group has the higher mean profit","groups")
    report.margin("p2_groups_top",I(gl)+M*I(gh-gl)-I(cost),"Strong upper group posterior recruits","groups")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry-output", type=Path, default=REGISTRY,
                        help="Write a candidate registry to this path before publication.")
    REGISTRY = parser.parse_args().registry_output.resolve()
    main()
