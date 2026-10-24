#!/usr/bin/env python3
"""P5 observables of the order slot: exact and interval evaluation.

Run from the repository root:
    .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/P5_observables/p5_observables.py

The program prints every observable of the order slot at calibration B
(interval arithmetic with mpmath.iv, 60 digits; the exponential constant is
enclosed, beta is the exact decimal 294655/1000000).  It also recomputes the
quantities of the earlier study at calibration A (exact rationals) and prints
them next to the values quoted in that study.  It writes
  registry/P5_observables.csv        one row per printed number,
  scripts/P5_observables/p5_numbers.tex   the same numbers as \\reg macros,
  scripts/P5_observables/curves_full_branch.csv   data for figures.
It contains no tests and no assertions.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pathlib
import platform
import sys
from decimal import Decimal, localcontext, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN
from fractions import Fraction as Fr

import mpmath
from mpmath import iv, mp

iv.dps = 60
mp.dps = 60

HERE = pathlib.Path(__file__).resolve().parent
TEAM = HERE.parents[1]
SCRIPT_REL = "scripts/P5_observables/p5_observables.py"
LOG_REL = "scripts/P5_observables/run_log.txt"
REGISTRY = TEAM / "registry/P5_observables.csv"

ROWS: list[dict] = []
FLAGS: list[str] = []
ENCLOSURES: dict[str, dict[str, str]] = {}

# Preserve the two corrected notes in every export.
PRESERVED_NOTES = {
    "vol_full_B": "Volume 2b+lambda: two-sided full informed trade. "
                  "The value is a point rounded to nearest at 20 digits, not an enclosure. "
                  "Outward enclosure [0.7273518492757511245590493, 0.7273518492757511245590494] "
                  "(scripts/R_referee/recompute.log); a wider certificate is in scripts/XP5/registry_recompute.csv.",
    "theta_max_full_eq_r1_B": "1 - 2k/(rho Delta_T(r_1)) = 19/25. "
                             "Under rule IM, full two-sided trade with share theta' is an equilibrium at r_1 "
                             "iff theta' <= this value; at equality the low-class sale earns exactly zero. "
                             "Strict incentives, and rule I0, need theta' < this value.",
}


# ----------------------------------------------------------------------------
# number helpers (Fraction or interval)
# ----------------------------------------------------------------------------

def I(x):
    """Lift a Fraction or int to a tight interval."""
    if isinstance(x, Fr):
        return iv.mpf(x.numerator) / iv.mpf(x.denominator)
    return iv.mpf(x)


def is_iv(x) -> bool:
    return not isinstance(x, Fr)


def lo(x):
    return mp.make_mpf(x._mpi_[0]) if is_iv(x) else mp.mpf(x.numerator) / x.denominator


def hi(x):
    return mp.make_mpf(x._mpi_[1]) if is_iv(x) else mp.mpf(x.numerator) / x.denominator


def midpoint(x):
    return (lo(x) + hi(x)) / 2


def sgn(x):
    """+1 / -1 if the sign is certain, 0 if x is exactly 0 (Fraction), None otherwise."""
    if not is_iv(x):
        return (x > 0) - (x < 0)
    if lo(x) > 0:
        return 1
    if hi(x) < 0:
        return -1
    return None


def fmt_dec(x, nd):
    """Round the enclosure to nd decimals; flag if the two ends round differently."""
    q = Decimal(1).scaleb(-nd)
    a = Decimal(mp.nstr(lo(x), 50)).quantize(q, rounding=ROUND_HALF_EVEN)
    b = Decimal(mp.nstr(hi(x), 50)).quantize(q, rounding=ROUND_HALF_EVEN)
    if a != b:
        FLAGS.append(f"AMBIGUOUS ROUNDING {a} vs {b}")
    if a == 0:
        a = abs(a)
    return format(a, "f")


def exact_endpoints(x):
    """Read the binary endpoints as exact rational numbers."""
    if not is_iv(x):
        return x, x
    ends = []
    for negative, mantissa, exponent, _ in x._mpi_:
        value = Fr(mantissa) * Fr(2) ** exponent
        ends.append(-value if negative else value)
    return ends[0], ends[1]


def enclosure(x, nd=20):
    """Round the exact lower end down and the exact upper end up."""
    lower, upper = exact_endpoints(x)
    with localcontext() as context:
        context.prec = nd
        context.rounding = ROUND_FLOOR
        low = Decimal(lower.numerator) / Decimal(lower.denominator)
        context.rounding = ROUND_CEILING
        high = Decimal(upper.numerator) / Decimal(upper.denominator)
    return f"[{low}, {high}]"


def kind_of(x):
    return "interval" if is_iv(x) else "exact"


def reg(key, x, nd=6, status="computer-assisted", note="", pct=False, rational=None, display=None):
    """Register one number.  x is a Fraction or an interval.  display overrides the format."""
    if display is not None:
        disp = display
    elif pct:
        y = x * (Fr(100) if not is_iv(x) else I(Fr(100)))
        disp = fmt_dec(y, nd) + r"\%"
    else:
        disp = fmt_dec(x, nd)
    if not is_iv(x):
        value = f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)
    else:
        value = mp.nstr(midpoint(x), 20)
        note = (note + " " if note else "") + f"Enclosure {enclosure(x)}."
        lower, upper = exact_endpoints(x)
        ENCLOSURES[key] = dict(lo=str(lower), hi=str(upper))
    note = PRESERVED_NOTES.get(key, note)
    ROWS.append(dict(key=key, value=value, display=disp, status=status,
                     source_script=SCRIPT_REL, run_log=LOG_REL, note=note.strip()))
    return x


def show(label, x, nd=6, pct=False):
    if pct:
        y = x * (Fr(100) if not is_iv(x) else I(Fr(100)))
        print(f"  {label:<52s} {fmt_dec(y, nd)}%   {enclosure(x, 16) if is_iv(x) else x}")
    else:
        print(f"  {label:<52s} {fmt_dec(x, nd)}   {enclosure(x, 16) if is_iv(x) else x}")


def yes(cond):
    return "yes" if cond else ("NO" if cond is False else "UNDECIDED")


# ----------------------------------------------------------------------------
# primitives, auction, slot (generic over Fraction / interval)
# ----------------------------------------------------------------------------

class Prim:
    def __init__(self, exact: bool):
        c = (lambda x: x) if exact else I
        self.c = c
        self.h, self.l, self.p = c(Fr(10)), c(Fr(1)), c(Fr(1, 2))
        self.rho, self.cH, self.k = c(Fr(1, 4)), c(Fr(6)), c(Fr(1, 50))
        self.pi, self.zero, self.one = c(Fr(1, 2)), c(Fr(0)), c(Fr(1))
        self.two = c(Fr(2))


def auction(P: Prim, r):
    t0 = P.p * (P.one - P.p / r)
    tH = r / P.two + P.p * P.p / (P.two * r)
    tL = P.l - (P.l * P.l - P.p * P.p) / (P.two * r)
    gH = P.h - tH
    gL = P.l - tL
    # g_L also equals (l^2-p^2)/(2r); printed as a check in main()
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=tH - tL)


def Bfun(P: Prim, au, mu):
    return au["gL"] + mu * (au["gH"] - au["gL"])


def Afun(au, mu):
    return au["tL"] - au["t0"] + au["D"] * mu


def tau_of(P: Prim, au):
    return (P.cH - au["gL"]) / (au["gH"] - au["gL"])


class Slot:
    """Slot parameters from (u, beta); prior 1/2."""
    def __init__(self, P: Prim, u, beta):
        self.u, self.beta = u, beta
        self.lam = u * beta / (P.one + u * beta)
        self.b = (P.one - self.lam) * beta
        self.d = self.b + self.lam / P.two
        self.M = (P.one + u) / (P.two + u)          # M(1/2)
        self.m = P.one - self.M
        self.theta = u / (P.two + u)                # lam/(lam+2b) = 2M-1
        self.vF = P.two * self.d                    # 2b + lam
        self.vU = P.two * self.b + self.lam / P.two  # 2b + lam/2
        self.vN = P.two * self.b


def rceil(P: Prim, S: Slot):
    """Closed form of the ceiling r_C with B_r(M) = c_H (interval type)."""
    a = S.M * P.h - P.cH
    disc = a * a + S.M * ((P.one - S.M) * P.l * P.l - P.p * P.p)
    return (a + iv.sqrt(disc)) / S.M


def outcome(P: Prim, S: Slot, r, regime: str, hide_price=False, tie_buy="C1"):
    """Observables of one trading outcome at strength r (regime N, U or F)."""
    au = auction(P, r)
    s = S.lam if regime in ("U", "F") else P.zero
    t = S.lam if regime == "F" else P.zero
    b = S.b
    aH = {1: b + s, -1: b, 0: P.one - P.two * b - s}
    aL = {1: b, -1: b + t, 0: P.one - P.two * b - t}
    pr = {x: P.pi * aH[x] + (P.one - P.pi) * aL[x] for x in (-1, 0, 1)}
    mu = {x: P.pi * aH[x] / pr[x] for x in (-1, 0, 1)}
    J = {}
    for x in (-1, 0, 1):
        if hide_price:
            J[x] = 1 if sgn(Bfun(P, au, P.pi) - P.cH) in (0, 1) else 0
        else:
            sg = sgn(Bfun(P, au, mu[x]) - P.cH)
            if sg is None:
                J[x] = None
            elif sg == 0:
                J[x] = 1 if tie_buy == "C1" else None
            else:
                J[x] = 1 if sg > 0 else 0
    e = {x: (P.rho + (P.one - P.rho) * (P.one if J[x] == 1 else P.zero)) for x in J}
    A = {x: Afun(au, mu[x]) for x in mu}
    price = {x: au["t0"] + e[x] * A[x] for x in mu}
    pbar = sum((pr[x] * price[x] for x in mu), P.zero)
    EX = pr[1] - pr[-1]
    vol = pr[1] + pr[-1]
    entry = sum((pr[x] * e[x] for x in e), P.zero)
    w = {x: mu[x] + (P.one - mu[x]) * P.l / r for x in mu}
    cov_entry = sum((pr[x] * x * e[x] for x in e), P.zero) - EX * entry
    winp = sum((pr[x] * e[x] * w[x] for x in e), P.zero)
    cov_win = sum((pr[x] * x * e[x] * w[x] for x in e), P.zero) - EX * winp
    evA = {x: (P.one - e[x]) * A[x] for x in mu}
    evN = {x: -e[x] * A[x] for x in mu}
    # informed share of nonzero orders (prior 1/2): informed trades per slot / volume
    inf_trades = P.pi * s + (P.one - P.pi) * t
    ownH = P.pi * sum((aH[x] * e[x] for x in (-1, 0, 1)), P.zero)
    if any(J[x] is None for x in J):
        FLAGS.append(f"UNDECIDED entry indicator at one order (regime {regime})")
    return dict(ownH=ownH, au=au, s=s, t=t, pr=pr, mu=mu, J=J, e=e, A=A, price=price, pbar=pbar,
                EX=EX, vol=vol, entry=entry, w=w, cov_entry=cov_entry, winp=winp,
                cov_win=cov_win, evA=evA, evN=evN, inf_share=inf_trades / vol,
                spread=price[1] - price[-1], imp_buy=price[1] - price[0],
                imp_sell=price[0] - price[-1])


# ----------------------------------------------------------------------------
# calibration B and calibration A
# ----------------------------------------------------------------------------

PB = Prim(exact=False)
UB = iv.e - 1
BETA_B = I(Fr(294655, 1000000))
SB = Slot(PB, UB, BETA_B)

PA = Prim(exact=True)
SA = Slot(PA, Fr(18, 11), Fr(1, 3))

R0, R1, R2 = Fr(6, 5), Fr(3), Fr(18, 5)
RCO = [Fr(31, 20), Fr(8, 5), Fr(33, 20)]


def header(text):
    print("\n" + "=" * 78)
    print(text)
    print("=" * 78)


def main():
    P, S = PB, SB
    header("P5 OBSERVABLES OF THE ORDER SLOT")
    print(f"python {platform.python_version()}, mpmath {mpmath.__version__}, "
          f"iv.dps={iv.dps}")
    print("Prior 1/2; h=10, l=1, p=1/2, rho=1/4, c_L=0, c_H=6, k=1/50.")
    print("Calibration B: 1+u = e, beta = 294655/1000000 (exact).")

    # ------------------------------------------------------------------ 0
    header("0. SHARED AUCTION OBJECTS: CHECK OF THE ALGEBRAIC FORMS AT r = 3")
    for r in (R1, R2):
        au = auction(PA, r)
        # integrate over R ~ U[0,r] exactly (piecewise linear integrands)
        p, l, h = PA.p, PA.l, PA.h
        E_max_Rp = (p * p + (r * r - p * p) / 2) / r
        tH_int = E_max_Rp
        tL_int = (p * p + (l * l - p * p) / 2) / r + l * (r - l) / r
        gL_int = (p * (l - p) + (l - p) ** 2 / 2) / r
        t0_int = p * (r - p) / r
        print(f"  r={r}: t0 {au['t0']} vs int {t0_int}; tH {au['tH']} vs {tH_int}; "
              f"tL {au['tL']} vs {tL_int}; gL {au['gL']} vs {gL_int}; "
              f"gH {au['gH']} vs {h - tH_int}; Delta_T {au['D']} vs {(r - l) ** 2 / (2 * r)}")

    # ------------------------------------------------------------------ 1
    header("1. SLOT PRIMITIVES AT B")
    show("u = e - 1", S.u, 12)
    show("beta", S.beta, 12)
    show("lambda = u beta/(1+u beta)", S.lam, 12)
    show("b = (1-lambda) beta", S.b, 12)
    show("check u - lambda/b (should be 0)", S.u - S.lam / S.b, 12)
    show("d = b + lambda/2", S.d, 12)
    show("M(1/2) = (1+u)/(2+u)", S.M, 12)
    show("m(1/2) = 1 - M", S.m, 12)
    show("theta = u/(2+u) = lambda/(lambda+2b)", S.theta, 12)
    show("check theta - (2M-1)", S.theta - (P.two * S.M - P.one), 12)
    show("v_F = 2b + lambda (volume, two-sided full)", S.vF, 12)
    show("v_U = 2b + lambda/2 (volume, buy-only)", S.vU, 12)
    show("v_N = 2b (volume, no informed trade)", S.vN, 12)
    show("beta <= 1/3: margin 1/3 - beta", I(Fr(1, 3)) - S.beta, 12)
    reg("u_p5_B", S.u, 6, note="Mirror of u_B (cross-check).")
    reg("lambda_p5_B", S.lam, 6, note="Mirror of lambda_B (cross-check).")
    reg("beta_p5_B", S.beta, 6, status="input", note="Mirror of beta_B (cross-check).")
    reg("b_p5_B", S.b, 6, note="Mirror of b_B: b=(1-lambda)beta.")
    reg("M_p5_B", S.M, 6, note="Mirror of M_half_B (cross-check).")
    reg("m_p5_B", S.m, 6, note="Mirror of m_half_B (cross-check).")
    reg("d_slot_B", S.d, 6, note="d = b + lambda/2 = Pr(X=1) = Pr(X=-1) on the full branch.")
    reg("vol_none_B", S.vN, 6, note="Volume 2b: no informed trade.")
    reg("vol_buy_B", S.vU, 6, note="Volume 2b+lambda/2: buy-only informed trade.")
    reg("vol_full_B", S.vF, 6, note="Volume 2b+lambda: two-sided full informed trade.")
    reg("theta_B", S.theta, 6, note="Informed share of nonzero orders on the full branch, u/(2+u)=2M-1.")
    reg("theta_pct_B", S.theta, 1, pct=True, note="Same as theta_B in percent.")

    # ------------------------------------------------------------------ 2
    header("2. THRESHOLDS, BOUNDARIES AND MARGINS AT B")
    au0, au1, au2 = (auction(P, I(r)) for r in (R0, R1, R2))
    tau1, tau2 = tau_of(P, au1), tau_of(P, au2)
    show("tau(3)  [141/200 = 0.705]", tau1, 9)
    show("tau(18/5)  [4245/5804]", tau2, 9)
    print(f"  tau(3) exact (Fraction arithmetic): {tau_of(PA, auction(PA, R1))}; tau(18/5) exact: {tau_of(PA, auction(PA, R2))}")
    show("M - tau(3)", S.M - tau1, 9)
    show("tau(18/5) - M", tau2 - S.M, 9)
    reg("margin_obs_beta_B", I(Fr(1, 3)) - S.beta, 6, note="1/3 - beta: the slot bound beta <= 1/3.")
    reg("margin_obs_u_hi_B", I(Fr(2686, 1559)) - S.u, 6, note="2686/1559 - u: upper end of the admitted u-band.")
    reg("margin_obs_buy_recruit_B", S.M - tau1, 6, note="M - tau(r_1): buy at r_1 recruits.")
    reg("margin_obs_ceiling_B", tau2 - S.M, 6, note="tau(r_2) - M: buy at r_2 does not recruit.")
    rC = rceil(P, S)
    show("r_C (closed form)", rC, 12)
    rC_lo_fr = Fr(int(lo(rC).man)) * Fr(2) ** int(lo(rC).exp) - Fr(1, 10 ** 30)
    rC_hi_fr = Fr(int(hi(rC).man)) * Fr(2) ** int(hi(rC).exp) + Fr(1, 10 ** 30)
    bl = Bfun(P, auction(P, I(rC_lo_fr)), S.M) - P.cH
    bh = Bfun(P, auction(P, I(rC_hi_fr)), S.M) - P.cH
    print(f"  B_r(M)-c_H at r_C - 1e-30: sign {sgn(bl)}; at r_C + 1e-30: sign {sgn(bh)}  (+1 and -1 certify the root)")
    reg("rC_check_B", rC, 6, note="Cross-check of the ceiling r_C: B_r(M)=c_H.")
    show("r_C - 3 (r_1 below the ceiling)", rC - I(R1), 9)
    show("18/5 - r_C (r_2 above the ceiling)", I(R2) - rC, 9)
    reg("margin_obs_r2_above_rC_B", I(R2) - rC, 6, note="r_2 - r_C.")
    D1, D2, D0 = au1["D"], au2["D"], au0["D"]
    print(f"  Delta_T(6/5)={au0['D']}, Delta_T(3)={au1['D']}, Delta_T(18/5)={au2['D']}  (exact)")
    show("k - Delta_T(r_0)  [= 1/300]", P.k - D0, 9)
    show("rho Delta_T(r_1)(1-M) - k (full buys / sells at r_1)", P.rho * D1 * S.m - P.k, 9)
    show("rho Delta_T(r_2)(1-M) - k", P.rho * D2 * S.m - P.k, 9)
    reg("margin_obs_full_orders_r1_B", P.rho * D1 * S.m - P.k, 6, note="rho Delta_T(r_1)(1-M) - k.")
    reg("margin_obs_full_orders_r2_B", P.rho * D2 * S.m - P.k, 6, note="rho Delta_T(r_2)(1-M) - k.")
    reg("margin_obs_weak_r0_B", P.k - D0, 6, status="analytical", note="k - Delta_T(r_0)=1/300.")
    show("B_{r_1}(1/2) - c_H (neutral order does not recruit)", Bfun(P, au1, P.pi) - P.cH, 9)
    show("B_{r_2}(1/2) - c_H", Bfun(P, au2, P.pi) - P.cH, 9)
    show("B_{r_1}(M) - c_H", Bfun(P, au1, S.M) - P.cH, 9)
    show("B_{r_2}(M) - c_H", Bfun(P, au2, S.M) - P.cH, 9)
    reg("margin_obs_neutral_r1_B", P.cH - Bfun(P, au1, P.pi), 6, note="c_H - B_{r_1}(1/2).")
    N_ = lambda D: iv.sqrt(D * D + P.two * D)
    rN = P.one + (P.two * P.k / P.rho) + N_(P.two * P.k / P.rho)
    rF = P.one + P.k / S.m + N_(P.k / S.m)
    rU = P.one + P.k / (P.rho * S.m) + N_(P.k / (P.rho * S.m))
    show("r_N = frak(2k/rho)", rN, 12)
    show("r_F = frak(k/(1-M)) at B", rF, 12)
    show("r_S = frak(k/(rho(1-M)))", rU, 12)
    reg("rF_check_B", rF, 6, note="r_F at B from Delta_T(r)(1-M)=k; agrees with rF_B of P1 and with the brief (1.467127).")
    reg("rS_p5_B", rU, 6,
        note="Mirror of rS_B (P1). Exact definition: r_S = fr(D_S) = 1 + D_S + sqrt(D_S^2 + 2 D_S) with D_S = k/(rho m) = 2(1+e)/25, "
             "the unique root r>1 of rho Delta_T(r) m = k. Full orders are unique for every r > r_S (open interval, exact r_S); "
             "the displayed 2.124148 lies below r_S and is not an endpoint; 2.124149 is a sufficient rounded endpoint (rS_cert_hi_B).")
    reg("rN_check_B", rN, 6, note="Cross-check of r_N: rho Delta_T(r)/2 = k.")
    # r_F at calibration A (exact formula, interval value) for the discrepancy note
    rF_A = P.one + P.k / I(Fr(11, 40)) + N_(P.k / I(Fr(11, 40)))
    show("r_F at M = 29/40 (calibration A)", rF_A, 9)
    for r in RCO:
        aur = auction(P, I(r))
        print(f"  r={r}: Delta_T={aur['D']}  Delta_T(1-M)-k = {fmt_dec(aur['D']*S.m-P.k, 6)}, "
              f"B_r(M)-c_H = {fmt_dec(Bfun(P, aur, S.M)-P.cH, 6)}, "
              f"k - rho Delta_T/2 = {fmt_dec(P.k-P.rho*aur['D']/P.two, 6)}")
    r165 = auction(P, I(Fr(33, 20)))
    reg("margin_obs_rF_B", I(Fr(31, 20)) - rF, 6, note="1.55 - r_F: the buy-only branch exists at 1.55.")
    reg("margin_obs_rN_B", rN - I(Fr(33, 20)), 6, note="r_N - 1.65: the buy-only branch exists at 1.65.")
    reg("margin_obs_lowsell_r165_B", P.k - P.rho * r165["D"] / P.two, 6,
        note="k - rho Delta_T(1.65)/2: the low class stays out on the buy-only branch.")
    r155 = auction(P, I(Fr(31, 20)))
    reg("margin_obs_buy_r155_B", r155["D"] * S.m - P.k, 6, note="Delta_T(1.55)(1-M) - k.")
    reg("margin_obs_buy_recruit_r165_B", Bfun(P, r165, S.M) - P.cH, 6, note="B_{1.65}(M) - c_H: the smallest recruit margin on the buy-only branch.")
    print(f"  Prop. 2 band for u: 82/59 = {float(Fr(82,59)):.6f} < u < 2686/1559 = {float(Fr(2686,1559)):.6f}; "
          f"u = {mp.nstr(midpoint(S.u), 8)}")
    show("2686/1559 - u", I(Fr(2686, 1559)) - S.u, 9)
    show("u - 82/59", S.u - I(Fr(82, 59)), 9)
    thlo = P.two * tau1 - P.one
    thhi = P.two * tau2 - P.one
    show("theta band lower 2 tau(3) - 1", thlo, 9)
    show("theta band upper 2 tau(18/5) - 1", thhi, 9)
    reg("theta_lo", thlo, 6, status="analytical", note="Lower end of the informed-share band: 2 tau(r_1) - 1 = 41/100.")
    reg("theta_hi", thhi, 6, note="Upper end of the informed-share band: 2 tau(r_2) - 1.")

    # ------------------------------------------------------------------ 3
    header("3. OUTCOMES AT THE THREE STRENGTHS AT B")
    cases = [("r_0=6/5, no informed trade (N)", R0, "N"),
             ("r_1=3, full orders (F)", R1, "F"),
             ("r_2=18/5, full orders (F)", R2, "F")]
    OC = {}
    for name, r, reg_ in cases:
        oc = outcome(P, S, I(r), reg_)
        OC[(r, reg_)] = oc
        print(f"\n  --- {name}")
        for x in (-1, 0, 1):
            print(f"  x={x:+d}: Pr={fmt_dec(oc['pr'][x], 6)}  mu={fmt_dec(oc['mu'][x], 6)}  "
                  f"entry={fmt_dec(oc['e'][x], 4)}  P={fmt_dec(oc['price'][x], 6)}  "
                  f"w={fmt_dec(oc['w'][x], 6)}  J={oc['J'][x]}")
        show("volume", oc["vol"])
        show("E[X]", oc["EX"])
        show("informed share of nonzero orders", oc["inf_share"])
        show("entry", oc["entry"])
        show("spread S = P(1)-P(-1)", oc["spread"])
        show("buy impact P(1)-P(0)", oc["imp_buy"])
        show("sell impact P(0)-P(-1)", oc["imp_sell"])
        show("mean price Pbar", oc["pbar"])
        show("P(0) - Pbar", oc["price"][0] - oc["pbar"])
        show("Cov(X, 1_A)", oc["cov_entry"])
        show("Cov(X, 1_W)", oc["cov_win"])
        show("Pr(challenger wins)", oc["winp"])
        show("H ownership (cross-check against the brief 0.3244)", oc["ownH"])

    o0, o1, o2 = OC[(R0, "N")], OC[(R1, "F")], OC[(R2, "F")]
    reg("own_p5_r1_B", o1["ownH"], 6, note="High-class ownership at r_1 (cross-check of own_r1_B).")
    reg("entry_floor_obs", P.rho, 2, status="input", note="rho = entry floor.")
    reg("entry_plateau_B", o1["entry"], 6, note="rho+(1-rho)d: entry at r_1 (buy recruits).")
    reg("entry_jump_B", o1["entry"] - P.rho, 6, note="(1-rho)d: entry rise from r_0 to r_1, and fall from r_1 to r_2.")
    reg("entry_r2_obs_B", o2["entry"], 2, status="analytical", note="Entry at r_2 equals rho.")

    # ------------------------------------------------------------------ 4
    header("4. SPREAD: CLASS COMPONENT AND ENTRY COMPONENT (F REGIME)")
    for name, r, o in (("r_1", R1, o1), ("r_2", R2, o2)):
        au = o["au"]
        Ainf = P.rho * au["D"] * S.theta
        Aent = (P.one - P.rho) * (P.one if o["J"][1] == 1 else P.zero) * o["A"][1]
        print(f"\n  --- {name}")
        show("class component rho Delta_T theta", Ainf)
        show("entry component (1-rho) J A(M)", Aent)
        show("sum", Ainf + Aent)
        show("spread S", o["spread"])
        show("entry share of the spread", Aent / o["spread"], 1, pct=True)
        show("hidden-price spread (entry stays at rho)", Ainf)
        show("spread ratio visible/hidden", o["spread"] / Ainf, 3)
        show("buy impact minus sell impact", o["imp_buy"] - o["imp_sell"])
        show("A(M) = t_L - t_0 + Delta_T M", o["A"][1])
    reg("ba_class_r1_B", P.rho * D1 * S.theta, 6, note="Class component rho Delta_T theta at r_1.")
    reg("ba_entry_r1_B", o1["spread"] - P.rho * D1 * S.theta, 6, note="Entry component (1-rho)A(M) at r_1.")
    reg("ba_r1_B", o1["spread"], 6, note="Spread P(1)-P(-1) at r_1.")
    reg("ba_share_r1_B", (o1["spread"] - P.rho * D1 * S.theta) / o1["spread"], 1, pct=True,
        note="Entry share of the spread at r_1.")
    reg("ba_ratio_r1_B", o1["spread"] / (P.rho * D1 * S.theta), 1, note="Spread with price access over spread with hidden price at r_1.")
    reg("impact_sell_r1_B", o1["imp_sell"], 6, note="Sell impact P(0)-P(-1) at r_1 = rho Delta_T theta/2.")
    reg("impact_buy_r1_B", o1["imp_buy"], 6, note="Buy impact P(1)-P(0) at r_1.")
    reg("impact_asym_r1_B", o1["imp_buy"] - o1["imp_sell"], 6, note="Buy impact minus sell impact at r_1 = (1-rho)A(M).")
    reg("ba_r2_B", o2["spread"], 6, note="Spread at r_2 (equals class component, no entry component).")
    reg("impact_sell_r2_B", o2["imp_sell"], 6, note="Sell impact at r_2 (equals buy impact).")
    reg("pbar_r1_B", o1["pbar"], 6, note="Expected price before the slot at r_1.")
    reg("p_neutral_r1_B", o1["price"][0], 6, note="Price after a neutral order at r_1.")
    reg("pdrop_neutral_r1_B", o1["price"][0] - o1["pbar"], 6, note="P(0) - Pbar at r_1 = -(1-rho)dA(M).")
    reg("pdrop_neutral_r2_B", o2["price"][0] - o2["pbar"], 2, note="P(0) - Pbar at r_2 is zero.")

    header("4b. THE CEILING r_C: LEFT VALUE (TIE RULE C1) AND RIGHT LIMIT")
    auC = auction(P, rC)
    # at r_C itself B_r(M) = c_H exactly, so the sign is undecided in the interval; use J = 1 (rule C1) and J = 0 (right limit)
    A_M_C = Afun(auC, S.M)
    inf_C = P.rho * auC["D"] * S.theta
    left = inf_C + (P.one - P.rho) * A_M_C
    right = inf_C
    show("Delta_T(r_C)", auC["D"])
    show("S(r_C) with rule C1 (buy recruits at indifference)", left)
    show("S(r_C+) right limit", right)
    show("jump (1-rho) A_{r_C}(M)", left - right)
    show("jump in Pbar: -(1-rho) d A_{r_C}(M)", -(P.one - P.rho) * S.d * A_M_C)
    show("buy impact left of r_C", P.rho * auC["D"] * S.theta / P.two + (P.one - P.rho) * A_M_C)
    show("buy impact right of r_C", P.rho * auC["D"] * S.theta / P.two)
    reg("ba_rC_left_B", left, 6, note="Spread at r_C under rule C1.")
    reg("ba_rC_right_B", right, 6, note="Right limit of the spread at r_C.")
    reg("ba_jump_rC_B", left - right, 6, note="Fall of the spread at r_C: (1-rho)A_{r_C}(M).")
    reg("pbar_jump_rC_B", -(P.one - P.rho) * S.d * A_M_C, 6, note="Change of the expected pre-slot price at r_C.")
    # monotonicity pieces
    print("\n  Derivatives at B (exact): Delta_T'(r)=1/2-1/(2r^2); d(t_L-t_0)/dr=(l^2-3p^2)/(2r^2)=1/(8r^2)")
    for r in (R1, R2):
        print(f"   r={r}: Delta_T'={Fr(1,2)-Fr(1,2)/(r*r)}, d(t_L-t_0)/dr={Fr(1,8)/(r*r)}")
    # spread just below and above r_C (rational points), for display
    for rr in (Fr(359, 100), Fr(3593, 1000), Fr(36, 10)):
        o = outcome(P, S, I(rr), "F")
        print(f"   r={float(rr)}: J(buy)={o['J'][1]}, S={fmt_dec(o['spread'], 6)}, buy impact={fmt_dec(o['imp_buy'], 6)}, sell impact={fmt_dec(o['imp_sell'], 6)}, entry={fmt_dec(o['entry'], 6)}")

    # ------------------------------------------------------------------ 5
    header("5. IDENTIFICATION OF THE INFORMED SHARE (F REGIME, r = r_1)")
    v = o1["vol"]
    Rhat = P.two * o1["imp_sell"] / (P.rho * D1)
    show("theta recovered: 2 [P(0)-P(-1)]/(rho Delta_T)", Rhat, 9)
    lam_hat = v * Rhat
    beta_hat = v * (P.one - Rhat) / (P.two * (P.one - v * Rhat))
    show("lambda recovered v theta", lam_hat, 9)
    show("beta recovered v(1-theta)/(2(1-v theta))", beta_hat, 9)
    show("true lambda", S.lam, 9)
    show("true beta", S.beta, 9)
    show("u recovered 2 theta/(1-theta)", P.two * Rhat / (P.one - Rhat), 9)
    # counts-only identified set
    vv = S.vF
    u_min = (P.c(Fr(3)) * vv - P.two) / (P.one - vv)
    th_min = u_min / (P.two + u_min)
    show("v (volume) at r_1", vv, 9)
    show("smallest u with beta <= 1/3 and the same volume", u_min, 9)
    show("informed share at that u", th_min, 9)
    print("  For every u' >= u_min there is one pair (lambda', beta') with the same volume and beta' <= 1/3;")
    print("  informed share u'/(2+u') then ranges over [theta_min, 1) and is not identified by counts.")
    print("  Inside the Proposition-2 band the informed share ranges over (0.41, theta_hi).")
    for up in (Fr(82, 59) + Fr(1, 1000), Fr(8, 5), Fr(2686, 1559) - Fr(1, 1000)):
        upi = I(up)
        lam_p = vv * upi / (upi + P.two)
        b_p = lam_p / upi
        beta_p = b_p / (P.one - lam_p)
        Sp = Slot(P, upi, beta_p)
        op = outcome(P, Sp, I(R1), "F")
        print(f"  u'={float(up):.6f}: lambda'={fmt_dec(lam_p, 6)}, beta'={fmt_dec(beta_p, 6)}, theta'={fmt_dec(Sp.theta, 6)}, "
              f"volume={fmt_dec(op['vol'], 6)}, entry={fmt_dec(op['entry'], 6)}, spread={fmt_dec(op['spread'], 6)}, "
              f"J(buy)={op['J'][1]}")
        if up == Fr(8, 5):
            reg("alt_lambda_B", lam_p, 6, note="Alternative pair with u'=8/5 and the same order frequencies as B: lambda'.")
            reg("alt_beta_B", beta_p, 6, note="Alternative pair with u'=8/5: beta'.")
            reg("alt_theta_B", Sp.theta, 6, note="Informed share at u'=8/5 (4/9).")
            reg("alt_ba_r1_B", op["spread"], 6, note="Spread at r_1 for the alternative pair u'=8/5.")
            reg("alt_entry_r1_B", op["entry"], 6, note="Entry at r_1 for the alternative pair (equals the entry at B).")
    reg("theta_min_counts_B", th_min, 6, note="Smallest informed share consistent with the order frequencies at B and beta<=1/3.")

    # buy-only branch identification
    header("5b. BUY-ONLY BRANCH: INFORMED SHARE FROM COUNTS")
    for r in RCO:
        ou = outcome(P, S, I(r), "U")
        show(f"r={r}: E[X] = lambda/2", ou["EX"], 9)
        show(f"r={r}: E[X]/volume = informed share", ou["EX"] / ou["vol"], 9)
    reg("imb_buy_B", S.lam / P.two, 6, note="Mean order E[X] = lambda/2 on the buy-only branch.")
    reg("theta_buy_B", S.u / (P.c(Fr(4)) + S.u), 6, note="Informed share of nonzero orders on the buy-only branch, u/(4+u).")
    reg("theta_buy_pct_B", S.u / (P.c(Fr(4)) + S.u), 1, pct=True, note="Same as theta_buy_B in percent.")

    # ------------------------------------------------------------------ 6
    header("6. COEXISTENCE BRANCH: OUTCOMES AT 1.55, 1.60, 1.65 (U) AND NO TRADE (N)")
    for r in RCO:
        ou = outcome(P, S, I(r), "U")
        on = outcome(P, S, I(r), "N")
        print(f"\n  --- r={r}")
        for x in (-1, 0, 1):
            print(f"  U: x={x:+d}: Pr={fmt_dec(ou['pr'][x], 6)}  mu={fmt_dec(ou['mu'][x], 6)}  entry={fmt_dec(ou['e'][x], 4)}  P={fmt_dec(ou['price'][x], 6)}  J={ou['J'][x]}")
        show("U: volume", ou["vol"])
        show("U: E[X]", ou["EX"])
        show("U: entry", ou["entry"])
        show("U: spread P(1)-P(-1)", ou["spread"])
        show("U: P(-1)-P(0) (sell executes above neutral)", ou["price"][-1] - ou["price"][0])
        show("U: P(1)-P(-1)", ou["price"][1] - ou["price"][-1])
        show("U: mean price", ou["pbar"])
        show("N: entry", on["entry"])
        show("N: price (all orders)", on["price"][0])
        show("N: spread", on["spread"])
    ou = outcome(P, S, I(Fr(8, 5)), "U")
    reg("U_entry_B", ou["entry"], 6, note="Entry on the buy-only branch (same at 1.55, 1.60, 1.65).")
    reg("ba_U_r160_B", ou["spread"], 6, note="Spread P(1)-P(-1) at 1.60 on the buy-only branch.")
    reg("U_gap_r160_B", ou["price"][-1] - ou["price"][0], 6, note="P(-1)-P(0) at 1.60 on the buy-only branch (positive).")
    reg("U_mu0_B", ou["mu"][0], 6, note="Posterior after a neutral order on the buy-only branch.")
    reg("U_sell_mu_B", ou["mu"][-1], 2, status="analytical", note="Posterior after a sale on the buy-only branch is 1/2.")
    o155 = outcome(P, S, I(Fr(31, 20)), "U")
    o165 = outcome(P, S, I(Fr(33, 20)), "U")
    reg("ba_U_r155_B", o155["spread"], 6, note="Spread at 1.55 on the buy-only branch.")
    reg("ba_U_r165_B", o165["spread"], 6, note="Spread at 1.65 on the buy-only branch.")

    # ------------------------------------------------------------------ 7
    header("7. WINNERS (F REGIME)")
    for name, r, o in (("r_1", R1, o1), ("r_2", R2, o2)):
        print(f"\n  --- {name}")
        for x in (-1, 0, 1):
            print(f"  x={x:+d}: Pr(W|x,A)={fmt_dec(o['w'][x], 6)}  Pr(W|x)={fmt_dec(o['e'][x]*o['w'][x], 6)}")
        show("gap Pr(W|buy,A)-Pr(W|sell,A) = theta(1-l/r)", o["w"][1] - o["w"][-1])
        show("Cov(X,1_A)", o["cov_entry"])
        show("Cov(X,1_W)", o["cov_win"])
        show("Pr(W)", o["winp"])
        show("d rho theta (1-l/r)  [formula above r_C]", S.d * P.rho * S.theta * (P.one - P.l / I(r)))
    reg("wgap_r1_B", o1["w"][1] - o1["w"][-1], 6, note="theta(1-l/r) at r_1.")
    reg("wgap_r2_B", o2["w"][1] - o2["w"][-1], 6, note="theta(1-l/r) at r_2.")
    reg("wprep_buy_r1_B", o1["w"][1], 6, note="Pr(W|buy, prepared) at r_1.")
    reg("wprep_sell_r1_B", o1["w"][-1], 6, note="Pr(W|sale, prepared) at r_1.")
    reg("wprep_neutral_r1_B", o1["w"][0], 6, note="Pr(W|neutral, prepared) at r_1.")
    reg("wprep_buy_r2_B", o2["w"][1], 6, note="Pr(W|buy, prepared) at r_2.")
    reg("wprep_sell_r2_B", o2["w"][-1], 6, note="Pr(W|sale, prepared) at r_2.")
    reg("wprep_neutral_r2_B", o2["w"][0], 6, note="Pr(W|neutral, prepared) at r_2.")
    reg("cov_entry_r1_B", o1["cov_entry"], 6, note="Cov(X, 1_A) at r_1 = d(1-rho).")
    reg("cov_entry_r2_B", o2["cov_entry"], 2, status="analytical", note="Cov(X, 1_A) at r_2 is zero.")
    reg("cov_win_r1_B", o1["cov_win"], 6, note="Cov(X, 1_W) at r_1.")
    reg("cov_win_r2_B", o2["cov_win"], 6, note="Cov(X, 1_W) at r_2 = d rho theta (1-l/r).")
    reg("win_prob_r1_B", o1["winp"], 6, note="Pr(challenger wins) at r_1.")
    reg("win_prob_r2_B", o2["winp"], 6, note="Pr(challenger wins) at r_2.")

    # ------------------------------------------------------------------ 8
    header("8. EVENT RETURNS AT THE ANNOUNCEMENT OF PREPARATION OR ITS ABSENCE")
    names = {-1: "sale", 0: "neutral", 1: "buy"}
    for name, r, o in (("r_1", R1, o1), ("r_2", R2, o2)):
        print(f"\n  --- {name}")
        for x in (-1, 0, 1):
            pa = o["evA"][x]
            pn = o["evN"][x]
            print(f"  {names[x]:8s}: P(x)={fmt_dec(o['price'][x], 6)}  prepare: +{fmt_dec(pa, 6)} ({fmt_dec(pa/o['price'][x], 6)} of P)   "
                  f"no preparation: {fmt_dec(pn, 6)} ({fmt_dec(pn/o['price'][x], 6)} of P)  e={fmt_dec(o['e'][x], 4)}")
            chk = o["e"][x] * pa + (P.one - o["e"][x]) * pn
            print(f"            cost-weighted mean change (should be 0): {fmt_dec(chk, 10)}")
    for tag, r, o in (("r1", R1, o1), ("r2", R2, o2)):
        for x, nm in ((-1, "sale"), (0, "neutral"), (1, "buy")):
            reg(f"evA_{tag}_{nm}_B", o["evA"][x], 6, note=f"Price change in dollars when preparation is announced, after a {nm}, at {tag}.")
            if tag == "r2" or nm != "buy":
                reg(f"evAr_{tag}_{nm}_B", o["evA"][x] / o["price"][x], 6, note=f"Same change divided by P(x), {nm}, {tag}.")
        for x, nm in ((-1, "sale"), (0, "neutral"), (1, "buy")):
            if tag == "r2" or nm != "buy":
                reg(f"evN_{tag}_{nm}_B", o["evN"][x], 6, note=f"Price change in dollars when no preparation is announced, after a {nm}, at {tag}.")
                reg(f"evNr_{tag}_{nm}_B", o["evN"][x] / o["price"][x], 6, note=f"Same change divided by P(x), {nm}, {tag}.")
    for tag, o in (("r1", o1), ("r2", o2)):
        for x, nm in ((-1, "sale"), (0, "neutral"), (1, "buy")):
            reg(f"price_{tag}_{nm}_B", o["price"][x], 6, note=f"Price P(x) after a {nm} at {tag}.")

    # ------------------------------------------------------------------ 9
    header("9. FIGURE DATA: FULL-ORDER BRANCH, r from 2.2 to 6.0")
    path = HERE / "curves_full_branch.csv"
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["r", "class_component", "entry_component", "spread", "buy_impact", "sell_impact", "entry", "winner_gap"])
        n = 0
        rr = Fr(22, 10)
        while rr <= Fr(6):
            o = outcome(P, S, I(rr), "F")
            au = o["au"]
            inf_c = P.rho * au["D"] * S.theta
            ent_c = o["spread"] - inf_c
            w.writerow([float(rr), f"{float(midpoint(inf_c)):.9f}", f"{float(midpoint(ent_c)):.9f}",
                        f"{float(midpoint(o['spread'])):.9f}", f"{float(midpoint(o['imp_buy'])):.9f}",
                        f"{float(midpoint(o['imp_sell'])):.9f}", f"{float(midpoint(o['entry'])):.9f}",
                        f"{float(midpoint(o['w'][1] - o['w'][-1])):.9f}"])
            rr += Fr(1, 100)
            n += 1
    print(f"  wrote {path.name}: {n} rows")

    # ------------------------------------------------------------------ 10
    header("10. CALIBRATION A (BETA = 1/3, LAMBDA = 6/17): EXACT RECOMPUTATION OF THE EARLIER STUDY")
    oA1 = outcome(PA, SA, R1, "F")
    oA2 = outcome(PA, SA, R2, "F")
    oAweak = outcome(PA, SA, R0, "N")
    entries = [
        ("M", SA.M, "29/40"),
        ("theta = 2M-1", SA.theta, "9/20"),
        ("volume at r_1, r_2", SA.vF, "40/51"),
        ("S(3)", oA1["spread"], "25/32"),
        ("class component at 3", PA.rho * oA1["au"]["D"] * SA.theta, "3/40"),
        ("entry share at 3", (oA1["spread"] - PA.rho * oA1["au"]["D"] * SA.theta) / oA1["spread"], "113/125"),
        ("S(18/5)", oA2["spread"], "169/1600"),
        ("gap at 3", oA1["w"][1] - oA1["w"][-1], "3/10"),
        ("gap at 18/5", oA2["w"][1] - oA2["w"][-1], "13/40"),
        ("Cov(X,1_A) at 3", oA1["cov_entry"], "5/17"),
        ("Cov(X,1_W) at 18/5", oA2["cov_win"], "13/408"),
        ("Pbar at 3", oA1["pbar"], "485/544"),
        ("P(0) at 3", oA1["price"][0], "59/96"),
        ("P(0)-Pbar at 3", oA1["price"][0] - oA1["pbar"], "-113/408"),
        ("entry at 3", oA1["entry"], "37/68"),
        ("announce, sale at 3", oA1["evA"][-1], "77/160"),
        ("announce, neutral at 3", oA1["evA"][0], "19/32"),
        ("announce, buy at 3", oA1["evA"][1], "0"),
        ("announce, sale at 18/5", oA2["evA"][-1], "5209/9600"),
        ("announce, neutral at 18/5", oA2["evA"][0], "673/960"),
        ("announce, buy at 18/5", oA2["evA"][1], "8251/9600"),
    ]
    for lab, val, quoted in entries:
        print(f"  {lab:<28s} recomputed {str(val):<14s} quoted {quoted:<12s} same: {val == Fr(quoted)}")
    print(f"  buy-only branch at A, r=1.55: volume {outcome(PA, SA, Fr(31, 20), 'U')['vol']}, informed share {outcome(PA, SA, Fr(31,20), 'U')['inf_share']}, E[X] {outcome(PA, SA, Fr(31,20), 'U')['EX']}  (quoted 31/51, 9/31, 3/17)")
    PAi = Prim(exact=False)
    SAi = Slot(PAi, I(Fr(18, 11)), I(Fr(1, 3)))
    rCAi = rceil(PAi, SAi)
    show("r_C at A  (quoted 3.45824702905933)", rCAi, 12)

    # ------------------------------------------------------------------ 11
    header("11. VERIFICATION AGAINST THE FIXED TUPLE: DEALER, INVESTOR AND CHALLENGER CONDITIONS")
    print("  Dealer check: P(x) vs E[V_T | X=x] computed class by class.")
    print("  Investor payoff U_j(q) = q [E[V_T|j,q] - P(q)] - k|q| at the fixed price and entry schedule.")
    print("  Challenger check: sign of B_r(mu_x) - c_H and the entry chosen.")
    ver = [("N", R0), ("F", R1), ("F", R2)] + [("U", r) for r in RCO]
    for reg_, r in ver:
        oc = outcome(P, S, I(r), reg_)
        au = oc["au"]
        print(f"\n  --- regime {reg_}, r={r}")
        for x in (-1, 0, 1):
            ev_H = au["t0"] + oc["e"][x] * (au["tH"] - au["t0"])
            ev_L = au["t0"] + oc["e"][x] * (au["tL"] - au["t0"])
            pc = oc["mu"][x] * ev_H + (P.one - oc["mu"][x]) * ev_L
            bsg = sgn(Bfun(P, au, oc["mu"][x]) - P.cH)
            print(f"  x={x:+d}: dealer check P-E[V_T|x] = {fmt_dec(oc['price'][x] - pc, 8)}; "
                  f"B(mu)-c_H = {fmt_dec(Bfun(P, au, oc['mu'][x]) - P.cH, 4)} (sign {bsg}); entry {fmt_dec(oc['e'][x], 4)}")
        for jn, tj in (("H", au["tH"]), ("L", au["tL"])):
            row = []
            for q in (-1, 0, 1):
                ev = au["t0"] + oc["e"][q] * (tj - au["t0"])
                row.append(q * (ev - oc["price"][q]) - P.k * (1 if q != 0 else 0))
            print(f"  class {jn}: U(-1)={fmt_dec(row[0], 6)}  U(0)={fmt_dec(row[1], 6)}  U(+1)={fmt_dec(row[2], 6)}")
        # equilibrium order and its margin against the best alternative
        rowH = []
        rowL = []
        for q in (-1, 0, 1):
            rowH.append(q * (au["t0"] + oc["e"][q] * (au["tH"] - au["t0"]) - oc["price"][q]) - P.k * (1 if q else 0))
            rowL.append(q * (au["t0"] + oc["e"][q] * (au["tL"] - au["t0"]) - oc["price"][q]) - P.k * (1 if q else 0))
        qH = 1 if reg_ in ("U", "F") else 0
        qL = -1 if reg_ == "F" else 0
        altH = [rowH[j] for j in range(3) if j != qH + 1]
        altL = [rowL[j] for j in range(3) if j != qL + 1]
        gapH = rowH[qH + 1] - (altH[0] if sgn(altH[0] - altH[1]) == 1 else altH[1])
        gapL = rowL[qL + 1] - (altL[0] if sgn(altL[0] - altL[1]) == 1 else altL[1])
        print(f"  equilibrium order H={qH:+d}, L={qL:+d}; payoff gap to the best alternative: H {fmt_dec(gapH, 6)}, L {fmt_dec(gapL, 6)}")

    # ------------------------------------------------------------------ 12
    header("12. ROUND 2: BOUND r_S, SPREAD COMPONENTS, COUNT RANGE, MIXTURE TUPLE, SAMPLE MEANS, MARGINS")

    # 12a ---------------------------------------------------------------
    print("\n  12a. The full-order bound r_S = fr(D_S), D_S = k/(rho m)")
    DS = P.k / (P.rho * S.m)
    show("D_S = k/(rho m)", DS, 12)
    show("D_S - 2(1+e)/25 (check, 0)", DS - P.two * (P.one + iv.e) / I(Fr(25)), 12)
    show("Delta_T(r_S) - D_S (check, 0)", auction(P, rU)["D"] - DS, 12)
    show("r_S", rU, 20)
    margins_rs = {}
    for label, rr_ in (("2.124148", Fr(2124148, 10 ** 6)), ("2.1241481", Fr(21241481, 10 ** 7)),
                       ("2.124149", Fr(2124149, 10 ** 6))):
        mg = P.rho * auction(P, I(rr_))["D"] * S.m - P.k
        margins_rs[label] = mg
        print(f"  r = {label}: rho Delta_T(r) m - k = {enclosure(mg, 12)}; sign {sgn(mg)}"
              f"  (positive: F is unique; negative: the low class prefers to abstain in F)")
    sci_lo = mp.nstr(lo(margins_rs["2.1241481"]), 3)
    sci_hi = mp.nstr(hi(margins_rs["2.1241481"]), 3)
    if sci_lo != sci_hi:
        FLAGS.append("AMBIGUOUS SCIENTIFIC ROUNDING in rS_counter_margin_B")
    mant, ex = sci_lo.split("e")
    reg("delta_rS_B", DS, 6, note="D_S = k/(rho m) = 2(1+e)/25: the value of Delta_T at r_S, and r_S = fr(D_S).")
    reg("rS_cert_hi_B", Fr(2124149, 10 ** 6), 6,
        note="Sufficient rounded endpoint: rho Delta_T(r) m - k > 0 for every r >= 2.124149 (interval test in the run log); r_S < 2.124149.")
    reg("rS_counter_r_B", Fr(21241481, 10 ** 7), 7,
        note="A strength inside the interval (2.124148, 10) that lies below r_S: F is not an equilibrium there.")
    reg("rS_counter_margin_B", margins_rs["2.1241481"], 3,
        display=rf"\ensuremath{{{mant}\times10^{{{int(ex)}}}}}",
        note="rho Delta_T(r) m - k at r = 2.1241481 (negative): the low class strictly prefers to abstain in F.")

    # 12b ---------------------------------------------------------------
    print("\n  12b. Spread components across the ceiling r_C (outcome F), r_S < r < h  [numerical diagnostic]")
    print(f"  r_C = {fmt_dec(rC, 9)}")
    grid = [Fr(j, 10) for j in range(22, 100)]
    rows_sp = []
    for rr_ in grid:
        o = outcome(P, S, I(rr_), "F")
        cls = P.rho * o["au"]["D"] * S.theta
        ent = (P.one - P.rho) * (P.one if o["J"][1] == 1 else P.zero) * o["A"][1]
        rows_sp.append((rr_, o["J"][1], cls, ent, o["imp_sell"], o["imp_buy"], o["spread"]))
    print("    r     J   class comp.   entry comp.   sell impact   buy impact    spread")
    for rr_, J_, cls, ent, isell, ibuy, sp in rows_sp:
        if rr_ in (Fr(22, 10), Fr(3), Fr(7, 2), Fr(36, 10), Fr(4), Fr(5), Fr(99, 10)):
            print(f"  {float(rr_):5.2f}  {J_}   {fmt_dec(cls, 6):>11s}   {fmt_dec(ent, 6):>11s}   {fmt_dec(isell, 6):>11s}   {fmt_dec(ibuy, 6):>11s}   {fmt_dec(sp, 6):>9s}")

    def rising(idx, subset):
        pts = [t for t in rows_sp if subset(t[0])]
        return yes(all(sgn(b_[idx] - a_[idx]) == 1 for a_, b_ in zip(pts, pts[1:])))

    below = lambda r_: r_ <= Fr(7, 2)
    above = lambda r_: r_ >= Fr(36, 10)
    allr = lambda r_: True
    names12 = [(2, "class component"), (3, "entry component"), (4, "sell impact I-"), (5, "buy impact I+"), (6, "spread S")]
    print("  strictly increasing on the grid (step 0.1):   r <= 3.5 | r >= 3.6 | whole grid")
    for idx, nm in names12:
        print(f"    {nm:<18s} {rising(idx, below):>8s} {rising(idx, above):>9s} {rising(idx, allr):>10s}")
    zero_ent = all(lo(t[3]) == 0 and hi(t[3]) == 0 for t in rows_sp if above(t[0]))
    print(f"  entry component exactly 0 at every grid point r >= 3.6: {yes(zero_ent)}")

    # 12c ---------------------------------------------------------------
    print("\n  12c. Counts: the informed share once full orders must be an equilibrium")
    thmax = {}
    for nm, r_ in (("r_1", R1), ("r_2", R2)):
        Dx = auction(PA, r_)["D"]
        thmax[nm] = Fr(1) - 2 * PA.k / (PA.rho * Dx)
        print(f"  {nm}: rho Delta_T(r) (1-theta')/2 - k >= 0  <=>  theta' <= {thmax[nm]} = {float(thmax[nm]):.12f}")
    reg("theta_max_full_eq_r1_B", thmax["r_1"], 6, status="analytical",
        note="1 - 2k/(rho Delta_T(r_1)) = 19/25: F is an equilibrium at r_1 iff theta' < this value (strict incentives).")
    reg("theta_max_full_eq_r2_B", thmax["r_2"], 6, status="analytical",
        note="1 - 2k/(rho Delta_T(r_2)) = 701/845: the same bound at r_2.")
    tau2_ex = tau_of(PA, auction(PA, R2))
    band_inc = PA.rho * auction(PA, R1)["D"] * (Fr(1) - tau2_ex) - PA.k
    print(f"  band incentive bound rho Delta_T(r_1)(1 - tau(r_2)) - k = {band_inc} = {float(band_inc):.9f}")
    reg("margin_obs_band_incentive_B", band_inc, 6, status="analytical",
        note="rho Delta_T(r_1)(1-tau(r_2)) - k: every pair in the share band has strict full-order incentives at r_1 and r_2.")
    th09 = Fr(9, 10)
    u09 = I(Fr(2) * th09 / (Fr(1) - th09))
    vv = S.vF
    lam09 = vv * u09 / (u09 + P.two)
    beta09 = (lam09 / u09) / (P.one - lam09)
    low09 = PA.rho * auction(PA, R1)["D"] * (Fr(1) - th09) / 2 - PA.k
    print(f"  theta'=0.9: u'=18, lambda'={fmt_dec(lam09, 9)}, beta'={fmt_dec(beta09, 9)} (<= 1/3), "
          f"same counts as B; low-class sale payoff in F at r_1 = {low09} = {float(low09):.9f}")
    reg("theta09_beta_B", beta09, 6, note="beta' of the full-order pair with theta'=0.9 and the volume of B: admissible for counts.")
    reg("theta09_lowsale_r1_B", low09, 6, status="analytical",
        note="Low-class sale payoff in F at r_1 for theta'=0.9: negative, so this pair gives its counts in no F equilibrium.")
    print(f"  volume at B {fmt_dec(vv, 9)} <= 200/259 = {float(Fr(200, 259)):.9f}: {yes(sgn(I(Fr(200, 259)) - vv) == 1)}")
    for up in (Fr(82, 59) + Fr(1, 1000), Fr(8, 5), Fr(2686, 1559) - Fr(1, 1000)):
        upi = I(up)
        mp_ = P.one / (P.two + upi)
        pay1 = P.rho * auction(P, I(R1))["D"] * mp_ - P.k
        pay2 = P.rho * auction(P, I(R2))["D"] * mp_ - P.k
        print(f"  band pair u'={float(up):.6f}: low-class sale payoff in F at r_1 {fmt_dec(pay1, 6)}, at r_2 {fmt_dec(pay2, 6)}")

    # 12d ---------------------------------------------------------------
    print("\n  12d. Strict margins added in round 2, and the open parameter set")
    reg("margin_obs_u_lo_B", S.u - I(Fr(82, 59)), 6, note="u - 82/59: lower end of the admitted u-band.")
    reg("margin_obs_post_over_58_B", S.M - I(Fr(5, 8)), 6, note="M - 5/8: the ceiling r_C(M) exists.")
    reg("margin_obs_rS_rC_B", rC - rU, 6, note="r_C - r_S: the ceiling lies inside the full-order interval.")
    reg("margin_obs_rN_rC_B", rC - rN, 6, note="r_C - r_N: recruitment holds on the whole coexistence interval.")
    reg("margin_obs_rS_h_B", P.h - rU, 6, note="h - r_S: the full-order interval is not empty.")

    def rC_of(Mx):
        a_ = Mx * P.h - P.cH
        return (a_ + iv.sqrt(a_ * a_ + Mx * ((P.one - Mx) * P.l * P.l - P.p * P.p))) / Mx

    print("  Thresholds at the two ends of the M-band (they are increasing in M, so the ends bound the open set):")
    for nm, Mx in (("M = tau(3) = 141/200", I(Fr(141, 200))), ("M = tau(18/5) = 4245/5804", I(Fr(4245, 5804)))):
        mx = P.one - Mx
        fr_ = lambda D_: P.one + D_ + iv.sqrt(D_ * D_ + P.two * D_)
        print(f"   {nm}: r_F {fmt_dec(fr_(P.k / mx), 6)}, r_N {fmt_dec(rN, 6)}, r_S {fmt_dec(fr_(P.k / (P.rho * mx)), 6)}, "
              f"r_C {fmt_dec(rC_of(Mx), 6)}")

    # 12e ---------------------------------------------------------------
    print("\n  12e. Partial-buy tuple when an indifferent challenger may mix, r = 1.60")
    r16 = I(Fr(8, 5))
    au16 = auction(P, r16)
    tau16 = tau_of(P, au16)
    D16 = au16["D"]
    s16 = S.b * (P.two * tau16 - P.one) / (P.one - tau16)
    sig16 = s16 / S.lam
    e16 = P.k / (D16 * (P.one - tau16))
    aH16 = {1: S.b + s16, -1: S.b, 0: P.one - P.two * S.b - s16}
    aL16 = {1: S.b, -1: S.b, 0: P.one - P.two * S.b}
    pr16 = {x: (aH16[x] + aL16[x]) / P.two for x in aH16}
    mu16 = {x: aH16[x] / (aH16[x] + aL16[x]) for x in aH16}
    ee16 = {1: e16, -1: P.rho, 0: P.rho}
    pc16 = {x: au16["t0"] + ee16[x] * Afun(au16, mu16[x]) for x in aH16}
    show("tau(1.60)", tau16, 9)
    show("sigma_H(1) = s_tau/lambda", sig16, 12)
    show("e_1 = k/(Delta_T (1 - tau))", e16, 12)
    print(f"  sigma in (0,1): {yes(sgn(sig16) == 1 and sgn(P.one - sig16) == 1)}; e_1 in (rho,1): {yes(sgn(e16 - P.rho) == 1 and sgn(P.one - e16) == 1)}")
    for x in (-1, 0, 1):
        evH = au16["t0"] + ee16[x] * (au16["tH"] - au16["t0"])
        evL = au16["t0"] + ee16[x] * (au16["tL"] - au16["t0"])
        dealer = mu16[x] * evH + (P.one - mu16[x]) * evL - pc16[x]
        print(f"  x={x:+d}: Pr={fmt_dec(pr16[x], 6)}  mu={fmt_dec(mu16[x], 9)}  entry={fmt_dec(ee16[x], 6)}  P={fmt_dec(pc16[x], 6)}  "
              f"B(mu)-c_H={enclosure(Bfun(P, au16, mu16[x]) - P.cH, 6)}  dealer check {fmt_dec(dealer, 10)}")
    print(f"  mu_1 - tau = {enclosure(mu16[1] - tau16, 6)} (0: the challenger with cost c_H is indifferent)")
    for jn, tj in (("H", au16["tH"]), ("L", au16["tL"])):
        row = [q * (au16["t0"] + ee16[q] * (tj - au16["t0"]) - pc16[q]) - P.k * (1 if q else 0) for q in (-1, 0, 1)]
        print(f"  class {jn}: U(-1)={enclosure(row[0], 8)}  U(0)={enclosure(row[1], 8)}  U(+1)={enclosure(row[2], 8)}")
    print(f"  prices ordered P(0) < P(-1) < P(1): {yes(sgn(pc16[-1] - pc16[0]) == 1 and sgn(pc16[1] - pc16[-1]) == 1)}")
    EX16 = pr16[1] - pr16[-1]
    ent16 = sum((pr16[x] * ee16[x] for x in aH16), P.zero)
    show("E[X] = s_tau/2", EX16, 9)
    show("entry", ent16, 9)
    low16 = P.rho * D16 / P.two - P.k
    show("low-class sale payoff rho Delta_T/2 - k", low16, 9)
    reg("mix_sigma_r160_B", sig16, 6, note="High-class buy probability in the partial-buy tuple at 1.60 (challenger mixes at indifference).")
    reg("mix_e1_r160_B", e16, 6, note="Entry after a buy in the partial-buy tuple at 1.60: k/(Delta_T(1-tau)).")
    low16_exact = PA.rho * auction(PA, Fr(8, 5))["D"] / 2 - PA.k
    print(f"  low-class sale payoff, exact rational: {low16_exact}")
    reg("mix_lowsale_r160_B", low16_exact, 6, status="analytical",
        note="Low-class sale payoff in the partial-buy tuple at 1.60: rho Delta_T(8/5)/2 - k = -19/3200 (negative).")
    reg("mix_mean_order_r160_B", EX16, 6, note="Mean order in the partial-buy tuple at 1.60.")
    reg("mix_entry_r160_B", ent16, 6, note="Entry in the partial-buy tuple at 1.60.")

    # 12f ---------------------------------------------------------------
    print("\n  12f. Announcement samples: all announcements against preparation announcements only")
    for tag, o in (("r1", o1), ("r2", o2)):
        wts = {x: o["pr"][x] * o["e"][x] / o["entry"] for x in (-1, 0, 1)}
        mean_d = sum((wts[x] * o["evA"][x] for x in wts), P.zero)
        mean_r = sum((wts[x] * o["evA"][x] / o["price"][x] for x in wts), P.zero)
        both = sum((o["pr"][x] * (o["e"][x] * o["evA"][x] + (P.one - o["e"][x]) * o["evN"][x]) for x in wts), P.zero)
        print(f"  {tag}: mean change over all announcements (model probabilities) {fmt_dec(both, 12)}; "
              f"mean change given preparation {fmt_dec(mean_d, 9)}; mean return given preparation {fmt_dec(mean_r, 9)}")
        reg(f"evprep_mean_{tag}_B", mean_d, 6, note=f"Mean price change (dollars) in the sample of preparation announcements at {tag}.")
        reg(f"evprep_meanr_{tag}_B", mean_r, 6, note=f"Mean ratio return in the sample of preparation announcements at {tag}.")

    # ------------------------------------------------------------------ files
    header("FLAGS")
    print("  " + ("none" if not FLAGS else "; ".join(FLAGS)))

    cols = ["key", "value", "display", "status", "source_script", "run_log", "note"]
    outcsv = REGISTRY
    with outcsv.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols)
        wr.writeheader()
        for r in ROWS:
            wr.writerow(r)
    (HERE / "EX_exact_enclosures.json").write_text(json.dumps(ENCLOSURES, indent=2) + "\n")
    tex = ["% p5_numbers.tex: generated by p5_observables.py from the P5 registry rows.",
           "% Prints with \\reg{<key>}.  Do not edit by hand.",
           "\\makeatletter",
           "\\providecommand{\\reg}[1]{\\ifcsname reg@#1\\endcsname\\csname reg@#1\\endcsname"
           "\\else\\textbf{??\\detokenize{#1}}\\fi}"]
    for r in ROWS:
        tex.append(f"\\expandafter\\def\\csname reg@{r['key']}\\endcsname{{{r['display']}}}")
    tex.append("\\makeatother")
    (HERE / "p5_numbers.tex").write_text("\n".join(tex) + "\n")
    print(f"\nregistry rows written: {len(ROWS)} -> {outcsv.relative_to(TEAM)}")
    print(f"script SHA-256: {hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry-output", type=pathlib.Path, default=REGISTRY,
                        help="Write a candidate registry to this path before publication.")
    REGISTRY = parser.parse_args().registry_output.resolve()
    main()
