"""Scratch model for W3: research branch beyond rho*Delta = 2k (prior 1/2).

Point-mass classes h > ell >= p, incumbent R ~ U[0, r].
Everything here is exploration code: prints, no assertions.
"""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Par:
    h: float
    ell: float
    p: float
    cH: float
    k: float
    rho: float
    beta: float
    a: float
    lbar: float


def bisect(f, lo, hi, it=200):
    flo = f(lo)
    fhi = f(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if (flo > 0) == (fhi > 0):
        raise ValueError(f"no sign change on [{lo},{hi}]: {flo},{fhi}")
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm == 0:
            return mid
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi, fhi = mid, fm
    return 0.5 * (lo + hi)


# ---------- auction objects, uniform incumbent on [0, r] ----------
def Fcdf(y, r):
    return min(max(y / r, 0.0), 1.0)


def integral_F(lo, hi, r):
    """int_lo^hi F(y) dy for U[0,r]."""
    if hi <= lo:
        return 0.0
    # piece on [lo, min(hi, r)] : y/r ; piece on [r, hi]: 1
    s = 0.0
    a1, b1 = lo, min(hi, r)
    if b1 > a1:
        s += (b1 * b1 - a1 * a1) / (2 * r)
    if hi > r:
        s += hi - max(lo, r)
    return s


def g_of(theta, P, r):
    return integral_F(P.p, theta, r)


def auction(P, r):
    gH = g_of(P.h, P, r)
    gL = g_of(P.ell, P, r)
    gam = gH - gL
    # Delta = int_ell^h (1 - F)
    Delta = (P.h - P.ell) - integral_F(P.ell, P.h, r)
    tau = (P.cH - gL) / gam
    WH = Fcdf(P.h, r)
    return dict(gH=gH, gL=gL, gam=gam, Delta=Delta, tau=tau, J=Delta * (1 - tau), WH=WH)


# ---------- slot / research objects at prior 1/2 ----------
def m_of(lam, P):
    b = P.beta
    return (1 - lam) * b / (2 * b + lam * (1 - 2 * b))


def M_of(lam, P):
    return 1 - m_of(lam, P)


def dm_of(lam, P):
    b = P.beta
    return -b / (2 * b + lam * (1 - 2 * b)) ** 2


def lamE_of(tau, P):
    b = P.beta
    return b * (2 * tau - 1) / (b + (1 - 2 * b) * (1 - tau))


def dlamE_of(tau, P):
    b = P.beta
    return b / (b + (1 - 2 * b) * (1 - tau)) ** 2


def Lam_R(Delta, P):
    """root of 2 a lam = Delta m_lam - k (branch R research), Delta > 2k."""
    f = lambda lam: Delta * m_of(lam, P) - P.k - 2 * P.a * lam
    return bisect(f, 0.0, 1.0 - 1e-15)


def Psi(lam, Delta, P):
    """research value times 2: purchase return net + (sale return net)^+ on the extended branch."""
    mm = m_of(lam, P)
    return Delta * mm - P.k + max(P.rho * Delta * mm - P.k, 0.0)


def Lam_star(Delta, P):
    f = lambda lam: Psi(lam, Delta, P) - 2 * P.a * lam
    return bisect(f, 0.0, 1.0 - 1e-15)


def Lam_Q(Delta, P):
    """non-recruiting research with full orders: a lam = rho Delta m_lam - k (needs rho Delta > 2k)."""
    f = lambda lam: P.rho * Delta * m_of(lam, P) - P.k - P.a * lam
    if f(0.0) <= 0:
        return None
    return bisect(f, 0.0, 1.0 - 1e-15)


def phi_a(Delta, tau, P):
    return Delta * (1 - tau) - P.k - 2 * P.a * lamE_of(tau, P)


def phi_star(Delta, tau, P):
    J = Delta * (1 - tau)
    return J - P.k + max(P.rho * J - P.k, 0.0) - 2 * P.a * lamE_of(tau, P)


def low_class_rate(lam, Delta, P):
    """class-L informed sale rate t (prob. of informed sale) at presence lam when
    the purchase is full; under rule IM.  Returns (t, mu_minus, regime)."""
    bb = (1 - lam) * P.beta
    if P.rho * Delta / 2 <= P.k:
        return 0.0, 0.5, "abstain"
    if P.rho * Delta * m_of(lam, P) < P.k:
        t = bb * (P.rho * Delta / P.k - 2)
        return t, bb / (2 * bb + t), "mix"
    return lam, m_of(lam, P), "sell"


def entry_branch(lam, P):
    return P.rho + (1 - P.rho) * (P.beta + (0.5 - P.beta) * lam)


def fr(d, P):
    """root above ell of Delta(r) = d for r < h (uniform family, r <= h)."""
    ell = P.ell
    return ell + d + math.sqrt(d * d + 2 * ell * d)
