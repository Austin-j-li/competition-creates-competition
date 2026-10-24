"""Independent check of the P4 information package (R5, R7, R8) in the order-slot model.

Run from the repository root:
    TMPDIR=audit/slot_manuscript_2026_10_23/scripts/XP4 \
    .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/XP4/xp4_check.py \
    > audit/slot_manuscript_2026_10_23/scripts/XP4/run.log

Method.
- Interval arithmetic with outward rounding (mpmath.iv, 60 digits). The constant e comes
  from the interval library's own enclosure, not from a Taylor partial sum.
- Exact decimal inputs enter as integer ratios.
- Auction objects come from direct piecewise integration over R ~ U[0, r] in exact fractions.
- Every tuple comes from a brute-force joint law over class, investor signal, challenger
  signal, slot identity and order. Posteriors, challenger beliefs, class entry rates, prices
  and unilateral order payoffs are read off that joint law; no closed-form entry formula is used.
- The equilibrium search is a complete enumeration on each order side (see side_equilibria).
The program prints results. It contains no assertions.
"""
from __future__ import annotations

import csv
import sys
from decimal import Decimal, ROUND_HALF_EVEN, localcontext
from fractions import Fraction as Fr
from pathlib import Path

from mpmath import iv, mp, mpf

iv.dps = 60
mp.dps = 80
IVT = type(iv.mpf(1))

HERE = Path(__file__).resolve().parent
TEAM = HERE.parent.parent
REGISTRY = TEAM / "registry" / "P4_information.csv"


# ----------------------------------------------------------------------------------------
# Interval helpers
# ----------------------------------------------------------------------------------------
def Q(x) -> "iv.mpf":
    """Exact rational (or int or string fraction) as an enclosing interval."""
    if isinstance(x, IVT) or hasattr(x, "_mpi_"):
        return x
    f = Fr(x)
    return iv.mpf(f.numerator) / iv.mpf(f.denominator)


def lo(x):
    return mpf(Q(x).a)


def hi(x):
    return mpf(Q(x).b)


def sign(x):
    x = Q(x)
    if lo(x) > 0:
        return "+"
    if hi(x) < 0:
        return "-"
    return "0?"


def ge0(x):
    """Decide x >= 0 for an interval. Returns True/False, or None if unresolved."""
    x = Q(x)
    if lo(x) >= 0:
        return True
    if hi(x) < 0:
        return False
    return None


def clip01(x):
    x = Q(x)
    a, b = max(mpf(0), min(mpf(1), lo(x))), max(mpf(0), min(mpf(1), hi(x)))
    return iv.mpf([a, b])


def fmt(x, places=6):
    x = Q(x)
    mid = (lo(x) + hi(x)) / 2
    return dstr(mid, places)


def dstr(v, places):
    with localcontext() as ctx:
        ctx.prec = 70
        d = Decimal(mp.nstr(v, 65, strip_zeros=False, min_fixed=-mp.inf, max_fixed=mp.inf))
        q = Decimal(1).scaleb(-places) if places > 0 else Decimal(1)
        return format(d.quantize(q, rounding=ROUND_HALF_EVEN), "f")


def show(name, x, places=9):
    x = Q(x)
    print(f"  {name:<48s} = {fmt(x, places):>16s}   [{mp.nstr(lo(x), 15)}, {mp.nstr(hi(x), 15)}] sign {sign(x)}")


def imin(*xs):
    return iv.mpf([min(lo(x) for x in xs), min(hi(x) for x in xs)])


# ----------------------------------------------------------------------------------------
# Auction objects by direct integration (exact fractions), R ~ U[0, r]
# ----------------------------------------------------------------------------------------
H_VAL, L_VAL, P_RES = Fr(10), Fr(1), Fr(1, 2)


def revenue_given_theta(theta: Fr, r: Fr) -> Fr:
    """E[target payment] when a prepared bidder of value theta >= p meets R ~ U[0,r].
    The payment is max{p, min{theta, R}} (second price with reserve p)."""
    p = P_RES
    cut = min(theta, r)
    total = p * p  # R in [0,p): payment p
    total += (cut * cut - p * p) / 2  # R in [p, cut): payment R
    if theta < r:
        total += theta * (r - theta)  # R in [theta, r): payment theta
    return total / r


def rent_given_theta(theta: Fr, r: Fr) -> Fr:
    """E[(theta - max{p, R})_+]."""
    p = P_RES
    cut = min(theta, r)
    total = p * (theta - p)  # R in [0,p)
    total += theta * (cut - p) - (cut * cut - p * p) / 2  # R in [p, cut)
    return total / r


def auction(r) -> dict:
    r = Fr(r)
    p = P_RES
    t0 = p * (r - p) / r  # payment p when R >= p
    tH, tL = revenue_given_theta(H_VAL, r), revenue_given_theta(L_VAL, r)
    gH, gL = rent_given_theta(H_VAL, r), rent_given_theta(L_VAL, r)
    WH = Fr(1) if r <= H_VAL else H_VAL / r
    return dict(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=tH - tL, wH=tH - t0, wL=tL - t0, WH=WH)


def team_formulas(r) -> dict:
    r = Fr(r)
    p, l = P_RES, L_VAL
    return dict(t0=p * (1 - p / r), tH=r / 2 + p * p / (2 * r), tL=l - (l * l - p * p) / (2 * r),
                gH=H_VAL - r / 2 - p * p / (2 * r), gL=(l * l - p * p) / (2 * r), D=(r - l) ** 2 / (2 * r))


def Bgross(z, mu):
    return Q(z["gL"]) + Q(mu) * (Q(z["gH"]) - Q(z["gL"]))


def tau(z, cH):
    return (Fr(cH) - z["gL"]) / (z["gH"] - z["gL"])


# ----------------------------------------------------------------------------------------
# Slot primitives at calibration B
# ----------------------------------------------------------------------------------------
E_CONST = iv.e + 0  # materialize the library enclosure as an interval
BETA = Q(Fr(294655, 1000000))
U_B = E_CONST - 1
LAM = U_B * BETA / (1 + U_B * BETA)
B_LIQ = (1 - LAM) * BETA
B0_LIQ = (1 - LAM) * (1 - 2 * BETA)
HALF = Q(Fr(1, 2))


class Slot:
    def __init__(self, lam, beta):
        self.lam, self.beta = lam, beta
        self.b = (1 - lam) * beta
        self.b0 = (1 - lam) * (1 - 2 * beta)
        self.eta = {-1: beta, 0: 1 - 2 * beta, 1: beta}

    def M(self, pi=HALF):
        pi = Q(pi)
        return pi * (self.b + self.lam) / (pi * (self.b + self.lam) + (1 - pi) * self.b)

    def m(self, pi=HALF):
        pi = Q(pi)
        return pi * self.b / (pi * self.b + (1 - pi) * (self.b + self.lam))


SB = Slot(LAM, BETA)


# ----------------------------------------------------------------------------------------
# Brute-force tuple engine
# ----------------------------------------------------------------------------------------
class Econ:
    """r, rho, cost law, fee k, investor accuracy a (a = 1: investor sees the class),
    challenger accuracy d (d = 1/2: no challenger signal), hidden price flag, prior pi."""

    def __init__(self, r, rho, k, a=1, d=Fr(1, 2), cH=None, mix=None, hidden=False, pi=Fr(1, 2), slot=SB):
        self.z = auction(r)
        self.rho, self.k, self.a, self.d = Q(rho), Q(k), Q(a), Q(d)
        self.cH, self.mix, self.hidden, self.pi, self.slot = cH, mix, hidden, Q(pi), slot
        self.rho_f = Fr(rho)

    def hc(self, B):
        """Preparation probability at gross profit B (C1 at a cost atom)."""
        if self.mix is None:
            g = ge0(B - Q(self.cH))
            if g is None:
                raise ArithmeticError("unresolved cost comparison")
            return self.rho + (1 - self.rho) * (1 if g else 0)
        L, cm, cp = (Q(v) for v in self.mix)
        return self.rho * clip01(B / L) + (1 - self.rho) * clip01((B - cm) / (cp - cm))


def tuple_eval(E: Econ, sig_plus: dict, sig_minus: dict):
    """Brute-force evaluation of the candidate tuple defined by signal-contingent order
    distributions. Returns a dict with every component and payoff."""
    s = E.slot
    a, d, pi = E.a, E.d, E.pi
    pJ = {"H": pi, "L": 1 - pi}
    pT = {("H", "+"): a, ("H", "-"): 1 - a, ("L", "+"): 1 - a, ("L", "-"): a}
    pY = {("H", "+"): d, ("H", "-"): 1 - d, ("L", "+"): 1 - d, ("L", "-"): d}
    sig = {"+": sig_plus, "-": sig_minus}
    joint = {}
    for J in "HL":
        for T in "+-":
            for Y in "+-":
                for x in (-1, 0, 1):
                    joint[(J, T, Y, x)] = pJ[J] * pT[(J, T)] * pY[(J, Y)] * (
                        s.lam * Q(sig[T].get(x, 0)) + (1 - s.lam) * s.eta[x])

    def P(pred):
        tot = Q(0)
        for key, v in joint.items():
            if pred(*key):
                tot = tot + v
        return tot

    z = E.z
    wH, wL, t0 = Q(z["wH"]), Q(z["wL"]), Q(z["t0"])
    out = {"x": {}}
    for x in (-1, 0, 1):
        px = P(lambda J, T, Y, xx: xx == x)
        mu = P(lambda J, T, Y, xx: xx == x and J == "H") / px
        nu = P(lambda J, T, Y, xx: xx == x and T == "+") / px
        post, gap, entr = {}, {}, {}
        for y in "+-":
            if E.hidden:
                post[y] = P(lambda J, T, Y, xx: J == "H" and Y == y) / P(lambda J, T, Y, xx: Y == y)
            else:
                post[y] = P(lambda J, T, Y, xx: xx == x and Y == y and J == "H") / P(
                    lambda J, T, Y, xx: xx == x and Y == y)
            Bg = Bgross(z, post[y])
            gap[y] = Bg - Q(E.cH) if E.cH is not None else None
            entr[y] = E.hc(Bg)
        eJ = {}
        for J in "HL":
            pjx = P(lambda JJ, T, Y, xx: xx == x and JJ == J)
            eJ[J] = sum((P(lambda JJ, T, Y, xx: xx == x and JJ == J and Y == y) / pjx * entr[y] for y in "+-"), Q(0))
        price = mu * (t0 + eJ["H"] * wH) + (1 - mu) * (t0 + eJ["L"] * wL)
        out["x"][x] = dict(px=px, mu=mu, nu=nu, post=post, gap=gap, entry=entr, eH=eJ["H"], eL=eJ["L"], price=price)
    # Unilateral order payoffs against the fixed prices and entry rule.
    pay = {}
    for T in "+-":
        pT_tot = P(lambda J, TT, Y, xx: TT == T)
        bel = P(lambda J, TT, Y, xx: TT == T and J == "H") / pT_tot
        for q in (-1, 0, 1):
            ex = out["x"][q]
            eH_dev = sum((pY[("H", y)] * ex["entry"][y] for y in "+-"), Q(0))
            eL_dev = sum((pY[("L", y)] * ex["entry"][y] for y in "+-"), Q(0))
            v = bel * (t0 + eH_dev * wH) + (1 - bel) * (t0 + eL_dev * wL)
            pay[(T, q)] = q * (v - ex["price"]) - abs(q) * E.k if q != 0 else Q(0)
    out["pay"] = pay
    # Outcomes: class entry, entry, ownership, proceeds.
    ebar = {}
    for J in "HL":
        pj = P(lambda JJ, T, Y, xx: JJ == J)
        ebar[J] = sum((P(lambda JJ, T, Y, xx: JJ == J and xx == x) / pj * out["x"][x]["eH" if J == "H" else "eL"]
                       for x in (-1, 0, 1)), Q(0))
    out["ebarH"], out["ebarL"] = ebar["H"], ebar["L"]
    out["entry"] = pi * ebar["H"] + (1 - pi) * ebar["L"]
    out["own"] = pi * ebar["H"] * Q(z["WH"])
    out["proceeds"] = t0 + pi * ebar["H"] * wH + (1 - pi) * ebar["L"] * wL
    # Price sufficiency: prices strictly increasing in the order posterior.
    order = sorted((-1, 0, 1), key=lambda x: float(mpf(out["x"][x]["mu"].mid)))
    incs = []
    for x1, x2 in zip(order, order[1:]):
        dmu = out["x"][x2]["mu"] - out["x"][x1]["mu"]
        dp = out["x"][x2]["price"] - out["x"][x1]["price"]
        incs.append((x1, x2, dmu, dp))
    out["price_incs"] = incs
    return out


def rates_to_sig(s, t, lam=None):
    lam = SB.lam if lam is None else lam
    sp = {1: Q(s) / lam, 0: 1 - Q(s) / lam}
    sm = {-1: Q(t) / lam, 0: 1 - Q(t) / lam}
    return sp, sm


def print_tuple(tag, E, s, t):
    sp, sm = rates_to_sig(s, t)
    out = tuple_eval(E, sp, sm)
    print(f"TUPLE {tag}: r={E.z['r']}, rho={E.rho_f}, a={mp.nstr(mpf(E.a.mid), 6)}, d={mp.nstr(mpf(E.d.mid), 6)}, "
          f"hidden={E.hidden}, mix={E.mix}")
    show("buy rate Pr(q=1|T=+)", Q(s) / SB.lam)
    show("sale rate Pr(q=-1|T=-)", Q(t) / SB.lam)
    for x in (-1, 0, 1):
        ex = out["x"][x]
        show(f"x={x:+d} mu", ex["mu"])
        show(f"x={x:+d} nu = Pr(T=+|x)", ex["nu"])
        show(f"x={x:+d} price", ex["price"])
        show(f"x={x:+d} class entry eH", ex["eH"])
        show(f"x={x:+d} class entry eL", ex["eL"])
        if E.cH is not None:
            for y in "+-":
                show(f"x={x:+d} Y={y} challenger belief", ex["post"][y])
                show(f"x={x:+d} Y={y} gross minus c_H", ex["gap"][y])
    for (T, q), v in out["pay"].items():
        show(f"payoff T={T} q={q:+d}", v)
    for x1, x2, dmu, dp in out["price_incs"]:
        print(f"  price increment {x1:+d}->{x2:+d}: dmu sign {sign(dmu)}, dP sign {sign(dp)}")
    show("entry", out["entry"])
    show("H ownership", out["own"])
    show("proceeds", out["proceeds"])
    return out


# ----------------------------------------------------------------------------------------
# Complete equilibrium enumeration on each order side (atomic costs)
# ----------------------------------------------------------------------------------------
def odds_inv(o):
    return o / (1 + o)


def mu_threshold(E, y):
    """Public posterior at which B(phi_y(mu)) = c_H. phi_y multiplies the odds by w/(1-w)."""
    tz = Q(tau(E.z, E.cH))
    w = E.d if y == "+" else 1 - E.d
    o = tz / (1 - tz) * (1 - w) / w
    return odds_inv(o)


def side_equilibria(E: Econ, side: str):
    """All equilibrium rates on one side.

    Wrong-signed orders lose under every profile, because Delta_P >= rho*Delta > 0 and the
    investor's class belief is at least as favorable as any public posterior. The buy return
    then depends only on the buy rate s (and the sale return only on t). On each piece of
    [0, lambda] between the challenger thresholds the entry configuration is fixed and the
    gross return equals (2a-1) * (1-nu) * Delta_P with 1-nu = b/(2b+s) strictly decreasing.
    The enumeration covers: s = 0, s = lambda, interior roots on each piece, and each
    threshold point (C1 value; CM interval)."""
    s = E.slot
    lam, b = s.lam, s.b
    a = E.a
    z = E.z
    wH, wL = Q(z["wH"]), Q(z["wL"])

    def nu_of(rate):  # Pr(T=+|x) at the used order: buy gives (b+s)/(2b+s); sale gives b/(2b+t)
        return (b + rate) / (2 * b + rate) if side == "buy" else b / (2 * b + rate)

    def mu_of(rate):
        return (1 - a) + (2 * a - 1) * nu_of(rate)

    def resid(rate):  # 1 - nu for the buy, nu for the sale
        return b / (2 * b + rate)

    def dP(cfg):
        Ip, Im = cfg
        eH = E.rho + (1 - E.rho) * (E.d * Ip + (1 - E.d) * Im)
        eL = E.rho + (1 - E.rho) * ((1 - E.d) * Ip + E.d * Im)
        return eH * wH - eL * wL

    def cfg_at(mu):
        if E.hidden:
            mu = E.pi
        out = []
        for y in "+-":
            g = ge0(mu - mu_threshold(E, y))
            if g is None:
                return None
            out.append(1 if g else 0)
        return tuple(out)

    # Breakpoints in rate space.
    bps = []
    if not E.hidden:
        for y in "+-":
            mst = mu_threshold(E, y)
            nst = (mst - (1 - a)) / (2 * a - 1) if lo(2 * a - 1) > 0 else None
            if nst is None:
                continue
            if side == "buy":
                r_ = b * (2 * nst - 1) / (1 - nst) if lo(1 - nst) > 0 else None
            else:
                r_ = b * (1 - 2 * nst) / nst if lo(nst) > 0 else None
            if r_ is not None and lo(r_) > 0 and hi(r_) < lo(lam):
                bps.append((r_, y))
    bps.sort(key=lambda p: float(mpf(p[0].mid)))
    merged = []  # with no challenger signal both thresholds coincide
    for r_, y in bps:
        if merged and lo(r_) <= hi(merged[-1][0]):
            merged[-1] = (merged[-1][0], merged[-1][1] + y)
        else:
            merged.append((r_, y))
    bps = merged
    pts = [Q(0)] + [p[0] for p in bps] + [lam]
    eqs = []
    k = E.k
    log = []
    for i in range(len(pts) - 1):
        left, right = pts[i], pts[i + 1]
        mid = (left + right) / 2
        cfg = cfg_at(mu_of(mid))
        D = dP(cfg)
        K_left, K_right = (2 * a - 1) * resid(left) * D, (2 * a - 1) * resid(right) * D
        log.append((left, right, cfg, D, K_left, K_right))
        root = (2 * a - 1) * b * D / k - 2 * b
        if lo(root) > hi(left) and hi(root) < lo(right):
            eqs.append(("interior", root, cfg, "IM only"))
        if i == 0 and hi(K_left - k) < 0:
            eqs.append(("zero", Q(0), cfg, "IM and I0"))
        if i == len(pts) - 2 and lo(K_right - k) > 0:
            eqs.append(("full", lam, cfg, "IM and I0"))
    # Threshold points: C1 includes the indifferent type; CM allows any mixture.
    cm_points = []
    for (r_, y) in bps:
        c_lo = cfg_at(mu_of(r_ * (1 - Q(Fr(1, 10**12)))))  # just below the threshold rate
        c_hi = cfg_at(mu_of(r_ * (1 + Q(Fr(1, 10**12)))))  # just above the threshold rate
        if side == "sale":
            c_lo, c_hi = c_hi, c_lo  # mu falls in t
        K_excl = (2 * a - 1) * resid(r_) * dP(c_lo)
        K_incl = (2 * a - 1) * resid(r_) * dP(c_hi)
        lo_K, hi_K = imin(K_excl, K_incl), (K_excl if hi(K_excl) > hi(K_incl) else K_incl)
        cm_points.append((r_, y, K_excl, K_incl))
        if lo(lo_K - k) <= 0 <= hi(hi_K - k):
            eqs.append(("CM threshold", r_, (c_lo, c_hi), "IM with CM"))
    return eqs, log, cm_points


def report_side(tag, E, side):
    eqs, log, cm = side_equilibria(E, side)
    print(f"SIDE {tag} {side}: pieces")
    for (left, right, cfg, D, Kl, Kr) in log:
        print(f"    [{fmt(left / SB.lam, 6)}, {fmt(right / SB.lam, 6)}] (rate/lambda) cfg(I+,I-)={cfg} "
              f"Delta_P={fmt(D, 9)} gross return {fmt(Kl, 9)} -> {fmt(Kr, 9)}; k={fmt(E.k, 6)}")
    for (r_, y, Ke, Ki) in cm:
        print(f"    threshold for Y={y} at rate/lambda={fmt(r_ / SB.lam, 9)}: gross excluding {fmt(Ke, 9)}, "
              f"including {fmt(Ki, 9)}")
    for kind, r_, cfg, rule in eqs:
        print(f"    EQUILIBRIUM {kind}: rate={fmt(r_, 12)} (rate/b={fmt(r_ / SB.b, 9)}, rate/lambda={fmt(r_ / SB.lam, 9)}) "
              f"cfg={cfg} [{rule}]")
    if not eqs:
        print("    NO EQUILIBRIUM RATE on this side")
    return eqs


# ----------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------
MY = {}  # my value for every registry key


def put(key, val):
    MY[key] = Q(val)


def main():
    print("XP4 independent check. Interval arithmetic, 60 digits, outward rounding.")
    print("Python", sys.version.split()[0])
    show("e (library enclosure)", E_CONST, 15)
    show("u = e - 1", U_B)
    show("beta", BETA)
    show("lambda = u beta/(1+u beta)", LAM)
    show("b = (1-lambda) beta", B_LIQ)
    show("b0 = (1-lambda)(1-2beta)", B0_LIQ)
    show("M(1/2) = (b+lambda)/(2b+lambda)", SB.M())
    show("m(1/2)", SB.m())
    show("M(1/2) - e/(1+e)", SB.M() - E_CONST / (1 + E_CONST), 12)
    show("u - lambda/b", U_B - LAM / B_LIQ, 12)
    show("b0 - b (needs beta <= 1/3)", B0_LIQ - B_LIQ)
    for key, val in (("u_B", U_B), ("beta_B", BETA), ("lambda_B", LAM), ("b_B", B_LIQ), ("b0_B", B0_LIQ),
                     ("M_half_B", SB.M()), ("m_half_B", SB.m())):
        put(key, val)

    # --- Auction objects ---------------------------------------------------------------
    print("\n== Auction objects: direct integration against the team-rule formulas")
    for r in (Fr(11, 10), Fr(6, 5), Fr(23, 10), Fr(3), Fr(18, 5)):
        z, f = auction(r), team_formulas(r)
        diffs = {k: z[k] - f[k] for k in f}
        print(f"  r={r}: t0={z['t0']}, tH={z['tH']}, tL={z['tL']}, gH={z['gH']}, gL={z['gL']}, D={z['D']}, "
              f"tau(6)={tau(z, 6)}; differences from formulas: {set(diffs.values())}")
    zs = {0: auction(Fr(6, 5)), 1: auction(3), 2: auction(Fr(18, 5))}
    for i, z in zs.items():
        for name, src in (("t0", "t0"), ("th", "tH"), ("tl", "tL"), ("gh", "gH"), ("gl", "gL"), ("D", "D"),
                          ("wh", "wH"), ("wl", "wL")):
            put(f"p4_r{i}_{name}", z[src])
        put(f"tau_r{i}", tau(z, 6))
        put(f"margin_p4_gross_gap_r{i}", z["gH"] - z["gL"])

    rho, k, cH = Fr(1, 4), Fr(1, 50), 6
    M, m = SB.M(), SB.m()
    z0, z1, z2 = zs[0], zs[1], zs[2]

    # --- Primitive declarations and domain margins ------------------------------------
    prim = {"h": 10, "ell": 1, "p": "1/2", "rho": "1/4", "cH": 6, "k": "1/50", "pi": "1/2", "r0": "6/5", "r1": 3,
            "r2": "18/5", "epsilon": "1/10", "low_upper": "1/5", "high_lower": "59/10", "high_upper": "61/10",
            "signal_a": "7/10", "signal_d": "3/4", "s_rho": "17/20", "s_cost": "357/50", "s_fee": "3/200",
            "s_r0": "11/10", "s_r1": "23/10", "valid_a": "19/20", "valid_d": "101/200"}
    for kk, v in prim.items():
        put("p4_input_" + kk, Fr(v))
    dom = {"beta_lower": BETA, "beta_upper": Q(Fr(1, 3)) - BETA, "lambda_lower": LAM, "lambda_upper": 1 - LAM,
           "pi_lower": Fr(1, 2), "pi_upper": Fr(1, 2), "rho_lower": Fr(1, 4), "rho_upper": Fr(3, 4),
           "reserve": Fr(1, 2), "ell_reserve": Fr(1, 2), "r0_ell": Fr(6, 5) - 1, "r1_r0": 3 - Fr(6, 5),
           "r2_r1": Fr(18, 5) - 3, "h_r2": 10 - Fr(18, 5), "cost": 6, "fee": Fr(1, 50), "epsilon": Fr(1, 10),
           "band_width": Fr(61, 10) - Fr(59, 10), "band_lower": Fr(59, 10), "s_rho_lower": Fr(17, 20),
           "s_rho_upper": 1 - Fr(17, 20), "s_r0_ell": Fr(11, 10) - 1, "s_r1_r0": Fr(23, 10) - Fr(11, 10),
           "s_h_r1": 10 - Fr(23, 10), "s_cost": Fr(357, 50), "s_fee": Fr(3, 200), "signal_a_lower": Fr(7, 10) - Fr(1, 2),
           "signal_a_upper": 1 - Fr(7, 10), "signal_d_lower": Fr(3, 4) - Fr(1, 2), "signal_d_upper": 1 - Fr(3, 4),
           "signal_d_a": Fr(3, 4) - Fr(7, 10), "valid_a_lower": Fr(19, 20) - Fr(1, 2), "valid_a_upper": 1 - Fr(19, 20),
           "valid_d_lower": Fr(101, 200) - Fr(1, 2), "valid_d_upper": 1 - Fr(101, 200)}
    for kk, v in dom.items():
        put("margin_p4_domain_" + kk, v)

    # --- Core margins at B --------------------------------------------------------------
    print("\n== Core hypothesis margins at B")
    core = {"weak_trade": Q(k) - Q(z0["D"]), "strong_trade": Q(rho) * m * Q(z1["D"]) - Q(k),
            "very_strong_trade": Q(rho) * m * Q(z2["D"]) - Q(k), "weak_prior": 6 - Bgross(z0, HALF),
            "strong_top": Bgross(z1, M) - 6, "return": 6 - Bgross(z2, M), "weak_top": Bgross(z0, M) - 6,
            "strong_prior": 6 - Bgross(z1, HALF), "atomless_floor": Bgross(z1, m) - Q(Fr(1, 5)),
            "atomless_weak": Q(Fr(59, 10)) - Bgross(z0, HALF), "atomless_strong": Bgross(z1, M) - Q(Fr(61, 10)),
            "atomless_return": Q(Fr(59, 10)) - Bgross(z2, M), "atomless_floor_r2": Bgross(z2, m) - Q(Fr(1, 5)),
            "atomless_top_upper_r2": Q(Fr(61, 10)) - Bgross(z2, M),
            "atomless_top_lower_r2": Bgross(z2, M) - Q(Fr(59, 10))}
    for kk, v in core.items():
        show(kk, v)
        put(f"margin_p4_{kk}_B", v)
    put("margin_p4_ownership_rise_B", (1 - Q(rho)) * (SB.b + SB.lam))
    show("ownership rise margin (1-rho)(b+lambda)", MY["margin_p4_ownership_rise_B"])
    show("kappa = min(m, 1-M)", imin(m, 1 - M))

    # --- R5 and Proposition 2 baseline tuples ------------------------------------------
    print("\n== Baseline (investor sees J, no challenger signal): complete side enumeration")
    base = {}
    for i, r in ((0, Fr(6, 5)), (1, Fr(3)), (2, Fr(18, 5))):
        E = Econ(r, rho, k, a=1, cH=cH)
        eb = report_side(f"base r{i}", E, "buy")
        es = report_side(f"base r{i}", E, "sale")
        base[i] = (E, eb, es)
    rates_base = {0: (Q(0), Q(0)), 1: (SB.lam, SB.lam), 2: (SB.lam, SB.lam)}

    def register_profile(tag, E, s, t):
        out = print_tuple(tag, E, s, t)
        put(tag + "_buy_rate", Q(s) / SB.lam)
        put(tag + "_sell_rate", Q(t) / SB.lam)
        for x, nm in ((-1, "sell"), (0, "zero"), (1, "buy")):
            ex = out["x"][x]
            put(f"{tag}_{nm}_mu", ex["mu"])
            put(f"{tag}_{nm}_nu", ex["nu"])
            put(f"{tag}_{nm}_price", ex["price"])
            put(f"{tag}_{nm}_eh", ex["eH"])
            put(f"{tag}_{nm}_el", ex["eL"])
            if E.cH is not None:
                put(f"{tag}_{nm}_yp_entry_gap", ex["gap"]["+"])
                put(f"{tag}_{nm}_ym_entry_gap", ex["gap"]["-"])
            put(f"{tag}_{nm}_tp_payoff", out["pay"][("+", x)])
            put(f"{tag}_{nm}_tm_payoff", out["pay"][("-", x)])
        put(tag + "_entry", out["entry"])
        put(tag + "_own", out["own"])
        put(tag + "_proceeds", out["proceeds"])
        return out

    print("\n== R5: baseline equilibria and the information controls (tuples)")
    for i in (0, 1, 2):
        E = base[i][0]
        s_, t_ = rates_base[i]
        out = register_profile(f"p4_base_r{i}", E, s_, t_)
        put({0: "entry_r0", 1: "entry_r1_B", 2: "entry_r2"}[i], out["entry"])
        put({0: "own_r0", 1: "own_r1_B", 2: "own_r2_B"}[i], out["own"])
    fro = {}
    for i, r in ((0, Fr(6, 5)), (1, Fr(3))):
        fro[i] = register_profile(f"p4_frozen_r{i}", Econ(r, rho, k, a=1, cH=cH), SB.lam, SB.lam)
    print("\n== R5: price-hidden economies: complete side enumeration, then tuples")
    for i, r in ((0, Fr(6, 5)), (1, Fr(3))):
        E = Econ(r, rho, k, a=1, cH=cH, hidden=True)
        report_side(f"hidden r{i}", E, "buy")
        report_side(f"hidden r{i}", E, "sale")
        s_, t_ = (Q(0), Q(0)) if i == 0 else (SB.lam, SB.lam)
        register_profile(f"p4_hidden_r{i}", E, s_, t_)

    # Strict crossing probabilities computed from indicator differences over the frozen order law.
    print("\n== R5: strict cost-crossing probability under frozen full orders")
    full = tuple_eval(Econ(Fr(6, 5), rho, k, a=1, cH=cH), *rates_to_sig(SB.lam, SB.lam))
    def crossing(zA, zB):
        tot = Q(0)
        for x in (-1, 0, 1):
            ex = full["x"][x]
            iA = 1 if ge0(Bgross(zA, ex["mu"]) - 6) else 0
            iB = 1 if ge0(Bgross(zB, ex["mu"]) - 6) else 0
            tot = tot + ex["px"] * (1 - Q(rho)) * (iA - iB)
        return tot
    put("p4_control_crossing_r0_r1", crossing(z0, z1))
    put("p4_control_crossing_r1_r2", crossing(z1, z2))
    show("crossing r0 -> r1", MY["p4_control_crossing_r0_r1"])
    show("crossing r1 -> r2", MY["p4_control_crossing_r1_r2"])
    print("  Frozen entry on a strength grid (full orders imposed; challenger reoptimizes):")
    for r in (Fr(11, 10), Fr(6, 5), Fr(2), Fr(3), Fr(7, 2), Fr(359, 100), Fr(3593, 1000), Fr(18, 5)):
        o = tuple_eval(Econ(r, rho, k, a=1, cH=cH), *rates_to_sig(SB.lam, SB.lam))
        zr = auction(r)
        print(f"    r={str(r):>9s} tau={float(tau(zr, 6)):.6f}  B_r(M)-6={fmt(Bgross(zr, M) - 6, 6):>10s}  "
              f"entry={fmt(o['entry'], 6)}  own={fmt(o['own'], 6)}")
    # Ceiling r_C: B_r(M) = 6, bisection on exact rationals with interval signs.
    lo_r, hi_r = Fr(3), Fr(18, 5)
    for _ in range(60):
        mid_r = (lo_r + hi_r) / 2
        if ge0(Bgross(auction(mid_r), M) - 6):
            lo_r = mid_r
        else:
            hi_r = mid_r
    print(f"  ceiling r_C in [{float(lo_r):.12f}, {float(hi_r):.12f}]")

    # --- R7: atomless cost law ----------------------------------------------------------
    print("\n== R7: atomless cost law 1/4 U[0,1/5] + 3/4 U[59/10,61/10]")
    mix = (Fr(1, 5), Fr(59, 10), Fr(61, 10))
    for i, r in ((0, Fr(6, 5)), (1, Fr(3)), (2, Fr(18, 5))):
        E = Econ(r, rho, k, a=1, mix=mix)
        z = E.z
        # Order bounds valid under every profile: e in [rho, 1] at every price.
        show(f"r{i}: Delta - k (upper bound on correct gross minus fee)", Q(z["D"]) - Q(k))
        show(f"r{i}: rho*kappa*Delta - k (lower bound on correct gross minus fee)", Q(rho) * imin(m, 1 - M) * Q(z["D"]) - Q(k))
        show(f"r{i}: B(m) - L (low component prepares everywhere)", Bgross(z, m) - Q(Fr(1, 5)))
        s_, t_ = (Q(0), Q(0)) if i == 0 else (SB.lam, SB.lam)
        register_profile(f"p4_atomless_r{i}", E, s_, t_)
    put("p4_atomless_max_width_floor_r2", 6 - Bgross(z2, M))
    put("p4_atomless_small_width", Fr(1, 1000))
    put("margin_p4_atomless_small_width_return", 6 - Bgross(z2, M) - Q(Fr(1, 1000)))
    show("max half-width for the return at r2: 6 - B_r2(M)", MY["p4_atomless_max_width_floor_r2"])
    print("  Half-width 0.001 (low support [0,1/5] and [0,1/500]):")
    for L in (Fr(1, 5), Fr(1, 500)):
        mx = (L, Fr(5999, 1000), Fr(6001, 1000))
        for i, r in ((0, Fr(6, 5)), (1, Fr(3)), (2, Fr(18, 5))):
            E = Econ(r, rho, k, a=1, mix=mx)
            s_, t_ = (Q(0), Q(0)) if i == 0 else (SB.lam, SB.lam)
            o = tuple_eval(E, *rates_to_sig(s_, t_))
            print(f"    L={L}, r{i}: entry={fmt(o['entry'], 9)} own={fmt(o['own'], 9)}; "
                  f"B(m)-L={fmt(Bgross(E.z, m) - Q(L), 6)}")
    print("  Atomic H^1 = point mass at 6 inside the band [59/10, 61/10] (the theorem's proof never uses atomlessness):")
    for i, r in ((0, Fr(6, 5)), (1, Fr(3))):
        E = Econ(r, rho, k, a=1, cH=6)
        s_, t_ = (Q(0), Q(0)) if i == 0 else (SB.lam, SB.lam)
        o = tuple_eval(E, *rates_to_sig(s_, t_))
        print(f"    r{i}: entry={fmt(o['entry'], 9)} own={fmt(o['own'], 9)}")
    print("  Atomless ramp at r2: a numerical scan of the buy return over s in [0, lambda] (diagnostic):")
    E2a = Econ(Fr(18, 5), rho, k, a=1, mix=mix)
    worst = None
    for j in range(0, 101):
        s_ = SB.lam * Q(Fr(j, 100))
        o = tuple_eval(E2a, *rates_to_sig(s_, SB.lam))
        v = o["pay"][("+", 1)]
        worst = v if worst is None or hi(v) < hi(worst) else worst
    show("min over grid of the H buy payoff at r2", worst)

    # --- R8: complementary private signals ---------------------------------------------
    print("\n== R8: signal margins (independent formulas from the joint law)")

    def phi(mu, w):
        mu, w = Q(mu), Q(w)
        return w * mu / (w * mu + (1 - w) * (1 - mu))

    def sig_margins(r0, r1, rho_, c_, k_, a_, d_):
        zA, zB = auction(r0), auction(r1)
        a_, d_, rho_, k_ = Q(a_), Q(d_), Q(rho_), Q(k_)
        mup = (1 - a_) + (2 * a_ - 1) * M
        return {"private": Q(c_) - Bgross(zA, d_), "joint": Bgross(zB, phi(mup, d_)) - Q(c_),
                "weak": k_ - (2 * a_ - 1) * (Q(zA["D"]) + (1 - rho_) * (2 * d_ - 1) * Q(zA["wH"])),
                "strong": (2 * a_ - 1) * rho_ * m * Q(zB["D"]) - k_,
                "other_pair": Q(c_) - Bgross(zB, phi(mup, 1 - d_)),
                "no_y_top_r1": Q(c_) - Bgross(zB, mup)}

    SBV = dict(r0=Fr(11, 10), r1=Fr(23, 10), rho=Fr(17, 20), c=Fr(357, 50), k=Fr(3, 200))
    BV = dict(r0=Fr(6, 5), r1=Fr(3), rho=Fr(1, 4), c=Fr(6), k=Fr(1, 50))
    for tag, V, a_, d_ in (("p4_signal_s", SBV, Fr(7, 10), Fr(3, 4)), ("p4_signal_b", BV, Fr(7, 10), Fr(3, 4)),
                           ("p4_signal_valid_b", BV, Fr(19, 20), Fr(101, 200))):
        mg = sig_margins(V["r0"], V["r1"], V["rho"], V["c"], V["k"], a_, d_)
        print(f"  {tag} (a={a_}, d={d_}):")
        for kk, v in mg.items():
            show(kk, v)
            if kk != "no_y_top_r1":
                put(f"margin_{tag}_{kk}", v)

    print("\n== R8: S(B) and its information controls (complete side enumeration, then tuples)")
    for regime, a_, d_ in (("signal", Fr(7, 10), Fr(3, 4)), ("no_y", Fr(7, 10), Fr(1, 2)), ("class", 1, Fr(1, 2))):
        for i, r in ((0, SBV["r0"]), (1, SBV["r1"])):
            E = Econ(r, SBV["rho"], SBV["k"], a=a_, d=d_, cH=SBV["c"])
            eb = report_side(f"S(B) {regime} r{i}", E, "buy")
            es = report_side(f"S(B) {regime} r{i}", E, "sale")
            s_ = eb[0][1] if len(eb) == 1 else None
            t_ = es[0][1] if len(es) == 1 else None
            register_profile(f"p4_s_{regime}_r{i}", E, s_, t_)

    print("\n== R8: unchanged B, new pair (19/20, 101/200), with its no-Y and class controls")
    newpair = {}
    for regime, a_, d_ in (("valid_b", Fr(19, 20), Fr(101, 200)), ("valid_no_y", Fr(19, 20), Fr(1, 2))):
        for i, r in ((0, BV["r0"]), (1, BV["r1"])):
            E = Econ(r, BV["rho"], BV["k"], a=a_, d=d_, cH=6)
            eb = report_side(f"B {regime} r{i}", E, "buy")
            es = report_side(f"B {regime} r{i}", E, "sale")
            s_, t_ = eb[0][1], es[0][1]
            if regime == "valid_b":
                newpair[i] = register_profile(f"p4_valid_b_r{i}", E, s_, t_)
            else:
                newpair[("noy", i)] = print_tuple(f"XP4 new-pair no-Y control r{i}", E, s_, t_)

    print("\n== R8: unchanged B, earlier pair (7/10, 3/4): complete side enumeration under IM, C1 and CM")
    bsig = {}
    for regime, a_, d_ in (("signal", Fr(7, 10), Fr(3, 4)), ("no_y", Fr(7, 10), Fr(1, 2))):
        for i, r in ((0, BV["r0"]), (1, BV["r1"])):
            E = Econ(r, BV["rho"], BV["k"], a=a_, d=d_, cH=6)
            eb = report_side(f"B {regime} r{i}", E, "buy")
            es = report_side(f"B {regime} r{i}", E, "sale")
            print(f"    I0 check: buy side pure corners {[e[0] for e in eb if e[3] == 'IM and I0']}, "
                  f"sale side pure corners {[e[0] for e in es if e[3] == 'IM and I0']}")
            s_, t_ = eb[0][1], es[0][1]
            bsig[(regime, i)] = register_profile(f"p4_b_{regime}_r{i}", E, s_, t_)
    put("p4_b_signal_entry_change", bsig[("signal", 1)]["entry"] - bsig[("signal", 0)]["entry"])
    put("p4_b_signal_own_change", bsig[("signal", 1)]["own"] - bsig[("signal", 0)]["own"])
    show("closed form check: 5/8 - 23b/40 minus engine entry", Q(Fr(5, 8)) - Q(Fr(23, 40)) * SB.b - bsig[("signal", 1)]["entry"], 12)
    show("closed form check: 13/32 - 63b/160 minus engine own", Q(Fr(13, 32)) - Q(Fr(63, 160)) * SB.b - bsig[("signal", 1)]["own"], 12)

    # Hard-coded rationals in the package, rederived.
    print("\n== Rationals used in the package's B continuation, rederived")
    a_, d_ = Q(Fr(7, 10)), Q(Fr(3, 4))
    eH = Q(rho) + (1 - Q(rho)) * d_
    eL = Q(rho) + (1 - Q(rho)) * (1 - d_)
    dp0 = eH * Q(z0["wH"]) - eL * Q(z0["wL"])
    dp1 = eH * Q(z1["wH"]) - eL * Q(z1["wL"])
    show("Delta_P(r0) - 311/1920", dp0 - Q(Fr(311, 1920)), 12)
    show("Delta_P(r1) - 137/192", dp1 - Q(Fr(137, 192)), 12)
    print(f"  Delta_P(r0) exact = {Fr(13,16)*z0['wH'] - Fr(7,16)*z0['wL']}, Delta_P(r1) exact = {Fr(13,16)*z1['wH'] - Fr(7,16)*z1['wL']}")
    s_root = Fr(2, 5) * Fr(311, 1920) / Fr(1, 50) - 2
    print(f"  weak interior rate / b = (2/5)(311/1920)/k - 2 = {s_root}  (package: 119/96 = {Fr(119,96)})")
    mu_star = (Fr(141, 200) / (1 - Fr(141, 200))) * Fr(1, 3)
    mu_star = mu_star / (1 + mu_star)
    nu_star = (mu_star - Fr(3, 10)) / Fr(2, 5)
    print(f"  favorable-signal threshold at r1: mu* = {mu_star} (package 47/106), nu* = {nu_star} (package 19/53), "
          f"t*/b = (1-2nu*)/nu* = {(1 - 2 * nu_star) / nu_star} (package 15/19)")
    floor_ret = Fr(2, 5) * nu_star * Fr(1, 4) * auction(3)["D"]
    print(f"  floor sale return at the threshold = {floor_ret} (package 19/795); minus k = {float(floor_ret - Fr(1, 50)):.9f}")
    t_root = Fr(2, 5) * Fr(1, 4) * auction(3)["D"] / Fr(1, 50) - 2
    print(f"  strong interior sale rate / b = {t_root} (package 4/3); nu_-1 = 1/(2+t/b) = {1 / (2 + t_root)}, "
          f"mu_-1 = {Fr(3, 10) + Fr(2, 5) / (2 + t_root)} (package 21/50)")

    # Package margin rows for the B continuation and controls, recomputed.
    mulo, muhi = (1 - a_) + (2 * a_ - 1) * m, (1 - a_) + (2 * a_ - 1) * M
    zs0, zs1 = auction(SBV["r0"]), auction(SBV["r1"])
    extra = {"b_weak_all_yplus": Bgross(z0, phi(mulo, d_)) - 6, "b_weak_no_yminus": 6 - Bgross(z0, phi(muhi, 1 - d_)),
             "b_weak_zero_return": (2 * a_ - 1) * dp0 / 2 - Q(k), "b_weak_full_loss": Q(k) - (2 * a_ - 1) * m * dp0,
             "b_weak_rate_room": U_B - Q(Fr(119, 96)), "b_strong_buy": (2 * a_ - 1) * m * dp1 - Q(k),
             "b_strong_prior_yplus": Bgross(z1, d_) - 6, "b_strong_no_yminus": 6 - Bgross(z1, phi(muhi, 1 - d_)),
             "b_strong_threshold_floor_return": Q(floor_ret) - Q(k), "b_strong_rate_room": U_B - Q(Fr(4, 3)),
             "b_strong_sale_public_gap": Q(mu_star) - Q(Fr(21, 50)),
             "b_strong_zero_yplus": bsig[("signal", 1)]["x"][0]["gap"]["+"],
             "b_no_y_top_exclusion_r0": 6 - Bgross(z0, muhi), "b_no_y_top_exclusion_r1": 6 - Bgross(z1, muhi),
             "s_no_y_weak": Q(SBV["k"]) - Q(Fr(2, 5)) * Q(zs0["D"]),
             "s_no_y_strong": Q(Fr(2, 5)) * Q(SBV["rho"]) * m * Q(zs1["D"]) - Q(SBV["k"]),
             "s_no_y_top_r0": Q(SBV["c"]) - Bgross(zs0, Q(Fr(3, 10)) + Q(Fr(2, 5)) * M),
             "s_no_y_top_r1": Q(SBV["c"]) - Bgross(zs1, Q(Fr(3, 10)) + Q(Fr(2, 5)) * M),
             "s_class_weak": Q(SBV["k"]) - Q(zs0["D"]), "s_class_strong": Q(SBV["rho"]) * m * Q(zs1["D"]) - Q(SBV["k"]),
             "s_class_prior_r0": Q(SBV["c"]) - Bgross(zs0, HALF), "s_class_top_r1": Q(SBV["c"]) - Bgross(zs1, M),
             "b_no_y_weak": Q(k) - Q(rho) * Q(Fr(2, 5)) * Q(z0["D"]) / 2,
             "b_no_y_zero_gain": Q(rho) * Q(Fr(2, 5)) * Q(z1["D"]) / 2 - Q(k),
             "b_no_y_full_loss": Q(k) - Q(rho) * Q(Fr(2, 5)) * Q(z1["D"]) * m}
    print("\n== Margin rows for the B continuation and the controls")
    for kk, v in extra.items():
        show(kk, v)
        put("margin_p4_" + kk, v)
    put("p4_b_signal_z_min", Q(k) / (Q(rho) * m * Q(z1["D"])))
    zmin = MY["p4_b_signal_z_min"]
    put("margin_p4_b_d_ge_a_impossible", zmin * (Q(z0["D"]) + (1 - Q(rho)) * zmin * Q(z0["wH"])) - Q(k))
    show("z_min = k/(m rho Delta_1)", zmin)
    show("d >= a contradiction margin", MY["margin_p4_b_d_ge_a_impossible"])
    show("private exclusion needs d < tau(r0)", Q(tau(z0, 6)))
    show("strong bound needs a > (1 + z_min)/2", (1 + zmin) / 2)

    # --- Accuracy grid in S(B) -----------------------------------------------------------
    print("\n== R8: accuracy grid in S(B): margins, sufficiency, and the complete equilibrium set at each pair")
    met = []
    for ai in range(68, 78):
        put(f"p4_accuracy_{ai}", Fr(ai, 100))
    for ai in range(68, 73):
        for di in range(73, 78):
            a_, d_ = Fr(ai, 100), Fr(di, 100)
            mg = sig_margins(SBV["r0"], SBV["r1"], SBV["rho"], SBV["c"], SBV["k"], a_, d_)
            tag = f"p4_grid_{ai}_{di}"
            for kk in ("private", "joint", "weak", "strong", "other_pair"):
                put(f"margin_{tag}_{kk}", mg[kk])
            yes = all(lo(mg[kk]) > 0 for kk in ("private", "joint", "weak", "strong"))
            put(tag + "_sufficient", 1 if yes else 0)
            summary = []
            for i, r in ((0, SBV["r0"]), (1, SBV["r1"])):
                E = Econ(r, SBV["rho"], SBV["k"], a=a_, d=d_, cH=SBV["c"])
                eb, _, _ = side_equilibria(E, "buy")
                es, _, _ = side_equilibria(E, "sale")
                if len(eb) == 1 and len(es) == 1:
                    o = tuple_eval(E, *rates_to_sig(eb[0][1], es[0][1]))
                    summary.append(f"r{i}: {eb[0][0]}/{es[0][0]} entry {fmt(o['entry'], 6)} own {fmt(o['own'], 6)}")
                    if i == 1 and yes:
                        put(tag + "_entry", o["entry"])
                        put(tag + "_own", o["own"])
                else:
                    summary.append(f"r{i}: buy {[e[0] for e in eb]} sale {[e[0] for e in es]}")
            if yes:
                met.append((ai, di))
            print(f"  ({a_}, {d_}) sufficient={yes} other_pair={sign(mg['other_pair'])} minmargin="
                  f"{fmt(imin(*(mg[kk] for kk in ('private', 'joint', 'weak', 'strong'))), 9)} | " + "; ".join(summary))
    put("p4_grid_met_count", len(met))
    print("  sufficient pairs:", met)

    # --- Complementarity at unchanged B ----------------------------------------------------
    print("\n== R8 at unchanged B: pairs that satisfy the theorem, the one-pair condition, and need the challenger signal")
    print("   (no-Y top public profit below c_H at r1, so the no-Y control has no reversal)")
    found = []
    for ai in range(900, 951, 2):
        for di in range(5005, 5101, 5):
            a_, d_ = Fr(ai, 1000), Fr(di, 10000)
            mg = sig_margins(BV["r0"], BV["r1"], BV["rho"], BV["c"], BV["k"], a_, d_)
            if all(lo(mg[kk]) > 0 for kk in ("private", "joint", "weak", "strong", "other_pair", "no_y_top_r1")):
                found.append((a_, d_, mg))
    if found:
        a_vals = sorted({f[0] for f in found})
        print(f"  {len(found)} grid pairs qualify; a ranges over [{float(a_vals[0])}, {float(a_vals[-1])}]")
        for a_, d_, mg in found[:: max(1, len(found) // 8)]:
            print(f"    ({float(a_)}, {float(d_)}): " + ", ".join(f"{kk} {fmt(v, 6)}" for kk, v in mg.items()))
    ex_a, ex_d = Fr(47, 50), Fr(101, 200)
    mg = sig_margins(BV["r0"], BV["r1"], BV["rho"], BV["c"], BV["k"], ex_a, ex_d)
    print(f"  Example pair ({ex_a}, {ex_d}) = (0.94, 0.505): all margins")
    for kk, v in mg.items():
        show(kk, v)
    for regime, d_ in (("signal", ex_d), ("no_y", Fr(1, 2))):
        for i, r in ((0, BV["r0"]), (1, BV["r1"])):
            E = Econ(r, BV["rho"], BV["k"], a=ex_a, d=d_, cH=6)
            eb = report_side(f"B (0.94, {float(d_)}) {regime} r{i}", E, "buy")
            es = report_side(f"B (0.94, {float(d_)}) {regime} r{i}", E, "sale")
            o = tuple_eval(E, *rates_to_sig(eb[0][1], es[0][1]))
            show(f"(0.94,{float(d_)}) {regime} r{i} entry", o["entry"])
            show(f"(0.94,{float(d_)}) {regime} r{i} own", o["own"])

    # --- S(B) display stability under the earlier B convention ----------------------------
    print("\n== S(B) declared pair under the earlier exact-entry-match B convention")
    tz = mp.mpf(141) / 200
    xs = mp.log(tz / (1 - tz))
    aH = 1 - mp.e ** ((xs - 1) / 2) / 2
    aL = mp.e ** (-(xs + 1) / 2) / 2
    bE2 = (aH + aL) / (1 + mp.e)
    lamE2 = (mp.e - 1) * bE2
    betaE2 = bE2 / (1 - lamE2)
    print(f"  earlier convention: beta = {mp.nstr(betaE2, 15)}, lambda = {mp.nstr(lamE2, 15)}, b = {mp.nstr(bE2, 15)}")
    slotE2 = Slot(iv.mpf(lamE2), iv.mpf(betaE2))
    for i, r in ((0, SBV["r0"]), (1, SBV["r1"])):
        E = Econ(r, SBV["rho"], SBV["k"], a=Fr(7, 10), d=Fr(3, 4), cH=SBV["c"], slot=slotE2)
        s_, t_ = (Q(0), Q(0)) if i == 0 else (slotE2.lam, slotE2.lam)
        sp = {1: Q(s_) / slotE2.lam, 0: 1 - Q(s_) / slotE2.lam}
        sm = {-1: Q(t_) / slotE2.lam, 0: 1 - Q(t_) / slotE2.lam}
        o = tuple_eval(E, sp, sm)
        print(f"    r{i}: entry {fmt(o['entry'], 9)} own {fmt(o['own'], 9)}")
    E = Econ(Fr(3), rho, k, a=1, cH=6, slot=slotE2)
    sp = {1: Q(1), 0: Q(0)}
    sm = {-1: Q(1), 0: Q(0)}
    o = tuple_eval(E, sp, sm)
    print(f"    benchmark r1 under the earlier convention: entry {fmt(o['entry'], 12)} own {fmt(o['own'], 12)}")
    E = Econ(Fr(18, 5), rho, k, a=1, mix=mix, slot=slotE2)
    o = tuple_eval(E, sp, sm)
    print(f"    atomless r2 under the earlier convention: entry {fmt(o['entry'], 12)} own {fmt(o['own'], 12)}")

    # --- Registry comparison --------------------------------------------------------------
    compare_registry()


def compare_registry():
    print("\n== Registry comparison: every row of registry/P4_information.csv")
    rows = list(csv.DictReader(REGISTRY.open()))
    # Group minima: recompute from my values of the listed member keys.
    for row in rows:
        if row["key"].startswith("margin_p4_min_"):
            members = row["note"].split(":", 1)[1].split(";")
            members = [mm.strip() for mm in members]
            vals = [MY[mm] for mm in members if mm in MY]
            if len(vals) == len(members):
                MY[row["key"]] = imin(*vals)
    # The e enclosure rows: rebuild the declared Taylor partial sum and check it brackets the library enclosure.
    from math import factorial
    part = sum((Fr(1, factorial(n)) for n in range(61)), Fr(0))
    MY["p4_e_lo"] = Q(part)
    MY["p4_e_hi"] = Q(part + Fr(1, 60 * factorial(60)))
    MY["p4_exp_terms"] = Q(60)
    with mp.workdps(250):  # the Taylor remainder is near 1e-84, so compare at 250 digits
        e250 = +mp.e
        lo_ok = mpf(part.numerator) / part.denominator < e250
        upf = part + Fr(1, 60 * factorial(60))
        hi_ok = mpf(upf.numerator) / upf.denominator > e250
        gap_lo = e250 - mpf(part.numerator) / part.denominator
    print(f"  e enclosure check at 250 digits: Taylor sum below e: {lo_ok}; Taylor sum plus 1/(60*60!) above e: {hi_ok}; "
          f"e minus the Taylor sum = {mp.nstr(gap_lo, 5)}")
    missing, mism, disp_diff, hazards = [], [], [], []
    maxdiff = mpf(0)
    for row in rows:
        key = row["key"]
        if key not in MY:
            missing.append(key)
            continue
        v = row["value"]
        f = Fr(v) if "/" in v else Fr(Decimal(v))
        regv = mpf(f.numerator) / f.denominator
        mine = MY[key]
        diff = max(abs(lo(mine) - regv), abs(hi(mine) - regv))
        disp = row["display"]
        places = len(disp.split(".")[1]) if "." in disp else 0
        my_lo, my_hi = dstr(lo(mine), places), dstr(hi(mine), places)
        def nz(sx):  # treat a signed zero display as zero
            return sx.lstrip("-") if set(sx.lstrip("-")) <= set("0.") else sx
        my_lo, my_hi, disp = nz(my_lo), nz(my_hi), nz(disp)
        tol = mpf(10) ** (-places) / 2
        if diff > tol:
            mism.append((key, v, fmt(mine, max(places, 9)), disp))
        if my_lo != disp or my_hi != disp:
            disp_diff.append((key, disp, my_lo, my_hi))
        # Distance from a rounding boundary of the display.
        midv = (lo(mine) + hi(mine)) / 2
        scaled = midv * mpf(10) ** places
        frac = scaled - mp.floor(scaled)
        dist = abs(frac - mpf(1) / 2) * mpf(10) ** (-places)
        if dist < mpf(10) ** (-places - 3) and places > 0:
            hazards.append((key, disp, mp.nstr(midv, 15), mp.nstr(dist, 3)))
        if diff > maxdiff and places >= 6 and key not in ("p4_e_lo", "p4_e_hi"):
            maxdiff = diff
    print(f"  rows: {len(rows)}; recomputed: {len(rows) - len(missing)}; not recomputed: {len(missing)} {missing}")
    print(f"  rows whose value differs from mine beyond half a unit of the display's last digit: {len(mism)}")
    for x in mism:
        print("    MISMATCH", x)
    print(f"  rows whose display differs from my rounding (either interval end): {len(disp_diff)}")
    for x in disp_diff:
        print("    DISPLAY", x)
    print(f"  rows within 10^-(places+3) of a rounding boundary: {len(hazards)}")
    for x in hazards:
        print("    NEAR-BOUNDARY", x)
    print(f"  largest absolute difference between a registry value and my enclosure (rows with >= 6 places): "
          f"{mp.nstr(maxdiff, 5)}")
    extra = sorted(set(MY) - {r['key'] for r in rows})
    print(f"  keys I computed that the registry lacks: {extra}")
    # Status labels on the shared keys.
    print("  status labels of shared keys (P4 vs P1):")
    p1 = {r["key"]: r for r in csv.DictReader((TEAM / "registry" / "P1_core.csv").open())}
    for row in rows:
        if row["key"] in p1:
            s4, s1 = row["status"], p1[row["key"]]["status"]
            d4, d1 = row["display"], p1[row["key"]]["display"]
            flag = "" if (s4 == s1 and d4 == d1) else "   <-- differs"
            print(f"    {row['key']:<14s} P4 {s4:<18s} {d4:<10s} P1 {s1:<18s} {d1:<10s}{flag}")


if __name__ == "__main__":
    main()
