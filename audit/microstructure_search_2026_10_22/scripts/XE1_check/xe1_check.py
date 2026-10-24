#!/usr/bin/env python
"""XE1: independent recomputation of the auction-side claims under the order slot.

Calibration A and every auction object use exact rational arithmetic.
Calibration B uses outward interval arithmetic at 40 decimal digits.
Auction objects come from quadrature of the sale payoffs, not from closed forms:
  - over the incumbent value R ~ U[0, r]: the midpoint rule on each linear piece (exact);
  - over a uniform class band: Milne's open rule on each polynomial piece (exact for cubics).
The program prints results. It contains no assertions.

Usage: python xe1_check.py > results.txt
"""
from fractions import Fraction as Fr
import platform
import sys

import mpmath
from mpmath import iv, mp

iv.dps = 40
mp.dps = 40


# ---------------------------------------------------------------- number kits
class ExactKit:
    name = "A"

    def c(self, x):
        return Fr(x)

    def sgn(self, x):
        return (x > 0) - (x < 0)

    def s(self, x):
        x = Fr(x)
        dec = mpmath.nstr(mp.mpf(x.numerator) / x.denominator, 13)
        if x.denominator <= 10**9 and abs(x.numerator) <= 10**13:
            return f"{x} ({dec})"
        return dec


class IntervalKit:
    name = "B"

    def c(self, x):
        if isinstance(x, Fr):
            return iv.mpf(x.numerator) / iv.mpf(x.denominator)
        if isinstance(x, int):
            return iv.mpf(x)
        return x

    def sgn(self, x):
        x = self.c(x)
        if x.a > 0:
            return 1
        if x.b < 0:
            return -1
        return 0

    def s(self, x):
        x = self.c(x)
        return f"{mpmath.nstr(mp.mpf(x.mid.a), 13)} [w {mpmath.nstr(mp.mpf(x.delta.a), 1)}]"


EX = ExactKit()
IV = IntervalKit()
SIGN = {1: "+", -1: "-", 0: "0/unresolved"}


def say(*a):
    print(*a)


def head(t):
    print()
    print("=" * 100)
    print(t)
    print("=" * 100)


# ------------------------------------------------------------ auction quadrature
def r_expect(fn, r, cuts):
    """E[fn(R)] for R ~ U[0, r]; fn is linear between cut points. Midpoint rule (exact)."""
    pts = sorted(set([Fr(0), Fr(r)] + [Fr(c) for c in cuts if 0 < c < r]))
    acc = None
    for x0, x1 in zip(pts, pts[1:]):
        val = fn((x0 + x1) / 2)
        term = tuple((x1 - x0) * v for v in val)
        acc = term if acc is None else tuple(a + b for a, b in zip(acc, term))
    return tuple(a / r for a in acc)


def value_objects(v, r, p):
    """Expected (payment, challenger profit, challenger wins, allocation value) over R, prepared challenger value v."""
    v, r, p = Fr(v), Fr(r), Fr(p)

    def f(R):
        if v >= p:
            pay = max(p, min(R, v))
            prof = max(v - max(p, R), Fr(0))
            win = Fr(1) if R < v else Fr(0)
            alloc = max(R if R >= p else Fr(0), v)
        else:
            pay = p if R >= p else Fr(0)
            prof, win = Fr(0), Fr(0)
            alloc = R if R >= p else Fr(0)
        return (pay, prof, win, alloc)

    return r_expect(f, r, [p, v])


def no_challenger(r, p):
    r, p = Fr(r), Fr(p)

    def f(R):
        return (p if R >= p else Fr(0), R if R >= p else Fr(0))

    t0, s0 = r_expect(f, r, [p])
    return t0, s0


def milne(fn, a, c):
    """Integral of a vector polynomial (degree <= 3) on [a, c] by Milne's open rule."""
    h = (c - a) / 4
    f1, f2, f3 = fn(a + h), fn(a + 2 * h), fn(a + 3 * h)
    return tuple((c - a) / 3 * (2 * x - y + 2 * z) for x, y, z in zip(f1, f2, f3))


def class_objects(law, r, p):
    """law: list of ('atom', v, w) or ('unif', a, c, w). Returns dict of t, g, W, S (allocation), A (admissible)."""
    r, p = Fr(r), Fr(p)
    tot = [Fr(0)] * 5
    for piece in law:
        if piece[0] == "atom":
            _, v, w = piece
            vals = value_objects(v, r, p) + ((Fr(1) if Fr(v) >= p else Fr(0)),)
            tot = [x + Fr(w) * y for x, y in zip(tot, vals)]
        else:
            _, a, c, w = piece
            a, c, w = Fr(a), Fr(c), Fr(w)
            dens = w / (c - a)
            cuts = sorted(set([a, c] + [x for x in (p, r) if a < x < c]))
            for x0, x1 in zip(cuts, cuts[1:]):
                vals = milne(lambda v: value_objects(v, r, p) + ((Fr(1) if v >= p else Fr(0)),), x0, x1)
                tot = [x + dens * y for x, y in zip(tot, vals)]
    t, g, W, S, A = tot
    return {"t": t, "g": g, "W": W, "S": S, "A": A}


def economy(lawH, lawL, r, p):
    t0, s0 = no_challenger(r, p)
    H = class_objects(lawH, r, p)
    L = class_objects(lawL, r, p)
    r, p = Fr(r), Fr(p)
    return {
        "r": r, "p": p, "t0": t0, "S0": s0,
        "tH": H["t"], "tL": L["t"], "gH": H["g"], "gL": L["g"],
        "WH": H["W"], "WL": L["W"], "SH": H["S"], "SL": L["S"], "AH": H["A"], "AL": L["A"],
        "D": H["t"] - L["t"], "FR": min(p, r) / r,  # FR = Pr(R < p)
    }


def atom(v):
    return [("atom", Fr(v), Fr(1))]


def unif(a, c):
    return [("unif", Fr(a), Fr(c), Fr(1))]


# ------------------------------------------------------------------ calibrations
def calibration_A():
    lam, beta = Fr(6, 17), Fr(1, 3)
    return {"kit": EX, "lam": lam, "beta": beta}


def calibration_B():
    """Calibration B from the paper's equation (12) at the benchmark, Laplace scale 2."""
    X = IV
    bench = economy(atom(10), atom(1), Fr(3), Fr(1, 2))
    cH, rho, bL = Fr(6), Fr(1, 4), 2
    tau = (cH - bench["gL"]) / (bench["gH"] - bench["gL"])
    tauI = X.c(tau)
    xstar = iv.mpf(bL) / 2 * iv.log(tauI / (1 - tauI))  # prior 1/2: log-odds term is zero
    aH = 1 - iv.mpf(1) / 2 * iv.exp((xstar - 1) / bL)
    aL = iv.mpf(1) / 2 * iv.exp(-(xstar + 1) / bL)
    Estar = X.c(rho) + (1 - X.c(rho)) * (aH + aL) / 2
    u = iv.exp(iv.mpf(2) / bL) - 1
    d = (Estar - X.c(rho)) / (1 - X.c(rho))
    bs = d / (1 + u / 2)
    lam = u * bs
    beta = bs / (1 - lam)
    return {"kit": X, "lam": lam, "beta": beta, "tau": tau, "Estar": Estar, "u": u}


def slot(cal):
    X = cal["kit"]
    lam, beta = X.c(cal["lam"]), X.c(cal["beta"])
    b = (1 - lam) * beta
    b0 = (1 - lam) * (1 - 2 * beta)
    return lam, beta, b, b0


def bounds(cal, pi):
    X = cal["kit"]
    lam, beta, b, b0 = slot(cal)
    pi = X.c(pi)
    u = lam / b
    m = pi / (pi + (1 - pi) * (1 + u))
    M = pi * (1 + u) / (pi * (1 + u) + 1 - pi)
    return m, M


def kmin(X, a, b):
    """min of two numbers in the kit; for intervals return the elementwise lower envelope."""
    if X is EX:
        return min(a, b)
    return iv.mpf([min(a.a, b.a), min(a.b, b.b)])


# ----------------------------------------------------- two-class slot equilibrium
FLOWS = (-1, 0, 1)


def node(E, cal, pi, rho, cH, k, orders, hidden=False):
    """Two-class node with pure informed orders (qH, qL). Returns flow objects and best-response table."""
    X = cal["kit"]
    lam, beta, b, b0 = slot(cal)
    pi, rho, cH, k = X.c(pi), X.c(rho), X.c(cH), X.c(k)
    t0, tH, tL, gH, gL = (X.c(E[x]) for x in ("t0", "tH", "tL", "gH", "gL"))
    D = tH - tL
    eta = {-1: beta, 0: 1 - 2 * beta, 1: beta}
    qH, qL = orders
    aH = {Q: (1 - lam) * eta[Q] + (lam if qH == Q else 0) for Q in FLOWS}
    aL = {Q: (1 - lam) * eta[Q] + (lam if qL == Q else 0) for Q in FLOWS}
    out = {"aH": aH, "aL": aL, "unresolved": []}
    mu, e, P, zeta = {}, {}, {}, {}
    for Q in FLOWS:
        mu[Q] = pi * aH[Q] / (pi * aH[Q] + (1 - pi) * aL[Q])
        bel = pi if hidden else mu[Q]
        s = X.sgn(gL + bel * (gH - gL) - cH)
        if s == 0 and X is IV:
            out["unresolved"].append(("entry", Q))
        zeta[Q] = 1 if s >= 0 else 0  # C1: prepare at indifference
        e[Q] = rho + (1 - rho) * zeta[Q]
        P[Q] = t0 + e[Q] * (tL - t0 + D * mu[Q])
    pay = {}
    for cls, tj in (("H", tH), ("L", tL)):
        for q in FLOWS:
            pay[(cls, q)] = 0 if q == 0 else q * (t0 + e[q] * (tj - t0) - P[q]) - k * abs(q)
    out.update(mu=mu, e=e, P=P, zeta=zeta, pay=pay)
    # equilibrium test: prescribed order is a best response for each class
    eq, strict = True, True
    for cls, q in (("H", qH), ("L", qL)):
        for qq in FLOWS:
            if qq == q:
                continue
            s = X.sgn(X.c(pay[(cls, q)]) - X.c(pay[(cls, qq)]))
            if s < 0:
                eq = False
            if s == 0:
                strict = False
                if X is IV:
                    out["unresolved"].append(("br", cls, q, qq))
    out["eq"], out["strict"] = eq, strict
    eH = sum((aH[Q] * e[Q] for Q in FLOWS), X.c(0))
    eL = sum((aL[Q] * e[Q] for Q in FLOWS), X.c(0))
    out["eH"], out["eL"] = eH, eL
    out["E"] = pi * eH + (1 - pi) * eL
    return out


def outcomes(E, cal, pi, rho, cH, nd):
    """Outcome measures for a node: entry, admissible, sale, two bidders, proceeds, ownership, net surplus."""
    X = cal["kit"]
    pi, rho, cH = X.c(pi), X.c(rho), X.c(cH)
    eH, eL = nd["eH"], nd["eL"]
    t0, tH, tL = X.c(E["t0"]), X.c(E["tH"]), X.c(E["tL"])
    A = pi * eH * X.c(E["AH"]) + (1 - pi) * eL * X.c(E["AL"])
    pRp = 1 - X.c(E["FR"])
    C2 = pRp * A
    S = pRp + A - C2
    RT = t0 + pi * eH * (tH - t0) + (1 - pi) * eL * (tL - t0)
    OH = pi * eH * X.c(E["WH"])
    # high-cost preparation probability, for net surplus
    lam, beta, b, b0 = slot(cal)
    prQ = {Q: pi * nd["aH"][Q] + (1 - pi) * nd["aL"][Q] for Q in FLOWS}
    zcost = sum((prQ[Q] * nd["zeta"][Q] for Q in FLOWS), X.c(0)) * (1 - rho) * cH
    S0, SH, SL = X.c(E["S0"]), X.c(E["SH"]), X.c(E["SL"])
    W = S0 + pi * eH * (SH - S0) + (1 - pi) * eL * (SL - S0) - zcost
    return {"E": nd["E"], "A": A, "S": S, "C2": C2, "RT": RT, "OH": OH, "W": W, "eH": eH, "eL": eL}


def enumerate_pure(E, cal, pi, rho, cH, k, hidden=False):
    found = []
    for qH in FLOWS:
        for qL in FLOWS:
            nd = node(E, cal, pi, rho, cH, k, (qH, qL), hidden)
            if nd["eq"]:
                found.append(((qH, qL), nd))
    return found


def prop2_margins(E0, E1, E2, cal, pi, rho, cH, k):
    """Margins of the corrected hypotheses (3) and of the coordinator's listed conditions."""
    X = cal["kit"]
    m, M = bounds(cal, pi)
    kap = kmin(X, m, 1 - M)
    pi_, rho_, cH_, k_ = X.c(pi), X.c(rho), X.c(cH), X.c(k)

    def B(E, mu):
        return X.c(E["gL"]) + mu * (X.c(E["gH"]) - X.c(E["gL"]))

    out = {
        "cH-B0(pi)": cH_ - B(E0, pi_),
        "B1(M)-cH": B(E1, M) - cH_,
        "k-D0": k_ - X.c(E0["D"]),
        "rho*kap*D1-k": rho_ * kap * X.c(E1["D"]) - k_,
    }
    if E2 is not None:
        out["cH-B2(M)"] = cH_ - B(E2, M)
        out["rho*kap*D2-k"] = rho_ * kap * X.c(E2["D"]) - k_
        out["cH-B1(pi) [coord]"] = cH_ - B(E1, pi_)
        out["cH-B2(pi) [coord]"] = cH_ - B(E2, pi_)
    return out, m, M, kap


def show_margins(X, d, indent="    "):
    for key, v in d.items():
        say(f"{indent}{key:24s} {X.s(v):48s} sign {SIGN[X.sgn(v)]}")


# ===================================================================== sections
def sec0_objects():
    head("0. Auction objects by quadrature versus the paper's closed forms (point masses 10 and 1, p = 1/2)")
    h, l, p = Fr(10), Fr(1), Fr(1, 2)
    for r in (Fr(6, 5), Fr(3), Fr(18, 5), Fr(8), Fr(21, 20), Fr(3, 2)):
        hh = Fr(2) if r in (Fr(21, 20), Fr(3, 2)) else h
        E = economy(atom(hh), atom(l), r, p)
        cf = {
            "t0": p * (1 - p / r), "tH": r / 2 + p * p / (2 * r), "tL": l - (l * l - p * p) / (2 * r),
            "gH": hh - r / 2 - p * p / (2 * r), "gL": (l * l - p * p) / (2 * r), "D": (r - l) ** 2 / (2 * r),
        }
        diffs = {x: E[x] - cf[x] for x in cf}
        say(f"  h={hh} r={r}: t0={E['t0']} tH={E['tH']} tL={E['tL']} gH={E['gH']} gL={E['gL']} D={E['D']}"
            f" | quadrature minus closed form: {set(diffs.values())}")
    # identity t + g = value for one class value inside and outside the incumbent support
    for v in (Fr(1), Fr(10), Fr(2)):
        t, g, w, s = value_objects(v, Fr(3), p)
        say(f"  identity check v={v}, r=3: t+g = {t + g}")


def sec1_prop2(A, B):
    head("1. General-prior Proposition 2: coordinator's listed conditions, the counterexample, corrected (3)")
    lawH, lawL = atom(10), atom(1)
    p, rho, k, pi = Fr(1, 2), Fr(1, 4), Fr(1, 50), Fr(1, 2)
    cH = Fr(47, 10)
    E0, E1, E2 = (economy(lawH, lawL, r, p) for r in (Fr(6, 5), Fr(3), Fr(8)))
    for cal in (A, B):
        X = cal["kit"]
        say(f"\n  Calibration {X.name}: counterexample c_H = 47/10, strengths (6/5, 3, 8)")
        mar, m, M, kap = prop2_margins(E0, E1, E2, cal, pi, rho, cH, k)
        say(f"    m = {X.s(m)}, M = {X.s(M)}, kappa = {X.s(kap)}")
        show_margins(X, mar)
        for lab, E in (("F0 (6/5)", E0), ("F1 (3)", E1), ("F2 (8)", E2)):
            eqs = enumerate_pure(E, cal, pi, rho, cH, k)
            for (o, nd) in eqs:
                say(f"    {lab}: pure equilibrium orders {o}, strict={nd['strict']}, entry E = {X.s(nd['E'])},"
                    f" e(Q) = {[X.s(nd['e'][Q]) for Q in FLOWS]} unresolved={nd['unresolved']}")
            if not eqs:
                say(f"    {lab}: no pure equilibrium")

    say("\n  Benchmark (c_H = 6, strengths 6/5, 3, 18/5) under the corrected (3):")
    E2b = economy(lawH, lawL, Fr(18, 5), p)
    for cal in (A, B):
        X = cal["kit"]
        mar, m, M, kap = prop2_margins(E0, E1, E2b, cal, pi, rho, Fr(6), k)
        say(f"   Calibration {X.name}")
        show_margins(X, mar)
        for lab, E in (("1.2", E0), ("3", E1), ("3.6", E2b)):
            eqs = enumerate_pure(E, cal, pi, rho, Fr(6), k)
            for (o, nd) in eqs:
                oc = outcomes(E, cal, pi, rho, Fr(6), nd)
                say(f"    r={lab}: orders {o} strict={nd['strict']} E={X.s(oc['E'])} O_H={X.s(oc['OH'])}")

    say("\n  Prior windows at the benchmark (all other inputs fixed): solve M(pi) = tau_1 and M(pi) = tau_2")
    for cal in (A, B):
        X = cal["kit"]
        lam, beta, b, b0 = slot(cal)
        u = lam / b
        out = []
        for E in (E1, E2b):
            tau = X.c((Fr(6) - E["gL"]) / (E["gH"] - E["gL"]))
            out.append(tau / (tau + (1 + u) * (1 - tau)))
        lo, hi = out
        say(f"   {X.name}: window ({X.s(lo)}, {X.s(hi)})")
        for edge in (lo, hi):
            mar, m, M, kap = prop2_margins(E0, E1, E2b, cal, edge, rho, Fr(6), k)
            say(f"     margins at pi = {X.s(edge)}:")
            show_margins(X, mar, indent="       ")

    say("\n  All-strategy posterior bound at the zero flow (sup over pure strategies) versus M; prior 1/2")
    for lab, lam, beta in (("A", Fr(6, 17), Fr(1, 3)), ("beta=2/5", Fr(6, 17), Fr(2, 5)), ("beta=1/4", Fr(6, 17), Fr(1, 4))):
        b = (1 - lam) * beta
        b0 = (1 - lam) * (1 - 2 * beta)
        u = lam / b
        M = (1 + u) / (2 + u)
        best = Fr(0)
        for sH in FLOWS:
            for sL in FLOWS:
                aH0 = b0 + (lam if sH == 0 else 0)
                aL0 = b0 + (lam if sL == 0 else 0)
                best = max(best, aH0 / (aH0 + aL0))
        say(f"   {lab}: lambda={lam} beta={beta}: M = {EX.s(M)}; max zero-flow posterior = {EX.s(best)}")
    say("   B: beta =", IV.s(B["beta"]), "(below 1/3 when the sign is negative:", SIGN[IV.sgn(B["beta"] - IV.c(Fr(1, 3)))], ")")

    say("\n  Ownership: paper's sufficient condition versus the slot condition (6) when b + lambda < 1/2")
    say("   Own example: point masses 10 and 1, p=1/2, rho=1/4, pi=1/10, lambda=2/25, beta=1/125,")
    say("   strengths (21/20, 40/3, 40), c_H = 17/10, k = 1/200.")
    calx = {"kit": EX, "lam": Fr(2, 25), "beta": Fr(1, 125)}
    lam, beta, b, b0 = slot(calx)
    say(f"   b + lambda = {EX.s(b + lam)}")
    Ex0, Ex1, Ex2 = (economy(lawH, lawL, r, p) for r in (Fr(21, 20), Fr(40, 3), Fr(40)))
    mar, m, M, kap = prop2_margins(Ex0, Ex1, Ex2, calx, Fr(1, 10), rho, Fr(17, 10), Fr(1, 200))
    show_margins(EX, mar)
    for lab, E in (("21/20", Ex0), ("40/3", Ex1), ("40", Ex2)):
        for (o, nd) in enumerate_pure(E, calx, Fr(1, 10), rho, Fr(17, 10), Fr(1, 200)):
            oc = outcomes(E, calx, Fr(1, 10), rho, Fr(17, 10), nd)
            say(f"    r={lab}: orders {o} strict={nd['strict']} E={EX.s(oc['E'])} W_H={EX.s(E['WH'])} O_H={EX.s(oc['OH'])}")
    eH = rho + (1 - rho) * (b + lam)
    sW = (1 + rho) * Ex1["WH"] - 2 * rho * Ex0["WH"]
    six = eH * Ex1["WH"] - rho * Ex0["WH"]
    say(f"   paper sufficient margin (1+rho)W_H(F1) - 2 rho W_H(F0) = {EX.s(sW)}")
    say(f"   slot condition (6) margin e_H W_H(F1) - rho W_H(F0)      = {EX.s(six)}")


def two_class_case(name, lawH, lawL, p, rho, pi, cH, k, rs, cals, extra_W=False):
    say(f"\n  {name}: pi={pi}, c_H={cH}, k={k}, strengths {tuple(str(r) for r in rs)}")
    Es = [economy(lawH, lawL, r, p) for r in rs]
    for E in Es:
        say(f"    r={E['r']}: t0={EX.s(E['t0'])} tH={EX.s(E['tH'])} tL={EX.s(E['tL'])}"
            f" gH={EX.s(E['gH'])} gL={EX.s(E['gL'])} D={EX.s(E['D'])} W_H={EX.s(E['WH'])}")
    res = {}
    for cal in cals:
        X = cal["kit"]
        E2 = Es[2] if len(Es) > 2 else None
        mar, m, M, kap = prop2_margins(Es[0], Es[1], E2, cal, pi, rho, cH, k)
        say(f"   Calibration {X.name}: m={X.s(m)} M={X.s(M)} kappa={X.s(kap)}")
        show_margins(X, mar)
        lam, beta, b, b0 = slot(cal)
        eH = X.c(rho) + (1 - X.c(rho)) * (b + lam)
        six = eH * X.c(Es[1]["WH"]) - X.c(rho) * X.c(Es[0]["WH"])
        sW = (1 + X.c(rho)) * X.c(Es[1]["WH"]) - 2 * X.c(rho) * X.c(Es[0]["WH"])
        say(f"    ownership (6) margin {X.s(six)}; paper sufficient margin s_W {X.s(sW)}")
        for E in Es:
            eqs = enumerate_pure(E, cal, pi, rho, cH, k)
            for (o, nd) in eqs:
                oc = outcomes(E, cal, pi, rho, cH, nd)
                say(f"    r={E['r']}: pure eq orders {o} strict={nd['strict']} E={X.s(oc['E'])}"
                    f" O_H={X.s(oc['OH'])} unresolved={nd['unresolved']}")
                res[(X.name, str(E["r"]))] = oc
    return Es, res


def sec2_classes(A, B):
    head("2. X2: two-class examples with the paper's costs and strengths")
    p, rho = Fr(1, 2), Fr(1, 4)
    two_class_case("Moderate values (h=2)", atom(2), atom(1), p, rho, Fr(1, 2), Fr(89, 100), Fr(1, 500),
                   (Fr(21, 20), Fr(3, 2)), (A, B))
    two_class_case("Point-mass benchmark", atom(10), atom(1), p, rho, Fr(1, 2), Fr(6), Fr(1, 50),
                   (Fr(6, 5), Fr(3), Fr(18, 5)), (A, B))
    two_class_case("Narrow bands (half-width 1/20)", unif(Fr(199, 20), Fr(201, 20)), unif(Fr(19, 20), Fr(21, 20)),
                   p, rho, Fr(1, 2), Fr(6), Fr(1, 50), (Fr(6, 5), Fr(3), Fr(18, 5)), (A, B))
    # band spread closed form check
    for r in (Fr(6, 5), Fr(3), Fr(18, 5)):
        E = economy(unif(Fr(199, 20), Fr(201, 20)), unif(Fr(19, 20), Fr(21, 20)), r, p)
        say(f"    band spread at r={r}: quadrature {E['D']} vs ((r-1)^2+eps^2/3)/(2r) = {((r - 1) ** 2 + Fr(1, 1200)) / (2 * r)}")
    two_class_case("Exhibit case A", atom(10), atom(1), p, rho, Fr(3, 10), Fr(9, 2), Fr(1, 100),
                   (Fr(11, 10), Fr(3), Fr(18, 5)), (A, B))
    two_class_case("Exhibit case B", atom(10), atom(1), p, rho, Fr(7, 10), Fr(36, 5), Fr(1, 100),
                   (Fr(11, 10), Fr(3), Fr(18, 5)), (A, B))
    two_class_case("Exhibit case C", unif(1, 19), unif(Fr(3, 5), Fr(7, 5)), p, rho, Fr(7, 10), Fr(67, 10), Fr(1, 50),
                   (Fr(1), Fr(9, 2), Fr(11, 2)), (A, B))
    two_class_case("Exhibit case D", atom(10), atom(1), p, rho, Fr(7, 10), Fr(67, 10), Fr(1, 50),
                   (Fr(1), Fr(9, 2), Fr(11, 2)), (A, B))

    say("\n  Constructive sequence of Online Appendix C.4 (prior 1/2): first feasible n in 1..20")
    say("  recipe 'paper': k = [D(r0) + (1/2) rho m D(r1)]/2 ; recipe 'slot': k = [D(r0) + rho m D(r1)]/2;")
    say("  c_H = [B_r0(1/2) + B_r1(M)]/2. Feasible: D(r0) < k < rho*kappa*D(r1) and B_r0(1/2) < c_H < B_r1(M).")
    for ratio in (Fr(105, 100), Fr(110, 100), Fr(125, 100), Fr(150, 100), Fr(2)):
        G = ratio - 1
        rows = {}
        for n in range(1, 21):
            dn = G / 2**n
            r1, r0 = 1 + dn, 1 + dn * dn / G
            E0 = economy(atom(ratio), atom(1), r0, p)
            E1 = economy(atom(ratio), atom(1), r1, p)
            for cal in (A, B):
                X = cal["kit"]
                m, M = bounds(cal, Fr(1, 2))
                for rec, fac in (("paper", Fr(1, 2)), ("slot", Fr(1))):
                    key = (X.name, rec)
                    if key in rows:
                        continue
                    D0, D1 = X.c(E0["D"]), X.c(E1["D"])
                    kk = (D0 + X.c(fac) * X.c(rho) * m * D1) / 2
                    B0 = X.c(E0["gL"]) + X.c(Fr(1, 2)) * (X.c(E0["gH"]) - X.c(E0["gL"]))
                    B1M = X.c(E1["gL"]) + M * (X.c(E1["gH"]) - X.c(E1["gL"]))
                    cc = (B0 + B1M) / 2
                    sig = [X.sgn(kk - D0), X.sgn(X.c(rho) * m * D1 - kk), X.sgn(cc - B0), X.sgn(B1M - cc), X.sgn(cc)]
                    if all(s > 0 for s in sig):
                        rows[key] = (n, kk, cc)
        say(f"   h/l={float(ratio)}: " + "; ".join(f"{a}/{rec}: n={rows[(a, rec)][0]} k={(EX if a == 'A' else IV).s(rows[(a, rec)][1])}"
                                                    f" c_H={(EX if a == 'A' else IV).s(rows[(a, rec)][2])}"
                                                    for (a, rec) in sorted(rows)))
        # the B-valued (Laplace-recipe) costs at n = 3, tested against calibration A's windows
        dn = G / 8
        r1, r0 = 1 + dn, 1 + dn * dn / G
        E0 = economy(atom(ratio), atom(1), r0, p)
        E1 = economy(atom(ratio), atom(1), r1, p)
        kB, cB = rows[("B", "paper")][1], rows[("B", "paper")][2]
        mA, MA = bounds(A, Fr(1, 2))
        sig = [IV.sgn(kB - IV.c(E0["D"])), IV.sgn(IV.c(rho * mA * E1["D"]) - kB),
               IV.sgn(cB - IV.c(E0["gL"] + (E0["gH"] - E0["gL"]) / 2)),
               IV.sgn(IV.c(E1["gL"] + MA * (E1["gH"] - E1["gL"])) - cB)]
        say(f"     n=3: B-valued costs inside calibration A's windows: signs {sig}")
        # margins at n = 1 and 2 under B, paper recipe, to show the failing members
        for n in (1, 2):
            dn = G / 2**n
            r1, r0 = 1 + dn, 1 + dn * dn / G
            E0 = economy(atom(ratio), atom(1), r0, p)
            E1 = economy(atom(ratio), atom(1), r1, p)
            m, M = bounds(B, Fr(1, 2))
            win = IV.c(Fr(1, 2)) * IV.c(rho) * m * IV.c(E1["D"]) - IV.c(E0["D"])
            say(f"     n={n}: B paper-recipe trade window width {IV.s(win)}")


def multi_node(classes, orders, cal, rho, cH, k, t0):
    """classes: list of (prior, t, g). Pure orders. Price cells by equal price (fixed point)."""
    X = cal["kit"]
    lam, beta, b, b0 = slot(cal)
    rho, cH, k, t0 = X.c(rho), X.c(cH), X.c(k), X.c(t0)
    eta = {-1: beta, 0: 1 - 2 * beta, 1: beta}
    joint = {Q: [X.c(pj) * ((1 - lam) * eta[Q] + (lam if q == Q else 0)) for (pj, tj, gj), q in zip(classes, orders)]
             for Q in FLOWS}
    prQ = {Q: sum(joint[Q], X.c(0)) for Q in FLOWS}
    post = {Q: [x / prQ[Q] for x in joint[Q]] for Q in FLOWS}
    tbar = {Q: sum((w * X.c(tj) for w, (pj, tj, gj) in zip(post[Q], classes)), X.c(0)) for Q in FLOWS}
    Bbar = {Q: sum((w * X.c(gj) for w, (pj, tj, gj) in zip(post[Q], classes)), X.c(0)) for Q in FLOWS}
    cells = [[Q] for Q in FLOWS]
    for _ in range(5):
        e = {}
        for cell in cells:
            pr = sum((prQ[Q] for Q in cell), X.c(0))
            Bc = sum((prQ[Q] * Bbar[Q] for Q in cell), X.c(0)) / pr
            z = 1 if X.sgn(Bc - cH) >= 0 else 0
            for Q in cell:
                e[Q] = rho + (1 - rho) * z
        P = {Q: t0 + e[Q] * (tbar[Q] - t0) for Q in FLOWS}
        new = []
        for Q in FLOWS:
            for cell in new:
                if X.sgn(P[cell[0]] - P[Q]) == 0:
                    cell.append(Q)
                    break
            else:
                new.append([Q])
        if new == cells:
            break
        cells = new
    pay = []
    for (pj, tj, gj) in classes:
        pay.append({q: (X.c(0) if q == 0 else q * e[q] * (X.c(tj) - tbar[q]) - k * abs(q)) for q in FLOWS})
    return {"post": post, "tbar": tbar, "Bbar": Bbar, "P": P, "e": e, "cells": cells, "pay": pay, "prQ": prQ}


def sec3_many(A, B):
    head("3. X2 with three classes: E1's pooled-price equilibrium, perturbation, collinearity, likelihood ratios")
    r, p, rho, cH, k = Fr(8), Fr(1), Fr(1, 4), Fr(10), Fr(1, 8)
    t0, S0 = no_challenger(r, p)
    t1, g1, W1, _ = value_objects(Fr(1), r, p)
    t10, g10, W10, _ = value_objects(Fr(10), r, p)
    say(f"  R~U[0,8], p=1: t0={t0}; value 1: t={t1}, g={g1}; value 10: t={t10}, g={g10}")
    prior = [Fr(1, 4), Fr(1, 2), Fr(1, 4)]
    orders = (-1, 0, 1)

    def classes_for(w, X):
        w = X.c(w)
        return [(prior[0], X.c(t1), X.c(g1)),
                (prior[1], X.c(t1) + w * (X.c(t10) - X.c(t1)), w * X.c(g10)),
                (prior[2], X.c(t10), X.c(g10))]

    # my own derivation: equal posterior means at flows 0 and +1 gives w = (2b + 3 b0 + 2 lam) / (2 (2b + b0 + lam))
    for cal in (A, B):
        X = cal["kit"]
        lam, beta, b, b0 = slot(cal)
        w = (2 * b + 3 * b0 + 2 * lam) / (2 * (2 * b + b0 + lam))
        say(f"\n  Calibration {X.name}: mixture weight w = {X.s(w)}; 2b+b0+lam = {X.s(2 * b + b0 + lam)}")
        nd = multi_node(classes_for(w, X), orders, cal, rho, cH, k, t0)
        for Q in FLOWS:
            say(f"    flow {Q:+d}: posterior {[X.s(x) for x in nd['post'][Q]]}")
            say(f"             tbar={X.s(nd['tbar'][Q])} Bbar={X.s(nd['Bbar'][Q])} price={X.s(nd['P'][Q])} e={X.s(nd['e'][Q])}")
        say(f"    price cells: {nd['cells']}; tbar(0)-tbar(+1) = {X.s(nd['tbar'][0] - nd['tbar'][1])};"
            f" Bbar(0)-Bbar(+1) = {X.s(nd['Bbar'][0] - nd['Bbar'][1])}")
        for j, pay in enumerate(nd["pay"]):
            q = orders[j]
            others = [X.sgn(pay[q] - pay[qq]) for qq in FLOWS if qq != q]
            say(f"    class {j + 1}: sell {X.s(pay[-1])}, wait {X.s(pay[0])}, buy {X.s(pay[1])}; prescribed {q:+d};"
                f" strict best response signs {others}")
        say(f"    max class profit {X.s(X.c(g10))} < c_H = 10; zero-cost entry has B > 0 at every flow:"
            f" {[SIGN[X.sgn(nd['Bbar'][Q])] for Q in FLOWS]}")
    say("\n  Perturbation under A: mixture weight 91/102 +- 1/1000")
    for dw in (Fr(1, 1000), Fr(-1, 1000)):
        w = Fr(91, 102) + dw
        nd = multi_node(classes_for(w, EX), orders, A, rho, cH, k, t0)
        strict = all(EX.sgn(nd["pay"][j][orders[j]] - nd["pay"][j][qq]) > 0 for j in range(3) for qq in FLOWS if qq != orders[j])
        say(f"   w = {w}: prices {[EX.s(nd['P'][Q]) for Q in FLOWS]}; cells {nd['cells']}; orders (-1,0,1) strict: {strict}")
    say("\n  Slot likelihood ratio f(+1|q)/f(0|q) by informed order q (MLR in q fails if not nondecreasing):")
    for cal in (A, B):
        X = cal["kit"]
        lam, beta, b, b0 = slot(cal)
        f = lambda Q, q: (1 - lam) * {-1: beta, 0: 1 - 2 * beta, 1: beta}[Q] + (lam if q == Q else 0)
        say(f"   {X.name}: " + ", ".join(f"q={q:+d}: {X.s(f(1, q) / f(0, q))}" for q in FLOWS))


def sec4_access(A, B):
    head("4. X5: access to prices at the strong benchmark (r = 3), by direct summation")
    p, rho, k, pi = Fr(1, 2), Fr(1, 4), Fr(1, 50), Fr(1, 2)
    E = economy(atom(10), atom(1), Fr(3), p)
    say(f"  S0={E['S0']} SH={E['SH']} SL={E['SL']} pF(p)={p * E['FR']}")
    for cal, cHs in ((A, (Fr(6), Fr(49, 20))), (B, (Fr(6), Fr(12, 5)))):
        X = cal["kit"]
        for cH in cHs:
            m, M = bounds(cal, pi)
            Bm = X.c(E["gL"]) + m * (X.c(E["gH"]) - X.c(E["gL"]))
            Bpi = X.c(E["gL"]) + X.c(pi) * (X.c(E["gH"]) - X.c(E["gL"]))
            BM = X.c(E["gL"]) + M * (X.c(E["gH"]) - X.c(E["gL"]))
            say(f"\n  Calibration {X.name}, c_H = {cH}: B(m)-cH {X.s(Bm - X.c(cH))}, B(pi)-cH {X.s(Bpi - X.c(cH))},"
                f" B(M)-cH {X.s(BM - X.c(cH))}; B(m)+pF(p)-cH {X.s(Bm + X.c(p * E['FR']) - X.c(cH))}")
            res = {}
            for hidden in (False, True):
                eqs = enumerate_pure(E, cal, pi, rho, cH, k, hidden=hidden)
                for (o, nd) in eqs:
                    oc = outcomes(E, cal, pi, rho, cH, nd)
                    lab = "hidden" if hidden else "access"
                    say(f"    {lab}: orders {o} strict={nd['strict']} E={X.s(oc['E'])} proceeds={X.s(oc['RT'])}"
                        f" net surplus={X.s(oc['W'])}")
                    res[lab] = oc
            if "access" in res and "hidden" in res:
                say(f"    access minus hidden: proceeds {X.s(res['access']['RT'] - res['hidden']['RT'])},"
                    f" net surplus {X.s(res['access']['W'] - res['hidden']['W'])}")
            kap = kmin(X, m, 1 - M)
            say(f"    full-order bound rho*kappa*D - k = {X.s(X.c(rho) * kap * X.c(E['D']) - X.c(k))}")
            if cH == 6 and "access" in res:
                # Section 6.1 transfer: unconditional informed gross trading profit under access, and the
                # trade scale below which the proceeds gain exceeds the transfer
                nd = node(E, cal, pi, rho, cH, k, (1, -1))
                lam, beta, b, b0 = slot(cal)
                gross = lam * (X.c(pi) * (nd["pay"][("H", 1)] + X.c(k)) + (1 - X.c(pi)) * (nd["pay"][("L", -1)] + X.c(k)))
                dR = res["access"]["RT"] - res["hidden"]["RT"]
                say(f"    informed gross trading profit (unconditional) = {X.s(gross)}; break-even trade scale"
                    f" = proceeds gain / profit = {X.s(dR / gross)} (paper, Laplace: 0.140731 and 1.831923)")


def sec5_bargaining():
    head("5. X6: verifiable-value bargaining at zero reserve (acquisition stage only)")
    h, l = Fr(10), Fr(1)
    res = {}
    for r in (Fr(6, 5), Fr(3)):
        def f(R, v):
            return (min(R, v), max(R, v), max(v - R, Fr(0)))
        mh = r_expect(lambda R: f(R, h), r, [h])
        ml = r_expect(lambda R: f(R, l), r, [l])
        # T_eta = (1-eta) min + eta max ; spread = E T(R,h) - E T(R,l) = a + b eta
        a = mh[0] - ml[0]
        bb = (mh[1] - ml[1]) - (mh[0] - ml[0])
        res[r] = (a, bb)
        Erl = r_expect(lambda R: (max(R - l, Fr(0)),), r, [l])[0]
        say(f"  r={r}: Delta_eta = {a} + ({bb}) eta ; paper (13): eta(h-l)+(1-2eta)E(R-l)+ = {Erl} + ({(h - l) - 2 * Erl}) eta;"
            f" g_H,eta = ({mh[2]})(1-eta); g_L,eta = ({ml[2]})(1-eta)")
    a0, b0 = res[Fr(6, 5)]
    a1, b1 = res[Fr(3)]
    say(f"  Delta_eta(3) - Delta_eta(6/5) = {a1 - a0} + ({b1 - b0}) eta  (zero at eta = {-(a1 - a0) / (b1 - b0)})")


def reserve_node(lawH, lawL, r, p, cal, rho, cH, k, pi=Fr(1, 2)):
    E = economy(lawH, lawL, r, p)
    X = cal["kit"]
    m, M = bounds(cal, pi)
    kap = kmin(X, m, 1 - M)
    zero_ok = X.sgn(X.c(k) - X.c(E["D"])) > 0
    full_ok = X.sgn(X.c(rho) * kap * X.c(E["D"]) - X.c(k)) > 0
    eqs = enumerate_pure(E, cal, pi, rho, cH, k)
    return E, zero_ok, full_ok, eqs


def sec6_reserves(A, B):
    head("6. X7: reserve comparisons (prior 1/2, c_H = 6, k = 1/50)")
    rho, cH, k = Fr(1, 4), Fr(6), Fr(1, 50)
    point = (atom(10), atom(1))
    band = (unif(Fr(199, 20), Fr(201, 20)), unif(Fr(19, 20), Fr(21, 20)))
    table = {}
    for lab, laws, ps in (("point", point, (Fr(1, 2), Fr(101, 100), Fr(31, 20))),
                          ("band", band, (Fr(1, 2), Fr(11, 10), Fr(31, 20)))):
        for cal in (A, B):
            X = cal["kit"]
            for r in (Fr(6, 5), Fr(3)):
                for p in ps:
                    E, zok, fok, eqs = reserve_node(laws[0], laws[1], r, p, cal, rho, cH, k)
                    for (o, nd) in eqs:
                        oc = outcomes(E, cal, Fr(1, 2), rho, cH, nd)
                        table[(lab, X.name, r, p)] = oc
                        say(f"  {lab:5s} {X.name} r={str(r):4s} p={str(p):7s} bound(zero)={zok!s:5s} bound(full)={fok!s:5s}"
                            f" orders {o} E={X.s(oc['E'])} S={X.s(oc['S'])} C2={X.s(oc['C2'])} proceeds={X.s(oc['RT'])}"
                            f" D={EX.s(E['D'])} zeta={[nd['zeta'][Q] for Q in FLOWS]}")
    say("\n  Margins for the narrowest recruiting node: bands, p = 11/10, r = 3 (B_1(M) - c_H)")
    E = economy(band[0], band[1], Fr(3), Fr(11, 10))
    for cal in (A, B):
        X = cal["kit"]
        m, M = bounds(cal, Fr(1, 2))
        say(f"   {X.name}: {X.s(X.c(E['gL']) + M * (X.c(E['gH']) - X.c(E['gL'])) - X.c(cH))}")
    say("\n  Exact strong-economy recruiting event p_H = sqrt(2r(h - c_H/M) - r^2) at r = 3:")
    for cal in (A, B):
        X = cal["kit"]
        m, M = bounds(cal, Fr(1, 2))
        q = 6 * (10 - X.c(cH) / M) - 9
        say(f"   {X.name}: p_H^2 = {X.s(q)}; p_H = {IV.s(iv.sqrt(IV.c(q)))}")

    say("\n  Endpoint reserve p = h = 10, point masses, r = 3:")
    for cal in (A, B):
        X = cal["kit"]
        E, zok, fok, eqs = reserve_node(point[0], point[1], Fr(3), Fr(10), cal, rho, cH, k)
        for (o, nd) in eqs:
            oc = outcomes(E, cal, Fr(1, 2), rho, cH, nd)
            say(f"   {X.name}: gH={E['gH']} D={E['D']} bound(full)={fok} orders {o} E={X.s(oc['E'])} S={X.s(oc['S'])}"
                f" C2={X.s(oc['C2'])} proceeds={X.s(oc['RT'])}")
    say("\n  Strong-economy proceeds without high-cost entry, point masses, r = 3 (low class excluded):")
    for p in (Fr(1), Fr(116, 100), Fr(6, 5), Fr(31, 20), Fr(21, 13)):
        E = economy(point[0], point[1], Fr(3), p)
        Rn = E["t0"] + rho / 2 * (E["tH"] - E["t0"]) + rho / 2 * (E["tL"] - E["t0"])
        say(f"   p={p}: proceeds with entry 1/4 = {EX.s(Rn)}")

    say("\n  Reserve scan, point masses, p = 1 + j/200 (j = 1..200): strict deterrence (weak recruits at +1,")
    say("  strong recruits nowhere), full orders forced at both strengths, proceeds above the p = 1/2 level")
    say("  in both economies, and weak incumbent admissibility (p < 6/5).")
    for cal in (A, B):
        X = cal["kit"]
        base = {r: table[("point", X.name, r, Fr(1, 2))]["RT"] for r in (Fr(6, 5), Fr(3))}
        det, both, adm = [], [], []
        for j in range(1, 201):
            p = 1 + Fr(j, 200)
            ok_all = True
            zs = {}
            rts = {}
            for r in (Fr(6, 5), Fr(3)):
                E, zok, fok, eqs = reserve_node(point[0], point[1], r, p, cal, rho, cH, k)
                full = [nd for (o, nd) in eqs if o == (1, -1)]
                if not fok or len(eqs) != 1 or not full:
                    ok_all = False
                    break
                nd = full[0]
                zs[r] = tuple(nd["zeta"][Q] for Q in FLOWS)
                rts[r] = outcomes(E, cal, Fr(1, 2), rho, cH, nd)["RT"]
            if not ok_all:
                continue
            if zs[Fr(6, 5)] == (0, 0, 1) and zs[Fr(3)] == (0, 0, 0):
                det.append(p)
                if all(X.sgn(rts[r] - base[r]) > 0 for r in rts):
                    both.append(p)
                    if p < Fr(6, 5):
                        adm.append(p)
        rng = lambda L: f"[{float(min(L)):.3f}, {float(max(L)):.3f}] ({len(L)} grid points)" if L else "empty"
        say(f"   {X.name}: strict deterrence on grid {rng(det)}; plus higher proceeds in both {rng(both)};"
            f" plus weak incumbent admissible {rng(adm)}")
        det_adm = [p for p in det if p < Fr(6, 5)]
        say(f"      strict deterrence with weak incumbent admissible: {rng(det_adm)}")
        for p in det_adm[:1] + det_adm[-1:]:
            E = economy(point[0], point[1], Fr(3), p)
            nd = [nd for (o, nd) in enumerate_pure(E, cal, Fr(1, 2), rho, cH, k) if o == (1, -1)][0]
            say(f"      p={p}: strong proceeds {X.s(outcomes(E, cal, Fr(1, 2), rho, cH, nd)['RT'])} vs p=1/2 level {X.s(base[Fr(3)])}")


def sec7_reserve_calibrations():
    head("7. Diagnostic: can any slot calibration give the paper's X7 pattern at a reserve in (1, 6/5)?")
    say("  Point masses 10 and 1, prior 1/2, rho=1/4, c_H=6, k=1/50. Exact rationals on a grid.")
    say("  Grid: M in {0.706, ..., 0.731} (benchmark Prop. 2 band), b in {0.005, 0.010, ...} with beta <= 1/2,")
    say("  p in {1.005, ..., 1.195}. Pattern: full orders forced at r = 6/5 and 3; strong entry strictly below weak")
    say("  entry; proceeds at p above proceeds at p = 1/2 in both economies (weak incumbent admissible: p < 6/5).")
    rho, cH, k, pi = Fr(1, 4), Fr(6), Fr(1, 50), Fr(1, 2)
    econ = {}
    for r in (Fr(6, 5), Fr(3)):
        econ[(r, Fr(1, 2))] = economy(atom(10), atom(1), r, Fr(1, 2))
        for j in range(1, 40):
            p = 1 + Fr(j, 200)
            econ[(r, p)] = economy(atom(10), atom(1), r, p)
    hits, tested, counts = [], 0, {}
    for iM in range(706, 732):
        M = Fr(iM, 1000)
        u = (2 * M - 1) / (1 - M)
        m = 1 - M
        ib = 1
        while True:
            b = Fr(ib, 200)
            lam = u * b
            if lam >= 1 or b / (1 - lam) >= Fr(1, 2):
                break
            ib += 1
            pr = {1: b + pi * lam, 0: 1 - 2 * b - lam, -1: b + (1 - pi) * lam}
            aH = {1: b + lam, 0: 1 - 2 * b - lam, -1: b}
            aL = {1: b, 0: 1 - 2 * b - lam, -1: b + lam}
            post = {1: M, 0: pi, -1: m}

            def summary(E):
                if not rho * min(m, 1 - M) * E["D"] > k:
                    return None
                z = {Q: 1 if E["gL"] + post[Q] * (E["gH"] - E["gL"]) >= cH else 0 for Q in FLOWS}
                eH = sum(aH[Q] * (rho + (1 - rho) * z[Q]) for Q in FLOWS)
                eL = sum(aL[Q] * (rho + (1 - rho) * z[Q]) for Q in FLOWS)
                RT = E["t0"] + pi * eH * (E["tH"] - E["t0"]) + (1 - pi) * eL * (E["tL"] - E["t0"])
                return pi * eH + (1 - pi) * eL, RT

            # base: p = 1/2 (weak: zero orders, entry rho; strong: full orders)
            Ew = econ[(Fr(6, 5), Fr(1, 2))]
            Rw0 = Ew["t0"] + pi * rho * (Ew["tH"] - Ew["t0"]) + (1 - pi) * rho * (Ew["tL"] - Ew["t0"])
            s0 = summary(econ[(Fr(3), Fr(1, 2))])
            if s0 is None:
                continue
            for j in range(1, 40):
                p = 1 + Fr(j, 200)
                tested += 1
                sw, ss = summary(econ[(Fr(6, 5), p)]), summary(econ[(Fr(3), p)])
                if sw is None or ss is None:
                    continue
                c1, c2, c3 = ss[0] < sw[0], sw[1] > Rw0, ss[1] > s0[1]
                for key, val in (("deter", c1), ("weakR", c2), ("strongR", c3), ("deter+weakR", c1 and c2),
                                 ("deter+strongR", c1 and c3), ("weakR+strongR", c2 and c3)):
                    counts[key] = counts.get(key, 0) + (1 if val else 0)
                if c1 and c2 and c3:
                    hits.append((M, b, p))
    say(f"  tested (M, b, p) triples: {tested}; component counts {counts}; triples with the full pattern: {len(hits)}")
    for h in hits[:10]:
        say(f"    M={h[0]} b={h[1]} p={h[2]}")


def main():
    say("XE1 independent check. Python", platform.python_version(), "mpmath", mpmath.__version__, "iv.dps", iv.dps)
    A = calibration_A()
    B = calibration_B()
    lamA, betaA, bA, b0A = slot(A)
    say(f"Calibration A: lambda={A['lam']} beta={A['beta']} b={bA} u={lamA / bA}")
    say(f"Calibration B: tau(3)={B['tau']}; E_* = {IV.s(B['Estar'])}; u = {IV.s(B['u'])}")
    lamB, betaB, bB, b0B = slot(B)
    say(f"  lambda_B = {IV.s(lamB)}; beta_B = {IV.s(betaB)}; b_B = {IV.s(bB)}")
    for pi in (Fr(1, 10), Fr(3, 10), Fr(1, 2), Fr(7, 10)):
        m, M = bounds(B, pi)
        piI = IV.c(pi)
        bL = 2
        Mlap = piI * iv.exp(iv.mpf(2) / bL) / (piI * iv.exp(iv.mpf(2) / bL) + 1 - piI)
        mlap = piI / (piI + (1 - piI) * iv.exp(iv.mpf(2) / bL))
        say(f"  prior {pi}: slot B M - Laplace M = {IV.s(M - Mlap)}; m - m_Laplace = {IV.s(m - mlap)}")
    sec0_objects()
    sec1_prop2(A, B)
    sec2_classes(A, B)
    sec3_many(A, B)
    sec4_access(A, B)
    sec5_bargaining()
    sec6_reserves(A, B)
    sec7_reserve_calibrations()


if __name__ == "__main__":
    main()
