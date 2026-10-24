"""Derive information controls, cost mixtures, and signal outcomes from primitives.

Run this file as a CLI. It prints rational interval enclosures and writes the
registry, a local LaTeX number file, the exact endpoints, and a run receipt.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import csv
import hashlib
import json
import platform
from datetime import datetime, timezone


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    @classmethod
    def point(cls, value):
        if isinstance(value, cls):
            return value
        value = F(value)
        return cls(value, value)

    def __add__(self, other):
        other = I(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -I(other)

    def __rsub__(self, other):
        return I(other) + -self

    def __mul__(self, other):
        other = I(other)
        ends = [self.lo * other.lo, self.lo * other.hi,
                self.hi * other.lo, self.hi * other.hi]
        return Interval(min(ends), max(ends))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = I(other)
        if other.lo <= 0 <= other.hi:
            raise ArithmeticError("A denominator interval contains zero")
        return self * Interval(1 / other.hi, 1 / other.lo)

    def __rtruediv__(self, other):
        return I(other) / self

    def sign(self):
        if self.lo > 0:
            return "positive"
        if self.hi < 0:
            return "negative"
        if self.lo == self.hi == 0:
            return "zero"
        return "contains_zero"


I = Interval.point
HERE = Path(__file__).resolve().parent
TEAM = HERE.parent.parent
SCRIPT = "audit/slot_manuscript_2026_10_23/scripts/P4_information/derive.py"
LOG = "audit/slot_manuscript_2026_10_23/scripts/P4_information/run.log"
ROWS = []
ENDPOINTS = {}


def decimal(value: F, rounding=None, digits=40):
    with localcontext() as ctx:
        ctx.prec = digits
        if rounding is not None:
            ctx.rounding = rounding
        return Decimal(value.numerator) / Decimal(value.denominator)


def record(key, value, note="", places=6, status=None):
    value = I(value)
    status = status or ("analytical" if value.lo == value.hi else "computer-assisted")
    display = f"{decimal((value.lo + value.hi) / 2):.{places}f}"
    lo = decimal(value.lo, ROUND_FLOOR)
    hi = decimal(value.hi, ROUND_CEILING)
    stored = str(value.lo) if value.lo == value.hi else str(decimal((value.lo + value.hi) / 2))
    ROWS.append(dict(key=key, value=stored, display=display, status=status,
                     source_script=SCRIPT, run_log=LOG, note=note))
    ENDPOINTS[key] = {"lo": str(value.lo), "hi": str(value.hi)}
    print(f"{key}: [{lo}, {hi}] sign={value.sign()} display={display}")
    return value


def indicator(gap):
    gap = I(gap)
    if gap.lo >= 0:
        return I(1)
    if gap.hi < 0:
        return I(0)
    raise ArithmeticError("An entry comparison is unresolved")


def clip(value):
    value = I(value)
    return Interval(min(F(1), max(F(0), value.lo)),
                    min(F(1), max(F(0), value.hi)))


def auction(r):
    r = I(r)
    p, ell, h = I("1/2"), I(1), I(10)
    t0 = p * (1-p/r)
    th = r/2 + p*p/(2*r)
    tl = ell-(ell*ell-p*p)/(2*r)
    return dict(r=r, t0=t0, th=th, tl=tl, gh=h-th, gl=ell-tl,
                D=th-tl, wh=th-t0, wl=tl-t0)


def B(z, mu):
    return z["gl"] + mu * (z["gh"]-z["gl"])


def phi(mu, d, positive):
    weight = d if positive else 1-d
    return weight*mu / (weight*mu+(1-weight)*(1-mu))


N = 60
partial = sum((F(1, factorial(n)) for n in range(N+1)), F(0))
EXP = Interval(partial, partial + F(1, N*factorial(N)))
U = EXP-1
BETA = I("0.294655")
LAM = U*BETA/(1+U*BETA)
b = BETA/(1+U*BETA)
c = (1-2*BETA)/(1+U*BETA)
m = 1/(1+EXP)
M = EXP/(1+EXP)


def profile(tag, r, rho, high_cost, fee, s, t, accuracy=1,
            buyer_accuracy="1/2", atomless=False, hidden=False):
    """Print the explicit tuple and every order payoff against its fixed prices."""
    z = auction(r)
    rho, high_cost, fee = I(rho), I(high_cost), I(fee)
    a, d = I(accuracy), I(buyer_accuracy)
    s, t = I(s), I(t)
    laws = {1: (b+s,b), 0: (c+LAM-s,c+LAM-t), -1: (b,b+t)}
    rows = {}
    ehbar, elbar = I(0), I(0)
    print("PROFILE", tag)
    record(tag+"_buy_rate", s/LAM, "Conditional probability of a unit buy after the positive signal")
    record(tag+"_sell_rate", t/LAM, "Conditional probability of a unit sale after the negative signal")
    for q in (-1,0,1):
        plus, minus = laws[q]
        ph, pl = a*plus+(1-a)*minus, (1-a)*plus+a*minus
        mu = ph/(ph+pl)
        nu = plus/(plus+minus)
        emu = I("1/2") if hidden else mu
        if atomless:
            gp = B(z, emu)
            e = rho*clip(gp/I("1/5"))+(1-rho)*clip((gp-I("59/10"))/I("1/5"))
            eh, el = e, e
        else:
            ip = indicator(B(z, phi(emu,d,True))-high_cost)
            im = indicator(B(z, phi(emu,d,False))-high_cost)
            eh = rho+(1-rho)*(d*ip+(1-d)*im)
            el = rho+(1-rho)*((1-d)*ip+d*im)
        price = z["t0"]+mu*eh*z["wh"]+(1-mu)*el*z["wl"]
        ehbar += ph*eh
        elbar += pl*el
        rows[q] = (mu,nu,eh,el,price)
        suffix = {-1:"sell",0:"zero",1:"buy"}[q]
        for name, val in (("mu",mu),("nu",nu),("price",price),("eh",eh),("el",el)):
            record(tag+"_"+suffix+"_"+name, val, "Candidate tuple at the stated order")
        if not atomless:
            for y, positive in (("yp",True),("ym",False)):
                gap = B(z,phi(emu,d,positive))-high_cost
                record(tag+"_"+suffix+"_"+y+"_entry_gap",gap,"Gross profit minus high preparation cost",9)
        for signal, belief in (("tp",a),("tm",1-a)):
            v = z["t0"]+belief*eh*z["wh"]+(1-belief)*el*z["wl"]
            utility = q*(v-price)-abs(q)*fee
            record(tag+"_"+suffix+"_"+signal+"_payoff",utility,"Order payoff against fixed prices and entry",9)
    entry = (ehbar+elbar)/2
    own = ehbar/2
    revenue = z["t0"]+(ehbar*z["wh"]+elbar*z["wl"])/2
    record(tag+"_entry",entry,"Unconditional preparation probability")
    record(tag+"_own",own,"Probability of acquisition by class H; h exceeds r")
    record(tag+"_proceeds",revenue,"Expected target proceeds")
    return entry, own, revenue, rows


def signal_margins(tag, r0, r1, rho, cost, fee, a, d, print_all=True):
    a,d,rho,cost,fee=map(I,(a,d,rho,cost,fee))
    z0,z1=auction(r0),auction(r1)
    muhi=1-a+(2*a-1)*M
    out={
        "private":cost-B(z0,d),
        "joint":B(z1,phi(muhi,d,True))-cost,
        "weak":fee-(2*a-1)*(z0["D"]+(1-rho)*(2*d-1)*z0["wh"]),
        "strong":(2*a-1)*rho*m*z1["D"]-fee,
        "other_pair":cost-B(z1,phi(muhi,d,False)),
    }
    if print_all:
        for name,val in out.items():
            record("margin_"+tag+"_"+name,val,"R8 strict condition; other_pair excludes the unfavorable private signal",9)
    return out


def main():
    print("Exact rational interval calculation", datetime.now(timezone.utc).isoformat())
    print("Python",platform.python_version())
    print("e enclosure: sum from zero through N, remainder less than 1/(N N!)")
    record("p4_exp_terms",N,"Final Taylor index",0,"input")
    record("p4_e_lo",EXP.lo,"Exact lower bound on e",15)
    record("p4_e_hi",EXP.hi,"Exact upper bound on e",15)
    for name,val in (("u_B",U),("beta_B",BETA),("lambda_B",LAM),("b_B",b),
                     ("b0_B",c),("M_half_B",M),("m_half_B",m)):
        record(name,val,"Calibration B as declared in BRIEF section 3",6,"input" if name in ("beta_B","u_B") else None)
    primitives={"h":10,"ell":1,"p":"1/2","rho":"1/4","cH":6,
                "k":"1/50","pi":"1/2","r0":"6/5","r1":3,"r2":"18/5",
                "epsilon":"1/10","low_upper":"1/5","high_lower":"59/10","high_upper":"61/10",
                "signal_a":"7/10","signal_d":"3/4",
                "s_rho":"17/20","s_cost":"357/50","s_fee":"3/200",
                "s_r0":"11/10","s_r1":"23/10","valid_a":"19/20","valid_d":"101/200",
                "comp_a":"47/50","comp_d":"101/200"}
    for name,val in primitives.items():
        record("p4_input_"+name,I(val),"Exact primitive",6,"input")
    domains={"beta_lower":BETA,"beta_upper":I("1/3")-BETA,
             "lambda_lower":LAM,"lambda_upper":1-LAM,"pi_lower":I("1/2"),
             "pi_upper":I("1/2"),"rho_lower":I("1/4"),"rho_upper":I("3/4"),
             "reserve":I("1/2"),"ell_reserve":I("1/2"),"r0_ell":I("1/5"),
             "r1_r0":I("9/5"),"r2_r1":I("3/5"),"h_r2":I("32/5"),
             "cost":I(6),"fee":I("1/50"),"epsilon":I("1/10"),
             "band_width":I("1/5"),"band_lower":I("59/10"),
             "s_rho_lower":I("17/20"),"s_rho_upper":I("3/20"),
             "s_r0_ell":I("1/10"),"s_r1_r0":I("6/5"),"s_h_r1":I("77/10"),
             "s_cost":I("357/50"),"s_fee":I("3/200"),
             "signal_a_lower":I("1/5"),"signal_a_upper":I("3/10"),
             "signal_d_lower":I("1/4"),"signal_d_upper":I("1/4"),
             "signal_d_a":I("1/20"),"valid_a_lower":I("9/20"),
             "valid_a_upper":I("1/20"),"valid_d_lower":I("1/200"),"valid_d_upper":I("99/200"),
             "comp_a_lower":I("11/25"),"comp_a_upper":I("3/50"),
             "comp_d_lower":I("1/200"),"comp_d_upper":I("99/200")}
    for name,val in domains.items():
        record("margin_p4_domain_"+name,val,"Positive distance to a primitive boundary",9)
    rho,fee=I("1/4"),I("1/50")
    z0,z1,z2=auction("6/5"),auction(3),auction("18/5")
    for idx,z in enumerate((z0,z1,z2)):
        for name in ("t0","th","tl","gh","gl","D","wh","wl"):
            record(f"p4_r{idx}_{name}",z[name],"Auction formula from direct integration")
        record(f"tau_r{idx}",(6-z["gl"])/(z["gh"]-z["gl"]),"High cost threshold")
        record(f"margin_p4_gross_gap_r{idx}",z["gh"]-z["gl"],"Strict class profit gap",9)
    margins={"weak_trade":fee-z0["D"],"strong_trade":rho*m*z1["D"]-fee,
             "very_strong_trade":rho*m*z2["D"]-fee,
             "weak_prior":6-B(z0,I("1/2")),"strong_top":B(z1,M)-6,
             "return":6-B(z2,M),"weak_top":B(z0,M)-6,
             "strong_prior":6-B(z1,I("1/2")),
             "atomless_floor":B(z1,m)-I("1/5"),
             "atomless_weak":I("59/10")-B(z0,I("1/2")),
             "atomless_strong":B(z1,M)-I("61/10"),
             "atomless_return":I("59/10")-B(z2,M),
             "atomless_floor_r2":B(z2,m)-I("1/5"),
             "atomless_top_upper_r2":I("61/10")-B(z2,M),
             "atomless_top_lower_r2":B(z2,M)-I("59/10")}
    for name,val in margins.items():
        record("margin_p4_"+name+"_B",val,"Strict margin; atomless_return is negative for width 0.1",9)
    record("margin_p4_ownership_rise_B",(1-rho)*(b+LAM),"High-class entry gain when both ownership probabilities conditional on entry equal one",9)
    zero,full=I(0),LAM
    for tag,r,s,t in (("p4_base_r0","6/5",zero,zero),("p4_base_r1",3,full,full),
                      ("p4_base_r2","18/5",full,full),
                      ("p4_frozen_r0","6/5",full,full),("p4_frozen_r1",3,full,full)):
        outcome=profile(tag,r,"1/4",6,"1/50",s,t)
        if tag.startswith("p4_base_"):
            idx=tag[-1]
            entry = outcome[0] if idx == "1" else I("1/4")
            own = outcome[1] if idx == "1" else I("1/8")
            record({"0":"entry_r0","1":"entry_r1_B","2":"entry_r2"}[idx],entry,"Core benchmark entry; the floor is exactly rho")
            record({"0":"own_r0","1":"own_r1_B","2":"own_r2_B"}[idx],own,"Core benchmark H ownership; at the floor pi rho W_H = 1/8")
    for tag,r,s,t in (("p4_hidden_r0","6/5",zero,zero),("p4_hidden_r1",3,full,full)):
        profile(tag,r,"1/4",6,"1/50",s,t,hidden=True)
    record("p4_control_crossing_r0_r1",0,"Probability of a strict cost crossing")
    record("p4_control_crossing_r1_r2",(1-rho)*(b+LAM/2),"Probability of a strict cost crossing")
    # B_r(M) decreases strictly; rational endpoint signs enclose its unique root.
    ceiling_lo, ceiling_hi = F(3), F(18,5)
    for _ in range(180):
        midpoint = (ceiling_lo+ceiling_hi)/2
        gap = B(auction(midpoint),M)-6
        if gap.lo > 0:
            ceiling_lo = midpoint
        elif gap.hi < 0:
            ceiling_hi = midpoint
        else:
            break
    record("rC_B",Interval(ceiling_lo,ceiling_hi),"Unique frozen-order ceiling; B_r(M) = 6")
    record("p4_frozen_ceiling_lower_gap",B(auction(ceiling_lo),M)-6,"Positive endpoint of the root bracket",55)
    record("p4_frozen_ceiling_upper_gap",B(auction(ceiling_hi),M)-6,"Negative endpoint of the root bracket",55)
    record("p4_frozen_entry_below_ceiling",rho+(1-rho)*(b+LAM/2),"Frozen entry for 1 < r <= r_C under C1")
    record("p4_frozen_entry_above_ceiling",rho,"Frozen entry for r > r_C")
    for tag,r,s,t in (("p4_atomless_r0","6/5",zero,zero),
                      ("p4_atomless_r1",3,full,full),("p4_atomless_r2","18/5",full,full)):
        profile(tag,r,"1/4",6,"1/50",s,t,atomless=True)
    record("p4_atomless_max_width_floor_r2",6-B(z2,M),"A smaller half width preserves the floor at r2",9)
    record("p4_atomless_small_width","1/1000","Example half width for all three parts",6,"input")
    record("margin_p4_atomless_small_width_return",6-B(z2,M)-I("1/1000"),"Positive return margin with half width 0.001",9)
    signal_margins("p4_signal_s", "11/10","23/10","17/20","357/50","3/200","7/10","3/4")
    signal_margins("p4_signal_b", "6/5",3,"1/4",6,"1/50","7/10","3/4")
    signal_margins("p4_signal_valid_b", "6/5",3,"1/4",6,"1/50","19/20","101/200")
    signal_margins("p4_signal_comp_b", "6/5",3,"1/4",6,"1/50","47/50","101/200")
    zs0,zs1=auction("11/10"),auction("23/10")
    signal_control={
        "s_no_y_weak":I("3/200")-I("2/5")*zs0["D"],
        "s_no_y_strong":I("2/5")*I("17/20")*m*zs1["D"]-I("3/200"),
        "s_no_y_top_r0":I("357/50")-B(zs0,I("3/10")+I("2/5")*M),
        "s_no_y_top_r1":I("357/50")-B(zs1,I("3/10")+I("2/5")*M),
        "s_class_weak":I("3/200")-zs0["D"],
        "s_class_strong":I("17/20")*m*zs1["D"]-I("3/200"),
        "s_class_prior_r0":I("357/50")-B(zs0,I("1/2")),
        "s_class_top_r1":I("357/50")-B(zs1,M),
        "b_no_y_weak":fee-I("1/4")*I("2/5")*z0["D"]/2,
        "b_no_y_zero_gain":I("1/4")*I("2/5")*z1["D"]/2-fee,
        "b_no_y_full_loss":fee-I("1/4")*I("2/5")*z1["D"]*m,
    }
    for name,val in signal_control.items():
        record("margin_p4_"+name,val,"Strict margin for a signal information control",9)
    for regime,accuracy,buyer in (("signal","7/10","3/4"),("no_y","7/10","1/2"),("class",1,"1/2")):
        for idx,r in enumerate(("11/10","23/10")):
            profile(f"p4_s_{regime}_r{idx}",r,"17/20","357/50","3/200",
                    zero if idx==0 else full,zero if idx==0 else full,accuracy,buyer)
    for idx,r in enumerate(("6/5",3)):
        profile(f"p4_valid_b_r{idx}",r,"1/4",6,"1/50",zero if idx==0 else full,
                zero if idx==0 else full,"19/20","101/200")
    # The selected pair needs Y at strong strength; the earlier pair does not.
    for regime,accuracy,buyer in (("comp_b","47/50","101/200"),
                                  ("comp_b_no_y","47/50","1/2"),
                                  ("comp_b_class",1,"1/2"),
                                  ("valid_b_no_y","19/20","1/2")):
        for idx,r in enumerate(("6/5",3)):
            profile(f"p4_{regime}_r{idx}",r,"1/4",6,"1/50",
                    zero if idx==0 else full,zero if idx==0 else full,accuracy,buyer)
    comp_a, comp_d = I("47/50"), I("101/200")
    comp_mu = 1-comp_a+(2*comp_a-1)*M
    valid_mu = I("1/20")+I("9/10")*M
    added_controls = {
        "comp_b_no_y_weak":fee-(2*comp_a-1)*z0["D"],
        "comp_b_no_y_strong":(2*comp_a-1)*rho*m*z1["D"]-fee,
        "comp_b_no_y_prior_r0":6-B(z0,I("1/2")),
        "comp_b_no_y_top_r1":6-B(z1,comp_mu),
        "comp_b_class_weak":fee-z0["D"],
        "comp_b_class_strong":rho*m*z1["D"]-fee,
        "comp_b_class_prior_r0":6-B(z0,I("1/2")),
        "comp_b_class_prior_r1":6-B(z1,I("1/2")),
        "comp_b_class_top_r1":B(z1,M)-6,
        "valid_b_no_y_weak":fee-I("9/10")*z0["D"],
        "valid_b_no_y_strong":I("9/10")*rho*m*z1["D"]-fee,
        "valid_b_no_y_prior_r0":6-B(z0,I("1/2")),
        "valid_b_no_y_prior_r1":6-B(z1,I("1/2")),
        "valid_b_no_y_top_r1":B(z1,valid_mu)-6,
    }
    for name,val in added_controls.items():
        record("margin_p4_"+name,val,"Strict margin for a B signal control; class control has no Y",9)
    record("margin_p4_valid_b_no_y_top_exclusion",6-B(z1,valid_mu),
           "Negative: the earlier pair recruits without Y",9)
    # At the unchanged B primitives, the earlier signal pair has interior rates.
    s0=b*I("119/96")
    t1=b*I("4/3")
    out0=profile("p4_b_signal_r0","6/5","1/4",6,"1/50",s0,s0,"7/10","3/4")
    out1=profile("p4_b_signal_r1",3,"1/4",6,"1/50",full,t1,"7/10","3/4")
    profile("p4_b_no_y_r0","6/5","1/4",6,"1/50",zero,zero,"7/10","1/2")
    s_no_y=b*I("4/3")
    profile("p4_b_no_y_r1",3,"1/4",6,"1/50",s_no_y,s_no_y,"7/10","1/2")
    record("p4_b_no_y_r1_zero_gross",rho*I("2/5")*z1["D"]/2,
           "Gross return at zero orders; exceeds k, so I0 cannot select zero",9)
    record("p4_b_no_y_r1_full_gross",rho*I("2/5")*z1["D"]*m,
           "Gross return at full orders; below k, so I0 cannot select full orders",9)
    record("p4_b_signal_entry_change",out1[0]-out0[0],"Strong minus weak entry with the earlier signal pair")
    record("p4_b_signal_own_change",out1[1]-out0[1],"Strong minus weak ownership with the earlier signal pair")
    a,d=I("7/10"),I("3/4")
    mulo=1-a+(2*a-1)*m
    muhi=1-a+(2*a-1)*M
    dp0=I("311/1920")
    dp1=I("137/192")
    extra={"b_weak_all_yplus":B(z0,phi(mulo,d,True))-6,
           "b_weak_no_yminus":6-B(z0,phi(muhi,d,False)),
           "b_weak_zero_return":(2*a-1)*dp0/2-fee,
           "b_weak_full_loss":fee-(2*a-1)*m*dp0,
           "b_weak_rate_room":U-I("119/96"),
           "b_strong_buy":(2*a-1)*m*dp1-fee,
           "b_strong_prior_yplus":B(z1,d)-6,
           "b_strong_no_yminus":6-B(z1,phi(muhi,d,False)),
           "b_strong_threshold_floor_return":I("19/795")-fee,
           "b_strong_rate_room":U-I("4/3"),
           "b_strong_sale_public_gap":I("47/106")-I("21/50"),
           "b_strong_zero_yplus":B(z1,phi(out1[3][0][0],d,True))-6,
           "b_no_y_top_exclusion_r0":6-B(z0,muhi),
           "b_no_y_top_exclusion_r1":6-B(z1,muhi)}
    for name,val in extra.items():
        record("margin_p4_"+name,val,"Strict condition for the unchanged B signal tuple",9)
    # The original rectangular grid, with exact decimal accuracies.
    met=[]
    grid_rows=[]
    for ai in range(68,78):
        record(f"p4_accuracy_{ai}",F(ai,100),"Exact accuracy grid input",2,"input")
    for ai in range(68,73):
        for di in range(73,78):
            a,d=I(F(ai,100)),I(F(di,100))
            tag=f"p4_grid_{ai}_{di}"
            mg=signal_margins(tag,"11/10","23/10","17/20","357/50","3/200",a,d)
            yes=all(mg[name].lo>0 for name in ("private","joint","weak","strong"))
            record(tag+"_sufficient",int(yes),"One means all four sufficient inequalities are strict",0,"computer-assisted")
            if yes:
                met.append((ai,di))
                eh=I("17/20")+I("3/20")*d*(b+a*LAM)
                el=I("17/20")+I("3/20")*(1-d)*(b+(1-a)*LAM)
                record(tag+"_entry",(eh+el)/2,"Strong entry in the signal example with B slot parameters")
                record(tag+"_own",eh/2,"Strong H ownership in the signal example with B slot parameters")
                grid_rows.append((tag,ai,di))
    print("The sufficient grid pairs are",met)
    record("p4_grid_met_count",len(met),"Number of sufficient pairs on the declared grid",0)
    # Universal contradiction for d >= a at the unchanged B primitives.
    zmin=fee/(rho*m*z1["D"])
    weak_min=zmin*(z0["D"]+(1-rho)*zmin*z0["wh"])
    record("p4_b_signal_z_min",zmin,"Strong bound requires 2 a_T minus 1 above this level",9)
    record("margin_p4_b_d_ge_a_impossible",weak_min-fee,"Positive value contradicts the weak upper bound when d >= a_T",9)
    groups={
        "domain_b":["margin_p4_domain_"+name for name in domains if not name.startswith(("s_","signal_","valid_","comp_"))],
        "domain_s":["margin_p4_domain_"+name for name in domains if name.startswith(("s_","signal_"))],
        "domain_valid":["margin_p4_domain_"+name for name in domains if name.startswith("valid_")],
        "domain_comp":["margin_p4_domain_"+name for name in domains if name.startswith("comp_")],
        "signal_comp_b":["margin_p4_signal_comp_b_"+name for name in ("private","joint","weak","strong","other_pair")],
        "comp_b_no_y":["margin_p4_"+name for name in added_controls if name.startswith("comp_b_no_y")],
        "comp_b_class":["margin_p4_"+name for name in added_controls if name.startswith("comp_b_class")],
        "valid_b_no_y":["margin_p4_"+name for name in added_controls if name.startswith("valid_b_no_y")],
        "auction":[f"p4_r{idx}_{name}" for idx in range(3) for name in ("D","wl")]+[f"margin_p4_gross_gap_r{idx}" for idx in range(3)],
        "actual_weak":["margin_p4_b_"+name for name in ("weak_all_yplus","weak_no_yminus","weak_zero_return","weak_full_loss","weak_rate_room")],
        "actual_strong":["margin_p4_b_"+name for name in ("strong_buy","strong_prior_yplus","strong_no_yminus","strong_threshold_floor_return","strong_rate_room","strong_sale_public_gap","strong_zero_yplus")],
        "s_no_y":["margin_p4_"+name for name in signal_control if name.startswith("s_no_y")],
        "s_class":["margin_p4_"+name for name in signal_control if name.startswith("s_class")],
        "b_no_y":["margin_p4_"+name for name in signal_control if name.startswith("b_no_y")]+["margin_p4_b_no_y_top_exclusion_r0","margin_p4_b_no_y_top_exclusion_r1"],
        "grid":[f"margin_p4_grid_{ai}_{di}_{name}" for ai,di in met for name in ("private","joint","weak","strong","other_pair")],
    }
    for name,keys in groups.items():
        vals=[Interval(F(ENDPOINTS[key]["lo"]),F(ENDPOINTS[key]["hi"])) for key in keys]
        record("margin_p4_min_"+name,Interval(min(v.lo for v in vals),min(v.hi for v in vals)),
               "Minimum over these strict margins: "+"; ".join(keys),9)
    # Store every interval exactly; decimals in the log round outwards.
    columns=["key","value","display","status","source_script","run_log","note"]
    target=TEAM/"registry"/"P4_information.csv"
    with target.open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=columns)
        writer.writeheader()
        writer.writerows(ROWS)
    (HERE/"endpoints.json").write_text(json.dumps(ENDPOINTS,indent=2)+"\n")
    tex=[r"\providecommand{\reg}[1]{\ifcsname p4num@#1\endcsname\csname p4num@#1\endcsname\else\textbf{??#1}\PackageWarning{registry}{Unknown key #1}\fi}"]
    for row in ROWS:
        tex.append(r"\expandafter\def\csname p4num@"+row["key"]+r"\endcsname{"+row["display"]+"}")
    (HERE/"numbers.tex").write_text("\n".join(tex)+"\n")
    outputs=[target,HERE/"endpoints.json",HERE/"numbers.tex"]
    receipt={"date":datetime.now(timezone.utc).isoformat(),"python":platform.python_version(),
             "method":"Exact Fraction interval operations; rational Taylor enclosure of e",
             "tolerances":"None; each strict sign uses a rational endpoint",
             "input_beta":"294655/1000000","input_u":"e - 1","taylor_final_index":N,
             "selected_B_signal_pair":{"a_T":"47/50","d":"101/200"},
             "selected_B_controls":["investor sees T, no Y","investor sees J, no Y"],
             "rows":len(ROWS),"sufficient_pairs":met,
             "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             "outputs":{str(p.relative_to(TEAM)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}}
    (HERE/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("Registry rows",len(ROWS))


if __name__=="__main__":
    main()
