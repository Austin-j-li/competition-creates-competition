"""Shared exact objects for the N4 scripts (one order slot, paper benchmark).

Auction objects are computed by direct integration over R ~ U[0, r] with fractions.Fraction.
Print-only helpers. No assertions. Run from the repository root.
"""
from fractions import Fraction as F
from math import isqrt

H, L, P, RHO, CL, CH, K, PI = F(10), F(1), F(1, 2), F(1, 4), F(0), F(6), F(1, 50), F(1, 2)
R0, R1, R2 = F(6, 5), F(3), F(18, 5)
BETA, LAM = F(1, 3), F(6, 17)          # calibration A


def dec(x, n=8):
    return f"{float(x):.{n}f}"


def head(text):
    print()
    print("=" * 100)
    print(text)
    print("=" * 100)


def expect(pieces, r):
    """E[f(R)] for R ~ U[0, r]; f(R) = a + b R on [lo, hi); hi = None means no upper limit."""
    tot = F(0)
    for lo, hi, a, b in pieces:
        lo2 = max(lo, F(0))
        hi2 = r if hi is None else min(hi, r)
        if hi2 > lo2:
            tot += a * (hi2 - lo2) + b * (hi2 * hi2 - lo2 * lo2) / 2
    return tot / r


def objects(r):
    """Paper objects at strength r: proceeds t, challenger gains g, allocation values S, incumbent profits I."""
    r = F(r)
    t0 = expect([(P, None, P, F(0))], r)                      # incumbent alone: pays p when R >= p

    def t(th):   # second-price proceeds with a prepared challenger of value th >= p: max(p, min(R, th))
        return expect([(F(0), P, P, F(0)), (P, th, F(0), F(1)), (th, None, th, F(0))], r)

    def g(th):   # challenger keeps (th - max(p, R))_+
        return expect([(F(0), P, th - P, F(0)), (P, th, th, F(-1))], r)

    def s(th):   # allocation value max(th, R)
        return expect([(F(0), th, th, F(0)), (th, None, F(0), F(1))], r)

    def inc(th):  # incumbent profit with a prepared challenger: (R - th)_+
        return expect([(th, None, -th, F(1))], r)

    s0 = expect([(P, None, F(0), F(1))], r)                   # R 1{R >= p}
    i0 = expect([(P, None, -P, F(1))], r)                     # (R - p)_+
    o = dict(r=r, t0=t0, tH=t(H), tL=t(L), gH=g(H), gL=g(L), sH=s(H), sL=s(L), s0=s0,
             iH=inc(H), iL=inc(L), i0=i0)
    o["D"] = o["tH"] - o["tL"]
    o["wL"] = o["tL"] - o["t0"]
    o["wH"] = o["tH"] - o["t0"]
    o["tau"] = (CH - o["gL"]) / (o["gH"] - o["gL"])
    return o


def Bf(o, mu):
    return o["gL"] + mu * (o["gH"] - o["gL"])


def entry_C1(o, mu):
    """Expected entry at posterior mu: the zero-cost type prepares; the high-cost type prepares iff B >= c_H."""
    return RHO + (1 - RHO) * (1 if Bf(o, mu) >= CH else 0)


def post(aH, aL):
    """Posterior at a flow. An unused flow (zero mass in both classes) gets the passive prior belief."""
    if aH == 0 and aL == 0:
        return PI
    return PI * aH / (PI * aH + (1 - PI) * aL)


def bisect(fun, lo, hi, n=40):
    """Rational bracket of a sign change of fun on [lo, hi]."""
    flo = fun(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = fun(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return lo, hi


def r_of_delta(d):
    """Strength r > 1 with Delta_T(r) = d: r = 1 + d + sqrt(d^2 + 2d) (rational bracket)."""
    num, den = (d * d + 2 * d).numerator, (d * d + 2 * d).denominator
    sc = 10 ** 14
    lo = F(isqrt(num * sc * sc // den), sc)
    return 1 + d + lo, 1 + d + lo + F(1, sc)
