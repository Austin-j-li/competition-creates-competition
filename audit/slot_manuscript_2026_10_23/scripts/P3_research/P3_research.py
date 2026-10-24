#!/usr/bin/env python3
"""P3: competition creates research in the order slot (result R10), general beta and calibration B.

Every number uses exact rational arithmetic (fractions.Fraction). A quantity that depends on e uses
rational interval arithmetic with rational bounds on e. The program prints results only. It writes
the registry rows of this workstream and a LaTeX file of registry macros for the proof package.

Model. Before it learns the class, the investor chooses a private research intensity z in [0, cap]
at cost (a/2) z^2. With probability z it learns the class j in {H, L} and fills the single order slot
with q in {-1, 0, 1} at cost k|q|. Otherwise a liquidity trader fills the slot and sells, abstains
or buys with probabilities beta, 1 - 2 beta, beta. Market makers see the order and price with the
conjectured intensity. The challenger sees the price and its cost. Second-price auction, reserve p,
incumbent value R ~ U[0, r], point-mass classes h and ell, prior 1/2.

Usage:
  python P3_research.py > P3_research.log
"""
from fractions import Fraction as Fr
import csv
import hashlib
import json
import pathlib
import platform
import sys

HERE = pathlib.Path(__file__).resolve().parent
TEAM = HERE.parents[1]
REG_CSV = TEAM / "registry" / "P3_research.csv"
NUM_TEX = HERE / "numbers_P3.tex"
EXACT_JSON = HERE / "P3_enclosures.json"
SCRIPT = "scripts/P3_research/P3_research.py"
LOG = "scripts/P3_research/P3_research.log"


# ================================================================================================
# Rational interval arithmetic
# ================================================================================================
class Iv:
    """A closed interval [lo, hi] with Fraction endpoints. Arithmetic is exact, so enclosures are valid."""
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = Fr(lo)
        self.hi = Fr(lo) if hi is None else Fr(hi)

    @staticmethod
    def of(x):
        return x if isinstance(x, Iv) else Iv(x)

    def __add__(self, o):
        o = Iv.of(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __sub__(self, o):
        o = Iv.of(o)
        return Iv(self.lo - o.hi, self.hi - o.lo)

    def __rsub__(self, o):
        return Iv.of(o) - self

    def __neg__(self):
        return Iv(-self.hi, -self.lo)

    def __mul__(self, o):
        o = Iv.of(o)
        ps = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Iv(min(ps), max(ps))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = Iv.of(o)
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError("interval divisor contains zero")
        return self * Iv(1 / o.hi, 1 / o.lo)

    def __rtruediv__(self, o):
        return Iv.of(o) / self

    def mid(self):
        return (self.lo + self.hi) / 2

    def width(self):
        return self.hi - self.lo

    def __repr__(self):
        return f"[{float(self.lo):.15g}, {float(self.hi):.15g}]"


def lo(x):
    return x.lo if isinstance(x, Iv) else Fr(x)


def hi(x):
    return x.hi if isinstance(x, Iv) else Fr(x)


def sign(x):
    """+1 or -1 if decided, 0 if the value is exactly zero, None if the enclosure contains zero."""
    if lo(x) > 0:
        return 1
    if hi(x) < 0:
        return -1
    if lo(x) == 0 and hi(x) == 0:
        return 0
    return None


def ge(x, y):
    """Decided comparison x >= y: True, False, or None (undecided)."""
    if lo(x) >= hi(y):
        return True
    if hi(x) < lo(y):
        return False
    return None


def gt(x, y):
    if lo(x) > hi(y):
        return True
    if hi(x) <= lo(y):
        return False
    return None


def isqrt_frac(x, width=Fr(1, 10 ** 40)):
    """Rational bounds on sqrt(x) for a Fraction x >= 0."""
    x = Fr(x)
    if x == 0:
        return Iv(0)
    a, b = Fr(0), max(Fr(1), x)
    while b - a > width:
        m = (a + b) / 2
        if m * m <= x:
            a = m
        else:
            b = m
    return Iv(a, b)


def sqrt_iv(x):
    x = Iv.of(x)
    return Iv(isqrt_frac(x.lo).lo, isqrt_frac(x.hi).hi)


def e_bounds(N=40):
    """Rational enclosure of e: partial sum of 1/n! and the remainder bound 2/(N+1)!."""
    s, f = Fr(0), Fr(1)
    for n in range(N + 1):
        if n > 0:
            f /= n
        s += f
    return Iv(s, s + 2 * f / (N + 1))


def dec(x, n=12):
    """Decimal display (display only). Intervals print their midpoint."""
    v = x.mid() if isinstance(x, Iv) else Fr(x)
    return f"{float(v):.{n}f}"


def _fixed(q, n):
    """Format the integer q / 10^n as a decimal with n places."""
    s = "-" if q < 0 else ""
    q = abs(q)
    return f"{s}{q // 10 ** n}.{q % 10 ** n:0{n}d}"


def enc(x, n=12):
    """Outward-rounded decimal enclosure with n places, computed from the exact rational endpoints.

    The lower end rounds down and the upper end rounds up, so the printed interval contains the
    exact interval. An exact value prints as one decimal if it terminates within n places;
    otherwise it prints as an outward pair one unit of the last place wide."""
    x = Iv.of(x)
    scale = 10 ** n
    lo_q = (x.lo.numerator * scale) // x.lo.denominator
    hi_q = -((-x.hi.numerator * scale) // x.hi.denominator)
    if lo_q == hi_q:
        return _fixed(lo_q, n)
    return f"[{_fixed(lo_q, n)}, {_fixed(hi_q, n)}]"


def endpoint_text(x, upper, places=60, max_len=400):
    """One endpoint for the machine-readable file: the exact rational if it is short, else a decimal
    with 60 places that rounds outward (down for a lower end, up for an upper end)."""
    s = f"{x.numerator}/{x.denominator}" if x.denominator != 1 else f"{x.numerator}"
    if len(s) <= max_len:
        return s, "exact"
    scale = 10 ** places
    q = -((-x.numerator * scale) // x.denominator) if upper else (x.numerator * scale) // x.denominator
    return _fixed(q, places), "outward decimal"


def fdisp(x, n=6):
    """Display string with n decimals from an exact value or an enclosure of width well below 10^-n."""
    v = x.mid() if isinstance(x, Iv) else Fr(x)
    q = round(v * 10 ** n)
    s = "-" if q < 0 else ""
    q = abs(q)
    return f"{s}{q // 10 ** n}.{q % 10 ** n:0{n}d}"


# ================================================================================================
# Primitives (calibration B)
# ================================================================================================
H_VAL, L_VAL, P_RES = Fr(10), Fr(1), Fr(1, 2)
RHO, C_H, K = Fr(1, 4), Fr(6), Fr(1, 50)
PI = Fr(1, 2)
BETA_B = Fr(294655, 1000000)
A_B = Fr(1, 40)
E_IV = e_bounds()
U_B = E_IV - 1
STRENGTHS = [Fr(6, 5), Fr(31, 20), Fr(8, 5), Fr(33, 20), Fr(3), Fr(18, 5)]
MIDDLE = [Fr(31, 20), Fr(8, 5), Fr(33, 20)]
R1, R2 = Fr(3), Fr(18, 5)
TAG = {Fr(6, 5): "r0", Fr(31, 20): "r155", Fr(8, 5): "r160", Fr(33, 20): "r165", Fr(3): "r1",
       Fr(18, 5): "r2"}


# ================================================================================================
# Auction objects
# ================================================================================================
def expect(r, f, kinks):
    """E f(R) for R ~ U[0, r] and f linear between kinks (the midpoint rule is exact)."""
    pts = sorted({Fr(0), r} | {x for x in kinks if 0 < x < r})
    tot = Fr(0)
    for a, b in zip(pts[:-1], pts[1:]):
        tot += (b - a) * f((a + b) / 2)
    return tot / r


_AUC = {}


def auction(r):
    """Closed forms of the Laplace manuscript eq. (4) for p < ell < r < h, plus surplus objects."""
    r = Fr(r)
    if r in _AUC:
        return _AUC[r]
    p, l, h = P_RES, L_VAL, H_VAL
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = l - (l * l - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (l * l - p * p) / (2 * r)
    Dl = (r - l) ** 2 / (2 * r)
    tau = (C_H - gL) / (gH - gL)
    S0 = (r * r - p * p) / (2 * r)            # E[R 1{R >= p}]
    SH = h                                    # E[max(h, R)], since r < h
    SL = (l * l + (r * r - l * l) / 2) / r    # E[max(ell, R)]
    out = dict(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, Delta=Dl, tau=tau, S0=S0, SH=SH, SL=SL)
    _AUC[r] = out
    return out


def auction_integrated(r):
    kinks = [P_RES, L_VAL, H_VAL]
    p, l, h = P_RES, L_VAL, H_VAL
    return dict(
        t0=expect(r, lambda x: p if x >= p else Fr(0), kinks),
        tH=expect(r, lambda x: min(h, max(p, x)), kinks),
        tL=expect(r, lambda x: min(l, max(p, x)), kinks),
        gH=expect(r, lambda x: max(Fr(0), h - max(p, x)), kinks),
        gL=expect(r, lambda x: max(Fr(0), l - max(p, x)), kinks),
        S0=expect(r, lambda x: x if x >= p else Fr(0), kinks),
        SH=expect(r, lambda x: max(h, x), kinks),
        SL=expect(r, lambda x: max(l, x), kinks))


def B_of(r, mu):
    A = auction(r)
    return A["gL"] + mu * (A["gH"] - A["gL"])


def r_of_Delta(D):
    """Inverse of Delta(r) = (r - 1)^2 / (2r) on r > 1 (ell = 1): r = 1 + D + sqrt(D^2 + 2D)."""
    D = Iv.of(D)
    return 1 + D + sqrt_iv(D * D + 2 * D)


# ================================================================================================
# Order-slot objects at general beta (prior 1/2)
# ================================================================================================
def eta(q, beta):
    return beta if q != 0 else 1 - 2 * beta


def d_full(lam, beta):
    """1 - mu(+1) under a full purchase and no informed sale: b / (2b + lam), b = (1 - lam) beta."""
    return (1 - lam) * beta / (2 * beta + lam * (1 - 2 * beta))


def lam_of_d(dv, beta):
    """Inverse of d_full on (0, 1/2]."""
    return beta * (1 - 2 * dv) / (beta + dv * (1 - 2 * beta))


def lam_E(tau, beta):
    """Recruitment intensity: 1 - d_full(lam_E) = tau."""
    return beta * (2 * tau - 1) / (beta + (1 - 2 * beta) * (1 - tau))


def lam_of_u(u, beta):
    return u * beta / (1 + u * beta)


def M_of(lam, beta):
    u = lam / ((1 - lam) * beta)
    return (1 + u) / (2 + u)


def F_res(lam, r, a, beta, E, Kc):
    """Research polynomial for a type with research value V = (E Delta d(lam) - Kc)/2:
    F = 2 (2 beta + lam (1 - 2 beta)) [a lam - V].  F rises strictly on lam >= 0."""
    Dl = auction(r)["Delta"]
    D = 2 * beta + lam * (1 - 2 * beta)
    return 2 * a * lam * D + Kc * D - E * Dl * beta * (1 - lam)


def F_coeffs(r, a, beta, E, Kc):
    Dl = auction(r)["Delta"]
    A2 = 2 * a * (1 - 2 * beta)
    A1 = 4 * a * beta + Kc * (1 - 2 * beta) + E * Dl * beta
    A0 = beta * (2 * Kc - E * Dl)
    return A2, A1, A0


def bracket_root(r, a, beta, E, Kc, width=Fr(1, 10 ** 24)):
    lo_, hi_ = Fr(0), Fr(1)
    while hi_ - lo_ > width:
        m = (lo_ + hi_) / 2
        if F_res(m, r, a, beta, E, Kc) < 0:
            lo_ = m
        else:
            hi_ = m
    return Iv(lo_, hi_)


# ================================================================================================
# Direct verification of a candidate tuple against its own price function and entry rule
# ================================================================================================
def verify(r, beta, cap, a, lam, sH, sL, zeta_override=None, inv_rule="IM", ch_rule="C1", hidden=False):
    """Compute every object of the tuple and every equilibrium condition.
    lam: conjectured intensity (Fraction or Iv). sH, sL: dicts q -> probability after success.
    zeta_override: dict q -> preparation probability of the high-cost challenger at a tie (rule CM)."""
    A = auction(r)
    Dl, tau, t0, tH, tL = A["Delta"], A["tau"], A["t0"], A["tH"], A["tL"]
    lamv = Iv.of(lam)
    out = dict(r=r, lam=lam, sH=sH, sL=sL)
    f = {}
    for j, s in (("H", sH), ("L", sL)):
        f[j] = {q: (1 - lamv) * eta(q, beta) + lamv * s[q] for q in (-1, 0, 1)}
    mu, zeta, e, P, Pr = {}, {}, {}, {}, {}
    ties = []
    for q in (-1, 0, 1):
        mu[q] = PI * f["H"][q] / (PI * f["H"][q] + (1 - PI) * f["L"][q])
        if hidden:
            zeta[q] = Fr(0)
        else:
            c = ge(mu[q], tau)
            if zeta_override is not None and q in zeta_override:
                zeta[q] = zeta_override[q]
                if not (lo(mu[q]) == hi(mu[q]) == tau):
                    ties.append(f"override at q={q} without an exact tie")
            elif c is True:
                zeta[q] = Fr(1)
                if lo(mu[q]) == tau:
                    ties.append(f"challenger tie at q={q}")
            elif c is False:
                zeta[q] = Fr(0)
            else:
                zeta[q] = None
                ties.append(f"undecided entry at q={q}")
        e[q] = RHO + (1 - RHO) * zeta[q] if zeta[q] is not None else None
        P[q] = t0 + e[q] * (tL - t0 + Dl * mu[q])
        Pr[q] = PI * f["H"][q] + (1 - PI) * f["L"][q]
    U = {"H": {}, "L": {}}
    for q in (-1, 0, 1):
        EVH = t0 + e[q] * (tH - t0)
        EVL = t0 + e[q] * (tL - t0)
        U["H"][q] = q * (EVH - P[q]) - K * abs(q)
        U["L"][q] = q * (EVL - P[q]) - K * abs(q)
    # investor order optimality
    order_ok, order_margin, order_notes = True, {}, []
    for j, s in (("H", sH), ("L", sL)):
        supp = [q for q in (-1, 0, 1) if hi(s[q]) > 0]
        unused = [q for q in (-1, 0, 1) if q not in supp]
        for q in supp:
            for q2 in (-1, 0, 1):
                if q2 == q:
                    continue
                sg = sign(U[j][q] - U[j][q2])
                if q2 in supp:
                    # a mixture needs indifference; an enclosure that contains zero is consistent with it
                    if sg not in (0, None):
                        order_ok = False
                        order_notes.append(f"{j}: support orders {q},{q2} not indifferent")
                elif sg is None or sg < 0:
                    order_ok = False
                    order_notes.append(f"{j}: order {q2} is not worse than used order {q}")
        if unused:
            best_used = max((U[j][q] for q in supp), key=lambda x: lo(x))
            order_margin[j] = min((Iv.of(best_used) - U[j][q2] for q2 in unused), key=lambda x: lo(x))
        else:
            order_margin[j] = None
        if inv_rule == "I0":
            zero_in_argmax = all(sign(U[j][0] - U[j][q2]) in (0, 1) for q2 in (-1, 1))
            if zero_in_argmax and not (lo(s[0]) == 1 and hi(s[0]) == 1):
                order_ok = False
                order_notes.append(f"{j}: rule I0 requires zero at indifference")
        if len(supp) > 1:
            order_notes.append(f"{j} mixes over {supp}")
    maxH = Iv(max(lo(U["H"][q]) for q in (-1, 0, 1)), max(hi(U["H"][q]) for q in (-1, 0, 1)))
    maxL = Iv(max(lo(U["L"][q]) for q in (-1, 0, 1)), max(hi(U["L"][q]) for q in (-1, 0, 1)))
    V = PI * maxH + (1 - PI) * maxL
    capv = Iv.of(cap)
    # research optimality: lam = min(cap, V / a)
    Va = V / a
    if lo(lamv) == 0 and hi(lamv) == 0:
        res_ok = (sign(V) == 0)
        res_kind = "zero"
        res_margin = None
    elif lo(lamv) == lo(capv) and hi(lamv) == hi(capv):
        res_kind = "cap"
        res_margin = Va - capv          # >= 0 needed
        res_ok = sign(res_margin) in (0, 1)
    else:
        res_kind = "interior"
        gap = Va - lamv
        res_margin = capv - Va          # > 0 needed
        res_ok = (lo(gap) <= 0 <= hi(gap)) and sign(res_margin) == 1
    # price sufficiency: price strictly increasing in the posterior across orders
    qs = sorted((-1, 0, 1), key=lambda q: lo(mu[q]))
    price_ok = True
    for qa, qb in zip(qs[:-1], qs[1:]):
        if gt(mu[qb], mu[qa]) and not gt(P[qb], P[qa]):
            price_ok = False
    Eagg = sum((Pr[q] * e[q] for q in (-1, 0, 1)), Fr(0))
    eH = sum((f["H"][q] * e[q] for q in (-1, 0, 1)), Fr(0))
    out.update(mu=mu, zeta=zeta, e=e, P=P, Pr=Pr, U=U, V=V, order_ok=order_ok, order_margin=order_margin,
               order_notes=order_notes, res_ok=res_ok, res_kind=res_kind, res_margin=res_margin,
               price_ok=price_ok, E=Eagg, own=PI * eH, ties=ties, f=f)
    out["ok"] = order_ok and res_ok and price_ok and not any(t.startswith("undecided") or t.startswith("override")
                                                             for t in ties)
    return out


def print_verification(v, indent="      "):
    mu, e, U, P = v["mu"], v["e"], v["U"], v["P"]
    print(f"{indent}posteriors mu(-1,0,+1) = {enc(mu[-1])}, {enc(mu[0])}, {enc(mu[1])}")
    print(f"{indent}entry      e(-1,0,+1)  = {enc(e[-1], 6)}, {enc(e[0], 6)}, {enc(e[1], 6)}")
    print(f"{indent}prices     P(-1,0,+1)  = {enc(P[-1])}, {enc(P[0])}, {enc(P[1])}")
    print(f"{indent}U_H(-1,0,+1) = {enc(U['H'][-1])}, {enc(U['H'][0])}, {enc(U['H'][1])}")
    print(f"{indent}U_L(-1,0,+1) = {enc(U['L'][-1])}, {enc(U['L'][0])}, {enc(U['L'][1])}")
    om = v["order_margin"]
    print(f"{indent}order margins (best used minus best unused): H {enc(om['H']) if om['H'] is not None else '-'}"
          f", L {enc(om['L']) if om['L'] is not None else '-'}")
    print(f"{indent}research value V = {enc(v['V'])}; research condition {v['res_kind']}: "
          f"margin {enc(v['res_margin']) if v['res_margin'] is not None else 'V = 0 exactly'}")
    print(f"{indent}aggregate entry E = {enc(v['E'])}; H ownership = {enc(v['own'])}")
    print(f"{indent}checks: orders {v['order_ok']}, research {v['res_ok']}, price sufficiency {v['price_ok']}, "
          f"ties {v['ties'] if v['ties'] else 'none'}, notes {v['order_notes'] if v['order_notes'] else 'none'}"
          f" -> equilibrium conditions hold: {v['ok']}")


# ================================================================================================
# Complete enumeration (the classification of Lemmas R3 and R4)
# ================================================================================================
def in_iv(x, iv):
    """Decided membership of x (Fraction or Iv) in iv = (lo, lo_closed, hi, hi_closed); None = unbounded."""
    a, ac, b, bc = iv
    res = True
    if a is not None:
        c = ge(x, a) if ac else gt(x, a)
        if c is None:
            return None
        res = res and c
    if b is not None:
        c = ge(b, x) if bc else gt(b, x)
        if c is None:
            return None
        res = res and c
    return res


def enumerate_eq(r, beta, cap, a, ch_rule="C1", inv_rule="IM", hidden=False):
    """Every equilibrium at strength r. Returns a list of (label, verification record)."""
    A = auction(r)
    Dl, tau = A["Delta"], A["tau"]
    found, notes = [], []
    if not tau > Fr(1, 2):
        notes.append("tau <= 1/2: classification not applicable")
        return found, notes
    zeroH = {-1: Fr(0), 0: Fr(1), 1: Fr(0)}
    # (Z) zero research
    if RHO * Dl / 2 <= K:
        v = verify(r, beta, cap, a, Fr(0), zeroH, zeroH, inv_rule=inv_rule, ch_rule=ch_rule, hidden=hidden)
        found.append(("Z: zero research, no informed order", v))
    l_sells = RHO * Dl / 2 > K
    lamL = lam_of_d(K / (RHO * Dl), beta) if l_sells else None
    lE = lam_E(tau, beta)
    capv = Iv.of(cap)
    pieces = []
    if l_sells:
        pieces.append(("L1", (Fr(0), False, lamL, inv_rule == "IM")))
        if inv_rule == "IM":
            pieces.append(("Lint", (lamL, False, None, False)))
    else:
        pieces.append(("L0", (Fr(0), False, None, False)))
    if hidden:
        regimes = [("lo", Fr(0), (None, False, None, False))]
    else:
        regimes = [("hi", Fr(1), (lE, True, None, False)),
                   ("lo", Fr(0), (None, False, lE, ch_rule == "CM"))]
    for reg, zeta_plus, reg_iv in regimes:
        e_plus = RHO + (1 - RHO) * zeta_plus
        for pc, pc_iv in pieces:
            E = e_plus + (RHO if pc == "L1" else 0)
            Kc = K * (2 if pc == "L1" else 1)

            def member(x):
                c1, c2 = in_iv(x, reg_iv), in_iv(x, pc_iv)
                if c1 is None or c2 is None:
                    return None
                return c1 and c2

            # interior research: root of F strictly below the cap
            if E * Dl > 2 * Kc:
                root = bracket_root(r, a, beta, E, Kc)
                below_cap = gt(capv, root)
                m = member(root)
                if below_cap is None or m is None:
                    notes.append(f"undecided interior candidate {reg}/{pc} at root {root}")
                elif below_cap and m:
                    sL = {-1: Fr(0), 0: Fr(1), 1: Fr(0)}
                    if pc == "L1":
                        sL = {-1: Fr(1), 0: Fr(0), 1: Fr(0)}
                    elif pc == "Lint":
                        bR = (1 - root) * beta
                        sig = (RHO * Dl * bR / K - 2 * bR) / root
                        sL = {-1: sig, 0: 1 - sig, 1: Fr(0)}
                    sHf = {-1: Fr(0), 0: Fr(0), 1: Fr(1)}
                    zo = None
                    v = verify(r, beta, cap, a, root, sHf, sL, zo, inv_rule, ch_rule, hidden)
                    found.append((f"{reg}/{pc}: interior research", v))
            # research at the cap
            m = member(capv)
            Fc = F_res(capv, r, a, beta, E, Kc)
            if m is None or sign(Fc) is None:
                notes.append(f"undecided cap candidate {reg}/{pc}")
            elif m and sign(Fc) in (-1, 0):
                sL = {-1: Fr(0), 0: Fr(1), 1: Fr(0)}
                if pc == "L1":
                    sL = {-1: Fr(1), 0: Fr(0), 1: Fr(0)}
                elif pc == "Lint":
                    bR = (1 - capv) * beta
                    sig = (RHO * Dl * bR / K - 2 * bR) / capv
                    sL = {-1: sig, 0: 1 - sig, 1: Fr(0)}
                sHf = {-1: Fr(0), 0: Fr(0), 1: Fr(1)}
                v = verify(r, beta, cap, a, capv, sHf, sL, None, inv_rule, ch_rule, hidden)
                found.append((f"{reg}/{pc}: research at the cap", v))
    # (T) challenger mixture at the recruitment threshold (rule CM only)
    if ch_rule == "CM" and not hidden:
        inside = gt(capv, lE)
        if inside is None:
            notes.append("undecided: lam_E against the cap")
        elif inside and lE > 0:
            if l_sells and lE <= lamL:
                pc, gL = "L1", RHO * Dl * (1 - tau) - K
                sL = {-1: Fr(1), 0: Fr(0), 1: Fr(0)}
            elif l_sells:
                pc, gL = "Lint", Fr(0)
                bR = (1 - lE) * beta
                sig = (RHO * Dl * bR / K - 2 * bR) / lE
                sL = {-1: sig, 0: 1 - sig, 1: Fr(0)}
            else:
                pc, gL = "L0", Fr(0)
                sL = {-1: Fr(0), 0: Fr(1), 1: Fr(0)}
            if pc != "Lint" or inv_rule == "IM":
                e_star = (2 * a * lE + K - gL) / (Dl * (1 - tau))
                if RHO < e_star < 1:
                    zeta_star = (e_star - RHO) / (1 - RHO)
                    sHf = {-1: Fr(0), 0: Fr(0), 1: Fr(1)}
                    v = verify(r, beta, cap, a, lE, sHf, sL, {1: zeta_star}, inv_rule, ch_rule, hidden)
                    v["e_star"] = e_star
                    found.append((f"th/{pc}: challenger mixture at the threshold", v))
                else:
                    notes.append(f"threshold candidate has e* = {dec(e_star, 6)} outside (rho, 1)")
        elif inside is False:
            notes.append("threshold: lam_E is not below the cap")
    return found, notes


# ================================================================================================
# Registry
# ================================================================================================
REG = []
EXACT = {}


def reg(key, value, display, status, note):
    if isinstance(value, Iv) and display == fdisp(value):
        if fdisp(Iv(value.lo)) != fdisp(Iv(value.hi)):
            print(f"  WARNING: the enclosure of {key} does not fix its display {display}")
    if isinstance(value, Iv):
        vtxt = f"{float(value.mid()):.15g}"
        note = f"{note}; enclosure {enc(value, 15)}"
    elif isinstance(value, Fr):
        vtxt = f"{value.numerator}/{value.denominator}" if value.denominator != 1 else f"{value.numerator}"
        if value.denominator != 1 and len(vtxt) > 60:
            vtxt = f"{float(value):.15g}"
            note = f"{note}; exact rational in the run log"
    else:
        vtxt = str(value)
    REG.append(dict(key=key, value=vtxt, display=display, status=status, source_script=SCRIPT, run_log=LOG,
                    note=note))
    if isinstance(value, (Iv, Fr, int)):
        x = Iv.of(value)
        lo_t, lo_k = endpoint_text(x.lo, upper=False)
        hi_t, hi_k = endpoint_text(x.hi, upper=True)
        EXACT[key] = dict(lo=lo_t, hi=hi_t, lo_form=lo_k, hi_form=hi_k)


def write_registry():
    cols = ["key", "value", "display", "status", "source_script", "run_log", "note"]
    with REG_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in REG:
            w.writerow(row)
    lines = ["% numbers_P3.tex: generated by scripts/P3_research/P3_research.py from registry/P3_research.csv.",
             "% Do not edit by hand.",
             "\\makeatletter",
             "\\providecommand{\\reg}[1]{\\ifcsname reg@#1\\endcsname\\csname reg@#1\\endcsname"
             "\\else\\textbf{??\\detokenize{#1}}\\fi}"]
    for row in REG:
        lines.append(f"\\expandafter\\def\\csname reg@{row['key']}\\endcsname{{{row['display']}}}")
    lines.append("\\makeatother")
    NUM_TEX.write_text("\n".join(lines) + "\n")
    EXACT_JSON.write_text(json.dumps(dict(
        description="Endpoints of the enclosure of each registry value of P3. 'exact' is the exact rational "
                    "endpoint; 'outward decimal' rounds the lower end down and the upper end up (60 places).",
        source_script=SCRIPT, rows=EXACT), indent=1) + "\n")


# ================================================================================================
# Main
# ================================================================================================
def main():
    src = pathlib.Path(__file__).read_bytes()
    print("P3: competition creates research in the order slot (R10)")
    print(f"python {platform.python_version()} | source sha256 {hashlib.sha256(src).hexdigest()}")
    print(f"primitives: h={H_VAL}, ell={L_VAL}, p={P_RES}, rho={RHO}, c_L=0, c_H={C_H}, k={K}, pi={PI}")
    print(f"slot primitives at B: 1+u = e, beta = {BETA_B} = {float(BETA_B)}")
    print(f"e enclosure: {enc(E_IV, 30)} (width {float(E_IV.width()):.2e})")
    beta = BETA_B
    capB = lam_of_u(U_B, beta)
    bB = (1 - capB) * beta
    MB = M_of(capB, beta)
    print(f"cap = lambda_B = u beta/(1 + u beta) = {enc(capB, 15)}")
    print(f"b_B = (1 - lambda_B) beta = {enc(bB, 15)}")
    print(f"M(1/2) at the cap = {enc(MB, 15)}; e/(1+e) = {enc(E_IV / (1 + E_IV), 15)}")
    print(f"research cost a = {A_B}")
    print()
    reg("res_a", A_B, "1/40", "input", "research cost parameter: cost (a/2) lambda^2")
    reg("res_cap", capB, fdisp(capB), "input", "research cap = lambda_B = u beta/(1 + u beta) at B with 1+u = e")

    # ------------------------------------------------------------------------------------------
    print("== A. Auction objects: closed forms against direct integration; tau > 1/2 ==")
    for r in STRENGTHS:
        A = auction(r)
        I = auction_integrated(r)
        diffs = {k_: A[k_] - I[k_] for k_ in I}
        print(f"  r = {r}: t0={A['t0']}, tH={A['tH']}, tL={A['tL']}, gH={A['gH']}, gL={A['gL']}, "
              f"Delta={A['Delta']} ({dec(A['Delta'], 9)}), tau={A['tau']} ({dec(A['tau'], 9)})")
        print(f"      closed form minus integral: {sorted(set(diffs.values()))}; "
              f"B(1/2) - c_H = {B_of(r, PI) - C_H}; rho Delta/2 - k = {RHO * A['Delta'] / 2 - K} "
              f"({dec(RHO * A['Delta'] / 2 - K, 9)})")
    print("  For 1 < r < 10, B_r(1/2) = 5 - r/4 + 1/(8r) < 6, so tau(r) > 1/2 (analytical).")
    rN = r_of_Delta(2 * K / RHO)
    print(f"  no-research boundary r_N = r(2k/rho) = {enc(rN, 15)}")
    MB_mid = MB
    # ceiling r_C: B_r(M) = c_H, root of 4M r^2 + (48 - 80M) r + (4M - 3) = 0 (benchmark), larger root
    Mi = MB
    disc = (80 * Mi - 48) * (80 * Mi - 48) - 16 * Mi * (4 * Mi - 3)
    rC = ((80 * Mi - 48) + sqrt_iv(disc)) / (8 * Mi)
    print(f"  entry ceiling r_C (B_r(M) = c_H) = {enc(rC, 15)}")
    print()

    # ------------------------------------------------------------------------------------------
    print("== B. Complete equilibrium sets at the six strengths (calibration B, cap lambda_B, a = 1/40) ==")
    sets = {}
    for ch in ("C1", "CM"):
        for inv in ("IM", "I0"):
            print(f" -- tie rules: investor {inv}, challenger {ch} --")
            for r in STRENGTHS:
                found, notes = enumerate_eq(r, beta, capB, A_B, ch, inv)
                sets[(r, inv, ch)] = found
                A = auction(r)
                print(f"  r = {r} ({dec(r, 2)}): number of equilibria {len(found)}; tau = {dec(A['tau'], 9)}, "
                      f"lam_E = {lam_E(A['tau'], beta)} = {dec(lam_E(A['tau'], beta), 12)}; notes: {notes}")
                for label, v in found:
                    lam = v["lam"]
                    extra = f", e* = {v['e_star']} = {dec(v['e_star'], 9)}" if "e_star" in v else ""
                    print(f"    {label}: lambda = {enc(lam, 15)}{extra}")
                    print_verification(v)
            print()

    # ------------------------------------------------------------------------------------------
    print("== C. The research branch at the three intermediate strengths ==")
    branch = {}
    for r in MIDDLE:
        lab, v = [x for x in sets[(r, "IM", "C1")] if x[0].startswith("hi/L0: interior")][0]
        lam = v["lam"]
        A = auction(r)
        A2, A1, A0 = F_coeffs(r, A_B, beta, Fr(1), K)
        closed = (-A1 + sqrt_iv(A1 * A1 - 4 * A2 * A0)) / (2 * A2)
        Ebr = RHO + (1 - RHO) * (beta + (Fr(1, 2) - beta) * lam)
        Fl = A2 * 2 * lam + A1
        dlam = beta * (1 - lam) * (Fr(1, 2) - 1 / (2 * r * r)) / Fl
        branch[r] = dict(lam=lam, E=v["E"], mu=v["mu"][1], UH=v["U"]["H"][1], own=v["own"])
        print(f"  r = {r}: lambda_R in {enc(lam, 18)} (width {float(lam.width()):.1e}); closed-form root "
              f"{enc(closed, 18)}")
        print(f"      F coefficients: A2 = {A2}, A1 = {A1}, A0 = {A0}")
        print(f"      mu(+1) = {enc(v['mu'][1], 15)} > tau = {dec(A['tau'], 15)}; U_H(+1) = 2 a lambda_R = "
              f"{enc(v['U']['H'][1], 15)}")
        print(f"      entry E_R = rho + (1-rho)(beta + (1/2 - beta) lambda_R) = {enc(Ebr, 15)}; "
              f"from the tuple {enc(v['E'], 15)}")
        print(f"      d lambda_R / d r = beta (1 - lambda) Delta'(r) / F_lambda = {enc(dlam, 12)} > 0")
        print(f"      cap minus lambda_R = {enc(capB - lam, 15)}; lambda_R minus lam_E = "
              f"{enc(lam - lam_E(A['tau'], beta), 15)}")
    order_ok = all(hi(branch[MIDDLE[i]]["E"]) < lo(branch[MIDDLE[i + 1]]["E"]) for i in range(2))
    order_lam = all(hi(branch[MIDDLE[i]]["lam"]) < lo(branch[MIDDLE[i + 1]]["lam"]) for i in range(2))
    print(f"  entry enclosures strictly ordered upward: {order_ok}; research enclosures strictly ordered: {order_lam}")
    for r in MIDDLE:
        t = TAG[r]
        reg(f"res_lambda_{t}", branch[r]["lam"], fdisp(branch[r]["lam"]), "computer-assisted",
            f"research on the branch at r = {float(r)}: positive root of F_r; exact rational bisection")
        reg(f"res_entry_{t}", branch[r]["E"], fdisp(branch[r]["E"]), "computer-assisted",
            f"entry on the research branch at r = {float(r)}")
        reg(f"res_muplus_{t}", branch[r]["mu"], fdisp(branch[r]["mu"]), "computer-assisted",
            f"purchase posterior on the research branch at r = {float(r)}")
        reg(f"res_own_{t}", branch[r]["own"], fdisp(branch[r]["own"]), "computer-assisted",
            f"high-class ownership on the research branch at r = {float(r)}")
        A = auction(r)
        lE = lam_E(A["tau"], beta)
        reg(f"res_lamE_{t}", lE, fdisp(lE), "analytical", f"recruitment intensity lambda_E at r = {float(r)}")
        reg(f"res_Delta_{t}", A["Delta"], fdisp(A["Delta"]), "analytical", f"target-payoff spread at r = {float(r)}")
        reg(f"res_tau_{t}", A["tau"], fdisp(A["tau"]), "analytical", f"preparation threshold tau at r = {float(r)}")
        reg(f"res_lamgap_{t}", branch[r]["lam"] - lE, fdisp(branch[r]["lam"] - lE), "computer-assisted",
            f"lambda_R - lambda_E at r = {float(r)}")
        reg(f"res_capgap_{t}", capB - branch[r]["lam"], fdisp(capB - branch[r]["lam"]), "computer-assisted",
            f"cap - lambda_R at r = {float(r)}")
        reg(f"res_UH_{t}", branch[r]["UH"], fdisp(branch[r]["UH"]), "computer-assisted",
            f"high-class purchase payoff 2 a lambda_R at r = {float(r)}")
        reg(f"res_ULgap_{t}", K - RHO * A["Delta"] / 2, fdisp(K - RHO * A["Delta"] / 2), "analytical",
            f"k - rho Delta/2 at r = {float(r)}: the low-class sale loses at least this amount")
    # threshold branch under CM
    print("  threshold equilibria (rule CM):")
    th_E = []
    for r in MIDDLE:
        lab, v = [x for x in sets[(r, "IM", "CM")] if x[0].startswith("th/")][0]
        A = auction(r)
        lE = lam_E(A["tau"], beta)
        es = v["e_star"]
        Eth = RHO + (es - RHO) * ((1 - lE) * beta + lE / 2)
        th_E.append(Eth)
        print(f"    r = {r}: lam_E = {lE} = {dec(lE, 12)}; e* = {es} = {dec(es, 12)}; aggregate entry = {dec(Eth, 12)};"
              f" from the tuple {enc(v['E'], 12)}")
        t = TAG[r]
        reg(f"res_th_estar_{t}", es, fdisp(es), "analytical", f"entry after a purchase in the threshold equilibrium (rule CM), r = {float(r)}")
        reg(f"res_th_entry_{t}", Eth, fdisp(Eth), "analytical", f"aggregate entry in the threshold equilibrium (rule CM), r = {float(r)}")
    direction = "falls" if th_E[0] > th_E[1] > th_E[2] else ("rises" if th_E[0] < th_E[1] < th_E[2] else "is not monotone")
    print(f"    threshold entry across 1.55, 1.60, 1.65 {direction}")
    print()

    # ------------------------------------------------------------------------------------------
    print("== D. The interval of the research branch at B (a = 1/40, cap lambda_B) ==")
    J_lo, J_hi = Fr(6, 5), Fr(7, 4)

    def phi(r, a=A_B, b_=beta):
        A = auction(r)
        return A["Delta"] * (1 - A["tau"]) - K - 2 * a * lam_E(A["tau"], b_)

    print(f"  phi(r) = Delta(r)(1 - tau(r)) - k - 2 a lam_E(r); phi(6/5) = {dec(phi(J_lo), 12)}, "
          f"phi(31/20) = {dec(phi(Fr(31, 20)), 12)}, phi(7/4) = {dec(phi(J_hi), 12)}")
    # monotonicity certificate on J = [6/5, 7/4]
    dDel_min = (1 - L_VAL ** 2 / J_lo ** 2) / 2
    tau_hi = auction(J_hi)["tau"]
    Del_hi = auction(J_hi)["Delta"]
    num_hi = 8 * J_hi ** 2 - J_hi + 2
    den_lo = 20 * J_lo - J_lo ** 2 - 1
    taup_max = 3 * num_hi / (2 * den_lo ** 2)
    Dmin = beta + (1 - 2 * beta) * (1 - tau_hi)
    lead = dDel_min * (1 - tau_hi) - Del_hi * taup_max
    lamEp_max = beta * taup_max / Dmin ** 2
    phip_lb = lead - 2 * A_B * lamEp_max
    a_mono = lead / (2 * lamEp_max)
    print(f"  bounds on J = [6/5, 7/4]: Delta' >= {dDel_min}; 1 - tau >= 1 - tau(7/4) = {1 - tau_hi} ({dec(1 - tau_hi, 9)});")
    print(f"     Delta <= {Del_hi}; tau' <= {taup_max} ({dec(taup_max, 9)}); lam_E' <= {dec(lamEp_max, 9)}")
    print(f"  (Delta(1 - tau))' >= {lead} = {dec(lead, 9)}")
    print(f"  phi' >= {phip_lb} = {dec(phip_lb, 9)} > 0 at a = 1/40; phi' > 0 on J for every a < a_mono = {a_mono} = {dec(a_mono, 9)}")
    # bisection for r_R
    lo_, hi_ = J_lo, J_hi
    while hi_ - lo_ > Fr(1, 10 ** 15):
        m = (lo_ + hi_) / 2
        if phi(m) < 0:
            lo_ = m
        else:
            hi_ = m
    rR = Iv(lo_, hi_)
    lEr = Iv(lam_E(auction(lo_)["tau"], beta), lam_E(auction(hi_)["tau"], beta))
    ER = RHO + (1 - RHO) * (beta + (Fr(1, 2) - beta) * lEr)
    print(f"  branch start r_R in {enc(rR, 15)}; lambda_R(r_R) = lam_E(r_R) in {enc(lEr, 12)}; entry at r_R in {enc(ER, 12)}")
    # cap point: Delta(r) = (2 a cap + k) / d(cap)
    dcap = 1 - MB
    Dcap = (2 * A_B * capB + K) / dcap
    rcap = r_of_Delta(Dcap)
    Ecap = RHO + (1 - RHO) * (beta + (Fr(1, 2) - beta) * capB)
    print(f"  cap point: Delta(rbar_R) = (2 a cap + k)(1 + e) = {enc(Dcap, 15)}; rbar_R = {enc(rcap, 15)}")
    print(f"  entry at the cap (fixed-lambda level) = {enc(Ecap, 15)}")
    print(f"  rbar_R < r_N: {gt(rN, rcap)} (r_N - rbar_R = {enc(rN - rcap, 12)}); "
          f"r_R < 31/20: {gt(Fr(31, 20), rR)}; 33/20 < rbar_R: {gt(rcap, Fr(33, 20))}")
    # fixed-lambda start r_A for comparison: Delta(r)(1 - tau(r)) = k
    lo_, hi_ = J_lo, J_hi
    while hi_ - lo_ > Fr(1, 10 ** 15):
        m = (lo_ + hi_) / 2
        A = auction(m)
        if A["Delta"] * (1 - A["tau"]) - K < 0:
            lo_ = m
        else:
            hi_ = m
    rA = Iv(lo_, hi_)
    print(f"  comparison: the fixed-lambda start r_A (Delta(1 - tau) = k) = {enc(rA, 12)}")
    reg("res_rR", rR, fdisp(rR), "computer-assisted", "start of the research branch: root of phi on [6/5, 7/4]")
    reg("res_rcap", rcap, fdisp(rcap), "computer-assisted", "research reaches the cap: Delta(r) = (2 a cap + k)(1+e)")
    reg("res_entry_rR", ER, fdisp(ER), "computer-assisted", "entry at the start of the research branch")
    reg("res_lambda_rR", lEr, fdisp(lEr), "computer-assisted", "research at the start of the research branch (= lam_E(r_R))")
    reg("res_entry_cap", Ecap, fdisp(Ecap), "computer-assisted", "entry with research at the cap and a recruiting purchase (fixed-lambda level)")
    reg("res_amono", a_mono, fdisp(a_mono), "analytical", "phi increases on [6/5, 7/4] for every a below this bound")
    Dmin3 = Fr(1, 3) + Fr(1, 3) * (1 - tau_hi)
    a_mono3 = lead / (2 * (Fr(1, 3) * taup_max / Dmin3 ** 2))
    print(f"  at beta = 1/3 the same bound gives a_mono = {a_mono3} = {dec(a_mono3, 9)}; a_mono falls in beta")
    reg("res_amono_third", a_mono3, fdisp(a_mono3), "analytical", "a_mono at beta = 1/3 (the smallest over beta <= 1/3)")
    reg("res_phi_r155", phi(Fr(31, 20)), fdisp(phi(Fr(31, 20))), "analytical", "recruitment margin phi at 31/20, a = 1/40")
    reg("res_phip_lb", phip_lb, fdisp(phip_lb), "analytical", "lower bound on phi' over [6/5, 7/4] at a = 1/40")
    reg("res_rA", rA, fdisp(rA), "computer-assisted", "fixed-lambda start of coexistence: Delta(1 - tau) = k (comparison)")
    reg("res_dphi_lead", lead, fdisp(lead), "analytical", "lower bound on (Delta(1 - tau))' over [6/5, 7/4]")
    reg("res_bound_dDelta", dDel_min, "11/72", "analytical", "Delta'(6/5), the minimum of Delta' on [6/5, 7/4]")
    reg("res_bound_tau74", 1 - tau_hi, "19/55", "analytical", "1 - tau(7/4), the minimum of 1 - tau on [6/5, 7/4]")
    reg("res_bound_Delta74", Del_hi, "9/56", "analytical", "Delta(7/4), the maximum of Delta on [6/5, 7/4]")
    reg("res_bound_taup", taup_max, f"{taup_max.numerator}/{taup_max.denominator}", "analytical",
        "upper bound on tau' over [6/5, 7/4]")
    lE74 = lam_E(tau_hi, beta)
    print(f"  lam_E(7/4) = {lE74} = {dec(lE74, 12)} < cap: {gt(capB, lE74)}")
    reg("res_lamE_r175", lE74, fdisp(lE74), "analytical", "lam_E(7/4), an upper bound on lam_E over (1, r_N]")
    reg("res_rN", rN, fdisp(rN), "analytical", "no-research boundary r_N = no-trade boundary (rho Delta = 2k)")
    reg("res_rC", rC, fdisp(rC), "computer-assisted", "entry ceiling B_r(M) = c_H with research at the cap")
    print()

    # ------------------------------------------------------------------------------------------
    print("== E. Strong incumbents: the uniform bound and research at the cap ==")
    for r in (R1, R2):
        A = auction(r)
        lb = RHO * A["Delta"] * (1 - MB) - K
        mar = lb - A_B * capB
        print(f"  r = {r}: rho Delta (1 - M) - k = {enc(lb, 15)}; minus a cap = {enc(mar, 15)}; "
              f"M - tau = {enc(MB - A['tau'], 15)}")
        reg(f"margin_res_bound_{TAG[r]}_B", mar, fdisp(mar), "computer-assisted",
            f"rho Delta(1 - M) - k - a cap at r = {float(r)} (uniform research bound)")
        reg(f"margin_res_tau_{TAG[r]}_B", MB - A["tau"] if r == R1 else A["tau"] - MB,
            fdisp(MB - A["tau"] if r == R1 else A["tau"] - MB), "computer-assisted",
            "M - tau(3)" if r == R1 else "tau(18/5) - M")
    v1 = [x for x in sets[(R1, "IM", "C1")]][0][1]
    v2 = [x for x in sets[(R2, "IM", "C1")]][0][1]
    print(f"  entry at r_1 with research = {enc(v1['E'], 15)}; at r_2 = {enc(v2['E'], 15)}")
    print(f"  H ownership at r_1 = {enc(v1['own'], 15)}")
    reg("res_entry_r1", v1["E"], fdisp(v1["E"]), "computer-assisted", "entry at r_1 with research at the cap (equals the fixed-lambda entry)")
    reg("res_entry_r2", v2["E"], fdisp(v2["E"]), "analytical", "entry at r_2 with research at the cap")
    Ustar = (K + A_B * capB) / (RHO * (1 - MB))
    rUR = r_of_Delta(Ustar)
    rU = r_of_Delta(K / (RHO * (1 - MB)))
    print(f"  uniform research bound holds for r > r_U^R = r((k + a cap)/(rho(1 - M))) = {enc(rUR, 12)}")
    print(f"  uniform trading bound alone holds for r > r_U = r(k/(rho(1 - M))) = {enc(rU, 12)}")
    reg("res_rUR", rUR, fdisp(rUR), "computer-assisted",
        "research at the cap is unique for r_U^R < r < h (uniform bound); the full tuple is unique there "
        "except at r = r_C under rule CM")
    # The entry ceiling r_C lies above r_U^R. There M = tau(r_C), so the challenger is indifferent after a purchase.
    Del_C = (rC - L_VAL) * (rC - L_VAL) / (2 * rC)
    mar_C = RHO * Del_C * (1 - MB) - K - A_B * capB
    print(f"  entry ceiling: r_C - r_U^R = {enc(rC - rUR, 12)} > 0: {gt(rC, rUR)}; (U) margin at r_C = {enc(mar_C, 15)}")
    print("  tau(r) rises strictly on (ell, h): c_H - g_L rises and g_H - g_L = h - r/2 - ell^2/(2r) falls,")
    print("  so r_C is the only strength in (r_U^R, h) with M = tau(r).")
    print(f"  at r_C under C1: zeta_1 = 1, unique tuple, entry {enc(Ecap, 15)}")
    print(f"  at r_C under CM: every zeta_1 in [0, 1]; research at the cap and full orders in each; "
          f"aggregate entry rho + (1 - rho) zeta_1 (b_cap + cap/2) spans [{RHO}, {enc(Ecap, 15)}]")
    print()

    # ------------------------------------------------------------------------------------------
    print("== F. The admissible region at B (beta = beta_B, other primitives at B) ==")
    tau3, tau36 = auction(R1)["tau"], auction(R2)["tau"]
    cap_lo, cap_hi = lam_E(tau3, beta), lam_E(tau36, beta)
    print(f"  strip for the cap: lam_E(3) = {cap_lo} = {dec(cap_lo, 12)} < cap < lam_E(18/5) = {cap_hi} = {dec(cap_hi, 12)}")
    print(f"  cap lambda_B = {enc(capB, 15)}; margins: cap - lam_E(3) = {enc(capB - cap_lo, 12)}, "
          f"lam_E(18/5) - cap = {enc(cap_hi - capB, 12)}")

    def a_up_r(r, b_=beta):
        A = auction(r)
        return (A["Delta"] * (1 - A["tau"]) - K) / (2 * lam_E(A["tau"], b_))

    def a_lo_r(r, cap, b_=beta):
        A = auction(r)
        return (A["Delta"] * d_full(cap, b_) - K) / (2 * cap)

    def a_U3(cap, b_=beta):
        return (RHO * auction(R1)["Delta"] * d_full(cap, b_) - K) / cap

    def a_36(cap, b_=beta):
        return (RHO * auction(R2)["Delta"] * d_full(cap, b_) - K) / cap

    for r in MIDDLE:
        print(f"  r = {r}: recruitment needs a < a_up(r) = {a_up_r(r)} = {dec(a_up_r(r), 12)}; interior research needs "
              f"a > a_lo(r, lambda_B) = {enc(a_lo_r(r, capB), 12)}")
    a_up = min(a_up_r(r) for r in MIDDLE)
    a_lo_B = a_lo_r(Fr(33, 20), capB)
    a_floor3 = (RHO * auction(R1)["Delta"] * (1 - tau3) - K) / cap_lo
    a3cap_end = (((1 + RHO) * auction(R1)["Delta"] * (1 - tau36)) / 2 - K) / cap_hi
    print(f"  binding: a_up = a_up(31/20) = {dec(a_up, 12)}; a_lo(lambda_B) = a_lo(33/20, lambda_B) = {enc(a_lo_B, 12)}")
    print(f"  cost window at the cap lambda_B: ({dec(a_lo_B, 6)}, {dec(a_up, 6)}); ratio a_up/a_lo = {dec(a_up / a_lo_B, 4)}")
    print(f"  a = 1/40 margins: a - a_lo = {enc(A_B - a_lo_B, 12)}, a_up - a = {dec(a_up - A_B, 12)}")
    print("  endpoint bounds over the strip (each is decreasing in the cap, so its infimum is at lam_E(18/5)):")
    print(f"    uniform bound at 3: a < a_U3(cap); a_U3(lam_E(18/5)) = {dec(a_U3(cap_hi), 12)}")
    print(f"    cap at 18/5: a <= a_36(cap); a_36(lam_E(18/5)) = {dec(a_36(cap_hi), 12)}")
    print(f"    exact cap condition at 3 on the recruiting piece at lam_E(18/5) = {dec(a3cap_end, 12)}; "
          f"no floor root at 3: a < {dec(a_floor3, 12)}")
    print(f"    a_up below every endpoint bound: {a_up < min(a_U3(cap_hi), a_36(cap_hi), a3cap_end, a_floor3)}")
    print(f"    a_lo at the lower end of the strip: a_lo(33/20, lam_E(3)) = {dec(a_lo_r(Fr(33, 20), cap_lo), 12)} < a_up: "
          f"{a_lo_r(Fr(33, 20), cap_lo) < a_up}")
    print(f"    a_lo is decreasing in the cap: numerator Delta d(cap) - k > 0 on the strip: "
          f"{auction(Fr(33, 20))['Delta'] * d_full(cap_hi, beta) - K > 0}")
    print(f"    monotonicity of phi certified for a < a_mono = {dec(a_mono, 9)} > a_up: {a_mono > a_up}")
    # cap range at a = 1/40: lambda_R(33/20) < cap < lam_E(18/5)
    lam165 = branch[Fr(33, 20)]["lam"]
    print(f"  cap range at a = 1/40: ({enc(lam165, 12)}, {dec(cap_hi, 12)}); lambda_B margins: "
          f"{enc(capB - lam165, 12)} above, {enc(cap_hi - capB, 12)} below")
    print("  table: cap, a_lo(cap), a_up, a_U3(cap), a_36(cap), window width")
    table_caps = [("lam_E(3)", cap_lo), ("0.30", Fr(3, 10)), ("0.31", Fr(31, 100)), ("0.32", Fr(32, 100)),
                  ("0.33", Fr(33, 100)), ("lambda_B", capB), ("lam_E(3.6)", cap_hi)]
    for i, (name, c) in enumerate(table_caps):
        al = a_lo_r(Fr(33, 20), c)
        print(f"    {name:11s} cap={enc(c, 6)}  a_lo={enc(al, 6)}  a_up={dec(a_up, 6)}  a_U3={enc(a_U3(c), 6)}  "
              f"a_36={enc(a_36(c), 6)}  width={enc(a_up - al, 6)}  1/40 inside: {gt(A_B, al) and A_B < a_up}")
        reg(f"res_region_cap_{i}", c, fdisp(c), "computer-assisted" if isinstance(c, Iv) else "analytical",
            f"admissible-region table: cap value ({name})")
        reg(f"res_region_alo_{i}", al, fdisp(al), "computer-assisted" if isinstance(al, Iv) else "analytical",
            f"admissible-region table: a_lo at cap {name}")
        reg(f"res_region_aU3_{i}", a_U3(c), fdisp(a_U3(c)), "computer-assisted" if isinstance(c, Iv) else "analytical",
            f"admissible-region table: uniform-bound cost limit at r_1, cap {name}")
        reg(f"res_region_a36_{i}", a_36(c), fdisp(a_36(c)), "computer-assisted" if isinstance(c, Iv) else "analytical",
            f"admissible-region table: cap condition at r_2, cap {name}")
        reg(f"res_region_width_{i}", a_up - al, fdisp(a_up - al), "computer-assisted" if isinstance(c, Iv) else "analytical",
            f"admissible-region table: window width a_up - a_lo at cap {name}")
    reg("res_cap_lo", cap_lo, fdisp(cap_lo), "analytical", "lower end of the cap strip: lam_E(3)")
    reg("res_cap_hi", cap_hi, fdisp(cap_hi), "analytical", "upper end of the cap strip: lam_E(18/5)")
    reg("res_a_up", a_up, fdisp(a_up), "analytical", "upper cost bound: recruitment at 31/20")
    reg("res_a_lo", a_lo_B, fdisp(a_lo_B), "computer-assisted", "lower cost bound at the cap lambda_B: interior research at 33/20")
    reg("res_cap_lo_a", lam165, fdisp(lam165), "computer-assisted", "lower end of the cap range at a = 1/40: lambda_R(33/20)")
    reg("margin_res_aup_B", a_up - A_B, fdisp(a_up - A_B), "analytical", "a_up - a at B")
    reg("margin_res_alo_B", A_B - a_lo_B, fdisp(A_B - a_lo_B), "computer-assisted", "a - a_lo(lambda_B) at B")
    reg("margin_res_caplo_B", capB - cap_lo, fdisp(capB - cap_lo), "computer-assisted", "lambda_B - lam_E(3)")
    reg("margin_res_caphi_B", cap_hi - capB, fdisp(cap_hi - capB), "computer-assisted", "lam_E(18/5) - lambda_B")
    reg("res_a_floor3", a_floor3, fdisp(a_floor3), "analytical", "a floor equilibrium at 3 needs a above this value")
    reg("res_aU3_B", a_U3(capB), fdisp(a_U3(capB)), "computer-assisted", "uniform-bound cost limit at r_1 at the cap lambda_B")
    print()

    # general beta at the cap lambda_B(beta) with u = e - 1
    print("  general beta with the cap lambda_B(beta) = u beta/(1 + u beta), u = e - 1 (M fixed at e/(1+e)):")
    D165 = auction(Fr(33, 20))["Delta"]
    num_lo = D165 / (1 + E_IV) - K
    t155 = auction(Fr(31, 20))["tau"]
    num_up = auction(Fr(31, 20))["Delta"] * (1 - t155) - K
    # a_lo(beta) < 1/40  <=>  lambda_B(beta) > 20 num_lo  <=>  u beta > x/(1 - x), x = 20 num_lo
    x = num_lo / (2 * A_B)
    beta_lo = x / (1 - x) / U_B
    # a_up(beta) > 1/40  <=>  lam_E(31/20; beta) < y, y = num_up/(2a)
    y = num_up / (2 * A_B)
    # beta (2tau - 1) < y (beta + (1 - 2 beta)(1 - tau))  <=>  beta [2tau - 1 - y + 2y(1 - tau)] < y (1 - tau)
    coef = 2 * t155 - 1 - y + 2 * y * (1 - t155)
    beta_hi = y * (1 - t155) / coef if coef > 0 else None
    print(f"    a = 1/40 is admissible iff beta in ({enc(beta_lo, 9)}, {dec(beta_hi, 9) if beta_hi else 'inf'}) "
          f"intersected with (0, 1/3]")
    print(f"    the endpoint conditions tau(3) < e/(1+e) < tau(18/5) do not depend on beta; uniform bound at 3 for every"
          f" beta <= 1/3: rho Delta(3)/(1+e) - k - a lambda_B(1/3) = "
          f"{enc(RHO * auction(R1)['Delta'] / (1 + E_IV) - K - A_B * lam_of_u(U_B, Fr(1, 3)), 9)}")
    reg("res_beta_lo", beta_lo, fdisp(beta_lo), "computer-assisted", "a = 1/40 admissible with cap lambda_B(beta) for beta above this value")
    reg("res_beta_hi", beta_hi, fdisp(beta_hi, 4), "analytical", "a_up(beta) > 1/40 for every beta below this value")
    for bb in (Fr(1, 5), Fr(1, 4), BETA_B, Fr(3, 10), Fr(1, 3)):
        cb = lam_of_u(U_B, bb)
        alb = (D165 / (1 + E_IV) - K) / (2 * cb)
        aub = num_up / (2 * lam_E(t155, bb))
        print(f"    beta = {float(bb):.6f}: cap = {enc(cb, 6)}, a_lo = {enc(alb, 6)}, a_up = {dec(aub, 6)}")
    print()

    # ------------------------------------------------------------------------------------------
    print("== G. Access to prices at r_1 = 3 ==")
    A = auction(R1)
    acc = verify(R1, beta, capB, A_B, capB, {-1: Fr(0), 0: Fr(0), 1: Fr(1)}, {-1: Fr(1), 0: Fr(0), 1: Fr(0)})
    hid_found, hid_notes = enumerate_eq(R1, beta, capB, A_B, "C1", "IM", hidden=True)
    print(f"  hidden-price equilibria: {len(hid_found)}; notes {hid_notes}")
    hid = hid_found[0][1]
    print_verification(hid)

    def welfare(v):
        f, e, zeta = v["f"], v["e"], v["zeta"]
        R, W = Fr(0), Fr(0)
        for j, t, S in (("H", A["tH"], A["SH"]), ("L", A["tL"], A["SL"])):
            for q in (-1, 0, 1):
                R = R + PI * f[j][q] * (A["t0"] + e[q] * (t - A["t0"]))
                W = W + PI * f[j][q] * (A["S0"] + e[q] * (S - A["S0"]) - (1 - RHO) * zeta[q] * C_H)
        return R, W

    Ra, Wa = welfare(acc)
    Rh, Wh = welfare(hid)
    rc = A_B * capB * capB / 2
    tc = capB * K
    dR, dW = Ra - Rh, Wa - Wh
    dR_form = (1 - RHO) * acc["Pr"][1] * (A["tL"] - A["t0"] + A["Delta"] * MB)
    dW_form = (1 - RHO) * acc["Pr"][1] * (B_of(R1, MB) - C_H + P_RES ** 2 / R1)
    print(f"  proceeds: access {enc(Ra, 12)}, hidden {enc(Rh, 12)}, gain {enc(dR, 12)} (formula {enc(dR_form, 12)})")
    print(f"  surplus net of preparation costs: access {enc(Wa, 12)}, hidden {enc(Wh, 12)}, gain {enc(dW, 12)} "
          f"(formula {enc(dW_form, 12)})")
    print(f"  research cost (a/2) cap^2 = {enc(rc, 12)} and trading cost k cap = {enc(tc, 12)} in both economies")
    print(f"  surplus net of preparation, research and trading costs: access {enc(Wa - rc - tc, 12)}, hidden "
          f"{enc(Wh - rc - tc, 12)}")
    reg("res_R_access_r1", Ra, fdisp(Ra), "computer-assisted", "expected proceeds at r_1 with research and price access")
    reg("res_R_hidden_r1", Rh, fdisp(Rh), "analytical", "expected proceeds at r_1 with research and hidden prices")
    reg("res_dR_r1", dR, fdisp(dR), "computer-assisted", "proceeds gain from price access at r_1 with research")
    reg("res_W_access_r1", Wa, fdisp(Wa), "computer-assisted", "surplus net of preparation costs at r_1, access")
    reg("res_W_hidden_r1", Wh, fdisp(Wh), "analytical", "surplus net of preparation costs at r_1, hidden prices")
    reg("res_dW_r1", dW, fdisp(dW), "computer-assisted", "net-surplus gain from price access at r_1 with research")
    reg("res_cost_r1", rc, fdisp(rc), "computer-assisted", "research cost at the cap (both economies)")
    reg("res_tcost_r1", tc, fdisp(tc), "computer-assisted", "expected trading cost at the cap (both economies)")
    print()

    # ------------------------------------------------------------------------------------------
    print("== H. Cross-check at calibration A (beta = 1/3, cap = 6/17, a = 1/40) ==")
    for r in MIDDLE + [R1, R2]:
        found, notes = enumerate_eq(r, Fr(1, 3), Fr(6, 17), A_B, "C1", "IM")
        txt = "; ".join(f"{lab}: lambda {enc(v['lam'], 12)}, entry {enc(v['E'], 12)}" for lab, v in found)
        print(f"  r = {r}: {len(found)} equilibria: {txt}")
        if r in MIDDLE:
            vR = [v for lab, v in found if lab.startswith("hi/L0: interior")][0]
            reg(f"res_calA_lambda_{TAG[r]}", vR["lam"], fdisp(vR["lam"]), "computer-assisted",
                f"cross-check at calibration A (beta 1/3, cap 6/17): research at r = {float(r)}")
            reg(f"res_calA_entry_{TAG[r]}", vR["E"], fdisp(vR["E"]), "computer-assisted",
                f"cross-check at calibration A (beta 1/3, cap 6/17): entry at r = {float(r)}")
    print()

    # ------------------------------------------------------------------------------------------
    print("== I. Margins of the strict hypotheses at B ==")
    rows = []
    A0 = auction(Fr(6, 5))
    reg("res_Delta_r0", A0["Delta"], "1/60", "analytical", "target-payoff spread at r_0 = 6/5")
    rows.append(("Delta(6/5) < k", K - A0["Delta"], "margin_res_weak_B", "k - Delta(6/5)"))
    A165 = auction(Fr(33, 20))
    rows.append(("rho Delta(33/20) < 2k", 2 * K - RHO * A165["Delta"], "margin_res_nosale_B", "2k - rho Delta(33/20)"))
    rows.append(("B_r(1/2) < c_H at 6/5 (smallest margin of the six)", C_H - B_of(Fr(6, 5), PI), "margin_res_half_B",
                 "c_H - B_{6/5}(1/2); B_r(1/2) falls in r"))
    rows.append(("a < a_up (recruitment at 31/20)", a_up - A_B, None, None))
    rows.append(("a > a_lo(lambda_B) (interior research at 33/20)", A_B - a_lo_B, None, None))
    rows.append(("lam_E(3) < cap", capB - cap_lo, None, None))
    rows.append(("cap < lam_E(18/5)", cap_hi - capB, None, None))
    rows.append(("tau(3) < M", MB - tau3, None, None))
    rows.append(("M < tau(18/5)", tau36 - MB, None, None))
    for r in (R1, R2):
        Ar = auction(r)
        rows.append((f"rho Delta(1 - M) - k - a cap > 0 at {r}", RHO * Ar["Delta"] * (1 - MB) - K - A_B * capB, None, None))
    rows.append(("beta < 1/3", Fr(1, 3) - beta, "margin_res_beta_B", "1/3 - beta"))
    rows.append(("r_R < 31/20", Fr(31, 20) - rR, "margin_res_rR_B", "31/20 - r_R"))
    rows.append(("33/20 < rbar_R", rcap - Fr(33, 20), "margin_res_rcap_B", "rbar_R - 33/20"))
    rows.append(("rbar_R < r_N", rN - rcap, "margin_res_rN_B", "r_N - rbar_R"))
    rows.append(("a < a_mono", a_mono - A_B, "margin_res_amono_B", "a_mono - a"))
    rows.append(("lambda_R(33/20) < cap", capB - lam165, "margin_res_lamcap_B", "cap - lambda_R(33/20)"))
    rows.append(("phi(31/20) > 0", phi(Fr(31, 20)), None, None))
    for name, val, key, note in rows:
        print(f"  {name:55s} margin {enc(val, 12)}")
        if key:
            st = "computer-assisted" if isinstance(val, Iv) else "analytical"
            reg(key, val, fdisp(val), st, note)
    print()

    print("== J. Outside the required claims: equilibrium sets between r_N and r_U^R (rule C1, both investor rules) ==")
    print("  The type list (Lemma 3 with the low-class cases L0, L1, Lint) covers every r with 1/2 < tau < 1.")
    print("  These lines are printed only; no registry row uses them.")
    for r in (Fr(9, 5), Fr(2), Fr(11, 5), Fr(12, 5)):
        for inv in ("IM", "I0"):
            found, notes = enumerate_eq(r, beta, capB, A_B, "C1", inv)
            txt = "; ".join(f"{lab}: lambda {dec(v['lam'], 6)}, entry {dec(v['E'], 6)}, conditions hold {v['ok']}"
                            for lab, v in found)
            print(f"  r = {float(r)}, rule {inv}: {len(found)} equilibria: {txt}")
    print()

    write_registry()
    print(f"registry rows written: {len(REG)} -> {REG_CSV.relative_to(TEAM.parents[1])}")
    print(f"registry macros written -> {NUM_TEX.relative_to(TEAM.parents[1])}")


if __name__ == "__main__":
    main()
