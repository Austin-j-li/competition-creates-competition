#!/usr/bin/env python
"""XP2: independent engine for the R6 and R9 objects in the order-slot model.

Exact Fractions give every rational auction object. Closed forms over the
incumbent law R ~ U[0, r] give each value kernel; Simpson's rule on each
polynomial piece gives each class average (exact for degree three).
Outward interval arithmetic (mpmath.iv, 60 digits) gives every quantity
that depends on e. The module prints nothing; xp2_check.py drives it.
"""
from __future__ import annotations

from fractions import Fraction as Fr

from mpmath import iv, mp

mp.dps = 60
iv.dps = 60


# ----------------------------------------------------------------------------
# Interval helpers
# ----------------------------------------------------------------------------
def I(x):
    """Return an outward interval for an int, a Fraction or an interval."""
    if isinstance(x, bool):
        x = int(x)
    if isinstance(x, int):
        return iv.mpf(x)
    if isinstance(x, Fr):
        if x.denominator == 1:
            return iv.mpf(x.numerator)
        return iv.mpf(x.numerator) / iv.mpf(x.denominator)
    return x


def ends(x):
    """Lower and upper endpoints as mpf numbers."""
    if isinstance(x, (int, Fr)):
        v = mp.mpf(x.numerator) / x.denominator if isinstance(x, Fr) else mp.mpf(x)
        return v, v
    return mp.mpf(x.a), mp.mpf(x.b)


def mid(x):
    a, b = ends(x)
    return (a + b) / 2


def sign(x):
    """'pos', 'neg', 'zero' (exact) or 'undetermined'."""
    if isinstance(x, (int, Fr)):
        return "pos" if x > 0 else "neg" if x < 0 else "zero"
    a, b = ends(x)
    if a > 0:
        return "pos"
    if b < 0:
        return "neg"
    if a == 0 and b == 0:
        return "zero"
    return "undetermined"


def imin(x, y):
    """Enclosure of min(x, y) for two intervals."""
    if isinstance(x, Fr) and isinstance(y, Fr):
        return min(x, y)
    xa, xb = ends(x)
    ya, yb = ends(y)
    return iv.mpf([min(xa, ya), min(xb, yb)])


def imax(x, y):
    if isinstance(x, Fr) and isinstance(y, Fr):
        return max(x, y)
    xa, xb = ends(x)
    ya, yb = ends(y)
    return iv.mpf([max(xa, ya), max(xb, yb)])


# ----------------------------------------------------------------------------
# Slot primitives of calibration B
# ----------------------------------------------------------------------------
E = iv.exp(1)
U = E - 1
BETA = Fr(58931, 200000)
LAM = U * I(BETA) / (1 + U * I(BETA))
BB = (1 - LAM) * I(BETA)            # b = (1 - lambda) beta
B0 = (1 - LAM) * (1 - 2 * I(BETA))  # liquidity mass at zero
ETA = {-1: BETA, 0: 1 - 2 * BETA, 1: BETA}


def Mpost(pi):
    """Top posterior M(pi) = pi(1+u)/(pi(1+u) + 1 - pi)."""
    pi = I(pi)
    return pi * E / (pi * E + 1 - pi)


def mpost(pi):
    """Bottom posterior m(pi) = pi/(pi + (1-pi)(1+u))."""
    pi = I(pi)
    return pi / (pi + (1 - pi) * E)


def Linv(t):
    """Inverse of pi -> M(pi): L(t) = t/(1 + u(1-t))."""
    t = I(t)
    return t / (1 + U * (1 - t))


# ----------------------------------------------------------------------------
# Auction kernel for R ~ U[0, r], reserve p, truthful bids
# ----------------------------------------------------------------------------
def cdf(x: Fr, r: Fr) -> Fr:
    return min(max(x / r, Fr(0)), Fr(1))


def int_cdf(a: Fr, b: Fr, r: Fr) -> Fr:
    """Integral of F over [a, b] with 0 <= a <= b."""
    def G(x):
        return x * x / (2 * r) if x <= r else r / 2 + (x - r)
    return G(b) - G(a)


def upper_excess(v: Fr, r: Fr) -> Fr:
    """E[(R - v)_+]."""
    return (r - v) ** 2 / (2 * r) if v < r else Fr(0)


def incumbent(p: Fr, r: Fr):
    """t0 = p Pr(R >= p), s0 = E[R 1{R >= p}], F(p)."""
    fp = cdf(p, r)
    s0 = (r * r - p * p) / (2 * r) if p < r else Fr(0)
    return p * (1 - fp), s0, fp


def kernel(v: Fr, p: Fr, r: Fr, admissible: bool):
    """(t, g, win, admissible, allocation) for one prepared value v."""
    t0, s0, _ = incumbent(p, r)
    if not admissible:
        return (t0, Fr(0), Fr(0), Fr(0), s0)
    g = int_cdf(p, v, r)          # E[(v - max(p, R))_+]
    t = v - g                     # E[max(p, min(R, v))] = v - g
    return (t, g, cdf(v, r), Fr(1), v + upper_excess(v, r))


def law_objects(law, p: Fr, r: Fr):
    """Average the kernel over a point mass (lo == hi) or U[lo, hi]."""
    lo, hi = law
    if lo == hi:
        return kernel(lo, p, r, lo >= p)
    cuts = sorted({lo, hi} | {x for x in (p, r) if lo < x < hi})
    tot = [Fr(0)] * 5
    for a, b in zip(cuts, cuts[1:]):
        m = (a + b) / 2
        adm = m >= p
        fa, fm, fb = (kernel(x, p, r, adm) for x in (a, m, b))
        for i in range(5):
            tot[i] += (b - a) * (fa[i] + 4 * fm[i] + fb[i]) / 6
    return tuple(x / (hi - lo) for x in tot)


def auction(H, L, p: Fr, r: Fr):
    t0, s0, fp = incumbent(p, r)
    oh = law_objects(H, p, r)
    ol = law_objects(L, p, r)
    return dict(t0=t0, s0=s0, fp=fp,
                th=oh[0], gh=oh[1], wh=oh[2], ah=oh[3], alh=oh[4],
                tl=ol[0], gl=ol[1], wl=ol[2], al=ol[3], all=ol[4],
                delta=oh[0] - ol[0])


def gross(ob, mu):
    """B(mu) = g_L + mu (g_H - g_L)."""
    return I(ob["gl"]) + I(mu) * I(ob["gh"] - ob["gl"])


# ----------------------------------------------------------------------------
# Two-class node in the order slot
# ----------------------------------------------------------------------------
QS = (-1, 0, 1)
QNAME = {-1: "minus", 0: "zero", 1: "plus"}


def masses(qh: int, ql: int):
    """Class-conditional order probabilities a_j(q) for pure informed orders."""
    aH, aL = {}, {}
    for q in QS:
        liq = (1 - LAM) * I(ETA[q])
        aH[q] = liq + (LAM if q == qh else 0)
        aL[q] = liq + (LAM if q == ql else 0)
    return aH, aL


def forced_profile(ob, pi, rho, k):
    """Orders forced under every candidate profile by the return bounds."""
    D = ob["delta"]
    kap = imin(mpost(pi), 1 - Mpost(pi))
    zero = sign(I(k) - I(D))
    full = sign(I(rho) * kap * I(D) - I(k))
    if zero == "pos":
        return (0, 0), "zero forced: Delta < k"
    if full == "pos":
        return (1, -1), "full forced: rho*kappa*Delta > k"
    return None, "open: neither bound holds"


def evaluate(ob, pi, rho, c, k, profile, regime="access", high_entry=None):
    """All node fields for a fixed pure profile.

    regime 'access': the challenger's belief at each price is the raw posterior.
    regime 'hidden': the challenger's belief is the prior at every price.
    high_entry: optional dict q -> 0/1 that overrides the C1 rule (used only
    at an exact equality that the defining identity settles).
    """
    qh, ql = profile
    aH, aL = masses(qh, ql)
    pi_i, rho_i, c_i, k_i = I(pi), I(rho), I(c), I(k)
    out, flags = {}, []
    mass, mu, ent, hi_e = {}, {}, {}, {}
    for q in QS:
        mass[q] = pi_i * aH[q] + (1 - pi_i) * aL[q]
        mu[q] = pi_i * aH[q] / mass[q]
        belief = mu[q] if regime == "access" else pi_i
        cs = gross(ob, belief) - c_i
        if high_entry is not None and q in high_entry:
            hi_e[q] = high_entry[q]
        else:
            s = sign(cs)
            if s == "undetermined" or s == "zero":
                flags.append(f"high-cost tie at q={q}")
                hi_e[q] = 1  # C1
            else:
                hi_e[q] = 1 if s == "pos" else 0
        ent[q] = rho_i + (1 - rho_i) * hi_e[q]
        out["mass_" + QNAME[q]] = mass[q]
        out["mu_" + QNAME[q]] = mu[q]
        out["cost_sign_" + QNAME[q]] = cs
        out["low_profit_" + QNAME[q]] = gross(ob, belief)
        if sign(gross(ob, belief)) != "pos":
            flags.append(f"zero-cost profit not positive at q={q}")
    price = {}
    for q in QS:
        price[q] = I(ob["t0"]) + ent[q] * (I(ob["tl"] - ob["t0"]) + I(ob["delta"]) * mu[q])
        out["price_" + QNAME[q]] = price[q]
        out["entry_" + QNAME[q]] = ent[q]
    out["prior_cost_margin"] = c_i - gross(ob, pi_i)
    for cls, tj, qj in (("h", ob["th"], qh), ("l", ob["tl"], ql)):
        pays = {}
        for q in QS:
            if q == 0:
                pays[q] = iv.mpf(0)
            else:
                pays[q] = q * (I(ob["t0"]) + ent[q] * I(tj - ob["t0"]) - price[q]) - k_i
            out[f"pay_{cls}_{q + 1}"] = pays[q]
        others = [pays[q] for q in QS if q != qj]
        best = imax(others[0], others[1])
        out["choice_" + cls] = pays[qj] - best
    eh = sum((aH[q] * ent[q] for q in QS), iv.mpf(0))
    el = sum((aL[q] * ent[q] for q in QS), iv.mpf(0))
    tot = pi_i * eh + (1 - pi_i) * el
    out["eh"], out["el"], out["entry"] = eh, el, tot
    out["ownership"] = pi_i * eh * I(ob["wh"])
    out["proceeds"] = (I(ob["t0"]) + pi_i * eh * I(ob["th"] - ob["t0"])
                       + (1 - pi_i) * el * I(ob["tl"] - ob["t0"]))
    alloc = (I(ob["s0"]) + pi_i * eh * I(ob["alh"] - ob["s0"])
             + (1 - pi_i) * el * I(ob["all"] - ob["s0"]))
    paid = (1 - rho_i) * c_i * sum((mass[q] * hi_e[q] for q in QS), iv.mpf(0))
    out["paid_cost"] = paid
    out["surplus"] = alloc - paid
    adm = pi_i * eh * I(ob["ah"]) + (1 - pi_i) * el * I(ob["al"])
    out["admissible"] = adm
    two = (1 - I(ob["fp"])) * adm
    out["two"] = two
    out["sale"] = 1 - I(ob["fp"]) + adm - two
    out["_pattern"] = tuple(hi_e[q] for q in QS)
    out["_flags"] = flags
    out["_profile"] = profile
    return out


def node(H, L, pi, p, rho, c, k, r, regime="access", high_entry=None, profile=None):
    ob = auction(H, L, p, r)
    why = "prescribed"
    if profile is None:
        profile, why = forced_profile(ob, pi, rho, k)
    res = {"t0": ob["t0"], "th": ob["th"], "tl": ob["tl"], "gh": ob["gh"],
           "gl": ob["gl"], "wh": ob["wh"], "delta": ob["delta"]}
    if profile is None:
        res["_why"] = why
        return res, ob
    res.update(evaluate(ob, pi, rho, c, k, profile, regime, high_entry))
    res["_why"] = why
    return res, ob


def pure_equilibria(ob, pi, rho, c, k, regime="access"):
    """Count the pure profiles whose prescribed orders are best responses.

    A profile counts when each class's prescribed payoff is not certified
    to be strictly below an alternative. This is a diagnostic beside the
    all-profile bounds; mixed profiles are covered by those bounds.
    """
    found = []
    for qh in QS:
        for ql in QS:
            res = evaluate(ob, pi, rho, c, k, (qh, ql), regime)
            ok = all(sign(res["choice_" + cl]) != "neg" for cl in ("h", "l"))
            if ok:
                found.append(((qh, ql), sign(res["choice_h"]), sign(res["choice_l"])))
    return found
